#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
import matplotlib.pyplot as plt
import numpy as np
import math

class LidarVisualizer(Node):
    def __init__(self):
        super().__init__('lidar_visualizer')

        self.ranges = None
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, qos_profile_sensor_data)

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        # 원본 라이다 점
        self.lidar_points = self.ax.scatter([], [], s=5)
        
        # 차량 중심
        self.ax.plot(0, 0, 'ro')

        # 시각화 그래픽 객체 미리 준비 (얇은 선)
        self.left_line_plot, = self.ax.plot([], [], 'g-', linewidth=1, label='Left Lane')
        self.right_line_plot, = self.ax.plot([], [], 'b-', linewidth=1, label='Right Lane')
        self.center_line_plot, = self.ax.plot([], [], 'r--', linewidth=1.5, label='Center Path')
        self.cone_scatter = self.ax.scatter([], [], s=60, facecolors='none', edgecolors='magenta', linewidths=1.5, label='Valid Cones')
        self.ax.legend(loc='upper right')

        plt.ion()
        plt.show()

        self.create_timer(0.2, self.timer_callback)

    def lidar_callback(self, msg):
        self.ranges = msg.ranges
        self.angle_min = msg.angle_min
        self.angle_max = msg.angle_max

    def timer_callback(self):
        if self.ranges is None: return
        
        ranges = self.ranges
        num_ranges = len(ranges)
        if num_ranges == 0: return

        valid = np.array([d if math.isfinite(d) else np.nan for d in ranges])
        angles = np.linspace(self.angle_min, self.angle_max, num_ranges)

        # Matplotlib 좌표: Y가 전방, 우측이 +X (알고리즘은 좌측이 +X)
        # Raw 데이터 그리기
        plot_y = valid * np.cos(angles)
        plot_x = -valid * np.sin(angles)

        indices = np.arange(num_ranges)
        colors = np.full(num_ranges, 'b', dtype=object)
        idx_ratio = (indices / num_ranges) * 360.0
        colors[(idx_ratio >= 0) & (idx_ratio < 45)] = 'r'
        colors[(idx_ratio >= 45) & (idx_ratio < 90)] = 'g'
        colors[(idx_ratio >= 90) & (idx_ratio < 270)] = 'b'
        colors[(idx_ratio >= 270) & (idx_ratio < 315)] = 'orange'
        colors[(idx_ratio >= 315) & (idx_ratio < 360)] = 'purple'

        self.lidar_points.set_offsets(np.c_[plot_x, plot_y])
        self.lidar_points.set_color(colors)

        # ==================================
        # 알고리즘 데이터 추출 (lidar_drive.py와 동일)
        # ==================================
        points = []
        for i in range(num_ranges):
            d = ranges[i]
            if not math.isfinite(d) or d <= 0.1 or d > 20.0: continue
            
            angle_rad = math.radians(i)
            y = d * math.cos(angle_rad) # 전방(+)
            x = d * math.sin(angle_rad) # 좌측(+)
            
            if y < 0.3: continue
            if (i < 20 or i > 340) and d <= 0.7: continue
            
            points.append((x, y))

        # 클러스터링
        clusters = []
        if points:
            current_cluster = [points[0]]
            for i in range(1, len(points)):
                p1 = points[i-1]
                p2 = points[i]
                if math.hypot(p1[0]-p2[0], p1[1]-p2[1]) < 0.4:
                    current_cluster.append(p2)
                else:
                    cx = sum(p[0] for p in current_cluster) / len(current_cluster)
                    cy = sum(p[1] for p in current_cluster) / len(current_cluster)
                    clusters.append((cx, cy))
                    current_cluster = [p2]
            if current_cluster:
                cx = sum(p[0] for p in current_cluster) / len(current_cluster)
                cy = sum(p[1] for p in current_cluster) / len(current_cluster)
                clusters.append((cx, cy))

        # 차선 추적 알고리즘
        def extract_lane(all_clusters, is_left):
            if not all_clusters: return []
            
            front_cones = sorted([c for c in all_clusters if c[1] < 12.0 and abs(c[0]) < 8.0], key=lambda c: math.hypot(c[0], c[1]))
            if not front_cones: return []
            
            C1 = front_cones[0]
            C2 = None
            for c in front_cones[1:]:
                if abs(c[0] - C1[0]) > 3.0:
                    C2 = c
                    break
                    
            if C2 is not None:
                left_start = C1 if C1[0] > C2[0] else C2
                right_start = C2 if C1[0] > C2[0] else C1
                start_c = left_start if is_left else right_start
            else:
                candidates = [c for c in front_cones if (c[0] > -1.5 if is_left else c[0] < 1.5)]
                if not candidates: return []
                start_c = min(candidates, key=lambda c: math.hypot(c[0], c[1]))
                
            lane = [start_c]
            remaining = list(all_clusters)
            remaining.remove(start_c)
            
            while remaining:
                last_c = lane[-1]
                neighbors = []
                for c in remaining:
                    # 절대 허용 불가: 왼쪽 차선이 오른쪽 깊숙이(X < -0.5) 침범하거나, 오른쪽이 왼쪽(X > 0.5) 침범하는 것 금지
                    if is_left and c[0] < -0.5:
                        continue
                    if not is_left and c[0] > 0.5:
                        continue
                        
                    dist = math.hypot(c[0] - last_c[0], c[1] - last_c[1])
                    dy = c[1] - last_c[1]
                    dx = abs(c[0] - last_c[0])
                    # 추적 반경 12m, U턴 대비 후퇴 허용(-2.0m), 차선 점프 완벽 방지(dx < 2.5m)
                    if dist < 12.0 and dy > -2.0 and dx < 2.5:
                        neighbors.append(c)
                if not neighbors: break
                best_c = min(neighbors, key=lambda c: math.hypot(c[0] - last_c[0], c[1] - last_c[1]))
                lane.append(best_c)
                remaining.remove(best_c)
            
            return lane

        left_lane = extract_lane(clusters, is_left=True)
        right_lane = extract_lane(clusters, is_left=False)

        if left_lane and right_lane and left_lane[0] == right_lane[0]:
            if left_lane[0][0] > 0:
                right_lane = []
            else:
                left_lane = []

        if left_lane and right_lane:
            shared = set(left_lane) & set(right_lane)
            if shared:
                first_shared = min(shared, key=lambda c: c[1])
                l_idx = left_lane.index(first_shared)
                r_idx = right_lane.index(first_shared)
                
                l_dist = math.hypot(left_lane[l_idx][0] - left_lane[l_idx-1][0], left_lane[l_idx][1] - left_lane[l_idx-1][1]) if l_idx > 0 else 999
                r_dist = math.hypot(right_lane[r_idx][0] - right_lane[r_idx-1][0], right_lane[r_idx][1] - right_lane[r_idx-1][1]) if r_idx > 0 else 999
                
                if l_dist < r_dist:
                    right_lane = right_lane[:r_idx]
                else:
                    left_lane = left_lane[:l_idx]

        # ---------------------------------------------------------
        # 3. 고깔이 1개만 남았을 때, 반대편 차선의 곡률(기울기)을 활용하여 부드럽게 연장
        # ---------------------------------------------------------
        if len(left_lane) == 1 and len(right_lane) >= 2:
            dx = right_lane[1][0] - right_lane[0][0]
            dy = right_lane[1][1] - right_lane[0][1]
            left_lane.append((left_lane[0][0] + dx, left_lane[0][1] + dy))
            
        elif len(right_lane) == 1 and len(left_lane) >= 2:
            dx = left_lane[1][0] - left_lane[0][0]
            dy = left_lane[1][1] - left_lane[0][1]
            right_lane.append((right_lane[0][0] + dx, right_lane[0][1] + dy))

        # 선 시각화 함수
        def draw_lane(lane_pts, line_obj):
            if not lane_pts:
                line_obj.set_data([], [])
                return
            y_eval = [p[1] for p in lane_pts]
            x_eval = [p[0] for p in lane_pts]
            line_obj.set_data([-x for x in x_eval], y_eval) # 화면(Matplotlib) 좌표계로 변환: -X

        draw_lane(left_lane, self.left_line_plot)
        draw_lane(right_lane, self.right_line_plot)

        # 인식된 고깔(차선) 동그라미 마킹
        valid_cones_x = [-p[0] for p in left_lane] + [-p[0] for p in right_lane]
        valid_cones_y = [p[1] for p in left_lane] + [p[1] for p in right_lane]
        if valid_cones_x:
            self.cone_scatter.set_offsets(np.c_[valid_cones_x, valid_cones_y])
        else:
            self.cone_scatter.set_offsets(np.empty((0,2)))

        # 특정 Y 좌표(전방 거리)에서 차선의 예상 X 좌표를 선형 보간/외삽
        def fit_lane_x_at_y(lane_pts, target_y):
            if not lane_pts: return None
            
            if target_y > lane_pts[-1][1] + 1.0:
                return None
                
            if len(lane_pts) == 1:
                return lane_pts[0][0]
                
            for i in range(len(lane_pts) - 1):
                p1 = lane_pts[i]
                p2 = lane_pts[i+1]
                if p1[1] <= target_y <= p2[1]:
                    ratio = (target_y - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else 0.0
                    return p1[0] + ratio * (p2[0] - p1[0])
            if target_y < lane_pts[0][1]:
                p1, p2 = lane_pts[0], lane_pts[1]
                ratio = (target_y - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else 0.0
                return p1[0] + ratio * (p2[0] - p1[0])
            p1, p2 = lane_pts[-2], lane_pts[-1]
            ratio = (target_y - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else 0.0
            return p1[0] + ratio * (p2[0] - p1[0])

        y_eval_center = np.linspace(0, 10, 30)
        center_x_eval = []
        for y in y_eval_center:
            l_x = fit_lane_x_at_y(left_lane, y)
            r_x = fit_lane_x_at_y(right_lane, y)
            if l_x is not None and r_x is not None:
                center_x_eval.append((l_x + r_x) / 2.0)
            elif l_x is not None:
                center_x_eval.append(l_x - 2.5)
            elif r_x is not None:
                center_x_eval.append(r_x + 2.5)
            else:
                center_x_eval.append(0.0)

        # 중앙선 시각화 (-X 적용)
        self.center_line_plot.set_data([-x for x in center_x_eval], y_eval_center)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

def main(args=None):
    rclpy.init(args=args)
    node = LidarVisualizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
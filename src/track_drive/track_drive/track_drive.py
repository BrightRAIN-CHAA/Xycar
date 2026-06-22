#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=============================================
# 자이트론 자율주행 시뮬레이터 - 트랙 주행 자율주행 SW
# 본 프로그램은 자이트론에서 제작한 것입니다.
# 상업라이센스에 의해 제공되므로 무단배포 및 상업적 이용을 금합니다.
# 교육과 실습 용도로만 사용가능하며 외부유출은 금지됩니다.
#=============================================

import rclpy
import time
import cv2
import os
import math
import numpy as np
import threading

from rclpy.node import Node
from xycar_msgs.msg import XycarMotor
from sensor_msgs.msg import Image, LaserScan
from rclpy.qos import qos_profile_sensor_data
from cv_bridge import CvBridge

# 자체 모듈 임포트
from track_drive.lane_detector import LaneDetector
from track_drive.traffic_light_detector import (
    TrafficLightDetector, SIGNAL_GREEN, SIGNAL_RED,
    SIGNAL_YELLOW, SIGNAL_LEFT_ARROW, SIGNAL_UNKNOWN
)
from track_drive.obstacle_detector import ObstacleDetector
from track_drive.road_sign_detector import RoadSignDetector, ZONE_SCHOOL

class DriveState:
    WAIT_FOR_GREEN = 0
    CONE_DRIVING = 1
    LANE_DRIVING = 2
    PEDESTRIAN_AVOID = 3
    VEHICLE_OVERTAKE = 4
    TRAFFIC_LIGHT_TURN = 5
    SHORTCUT_DRIVING = 6
    FINISHED = 7

# 속도 설정
SPEED_NORMAL = 15
SPEED_SLOW = 7
SPEED_CONE = 8     # 라바콘 구간은 속도를 약간 낮춤
SPEED_OVERTAKE = 12
SPEED_SHORTCUT = 10
SPEED_STOP = 0

ANGLE_MAX = 50
ANGLE_MIN = -50

PID_KP = 0.5
PID_KI = 0.001
PID_KD = 0.3

CONE_TO_LANE_TRANSITION_COUNT = 30
OVERTAKE_DURATION = 2.0
PEDESTRIAN_STOP_DURATION = 3.0

class TrackDriverNode(Node):
    def __init__(self):
        super().__init__('driver')
        self.get_logger().info('----- Xycar 자율주행 노드 시작 -----')

        self.image = None
        self.lidar_ranges = None
        self.bridge = CvBridge()
        self.motor_msg = XycarMotor()

        self.lane_detector = LaneDetector()
        self.traffic_detector = TrafficLightDetector()
        self.obstacle_detector = ObstacleDetector()
        self.road_sign_detector = RoadSignDetector()

        self.drive_state = DriveState.WAIT_FOR_GREEN
        self.lap_count = 0
        self.total_laps = 3

        self.pid_error_sum = 0.0
        self.pid_prev_error = 0.0

        self.cone_no_detect_count = 0
        self.overtake_start_time = 0
        self.overtake_direction = 0
        self.pedestrian_stop_time = 0
        self.is_pedestrian_waiting = False
        self.shortcut_available = False
        self.left_turn_checked = False

        self.has_seen_cones = False
        self.last_cone_angle = 0.0

        self.speed_limit_ratio = 1.0
        self.debug_mode = True

        self.motor_pub = self.create_publisher(XycarMotor, 'xycar_motor', 10)
        self.sub_front = self.create_subscription(
            Image, '/usb_cam/image_raw/front',
            self.cam_callback, qos_profile_sensor_data)
        self.subscription = self.create_subscription(
            LaserScan, '/scan',
            self.lidar_callback, qos_profile_sensor_data)

        self.get_logger().info("모든 모듈 초기화 완료. 주행 준비 상태.")

    def cam_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    def lidar_callback(self, msg):
        self.lidar_ranges = msg.ranges

    def drive(self, angle, speed):
        angle = max(ANGLE_MIN, min(ANGLE_MAX, angle))
        speed = speed * self.speed_limit_ratio

        self.motor_msg.angle = float(angle)
        self.motor_msg.speed = float(speed)
        self.motor_pub.publish(self.motor_msg)

    def pid_steering(self, error):
        self.pid_error_sum += error
        self.pid_error_sum = max(-500, min(500, self.pid_error_sum))

        d_error = error - self.pid_prev_error
        self.pid_prev_error = error

        angle = (PID_KP * error) + (PID_KI * self.pid_error_sum) + (PID_KD * d_error)

        return max(ANGLE_MIN, min(ANGLE_MAX, angle))

    def handle_wait_for_green(self):
        signal, _ = self.traffic_detector.detect(self.image)

        if signal == SIGNAL_GREEN:
            self.get_logger().info("★ 녹색 신호 감지! 출발합니다!")
            self.drive_state = DriveState.CONE_DRIVING
            self.traffic_detector.reset()
        else:
            self.drive(angle=0, speed=SPEED_STOP)
            if signal != SIGNAL_UNKNOWN:
                self.get_logger().info(f"신호 대기 중... 현재: {signal}")

    def handle_cone_driving(self):
        cone_info = self.obstacle_detector.detect_cones(self.lidar_ranges)

        if cone_info['cone_detected']:
            angle = cone_info['steer_offset']
            angle = max(ANGLE_MIN, min(ANGLE_MAX, angle))
            self.drive(angle=angle, speed=SPEED_CONE)
            self.cone_no_detect_count = 0
            self.has_seen_cones = True
            self.last_cone_angle = angle
        else:
            if not self.has_seen_cones:
                # 라바콘을 아직 못 본 상태면 직진 (출발 직후)
                self.drive(angle=0, speed=SPEED_CONE)
            else:
                self.cone_no_detect_count += 1

                if self.cone_no_detect_count > CONE_TO_LANE_TRANSITION_COUNT:
                    self.get_logger().info("★ 라바콘 구간 통과 완료 → 차선 주행 모드 전환")
                    self.drive_state = DriveState.LANE_DRIVING
                    self.cone_no_detect_count = 0
                else:
                    # 미감지 시 이전 조향 유지하며 주행
                    self.drive(angle=self.last_cone_angle, speed=SPEED_CONE)

    def handle_lane_driving(self):
        zone_state, speed_ratio = self.road_sign_detector.detect(self.image)
        self.speed_limit_ratio = speed_ratio
        if zone_state == ZONE_SCHOOL:
            self.get_logger().info("⚠ 어린이 보호구역 진입 → 속도 제한")

        signal, _ = self.traffic_detector.detect(self.image)

        if self.lap_count >= 1 and signal == SIGNAL_LEFT_ARROW:
            police_blocking = self.obstacle_detector.detect_police_car(self.image)
            if not police_blocking:
                self.get_logger().info("★ 좌회전 신호 + 경찰차 없음 → 좌회전 지름길 진입!")
                self.drive_state = DriveState.TRAFFIC_LIGHT_TURN
                self.shortcut_available = True
                return
            else:
                self.get_logger().info("⚠ 좌회전 신호이나 경찰차가 막고 있음 → 직진")

        ped_info = self.obstacle_detector.detect_pedestrian(self.image, self.lidar_ranges)
        if ped_info['pedestrian_detected'] and ped_info['should_stop']:
            self.get_logger().info("★ 보행자 감지 → 회피/정지 모드 전환")
            self.drive_state = DriveState.PEDESTRIAN_AVOID
            self.pedestrian_stop_time = time.time()
            return

        vehicle_info = self.obstacle_detector.detect_vehicle(self.image, self.lidar_ranges)
        if vehicle_info['should_overtake']:
            self.get_logger().info(f"★ 전방 차량 감지 → {vehicle_info['overtake_direction']}으로 추월")
            self.drive_state = DriveState.VEHICLE_OVERTAKE
            self.overtake_start_time = time.time()
            self.overtake_direction = -1 if vehicle_info['overtake_direction'] == 'LEFT' else 1
            return

        steer_offset, debug_img = self.lane_detector.detect(self.image)
        angle = self.pid_steering(steer_offset)

        front_info = self.obstacle_detector.detect_front_obstacle(self.lidar_ranges)
        if front_info['danger'] == 'NEAR':
            speed = SPEED_SLOW
        elif front_info['danger'] == 'DANGER':
            speed = SPEED_STOP
        else:
            speed = SPEED_NORMAL

        self.drive(angle=angle, speed=speed)

        if self.debug_mode and debug_img is not None:
            cv2.putText(debug_img, f"Lap: {self.lap_count}/{self.total_laps}",
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(debug_img, f"State: LANE | Zone: {zone_state}",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(debug_img, f"Angle: {angle:.1f} Speed: {speed:.1f}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    def handle_pedestrian_avoid(self):
        ped_info = self.obstacle_detector.detect_pedestrian(self.image, self.lidar_ranges)

        if ped_info['pedestrian_detected']:
            if ped_info['should_stop']:
                self.drive(angle=0, speed=SPEED_STOP)
                self.is_pedestrian_waiting = True
                self.pedestrian_stop_time = time.time()
                self.get_logger().info(f"보행자 정지 대기 중... 거리: {ped_info['pedestrian_dist']:.1f}m")
            else:
                steer_offset, _ = self.lane_detector.detect(self.image)
                angle = self.pid_steering(steer_offset)
                self.drive(angle=angle, speed=SPEED_SLOW)
        else:
            elapsed = time.time() - self.pedestrian_stop_time
            if elapsed > PEDESTRIAN_STOP_DURATION or not self.is_pedestrian_waiting:
                self.get_logger().info("★ 보행자 통과 확인 → 차선 주행 복귀")
                self.drive_state = DriveState.LANE_DRIVING
                self.is_pedestrian_waiting = False
            else:
                self.drive(angle=0, speed=SPEED_STOP)

    def handle_vehicle_overtake(self):
        elapsed = time.time() - self.overtake_start_time

        if elapsed < OVERTAKE_DURATION * 0.4:
            angle = self.overtake_direction * 35
            self.drive(angle=angle, speed=SPEED_OVERTAKE)
        elif elapsed < OVERTAKE_DURATION * 0.7:
            steer_offset, _ = self.lane_detector.detect(self.image)
            angle = self.pid_steering(steer_offset)
            self.drive(angle=angle, speed=SPEED_OVERTAKE)
        elif elapsed < OVERTAKE_DURATION:
            angle = -self.overtake_direction * 30
            self.drive(angle=angle, speed=SPEED_OVERTAKE)
        else:
            self.get_logger().info("★ 추월 완료 → 차선 주행 복귀")
            self.drive_state = DriveState.LANE_DRIVING

    def handle_traffic_light_turn(self):
        if self.shortcut_available:
            self.drive(angle=-45, speed=SPEED_SLOW)
            time.sleep(1.5)
            self.get_logger().info("★ 좌회전 완료 → 지름길 주행 모드")
            self.drive_state = DriveState.SHORTCUT_DRIVING
            self.shortcut_available = False
        else:
            self.drive_state = DriveState.LANE_DRIVING

    def handle_shortcut_driving(self):
        front_info = self.obstacle_detector.detect_front_obstacle(self.lidar_ranges)

        if front_info['danger'] == 'DANGER':
            if front_info['left_dist'] > front_info['right_dist']:
                angle = -30
            else:
                angle = 30
            self.drive(angle=angle, speed=SPEED_SLOW)
        elif front_info['danger'] == 'NEAR':
            if front_info['min_angle'] > 0:
                angle = -20
            else:
                angle = 20
            self.drive(angle=angle, speed=SPEED_SLOW)
        else:
            steer_offset, _ = self.lane_detector.detect(self.image)
            angle = self.pid_steering(steer_offset)
            self.drive(angle=angle, speed=SPEED_SHORTCUT)

    def check_lap_completion(self):
        if self.drive_state in (DriveState.WAIT_FOR_GREEN, DriveState.FINISHED):
            return

        signal, _ = self.traffic_detector.detect(self.image)

    def main_loop(self):
        self.get_logger().info("======================================")
        self.get_logger().info("  자 율 주 행   시 작 ...              ")
        self.get_logger().info("======================================")

        while rclpy.ok() and self.image is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            self.get_logger().info("카메라 데이터 수신 대기 중...")
            time.sleep(0.5)

        self.get_logger().info("센서 데이터 수신 시작. 자율주행 루프 진입.")

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.01)

            if self.lap_count >= self.total_laps:
                self.get_logger().info("★★★ 3바퀴 완주! 주행 종료! ★★★")
                self.drive(angle=0, speed=SPEED_STOP)
                self.drive_state = DriveState.FINISHED
                break

            try:
                if self.drive_state == DriveState.WAIT_FOR_GREEN:
                    self.handle_wait_for_green()

                elif self.drive_state == DriveState.CONE_DRIVING:
                    self.handle_cone_driving()

                elif self.drive_state == DriveState.LANE_DRIVING:
                    self.handle_lane_driving()

                elif self.drive_state == DriveState.PEDESTRIAN_AVOID:
                    self.handle_pedestrian_avoid()

                elif self.drive_state == DriveState.VEHICLE_OVERTAKE:
                    self.handle_vehicle_overtake()

                elif self.drive_state == DriveState.TRAFFIC_LIGHT_TURN:
                    self.handle_traffic_light_turn()

                elif self.drive_state == DriveState.SHORTCUT_DRIVING:
                    self.handle_shortcut_driving()

                elif self.drive_state == DriveState.FINISHED:
                    self.drive(angle=0, speed=SPEED_STOP)
                    break

            except Exception as e:
                self.get_logger().error(f"주행 오류 발생: {e}")
                self.drive(angle=0, speed=SPEED_STOP)

            time.sleep(0.02)


def main(args=None):
    rclpy.init(args=args)
    node = TrackDriverNode()

    try:
        node.main_loop()
    except KeyboardInterrupt:
        node.get_logger().info("사용자 중단 요청. 안전 정지 중...")
    finally:
        node.drive(angle=0, speed=0)
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

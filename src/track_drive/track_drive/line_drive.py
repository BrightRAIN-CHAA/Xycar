import cv2
import numpy as np
import math

class LineDriver:
    def __init__(self, target_speed=10, kp=0.5, kd=0.4, a_max=0.01, k_expand=50000.0, max_expand=360.0, lane_width=360, lookahead_dist=100):
        """
        카메라 차선 인식 주행(Phase 2)을 위한 클래스입니다.
        Bird's Eye View 변환 및 Sliding Window를 사용합니다.
        물리 기반(Square Root 모델) 속도 제어 및 동적 FOV 제어가 적용되었습니다.
        """
        self.target_speed = target_speed
        self.kp = kp  # 직선 구간의 흔들림을 막기 위해 기본값(0.5)을 대폭 낮춤
        self.kd = kd  # D게인도 비율에 맞게 조정 (0.4)
        self.lookahead_dist = lookahead_dist # 전방 주시거리 (코너 선제 조향용)
        
        # 물리 제어 및 동적 FOV 파라미터
        self.a_max = a_max       # 최대 횡가속도 한계 (튜닝 필요)
        self.k_expand = k_expand # 곡률 비례 시야 확장 계수 (튜닝 필요)
        self.max_expand = max_expand # 한쪽 방향 최대 확장 픽셀 (360으로 대폭 확대)
        self.lane_width = lane_width # 단일 차선 검출 시 사용할 차선 폭 (픽셀 단위)
        
        self.prev_error = 0.0
        self.prev_angle = 0.0
        self.prev_kappa = 0.0    # 이전 프레임의 곡률(EMA 스무딩 적용)
        self.prev_speed = target_speed
        
        # 튜닝이 필요한 부분: 원근 변환(Perspective Transform) 기본 좌표
        self.base_src_points = np.float32([
            [78, 260], [562, 260],
            [-87, 480], [727, 480]
        ])
        self.src_points = self.base_src_points.copy()
        
        # 위 사다리꼴을 펼칠 직사각형 좌표 (Top View)
        self.dst_points = np.float32([
            [0, 0], [640, 0],
            [0, 480], [640, 480]
        ])
        
        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)
        self.Minv = cv2.getPerspectiveTransform(self.dst_points, self.src_points)

    def color_filter(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 노란색 차선 (좌측 중앙선) 추출
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([45, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # 흰색 차선 (우측 갓길선) 추출
        # 음영(그림자) 구간에서도 차선을 안정적으로 검출할 수 있도록 V(Value) 하한선을 200 -> 140으로 대폭 하향
        lower_white = np.array([0, 0, 140])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # 마스크를 합치지 않고 개별 반환 (체크무늬 간섭 방지)
        return yellow_mask, white_mask

    def sliding_window(self, left_warped, right_warped, dynamic_lane_width):
        height = left_warped.shape[0]
        hist_left = np.sum(left_warped[height//2:, :], axis=0)
        hist_right = np.sum(right_warped[height//2:, :], axis=0)
        
        midpoint = int(hist_left.shape[0] // 2)
        width = left_warped.shape[1]
        
        # 1. 좌측 차선 우선 탐색
        if np.max(hist_left[:midpoint]) > 0:
            leftx_base = np.argmax(hist_left[:midpoint])
        else:
            leftx_base = None
            
        # 2. 우측 차선 탐색 (좌측 차선이 검출되었다면 인접 차선 간섭 방지를 위해 탐색 영역을 제한)
        if leftx_base is not None:
            expected_right = int(leftx_base + dynamic_lane_width)
            r_start = max(midpoint, expected_right - 80)
            r_end = min(width, expected_right + 80)
            if r_start < r_end and np.max(hist_right[r_start:r_end]) > 0:
                rightx_base = np.argmax(hist_right[r_start:r_end]) + r_start
            else:
                rightx_base = min(width - 1, expected_right)
        else:
            # 좌측 차선이 없는 경우 우측 절반 영역에서 탐색
            if np.max(hist_right[midpoint:]) > 0:
                rightx_base = np.argmax(hist_right[midpoint:]) + midpoint
            else:
                rightx_base = None
                
            # 우측 차선이 검출되었다면 좌측 차선 역유도
            if rightx_base is not None:
                expected_left = int(rightx_base - dynamic_lane_width)
                l_start = max(0, expected_left - 80)
                l_end = min(midpoint, expected_left + 80)
                if l_start < l_end and np.max(hist_left[l_start:l_end]) > 0:
                    leftx_base = np.argmax(hist_left[l_start:l_end]) + l_start
                else:
                    leftx_base = max(0, expected_left)
            
        nwindows = 9
        window_height = int(height // nwindows)
        
        nonzero_l = left_warped.nonzero()
        nonzeroy_l = np.array(nonzero_l[0])
        nonzerox_l = np.array(nonzero_l[1])
        
        nonzero_r = right_warped.nonzero()
        nonzeroy_r = np.array(nonzero_r[0])
        nonzerox_r = np.array(nonzero_r[1])
        
        leftx_current = leftx_base
        rightx_current = rightx_base
        
        margin = 120 # 급코너 추적을 위해 마진 넉넉하게 유지
        minpix = 40
        
        left_lane_inds = []
        right_lane_inds = []
        
        for window in range(nwindows):
            win_y_low = height - (window + 1) * window_height
            win_y_high = height - window * window_height
            
            # 왼쪽 차선 슬라이딩 윈도우
            if leftx_current is not None:
                win_xleft_low = leftx_current - margin
                win_xleft_high = leftx_current + margin
                good_left_inds = ((nonzeroy_l >= win_y_low) & (nonzeroy_l < win_y_high) & 
                                  (nonzerox_l >= win_xleft_low) & (nonzerox_l < win_xleft_high)).nonzero()[0]
                
                # 가로선(정지선) 필터링: 넓게 퍼져있으면 무시
                is_valid = True
                if len(good_left_inds) > 0:
                    x_pixels = nonzerox_l[good_left_inds]
                    if (np.max(x_pixels) - np.min(x_pixels)) > 80:
                        is_valid = False
                
                if is_valid and len(good_left_inds) > 0:
                    left_lane_inds.append(good_left_inds)
                    if len(good_left_inds) > minpix:
                        leftx_current = int(np.mean(nonzerox_l[good_left_inds]))
                        
            # 오른쪽 차선 슬라이딩 윈도우
            if rightx_current is not None:
                win_xright_low = rightx_current - margin
                win_xright_high = rightx_current + margin
                good_right_inds = ((nonzeroy_r >= win_y_low) & (nonzeroy_r < win_y_high) & 
                                   (nonzerox_r >= win_xright_low) & (nonzerox_r < win_xright_high)).nonzero()[0]
                
                # 가로선(정지선) 필터링: 넓게 퍼져있으면 무시
                is_valid = True
                if len(good_right_inds) > 0:
                    x_pixels = nonzerox_r[good_right_inds]
                    if (np.max(x_pixels) - np.min(x_pixels)) > 80:
                        is_valid = False
                        
                if is_valid and len(good_right_inds) > 0:
                    right_lane_inds.append(good_right_inds)
                    if len(good_right_inds) > minpix:
                        rightx_current = int(np.mean(nonzerox_r[good_right_inds]))
                        
        min_y_l = height
        min_y_r = height
        
        # 왼쪽 차선 다항식 피팅
        if len(left_lane_inds) > 0:
            left_lane_inds = np.concatenate(left_lane_inds)
            leftx = nonzerox_l[left_lane_inds]
            lefty = nonzeroy_l[left_lane_inds] 
            if len(leftx) > 50:
                y_span = np.max(lefty) - np.min(lefty)
                if y_span > 220:
                    left_fit = np.polyfit(lefty, leftx, 3) # S자 코너 대응 3차식
                elif y_span > 100:
                    left_fit = np.polyfit(lefty, leftx, 2) # 일반 코너 2차식
                else:
                    left_fit = np.polyfit(lefty, leftx, 1) # 짧은 구간/직선 1차식
            else:
                left_fit = None
            if len(lefty) > 0:
                min_y_l = np.min(lefty)
        else:
            left_fit = None
            
        # 오른쪽 차선 다항식 피팅
        if len(right_lane_inds) > 0:
            right_lane_inds = np.concatenate(right_lane_inds)
            rightx = nonzerox_r[right_lane_inds]
            righty = nonzeroy_r[right_lane_inds]
            if len(rightx) > 50:
                y_span = np.max(righty) - np.min(righty)
                if y_span > 220:
                    right_fit = np.polyfit(righty, rightx, 3) # S자 코너 대응 3차식
                elif y_span > 100:
                    right_fit = np.polyfit(righty, rightx, 2) # 일반 코너 2차식
                else:
                    right_fit = np.polyfit(righty, rightx, 1) # 짧은 구간/직선 1차식
            else:
                right_fit = None
            if len(righty) > 0:
                min_y_r = np.min(righty)
        else:
            right_fit = None
            
        return left_fit, right_fit, min_y_l, min_y_r

    def compute_curvature(self, fit, y_eval):
        """ 다항식 차수(fit의 길이)에 맞춰 곡률(|k|)을 계산합니다. """
        if fit is None:
            return 0.0
        
        deg = len(fit) - 1
        if deg == 3:
            A, B, C, D = fit
            dx = 3 * A * y_eval**2 + 2 * B * y_eval + C
            d2x = 6 * A * y_eval + 2 * B
        elif deg == 2:
            A, B, C = fit
            dx = 2 * A * y_eval + B
            d2x = 2 * A
        elif deg == 1:
            dx = fit[0]
            d2x = 0.0
        else:
            return 0.0
            
        numerator = abs(d2x)
        denominator = (1 + dx**2)**1.5
        if denominator < 1e-6:
            return 0.0
        return numerator / denominator

    def compute_steering(self, cv_image):
        if cv_image is None:
            return 0.0, 0.0
            
        height, width = cv_image.shape[:2]
        
        # --- 0. 동적 시야각(Dynamic FOV) 적용 ---
        # 코너 감지 시점부터 부드럽고 신속하게 시야를 확장하기 위해 소프트스텝 함수 적용
        expansion = self.max_expand * (self.prev_kappa / (self.prev_kappa + 0.0015))
        
        self.src_points = self.base_src_points.copy()
        
        # FOV 확장 적용 (상하좌우 대칭 확장으로 불안정한 Jittering 제거)
        self.src_points[0][0] -= expansion
        self.src_points[1][0] += expansion
        self.src_points[2][0] -= expansion
        self.src_points[3][0] += expansion
        
        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)
        self.Minv = cv2.getPerspectiveTransform(self.dst_points, self.src_points)
        
        # 1. ROI 적용
        roi_img = cv_image.copy()
        
        # 2. 색상 필터링 (분리된 마스크)
        yellow_mask, white_mask = self.color_filter(roi_img)
        
        # 3. 버드아이뷰 변환 (각각 독립 변환)
        yellow_warped = cv2.warpPerspective(yellow_mask, self.M, (width, height), flags=cv2.INTER_LINEAR)
        white_warped = cv2.warpPerspective(white_mask, self.M, (width, height), flags=cv2.INTER_LINEAR)
        
        # FOV 확장에 따른 BEV 이미지 내 실제 차선 폭(lane_width) 변형 보정
        src_width_base = 745.0
        dynamic_lane_width = self.lane_width * src_width_base / (src_width_base + 2.0 * expansion)
        
        # 4. 슬라이딩 윈도우 및 다항식 피팅
        left_fit, right_fit, min_y_l, min_y_r = self.sliding_window(yellow_warped, white_warped, dynamic_lane_width)
        
        # --- Look-ahead 전방 주시 곡률 예측 ---
        # 외삽 방지: 차선이 실제 검출된 가장 높은 지점(min_y)과 기본 전방주시점(height*0.2) 중 더 낮은 곳(y값이 큰 곳)을 기준
        lookahead_y_left = max(height * 0.2, min_y_l)
        lookahead_y_right = max(height * 0.2, min_y_r)
        
        kappa_left = self.compute_curvature(left_fit, lookahead_y_left)
        kappa_right = self.compute_curvature(right_fit, lookahead_y_right)
        
        if left_fit is not None and right_fit is not None:
            target_kappa = max(kappa_left, kappa_right)
        elif left_fit is not None:
            target_kappa = kappa_left
        elif right_fit is not None:
            target_kappa = kappa_right
        else:
            target_kappa = 0.0
            
        self.prev_kappa = self.prev_kappa * 0.7 + target_kappa * 0.3
        
        # --- 물리 기반 목표 속도 제어 (Square Root 모델) ---
        if self.prev_kappa > 1e-6:
            v_curve = math.sqrt(self.a_max / self.prev_kappa)
        else:
            v_curve = self.target_speed
            
        target_v = min(self.target_speed, v_curve)
        current_speed = self.prev_speed * 0.8 + target_v * 0.2
        self.prev_speed = current_speed

        # --- 디버깅용 이미지 생성 (버드아이뷰 + 목표 경로 + 데이터) ---
        binary_warped = cv2.bitwise_or(yellow_warped, white_warped)
        out_img = np.dstack((binary_warped, binary_warped, binary_warped)).astype(np.uint8)
        
        ploty = np.linspace(0, height - 1, height)
        target_fitx = None
        
        if left_fit is not None and right_fit is not None:
            left_fitx = np.polyval(left_fit, ploty)
            right_fitx = np.polyval(right_fit, ploty)
            target_fitx = (left_fitx + right_fitx) / 2.0
            
            left_pts = np.array([np.transpose(np.vstack([left_fitx, ploty]))], np.int32)
            right_pts = np.array([np.transpose(np.vstack([right_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [left_pts], isClosed=False, color=(255, 0, 0), thickness=2)
            cv2.polylines(out_img, [right_pts], isClosed=False, color=(0, 255, 0), thickness=2)
            
        elif left_fit is not None:
            left_fitx = np.polyval(left_fit, ploty)
            target_fitx = left_fitx + (dynamic_lane_width / 2.0)
            
            left_pts = np.array([np.transpose(np.vstack([left_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [left_pts], isClosed=False, color=(255, 0, 0), thickness=2)
            
        elif right_fit is not None:
            right_fitx = np.polyval(right_fit, ploty)
            target_fitx = right_fitx - (dynamic_lane_width / 2.0)
            
            right_pts = np.array([np.transpose(np.vstack([right_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [right_pts], isClosed=False, color=(0, 255, 0), thickness=2)
            
        if target_fitx is not None:
            target_pts = np.array([np.transpose(np.vstack([target_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [target_pts], isClosed=False, color=(0, 0, 255), thickness=1)
            
        # 텍스트 오버레이
        cv2.putText(out_img, f"Kappa: {self.prev_kappa:.5f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(out_img, f"Speed: {current_speed:.2f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(out_img, f"FOV Exp: {expansion:.1f} px", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        self.debug_img = out_img
        
        # 5. Cross Track Error 계산 및 조향 제어
        # 전방 주시거리(lookahead_dist)만큼 위쪽 차선을 바라보아 코너 진입 시 미리 감아 나가도록 함
        y_eval = max(0, min(height - 1, height - 1 - self.lookahead_dist))
        
        target_x = width / 2.0
        if target_fitx is not None:
            target_x = target_fitx[int(y_eval)] 
            
            # BEV 타겟 점을 다시 카메라 원본 이미지 좌표계로 역투영하여 
            # FOV Shift 및 확장으로 인한 겉보기 위치 변화를 완벽하게 제거하고 정확한 조향 에러 계산
            bev_target = np.array([[[target_x, y_eval]]], dtype=np.float32)
            camera_target = cv2.perspectiveTransform(bev_target, self.Minv)
            camera_target_x = camera_target[0][0][0]
            error = camera_target_x - (width / 2.0)
        else:
            error = 0.0
        derivative = error - self.prev_error
        
        # --- 비선형(Quadratic) 조향 게인 스케줄링 ---
        # 직선(error가 작을 때)에서는 게인을 대폭 낮추어(최소 0.1배) 미세 조향하고,
        # 코너(error가 클 때)에서는 게인을 대폭 높여(최대 5.0배) 강하게 조향하도록 설계
        e_norm = abs(error) / 40.0
        scale = e_norm ** 2
        scale = max(0.1, min(5.0, scale))
        
        dynamic_kp = self.kp * scale
        dynamic_kd = self.kd * scale
        
        raw_angle = (dynamic_kp * error) + (dynamic_kd * derivative)
        self.prev_error = error
        
        angle = self.prev_angle * 0.7 + raw_angle * 0.3
        angle = max(-100.0, min(100.0, angle))
        self.prev_angle = angle
        
        return float(angle), float(current_speed)

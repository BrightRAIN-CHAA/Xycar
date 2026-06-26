import cv2
import numpy as np
import math

class LineDriver:
    def __init__(self, target_speed=23, kp=0.5, kd=0.9, a_max=0.15, k_expand=50000.0, max_expand=360.0, lane_width=360, lookahead_dist=100):
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
        
        # 장애물 회피(치우침 주행) 상태 변수
        self.lane_shift_offset = 0.0
        self.shift_state = 'CENTER'
        self.shift_timer = 0
        
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

    def sliding_window(self, yellow_warped, white_warped, dynamic_lane_width):
        """3차선 검출: 좌측 흰색 실선, 노란색 중앙선, 우측 흰색 실선"""
        height = yellow_warped.shape[0]
        img_width = yellow_warped.shape[1]
        
        hist_yellow = np.sum(yellow_warped[height//2:, :], axis=0)
        hist_white = np.sum(white_warped[height//2:, :], axis=0)
        
        midpoint = img_width // 2
        
        # === 1. 노란색 중앙선 베이스 탐색 (좌측 절반) ===
        if np.max(hist_yellow[:midpoint]) > 0:
            yellowx_base = np.argmax(hist_yellow[:midpoint])
        else:
            yellowx_base = None
        
        # === 2. 우측 흰색 차선 베이스 탐색 (노란선 기준 크로스 가이드) ===
        if yellowx_base is not None:
            expected_right = int(yellowx_base + dynamic_lane_width)
            r_start = max(midpoint, expected_right - 80)
            r_end = min(img_width, expected_right + 80)
            if r_start < r_end and np.max(hist_white[r_start:r_end]) > 0:
                right_whitex_base = np.argmax(hist_white[r_start:r_end]) + r_start
            else:
                right_whitex_base = min(img_width - 1, expected_right)
        else:
            if np.max(hist_white[midpoint:]) > 0:
                right_whitex_base = np.argmax(hist_white[midpoint:]) + midpoint
            else:
                right_whitex_base = None
            # 우측 차선으로부터 노란선 역유도
            if right_whitex_base is not None and yellowx_base is None:
                expected_yellow = int(right_whitex_base - dynamic_lane_width)
                y_start = max(0, expected_yellow - 80)
                y_end = min(midpoint, expected_yellow + 80)
                if y_start < y_end and np.max(hist_yellow[y_start:y_end]) > 0:
                    yellowx_base = np.argmax(hist_yellow[y_start:y_end]) + y_start
                else:
                    yellowx_base = max(0, expected_yellow)
        
        # === 3. 좌측 흰색 차선 베이스 탐색 (노란선 왼쪽에 위치) ===
        if yellowx_base is not None:
            expected_left_white = int(yellowx_base - dynamic_lane_width)
            lw_start = max(0, expected_left_white - 80)
            lw_end = max(lw_start, min(int(yellowx_base) - 20, expected_left_white + 80))
            if lw_start < lw_end and np.max(hist_white[lw_start:lw_end]) > 0:
                left_whitex_base = np.argmax(hist_white[lw_start:lw_end]) + lw_start
            else:
                left_whitex_base = None
        else:
            lw_region = img_width // 3
            if np.max(hist_white[:lw_region]) > 0:
                left_whitex_base = np.argmax(hist_white[:lw_region])
            else:
                left_whitex_base = None
        
        # === 슬라이딩 윈도우 설정 ===
        nwindows = 9
        window_height = int(height // nwindows)
        
        nonzero_y = yellow_warped.nonzero()
        nonzeroy_y = np.array(nonzero_y[0])
        nonzerox_y = np.array(nonzero_y[1])
        
        nonzero_w = white_warped.nonzero()
        nonzeroy_w = np.array(nonzero_w[0])
        nonzerox_w = np.array(nonzero_w[1])
        
        yellowx_current = yellowx_base
        right_whitex_current = right_whitex_base
        left_whitex_current = left_whitex_base
        
        margin = 120
        minpix = 40
        
        yellow_lane_inds = []
        right_white_lane_inds = []
        left_white_lane_inds = []
        
        for window in range(nwindows):
            win_y_low = height - (window + 1) * window_height
            win_y_high = height - window * window_height
            
            # --- 노란색 중앙선 윈도우 ---
            if yellowx_current is not None:
                win_x_low = yellowx_current - margin
                win_x_high = yellowx_current + margin
                good_inds = ((nonzeroy_y >= win_y_low) & (nonzeroy_y < win_y_high) &
                             (nonzerox_y >= win_x_low) & (nonzerox_y < win_x_high)).nonzero()[0]
                is_valid = True
                if len(good_inds) > 0:
                    x_pixels = nonzerox_y[good_inds]
                    if (np.max(x_pixels) - np.min(x_pixels)) > 80:
                        is_valid = False
                if is_valid and len(good_inds) > 0:
                    yellow_lane_inds.append(good_inds)
                    if len(good_inds) > minpix:
                        yellowx_current = int(np.mean(nonzerox_y[good_inds]))
            
            # --- 우측 흰색 차선 윈도우 ---
            if right_whitex_current is not None:
                win_x_low = right_whitex_current - margin
                win_x_high = right_whitex_current + margin
                good_inds = ((nonzeroy_w >= win_y_low) & (nonzeroy_w < win_y_high) &
                             (nonzerox_w >= win_x_low) & (nonzerox_w < win_x_high)).nonzero()[0]
                is_valid = True
                if len(good_inds) > 0:
                    x_pixels = nonzerox_w[good_inds]
                    if (np.max(x_pixels) - np.min(x_pixels)) > 80:
                        is_valid = False
                if is_valid and len(good_inds) > 0:
                    right_white_lane_inds.append(good_inds)
                    if len(good_inds) > minpix:
                        right_whitex_current = int(np.mean(nonzerox_w[good_inds]))
            
            # --- 좌측 흰색 차선 윈도우 ---
            if left_whitex_current is not None:
                win_x_low = left_whitex_current - margin
                win_x_high = left_whitex_current + margin
                good_inds = ((nonzeroy_w >= win_y_low) & (nonzeroy_w < win_y_high) &
                             (nonzerox_w >= win_x_low) & (nonzerox_w < win_x_high)).nonzero()[0]
                is_valid = True
                if len(good_inds) > 0:
                    x_pixels = nonzerox_w[good_inds]
                    if (np.max(x_pixels) - np.min(x_pixels)) > 80:
                        is_valid = False
                if is_valid and len(good_inds) > 0:
                    left_white_lane_inds.append(good_inds)
                    if len(good_inds) > minpix:
                        left_whitex_current = int(np.mean(nonzerox_w[good_inds]))
        
        # === 다항식 피팅 (공통 헬퍼) ===
        def _fit_lane(lane_inds_list, nonzerox, nonzeroy):
            if len(lane_inds_list) > 0:
                all_inds = np.concatenate(lane_inds_list)
                x = nonzerox[all_inds]
                y = nonzeroy[all_inds]
                if len(x) > 50:
                    y_span = np.max(y) - np.min(y)
                    if y_span > 220:
                        fit = np.polyfit(y, x, 3)
                    elif y_span > 100:
                        fit = np.polyfit(y, x, 2)
                    else:
                        fit = np.polyfit(y, x, 1)
                else:
                    fit = None
                min_y = np.min(y) if len(y) > 0 else height
                return fit, min_y
            return None, height
        
        yellow_fit, min_y_yellow = _fit_lane(yellow_lane_inds, nonzerox_y, nonzeroy_y)
        rw_fit, min_y_rw = _fit_lane(right_white_lane_inds, nonzerox_w, nonzeroy_w)
        lw_fit, min_y_lw = _fit_lane(left_white_lane_inds, nonzerox_w, nonzeroy_w)
        
        return yellow_fit, rw_fit, lw_fit, min_y_yellow, min_y_rw, min_y_lw

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

    def compute_steering(self, cv_image, lidar_ranges=None):
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
        
        # 4. 슬라이딩 윈도우 및 다항식 피팅 (3차선 검출)
        yellow_fit, rw_fit, lw_fit, min_y_y, min_y_rw, min_y_lw = self.sliding_window(yellow_warped, white_warped, dynamic_lane_width)
        
        # --- 다중 지점 곡률(Kappa) 스캔 (완전한 직선 탈출 확인) ---
        # 차량 코앞(y=height*0.9), 중간(y=height*0.5), 멀리(y=height*0.2) 
        # 세 지점의 꺾임 정도를 모두 스캔하여 차가 온전히 직선에 들어왔는지 확인합니다.
        kappas = []
        eval_points = [height * 0.9, height * 0.5, height * 0.2]
        for eval_y in eval_points:
            if yellow_fit is not None and eval_y > min_y_y:
                kappas.append(self.compute_curvature(yellow_fit, eval_y))
            if rw_fit is not None and eval_y > min_y_rw:
                kappas.append(self.compute_curvature(rw_fit, eval_y))
            if lw_fit is not None and eval_y > min_y_lw:
                kappas.append(self.compute_curvature(lw_fit, eval_y))
                
        target_kappa = max(kappas) if kappas else 0.0
            
        self.prev_kappa = self.prev_kappa * 0.7 + target_kappa * 0.3
        
        # --- 물리 기반 목표 속도 제어 (Square Root 모델) ---
        if self.prev_kappa > 1e-6:
            # 곡선 구간의 속도를 기존 계산값 대비 70% 수준으로 강제 억제합니다.
            v_curve = math.sqrt(self.a_max / self.prev_kappa) * 0.70
        else:
            v_curve = self.target_speed
            
        target_v = min(self.target_speed, v_curve)
        
        # --- 비대칭 가/감속 필터 ---
        # 브레이크(감속)는 팍 밟고, 악셀(가속)은 매우 천천히 지그시 밟아서 
        # 차량이 완전히 코너를 빠져나와 궤도를 확실히 잡은 뒤에야 속도가 올라가도록 설정합니다.
        if target_v > self.prev_speed:
            current_speed = self.prev_speed * 0.95 + target_v * 0.05 # 느린 가속
        else:
            current_speed = self.prev_speed * 0.4 + target_v * 0.6   # 즉각적인 감속
            
        self.prev_speed = current_speed

        # --- 디버깅용 이미지 생성 (버드아이뷰 + 3차선 + 목표 경로) ---
        binary_warped = cv2.bitwise_or(yellow_warped, white_warped)
        out_img = np.dstack((binary_warped, binary_warped, binary_warped)).astype(np.uint8)
        
        ploty = np.linspace(0, height - 1, height)
        
        # --- 주행 경로 추정 (중앙선 최우선 추종) ---
        target_fitx = None
        
        if yellow_fit is not None:
            yellow_fitx = np.polyval(yellow_fit, ploty)
            yellow_pts = np.array([np.transpose(np.vstack([yellow_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [yellow_pts], isClosed=False, color=(255, 0, 0), thickness=2)  # 파란색: 노란 중앙선
            # 1. 평균 계산 제거: 노란선(중앙선)이 보이면 1순위 메인 타겟으로 고정합니다.
            target_fitx = yellow_fitx.copy()
        else:
            # 중앙선이 유실된 극한 상황에서만 양쪽 실선으로 중앙선을 임시 추정합니다.
            estimates = []
            if rw_fit is not None:
                rw_fitx = np.polyval(rw_fit, ploty)
                estimates.append(rw_fitx - dynamic_lane_width)
            if lw_fit is not None:
                lw_fitx = np.polyval(lw_fit, ploty)
                estimates.append(lw_fitx + dynamic_lane_width)
            if len(estimates) > 0:
                target_fitx = np.mean(estimates, axis=0)
        
        if target_fitx is not None:
            # --- LiDAR 기반 지능형 장애물 양방향 추월 로직 ---
            left_obs_dist = float('inf')
            right_obs_dist = float('inf')
            
            if lidar_ranges is not None and len(lidar_ranges) >= 360:
                for idx in range(len(lidar_ranges)):
                    d = lidar_ranges[idx]
                    if math.isfinite(d) and d > 0.1:
                        y = d * math.cos(math.radians(idx))
                        x = d * math.sin(math.radians(idx))
                        
                        # 전방 4.5m 이내, 차체 기준 좌우측 1.0m 영역 스캔
                        if 0.1 < y < 4.5 and abs(x) < 1.0:
                            if x > 0.0:  # 좌측(1차선)에 장애물
                                left_obs_dist = min(left_obs_dist, y)
                            else:        # 우측(2차선)에 장애물
                                right_obs_dist = min(right_obs_dist, y)
            
            # 상태 전이 (State Machine)
            if left_obs_dist < 4.5 and right_obs_dist >= 4.5:
                self.shift_state = 'RIGHT_OVERTAKE'
                self.shift_timer = 30 # 약 1초(30프레임) 동안 회피 상태 유지
            elif right_obs_dist < 4.5 and left_obs_dist >= 4.5:
                self.shift_state = 'LEFT_OVERTAKE'
                self.shift_timer = 30
            elif left_obs_dist < 4.5 and right_obs_dist < 4.5:
                # 양쪽 모두 장애물이면 더 가까운 장애물의 반대 방향으로 회피
                if left_obs_dist < right_obs_dist:
                    self.shift_state = 'RIGHT_OVERTAKE'
                else:
                    self.shift_state = 'LEFT_OVERTAKE'
                self.shift_timer = 30
            else:
                if self.shift_timer > 0:
                    self.shift_timer -= 1
                else:
                    self.shift_state = 'CENTER'
                    
            # 오프셋 산출: 중앙선에서 차선폭의 55% 만큼 이동하여 빈 차선으로 진입
            if self.shift_state == 'RIGHT_OVERTAKE':
                target_offset = dynamic_lane_width * 0.55  # 우측(2차선)으로 양수(+) 이동
            elif self.shift_state == 'LEFT_OVERTAKE':
                target_offset = -dynamic_lane_width * 0.55 # 좌측(1차선)으로 음수(-) 이동
            else:
                target_offset = 0.0 # 정중앙선 복귀
                
            # 부드러운 차선 변경을 위한 Low Pass Filter (LPF)
            self.lane_shift_offset = self.lane_shift_offset * 0.92 + target_offset * 0.08
            target_fitx = target_fitx + self.lane_shift_offset
            
            # --- 2. 외곽 실선 임계점(Boundary) 방어 로직 ---
            # 평소에는 목표 경로에 아무런 간섭도 하지 않다가, 
            # 타겟 경로가 외곽 실선을 밟으려 할 때만 강제로 안쪽으로 밀어넣습니다.
            car_margin = 120 # 차체 폭 절반 수준의 안전 마진 (픽셀)
            
            if rw_fit is not None:
                rw_fitx = np.polyval(rw_fit, ploty)
                rw_pts = np.array([np.transpose(np.vstack([rw_fitx, ploty]))], np.int32)
                cv2.polylines(out_img, [rw_pts], isClosed=False, color=(0, 255, 0), thickness=2)
                # 타겟 경로가 우측 흰선을 120px 이내로 침범하려 하면 안쪽으로 강제 푸쉬 (Minimum 캡)
                target_fitx = np.minimum(target_fitx, rw_fitx - car_margin)
                
            if lw_fit is not None:
                lw_fitx = np.polyval(lw_fit, ploty)
                lw_pts = np.array([np.transpose(np.vstack([lw_fitx, ploty]))], np.int32)
                cv2.polylines(out_img, [lw_pts], isClosed=False, color=(255, 255, 0), thickness=2)
                # 타겟 경로가 좌측 흰선을 120px 이내로 침범하려 하면 안쪽으로 강제 푸쉬 (Maximum 캡)
                target_fitx = np.maximum(target_fitx, lw_fitx + car_margin)
        
        if target_fitx is not None:
            target_pts = np.array([np.transpose(np.vstack([target_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [target_pts], isClosed=False, color=(0, 0, 255), thickness=3)
            
        # 텍스트 오버레이
        n_lanes = sum(1 for f in [yellow_fit, rw_fit, lw_fit] if f is not None)
        cv2.putText(out_img, f"Kappa: {self.prev_kappa:.5f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(out_img, f"Speed: {current_speed:.2f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(out_img, f"FOV Exp: {expansion:.1f} px", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(out_img, f"Lanes: {n_lanes}/3", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        self.debug_img = out_img
        
        # 5. Cross Track Error 계산 및 조향 제어
        # --- 동적 전방 주시거리 (Dynamic Lookahead) 복구 ---
        # "뒤늦게 움직이는" 현상은 주시 거리가 너무 짧기 때문입니다.
        # 속도가 빠를수록 차선 위쪽(더 멀리)을 바라보아 코너 진입 시 미리 감아 나가도록 합니다.
        base_lookahead = self.lookahead_dist
        speed_factor = max(0.0, current_speed - 10.0) * 12.0
        dynamic_lookahead = int(min(280, base_lookahead + speed_factor))
        y_eval = max(0, min(height - 1, height - 1 - dynamic_lookahead))
        
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
        
        # --- 조향 튜닝 (Understeering 해결) ---
        # "차선을 하나도 못 따라가는" 현상은 조향력이 부족하기 때문입니다.
        # 비례 제어(P게인)를 1.3배 늘려 추종력을 확실히 높이고, 
        # 억누르는 힘(D게인)은 다시 정상 수준으로 되돌립니다.
        dynamic_kp = self.kp * 1.3
        dynamic_kd = self.kd * 1.0
        
        raw_angle = (dynamic_kp * error) + (dynamic_kd * derivative)
        
        # --- 심한 곡률에서 조향 증폭 ---
        # "곡률이 심할 때에는 더 많이 조향을 하도록" 요청 반영
        # 곡률(kappa) 값에 비례하여 최대 1.5배까지 전체 조향각을 뻥튀기합니다.
        kappa_multiplier = 1.0 + min(0.5, self.prev_kappa * 50.0)
        raw_angle *= kappa_multiplier
        
        # --- 전방 근접 차량 미세 회피 보완 (Micro-Evasion) ---
        # 원거리 차선 변경(Overtake)과 별개로, 1.5m 이내로 아주 가깝게 접근해오는 차량이 있으면
        # 닿지 않도록 스티어링 휠을 아주 살짝(약 8도) 직접적으로 쳐서 밀어냅니다.
        evasion_steer = 0.0
        if lidar_ranges is not None and len(lidar_ranges) >= 360:
            for idx in range(len(lidar_ranges)):
                d = lidar_ranges[idx]
                if math.isfinite(d) and 0.1 < d < 1.5: # 1.5m 이내 초근접 시
                    y = d * math.cos(math.radians(idx))
                    x = d * math.sin(math.radians(idx))
                    if 0.1 < y < 1.5 and abs(x) < 0.8: # 차체 좌우 폭 주변
                        if x > 0.0:  # 왼쪽 전방에서 접근 -> 오른쪽(+)으로 정말 약간 조향
                            evasion_steer = max(evasion_steer, 8.0) 
                        else:        # 오른쪽 전방에서 접근 -> 왼쪽(-)으로 정말 약간 조향
                            evasion_steer = min(evasion_steer, -8.0)
                            
        raw_angle += evasion_steer
        
        # --- 비대칭 조향 (우회전 강화) 조건부 적용 ---
        if raw_angle > 0 and abs(error) > 40.0:
            raw_angle *= 1.4
            
        self.prev_error = error
        
        # 제어 지연(Lag) 최소화: 즉각적으로 핸들이 반응하도록 유지
        angle = self.prev_angle * 0.3 + raw_angle * 0.7
        angle = max(-100.0, min(100.0, angle))
        self.prev_angle = angle
        
        return float(angle), float(current_speed)

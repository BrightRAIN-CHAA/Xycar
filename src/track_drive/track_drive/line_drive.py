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
        
        # === 3. 좌측 흰색 차선 베이스 탐색 (노란선 왼쪽 전체 영역) ===
        if yellowx_base is not None:
            lw_search_end = max(0, int(yellowx_base) - 20)  # 노란선과 최소 20px 간격
            if lw_search_end > 0 and np.max(hist_white[:lw_search_end]) > 0:
                left_whitex_base = np.argmax(hist_white[:lw_search_end])
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
        
        # 4. 슬라이딩 윈도우 및 다항식 피팅 (3차선 검출)
        yellow_fit, rw_fit, lw_fit, min_y_y, min_y_rw, min_y_lw = self.sliding_window(yellow_warped, white_warped, dynamic_lane_width)
        
        # --- Look-ahead 전방 주시 곡률 예측 ---
        lookahead_y_y = max(height * 0.2, min_y_y)
        lookahead_y_rw = max(height * 0.2, min_y_rw)
        lookahead_y_lw = max(height * 0.2, min_y_lw)
        
        kappa_y = self.compute_curvature(yellow_fit, lookahead_y_y)
        kappa_rw = self.compute_curvature(rw_fit, lookahead_y_rw)
        kappa_lw = self.compute_curvature(lw_fit, lookahead_y_lw)
        
        kappa_list = [k for k in [kappa_y, kappa_rw, kappa_lw] if k > 0]
        target_kappa = max(kappa_list) if kappa_list else 0.0
            
        self.prev_kappa = self.prev_kappa * 0.7 + target_kappa * 0.3
        
        # --- 물리 기반 목표 속도 제어 (Square Root 모델) ---
        if self.prev_kappa > 1e-6:
            v_curve = math.sqrt(self.a_max / self.prev_kappa)
        else:
            v_curve = self.target_speed
            
        target_v = min(self.target_speed, v_curve)
        current_speed = self.prev_speed * 0.8 + target_v * 0.2
        self.prev_speed = current_speed

        # --- 디버깅용 이미지 생성 (버드아이뷰 + 3차선 + 목표 경로) ---
        binary_warped = cv2.bitwise_or(yellow_warped, white_warped)
        out_img = np.dstack((binary_warped, binary_warped, binary_warped)).astype(np.uint8)
        
        ploty = np.linspace(0, height - 1, height)
        
        # 각 차선별 경로선 그리기 및 주행 경로 추정값 수집
        estimates = []
        
        if yellow_fit is not None:
            yellow_fitx = np.polyval(yellow_fit, ploty)
            yellow_pts = np.array([np.transpose(np.vstack([yellow_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [yellow_pts], isClosed=False, color=(255, 0, 0), thickness=2)  # 파란색: 노란 중앙선
            estimates.append(yellow_fitx + dynamic_lane_width / 2.0)
        
        if rw_fit is not None:
            rw_fitx = np.polyval(rw_fit, ploty)
            rw_pts = np.array([np.transpose(np.vstack([rw_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [rw_pts], isClosed=False, color=(0, 255, 0), thickness=2)  # 초록색: 우측 흰선
            estimates.append(rw_fitx - dynamic_lane_width / 2.0)
        
        if lw_fit is not None:
            lw_fitx = np.polyval(lw_fit, ploty)
            lw_pts = np.array([np.transpose(np.vstack([lw_fitx, ploty]))], np.int32)
            cv2.polylines(out_img, [lw_pts], isClosed=False, color=(255, 255, 0), thickness=2)  # 시안색: 좌측 흰선
            estimates.append(lw_fitx + 1.5 * dynamic_lane_width)
        
        target_fitx = None
        if len(estimates) > 0:
            target_fitx = np.mean(estimates, axis=0)
        
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

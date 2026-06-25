import cv2
import numpy as np
import math

class LineDriver:
    def __init__(self, target_speed=15, kp=0.4, kd=0.2):
        """
        카메라 차선 인식 주행(Phase 2)을 위한 클래스입니다.
        Bird's Eye View 변환 및 Sliding Window를 사용합니다.
        """
        self.target_speed = target_speed
        self.kp = kp
        self.kd = kd
        
        self.prev_error = 0.0
        self.prev_angle = 0.0
        
        # 튜닝이 필요한 부분: 원근 변환(Perspective Transform) 좌표
        # Xycar 시뮬레이터 카메라 해상도: 640x480
        # 도로 위 차선 영역의 사다리꼴 좌표 (상단 좌/우, 하단 좌/우)
        self.src_points = np.float32([
            [150, 320], [490, 320],
            [0, 480], [640, 480]
        ])
        
        # 위 사다리꼴을 펼칠 직사각형 좌표 (Top View)
        self.dst_points = np.float32([
            [0, 0], [640, 0],
            [0, 480], [640, 480]
        ])
        
        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)
        self.Minv = cv2.getPerspectiveTransform(self.dst_points, self.src_points)

    def color_filter(self, img):
        """
        HSV 색공간을 이용하여 노란색 중앙선과 흰색 바깥선을 추출합니다.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 노란색 (Yellow)
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([45, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # 흰색 (White)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # 두 마스크 합치기
        combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
        return combined_mask

    def sliding_window(self, binary_warped):
        """
        버드아이뷰 이미지에서 슬라이딩 윈도우를 통해 차선 픽셀을 찾고 다항식으로 피팅합니다.
        """
        # 이미지 하단부의 히스토그램을 계산하여 왼쪽/오른쪽 차선의 시작 X 좌표를 찾음
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:, :], axis=0)
        
        midpoint = int(histogram.shape[0] // 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint
        
        # 윈도우 설정
        nwindows = 9
        window_height = int(binary_warped.shape[0] // nwindows)
        
        # 이미지 내의 모든 non-zero 픽셀의 위치 추출
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        
        leftx_current = leftx_base
        rightx_current = rightx_base
        
        margin = 60 # 윈도우 너비 절반
        minpix = 40 # 윈도우 내 최소 픽셀 수
        
        left_lane_inds = []
        right_lane_inds = []
        
        # 각 윈도우별로 픽셀 찾기
        for window in range(nwindows):
            win_y_low = binary_warped.shape[0] - (window + 1) * window_height
            win_y_high = binary_warped.shape[0] - window * window_height
            
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            
            # 윈도우 안에 들어오는 픽셀들의 인덱스
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                              (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                               (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
            
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            
            # 픽셀 수가 minpix보다 많으면, 다음 윈도우의 중심을 현재 픽셀들의 평균 X 좌표로 이동
            if len(good_left_inds) > minpix:
                leftx_current = int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = int(np.mean(nonzerox[good_right_inds]))
                
        # 배열 합치기
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
        
        # 차선 픽셀들의 x, y 좌표
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds] 
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]
        
        # 2차 다항식 피팅
        left_fit = np.polyfit(lefty, leftx, 2) if len(leftx) > 0 else None
        right_fit = np.polyfit(righty, rightx, 2) if len(rightx) > 0 else None
        
        return left_fit, right_fit, len(leftx), len(rightx)

    def compute_steering(self, cv_image):
        """
        이미지를 입력받아 차선을 인식하고, 조향각과 속도를 반환합니다.
        """
        if cv_image is None:
            return 0.0, 0.0
            
        height, width = cv_image.shape[:2]
        
        # 1. ROI 적용 (하늘과 본넷 제거)
        roi_img = cv_image.copy()
        
        # 2. 색상 필터링을 통한 차선 이진화
        binary_img = self.color_filter(roi_img)
        
        # 3. 버드아이뷰 변환 (Perspective Transform)
        binary_warped = cv2.warpPerspective(binary_img, self.M, (width, height), flags=cv2.INTER_LINEAR)
        
        # 4. 슬라이딩 윈도우 및 다항식 피팅
        left_fit, right_fit, _, _ = self.sliding_window(binary_warped)
        
        # 5. Cross Track Error 계산 및 조향 제어
        y_eval = height # 차량 바로 앞 (이미지 최하단) 기준
        
        target_x = width / 2.0
        if left_fit is not None and right_fit is not None:
            left_x = left_fit[0]*y_eval**2 + left_fit[1]*y_eval + left_fit[2]
            right_x = right_fit[0]*y_eval**2 + right_fit[1]*y_eval + right_fit[2]
            target_x = (left_x + right_x) / 2.0
        elif left_fit is not None:
            left_x = left_fit[0]*y_eval**2 + left_fit[1]*y_eval + left_fit[2]
            target_x = left_x + 300 # 차선폭에 비례한 오프셋 (튜닝 필요)
        elif right_fit is not None:
            right_x = right_fit[0]*y_eval**2 + right_fit[1]*y_eval + right_fit[2]
            target_x = right_x - 300 # 차선폭에 비례한 오프셋 (튜닝 필요)
            
        # 오차 계산 (이미지 중앙 기준)
        error = target_x - (width / 2.0)
        
        # PD 제어
        derivative = error - self.prev_error
        raw_angle = (self.kp * error) + (self.kd * derivative)
        self.prev_error = error
        
        # 스무딩
        angle = self.prev_angle * 0.7 + raw_angle * 0.3
        
        # 자이카 조향 스케일 조정 (좌측이 음수 조향각일 수 있으므로 부호 조정 필요)
        # 이미지상 target_x가 중앙보다 크면(오른쪽) error > 0 -> 자이카는 우회전(양수)
        # 만약 실제 동작 시 조향이 반대라면 angle = -angle 처리
        
        angle = max(-50.0, min(50.0, angle))
        self.prev_angle = angle
        
        # 속도 감속 로직
        speed = self.target_speed
        if abs(angle) > 20.0:
            speed = self.target_speed * 0.7
            
        return float(angle), float(speed)

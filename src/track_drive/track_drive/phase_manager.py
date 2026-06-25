import cv2
import numpy as np

class PhaseManager:
    def __init__(self):
        """
        주행 상태(Phase) 전환 여부를 판단하는 로직을 모아둔 클래스입니다.
        """
        pass

    def detect_traffic_light(self, cv_image):
        """
        [Phase 2 진입 조건] 
        신호등 색상을 판별하여 'GREEN'이면 출발 신호로 간주합니다.
        """
        if cv_image is None:
            return "UNKNOWN"
            
        # 1. ROI(관심 영역) 강력 축소: 
        # 주변 배경(특히 노란색, 초록색 나무 등)을 피하기 위해 화면의 가로 중앙부, 세로 상단부만 극도로 좁혀서 봅니다.
        h, w = cv_image.shape[:2]
        # 세로: 상단 10% ~ 40%, 가로: 중앙 35% ~ 65% (신호등 위치만 타겟팅)
        roi = cv_image[int(h*0.1):int(h*0.4), int(w*0.35):int(w*0.65)]
        
        # BGR 이미지를 HSV 색공간으로 변환
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 2. 색상 임계값 설정 (빛나는 신호등만 잡기 위해 S와 V를 매우 높게 설정)
        # 빨간색(Red) 영역 감지
        mask_red1 = cv2.inRange(hsv, np.array([0, 180, 180]), np.array([10, 255, 255]))
        mask_red2 = cv2.inRange(hsv, np.array([160, 180, 180]), np.array([180, 255, 255]))
        red_pixels = cv2.countNonZero(mask_red1) + cv2.countNonZero(mask_red2)
        
        # 노란색(Yellow) 영역 감지
        mask_yellow = cv2.inRange(hsv, np.array([15, 180, 180]), np.array([35, 255, 255]))
        yellow_pixels = cv2.countNonZero(mask_yellow)

        # 초록색(Green) 영역 감지
        mask_green = cv2.inRange(hsv, np.array([45, 180, 180]), np.array([90, 255, 255]))
        green_pixels = cv2.countNonZero(mask_green)

        # 3. 신호 판별
        min_pixels = 10  # ROI가 매우 좁아졌으므로 최소 픽셀 기준도 낮춤

        # 가장 픽셀 수가 많은 색상을 현재 신호로 판단
        if green_pixels > min_pixels and green_pixels > red_pixels and green_pixels > yellow_pixels:
            return "GREEN"
        elif red_pixels > min_pixels and red_pixels > yellow_pixels:
            return "RED"
        elif yellow_pixels > min_pixels:
            return "YELLOW"
            
        return "UNKNOWN"

    def detect_asphalt(self, cv_image):
        """
        [Phase 3 진입 조건]
        카메라 이미지를 바탕으로 현재 아스팔트 차선 위에 확실하게 진입했는지 판단합니다.
        바닥의 '검은색 아스팔트' 영역을 인식합니다.
        """
        if cv_image is None:
            return False
            
        # 차량 바로 앞 바닥(ROI)을 잘라냅니다. (예: 세로 350~480, 가로 200~440)
        roi = cv_image[350:480, 200:440]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 검은색/어두운 회색 아스팔트 색상 범위 (채도와 명도가 낮음)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 60, 90]) # 명도 최대치 90 (상황에 따라 튜닝 가능)
        
        mask = cv2.inRange(hsv, lower_black, upper_black)
        
        black_pixels = cv2.countNonZero(mask)
        total_pixels = roi.shape[0] * roi.shape[1]
        
        # 해당 영역의 50% 이상이 검은색이면 아스팔트 진입으로 판단!
        if black_pixels > total_pixels * 0.5:
            return True
            
        return False

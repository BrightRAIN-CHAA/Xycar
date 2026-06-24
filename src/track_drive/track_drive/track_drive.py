#!/usr/bin/env python3
# -*- coding: utf-8 -*- 1
#=============================================
# 본 프로그램은 자이트론에서 제작한 것입니다.
# 상업라이센스에 의해 제공되므로 무단배포 및 상업적 이용을 금합니다.
# 교육과 실습 용도로만 사용가능하며 외부유출은 금지됩니다.
#=============================================
import rclpy, time, cv2, os, math
import numpy as np
from rclpy.node import Node
from xycar_msgs.msg import XycarMotor
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from rclpy.duration import Duration
from cv_bridge import CvBridge

#=============================================
# ROS2 Node 클래스 정의
#=============================================
class TrackDriverNode(Node):

    #=============================================
    # 클래스 생성 초기화 함수
    #=============================================
    def __init__(self):

        super().__init__('driver')
        self.get_logger().info('----- Xycar self-driving node started -----')
        
        # 상수값 및 초기값 설정
        self.image = None  # 카메라 토픽 데이터를 저장할 변수
        self.motor_msg = XycarMotor()  # 모터토픽 메시지        
        self.lidar_ranges = None
        self.bridge = CvBridge()
        
        # ROS2 Publisher & Subscriber 설정
        self.motor_pub = self.create_publisher(XycarMotor,'xycar_motor',10)
        
        self.sub_front = self.create_subscription(
            Image, '/usb_cam/image_raw/front', self.cam_callback, qos_profile_sensor_data)
        
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, qos_profile_sensor_data)
		
        self.get_logger().info("Track Driver Node Initialized")
              
    #=============================================
    # 카메라 토픽을 수신하는 콜백 함수
    #=============================================
    def cam_callback(self, data):
        # 수신한 메시지를 OpenCV 이미지로 변환하여 저장
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    
    #=============================================
    # 라이다 토픽을 수신하는 콜백 함수
    #=============================================
    def lidar_callback(self, msg):
        self.lidar_ranges = msg.ranges   
      
    #=============================================
    # 모터제어 토픽을 발행하는 Publisher 함수
    #=============================================
    def drive(self, angle, speed):
        self.motor_msg.angle = float(angle)
        self.motor_msg.speed = float(speed)
        self.motor_pub.publish(self.motor_msg)
    
    #=============================================
    # 신호등 상태 감지 함수 (빨강/노랑/초록 비교)
    #=============================================
    def detect_traffic_light(self):
        if self.image is None:
            return "UNKNOWN"
            
        # 1. ROI(관심 영역) 강력 축소: 
        # 주변 배경(특히 노란색, 초록색 나무 등)을 피하기 위해 화면의 가로 중앙부, 세로 상단부만 극도로 좁혀서 봅니다.
        h, w = self.image.shape[:2]
        # 세로: 상단 10% ~ 40%, 가로: 중앙 35% ~ 65% (신호등 위치만 타겟팅)
        roi = self.image[int(h*0.1):int(h*0.4), int(w*0.35):int(w*0.65)]
        
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
    
    #=============================================
    # 메인 루프
    #=============================================
    def main_loop(self):
    
        self.get_logger().info("======================================")
        self.get_logger().info("  신호등 감지 대기 중 ...             ")
        self.get_logger().info("======================================")

        is_started = False
        wait_log_count = 0

        while rclpy.ok():
            # ROS2 콜백 처리를 위해 spin_once 호출 필수
            rclpy.spin_once(self, timeout_sec=0.05)
            
            if self.image is None:
                continue
                
            if not is_started:
                # 정지 상태 유지
                self.drive(angle=0, speed=0)
                
                # 신호등 상태 확인
                signal = self.detect_traffic_light()
                
                if signal == "GREEN":
                    self.get_logger().info("★ 초록불 감지! 직진으로 출발합니다!")
                    is_started = True
                else:
                    # 로그가 너무 빨리 올라가는 것을 방지 (약 0.5초마다 한 번씩만 출력)
                    wait_log_count += 1
                    if wait_log_count % 10 == 0:
                        self.get_logger().info(f"신호 대기 중... 현재 감지된 신호: {signal}")
            else:
                # 초록불이 켜진 이후로는 계속 직진
                self.drive(angle=0, speed=15)
                
#=============================================
# 메인 함수
#=============================================
def main(args=None):
      
    rclpy.init(args=args)
    node = TrackDriverNode()
	
    try:
        # main_loop() 함수를 호출하여 실행합니다.
        node.main_loop()
    except KeyboardInterrupt:
        # 사용자 인터럽트 (Ctrl+C)가 발생하면 예외를 처리합니다.
        pass
    finally:
        # 노드를 종료하고 ROS2를 정리합니다.
        node.drive(angle=0, speed=0)
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

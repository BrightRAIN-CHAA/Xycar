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
from track_drive.lidar_drive import ConeDriver
from track_drive.line_drive import LineDriver
from track_drive.phase_manager import PhaseManager

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
        self.cone_driver = ConeDriver()
        self.line_driver = LineDriver()
        self.phase_manager = PhaseManager()
        self.phase = 1  # 1: 신호등 대기, 2: 라바콘 주행, 3: 아스팔트 차선 주행
        
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
    # 메인 루프
    #=============================================
    def main_loop(self):
    
        self.get_logger().info("======================================")
        self.get_logger().info("  [Phase 1] 신호등 감지 대기 중 ...             ")
        self.get_logger().info("======================================")

        wait_log_count = 0

        while rclpy.ok():
            # ROS2 콜백 처리를 위해 spin_once 호출 필수
            rclpy.spin_once(self, timeout_sec=0.05)
            
            if self.phase == 1:
                if self.image is None:
                    continue
                    
                # 정지 상태 유지
                self.drive(angle=0, speed=0)
                
                # 신호등 상태 확인
                signal = self.phase_manager.detect_traffic_light(self.image)
                
                if signal == "GREEN":
                    self.get_logger().info("★ 초록불 감지! [Phase 2] 라바콘 회피 주행을 시작합니다!")
                    self.phase = 2
                else:
                    # 로그가 너무 빨리 올라가는 것을 방지 (약 0.5초마다 한 번씩만 출력)
                    wait_log_count += 1
                    if wait_log_count % 10 == 0:
                        self.get_logger().info(f"신호 대기 중... 현재 감지된 신호: {signal}")
                        
            elif self.phase == 2:
                # 초기 타이머(프레임 카운터) 초기화
                if not hasattr(self, 'phase2_frame_count'):
                    self.phase2_frame_count = 0
                self.phase2_frame_count += 1
                
                # 라바콘 회피 주행 모드
                angle, speed = self.cone_driver.compute_steering(self.lidar_ranges)
                self.drive(angle, speed)
                
                # 출발 직후 바닥의 마크를 아스팔트로 오인하는 것을 방지하기 위해, 약 3초(60프레임) 이후부터 체크!
                is_on_asphalt = False
                if self.phase2_frame_count > 60:
                    is_on_asphalt = self.phase_manager.detect_asphalt(self.image)
                
                if is_on_asphalt:
                    self.get_logger().info("★ 아스팔트 차선 진입 확인! [Phase 3] 아스팔트 차선 주행 모드로 전환합니다!")
                    self.phase = 3
                    
            elif self.phase == 3:
                # 아스팔트 차선 주행 모드 (카메라 기반 + 라이다 장애물 회피 퓨전)
                if self.image is None:
                    continue
                angle, speed = self.line_driver.compute_steering(self.image, self.lidar_ranges)
                self.drive(angle, speed)
                
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

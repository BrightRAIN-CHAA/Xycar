#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
import cv2
import time
from rclpy.node import Node
from sensor_msgs.msg import Image
from xycar_msgs.msg import XycarMotor
from cv_bridge import CvBridge
from rclpy.qos import qos_profile_sensor_data
# 기존에 만들어진 신호등 인식기 재사용
from track_drive.traffic_light_detector import TrafficLightDetector, SIGNAL_GREEN, SIGNAL_RED, SIGNAL_YELLOW, SIGNAL_UNKNOWN
class StartOnGreenNode(Node):
    """
    처음 정지 상태에서 빨강, 노랑, 초록 신호를 확인하고,
    초록불이 켜지면 직진으로 출발하는 단순한 예제 노드입니다.
    """
    def __init__(self):
        super().__init__('start_on_green_node')
        self.get_logger().info('--- 신호등 인식 출발 노드 시작 ---')
        self.get_logger().info('카메라 데이터 수신을 기다립니다...')
        self.bridge = CvBridge()
        self.image = None
        
        # 신호등 감지 인스턴스 생성
        self.traffic_detector = TrafficLightDetector()
        
        # 상태 변수 (출발 여부)
        self.is_started = False
        
        # ROS2 Publisher: 모터 제어 토픽
        self.motor_pub = self.create_publisher(XycarMotor, 'xycar_motor', 10)
        
        # ROS2 Subscriber: 전방 카메라 토픽
        self.image_sub = self.create_subscription(
            Image, '/usb_cam/image_raw/front',
            self.cam_callback, qos_profile_sensor_data)
            
        # 메인 루프 타이머 (약 50Hz: 0.02초 주기)
        self.timer = self.create_timer(0.02, self.timer_callback)
    def cam_callback(self, data):
        """ROS Image 메시지를 OpenCV BGR 이미지로 변환"""
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    def timer_callback(self):
        """주기적으로 카메라 이미지를 확인해 신호등에 따른 모터 제어"""
        if self.image is None:
            return
            
        # 이미 출발한 상태라면 계속 직진(속도 15, 조향 0)
        if self.is_started:
            self.drive(angle=0.0, speed=15.0)
            return
        # 신호등 감지 수행
        signal, debug_img = self.traffic_detector.detect(self.image)
        
        if signal == SIGNAL_GREEN:
            self.get_logger().info('★ 초록불 감지! 직진으로 출발합니다!')
            self.is_started = True
            self.drive(angle=0.0, speed=15.0)
        else:
            # 빨강불이나 노랑불 등일 때 대기
            if signal != SIGNAL_UNKNOWN:
                self.get_logger().info(f'신호 대기 중... 현재 확인된 신호: {signal}')
            # 정지 상태 유지
            self.drive(angle=0.0, speed=0.0)
            
        # (선택) 디버그 창으로 현재 인식 상태를 확인
        if debug_img is not None:
            cv2.imshow("Traffic Light Detection", debug_img)
            cv2.waitKey(1)
    def drive(self, angle, speed):
        """모터 토픽 발행 함수"""
        msg = XycarMotor()
        msg.angle = float(angle)
        msg.speed = float(speed)
        self.motor_pub.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = StartOnGreenNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('사용자 요청으로 노드를 종료합니다.')
    finally:
        # 종료 시 차량 안전하게 정지
        node.drive(0.0, 0.0)
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()

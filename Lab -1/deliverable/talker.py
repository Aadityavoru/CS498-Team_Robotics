#!/usr/bin/env python3
"""talker.py - Publishes AckermannDriveStamped messages with speed v and steering angle d."""
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped


class Talker(Node):
    """Publishes drive commands from ROS parameters v and d."""
    
    def __init__(self):
        super().__init__('talker')
        self.declare_parameter('v', 0.0)
        self.declare_parameter('d', 0.0)
        self.publisher_ = self.create_publisher(AckermannDriveStamped, 'drive', 10)
        self.timer = self.create_timer(0.001, self.timer_callback)

    def timer_callback(self):
        v = self.get_parameter('v').get_parameter_value().double_value
        d = self.get_parameter('d').get_parameter_value().double_value
        msg = AckermannDriveStamped()
        msg.drive.speed = v
        msg.drive.steering_angle = d
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Talker())
    rclpy.shutdown()


if __name__ == '__main__':
    main()

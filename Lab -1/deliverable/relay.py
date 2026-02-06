#!/usr/bin/env python3
"""relay.py - Subscribes to drive, multiplies speed and steering by 3, publishes to drive_relay."""
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped


class Relay(Node):
    """Relays drive commands with values multiplied by 3."""
    
    def __init__(self):
        super().__init__('relay')
        self.subscription = self.create_subscription(AckermannDriveStamped, 'drive', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(AckermannDriveStamped, 'drive_relay', 10)

    def listener_callback(self, msg):
        new_msg = AckermannDriveStamped()
        new_msg.drive.speed = msg.drive.speed * 3.0
        new_msg.drive.steering_angle = msg.drive.steering_angle * 3.0
        self.publisher_.publish(new_msg)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Relay())
    rclpy.shutdown()


if __name__ == '__main__':
    main()

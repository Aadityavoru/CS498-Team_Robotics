#!/usr/bin/env python3
"""
Lab 2: Automatic Emergency Braking (AEB) Safety Node
Implements iTTC-based collision detection to automatically brake the vehicle.
"""
import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped


class SafetyNode(Node):
    """Handles emergency braking using Instantaneous Time to Collision (iTTC)."""
    
    TTC_THRESHOLD = 0.5  # Seconds before collision to trigger brake
    
    def __init__(self):
        super().__init__('safety_node')
        self.speed = 0.0
        
        self.drive_publisher = self.create_publisher(AckermannDriveStamped, '/drive', 10)
        self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        self.get_logger().info(f'Safety Node initialized (TTC threshold: {self.TTC_THRESHOLD}s)')

    def odom_callback(self, odom_msg):
        """Update current vehicle speed from odometry."""
        self.speed = odom_msg.twist.twist.linear.x

    def scan_callback(self, scan_msg):
        """Calculate iTTC and brake if collision is imminent."""
        ranges = np.array(scan_msg.ranges)
        angles = np.arange(scan_msg.angle_min, scan_msg.angle_max + scan_msg.angle_increment, scan_msg.angle_increment)
        
        if len(angles) > len(ranges):
            angles = angles[:len(ranges)]
        elif len(angles) < len(ranges):
            ranges = ranges[:len(angles)]
        
        # iTTC = r / max(-v*cos(theta), 0)
        range_rate = self.speed * np.cos(angles)
        denominator = np.maximum(-range_rate, 0.0)
        
        valid_ranges = np.where(np.isfinite(ranges) & (ranges > 0.0), ranges, np.inf)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            ittc = np.where(denominator > 1e-6, valid_ranges / denominator, np.inf)
        
        if np.nanmin(ittc) < self.TTC_THRESHOLD:
            self.emergency_brake()
            self.get_logger().warn(f'EMERGENCY BRAKE! Min iTTC: {np.nanmin(ittc):.3f}s')

    def emergency_brake(self):
        """Publish brake command (speed = 0)."""
        brake_msg = AckermannDriveStamped()
        brake_msg.header.stamp = self.get_clock().now().to_msg()
        brake_msg.drive.speed = 0.0
        self.drive_publisher.publish(brake_msg)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(SafetyNode())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import numpy as np
# TODO: include needed ROS msg type headers and libraries
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from std_msgs.msg import Bool

class SafetyNode(Node):
    """
    The class that handles simulation safety calculations
    """
    def __init__(self):
        super().__init__('safety_node')
        """
        One publisher should publish to the /drive topic with a Twist message
        You can also publish the boolean value of whether the car is currently in 
        collision behavior to the /brake_bool topic
        """
        # Declare parameters
        self.declare_parameter('ttc_threshold', 0.7)
        self.ttc_threshold = self.get_parameter('ttc_threshold').get_parameter_value().double_value

        # Publishers
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)
        self.brake_bool_pub = self.create_publisher(Bool, '/brake_bool', 10)

        # Subscribers
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 10)

        # State
        self.speed = 0.0

    def odom_callback(self, odom_msg):
        # Update current speed
        self.speed = odom_msg.twist.twist.linear.x

    def scan_callback(self, scan_msg):
        """
        1. Calculate the instantaneous time to collision (iTTC) for each beam
        2. If any iTTC is less than the threshold, brake
        """
        
        # 1. Parse LaserScan Data
        ranges = np.array(scan_msg.ranges)
        
        # Calculate angles for each range measurement
        # angle = angle_min + i * angle_increment
        angle_min = scan_msg.angle_min
        angle_increment = scan_msg.angle_increment
        angles = angle_min + np.arange(len(ranges)) * angle_increment
        
        # 2. Calculate Range Rate (r_dot)
        # r_dot = v * cos(theta)
        # We project the vehicle's forward velocity onto the beam direction.
        # A positive velocity towards an obstacle means the range is decreasing.
        # But wait, r_dot is rate of change of range.
        # If moving forward (v > 0) towards obstacle in front (theta ~ 0), r is decreasing, so r_dot should be negative.
        # v_proj = v * cos(theta)
        # If v > 0 and theta=0 (front), v_proj = v.
        # Rate of change of range r is -v_proj.
        # r_dot = -v * cos(theta)
        
        # However, the formula in instructions says: r_dot = - v * cos(theta) for closing rate?
        # Actually instructions say "calculate range rate ... by using v_x * cos(theta)". 
        # And "For a vehicle travelling forward ... range measurement should be shrinking... corresponding range rate ... should be negative".
        # So r_dot = - speed * cos(angles) is correct if speed is positive forward.
        
        r_dot = -self.speed * np.cos(angles)
        
        # 3. Calculate iTTC
        # iTTC = r / {-r_dot}_+ = r / max(-r_dot, 0)
        # Here -r_dot is the closing speed. If closing speed <= 0, we are not colliding (opening or static), so iTTC -> inf.
        
        closing_speed = -r_dot # This is max(-r_dot, 0) effectively if we filter
        
        # Avoid division by zero and only consider positive closing speeds (collision course)
        # We only care when closing_speed > 0
        
        # Initialize TTC with infinity
        ttc = np.full_like(ranges, np.inf)
        
        # Mask for valid ranges and positive closing speed
        valid_mask = (ranges > 0) & (closing_speed > 0)
        
        # Calculate TTC only for valid beams
        ttc[valid_mask] = ranges[valid_mask] / closing_speed[valid_mask]
        
        # 4. Check for collision imminent
        # Filter out NaN/Inf just in case, though logic above handles it
        min_ttc = np.min(ttc)
        
        if min_ttc < self.ttc_threshold:
            self.get_logger().warn(f'Collision Imminent! Min TTC: {min_ttc:.2f}s. BRAKING!')
            self.publish_brake()
        else:
            # Optional: publish safe status or just do nothing
            # Publishing false to brake_bool for visualization
            brake_msg = Bool()
            brake_msg.data = False
            self.brake_bool_pub.publish(brake_msg)

    def publish_brake(self):
        # Publish 0 speed to /drive
        drive_msg = AckermannDriveStamped()
        drive_msg.drive.speed = 0.0
        self.drive_pub.publish(drive_msg)
        
        # Publish brake bool
        brake_bool_msg = Bool()
        brake_bool_msg.data = True
        self.brake_bool_pub.publish(brake_bool_msg)

def main(args=None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    rclpy.spin(safety_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    safety_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

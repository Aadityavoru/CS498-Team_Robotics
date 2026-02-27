import rclpy
from rclpy.node import Node

import numpy as np
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped
import math

class WallFollow(Node):
    """ 
    Implement Wall Following on the car
    """
    def __init__(self):
        super().__init__('wall_follow_node')

        lidarscan_topic = '/scan'
        drive_topic = '/drive'

        # TODO: create subscribers and publishers
        self.subscription = self.create_subscription(
            LaserScan,
            lidarscan_topic,
            self.scan_callback,
            10
        )
        self.publisher_ = self.create_publisher(AckermannDriveStamped, drive_topic, 10)

        # TODO: set PID gains
        self.kp = 1.0 # Tune this
        self.kd = 0.05 # Tune this
        self.ki = 0.001 # Tune this

        # TODO: store history
        self.integral = 0.0
        self.prev_error = 0.0
        
        self.get_logger().info("WallFollow node started!")

        # Desired distance to the wall
        self.desired_dist = 1.0 # Assume 1.0 meters for now, can be tuned
        self.lookahead_dist = 0.5 # Lookahead distance in meters

    def get_range(self, range_data, angle):
        """
        Simple helper to return the corresponding range measurement at a given angle. Make sure you take care of NaNs and infs.

        Args:
            range_data: single range array from the LiDAR
            angle: between angle_min and angle_max of the LiDAR

        Returns:
            range: range measurement in meters at the given angle

        """

        #TODO: implement
        
        # Calculate the index corresponding to the given angle
        # Ensure angle is within bounds
        if angle < range_data.angle_min or angle > range_data.angle_max:
            return 0.0 # Or some large default value, or handle differently based on context
            
        index = int((angle - range_data.angle_min) / range_data.angle_increment)
        
        # Check bounds just in case
        if index < 0 or index >= len(range_data.ranges):
            return 0.0
            
        range_val = range_data.ranges[index]
        
        # Handle NaNs and infs
        if math.isnan(range_val) or math.isinf(range_val):
            # Return a large value or the max range to prevent issues
            return float(range_data.range_max)
            
        return range_val

    def get_error(self, range_data, dist):
        """
        Calculates the error to the wall. Follow the wall to the left (going counter clockwise in the Levine loop). You potentially will need to use get_range()

        Args:
            range_data: single range array from the LiDAR
            dist: desired distance to the wall

        Returns:
            error: calculated error
        """

        #TODO:implement
        # We want to follow the left wall, so we look to the left.
        # Let's say beam b is exactly 90 degrees left (pi/2)
        # and beam a is 45 degrees left (pi/4) - so theta = pi/4
        
        angle_b = math.pi / 2.0
        angle_a = math.pi / 4.0
        theta = angle_b - angle_a
        
        b = self.get_range(range_data, angle_b)
        a = self.get_range(range_data, angle_a)
        
        # Calculate alpha
        alpha = math.atan((a * math.cos(theta) - b) / (a * math.sin(theta)))
        
        # Current distance to wall
        D_t = b * math.cos(alpha)
        
        # Estimated future distance to wall
        D_t_plus_1 = D_t + self.lookahead_dist * math.sin(alpha)
        
        # Error is the difference between desired distance and estimated future distance
        # We want D_t_plus_1 to equal dist
        error = dist - D_t_plus_1
        
        return error

    def pid_control(self, error, velocity):
        """
        Based on the calculated error, publish vehicle control

        Args:
            error: calculated error
            velocity: desired velocity

        Returns:
            None
        """
        angle = 0.0
        # TODO: Use kp, ki & kd to implement a PID controller
        
        p = self.kp * error
        self.integral += error
        i = self.ki * self.integral
        d = self.kd * (error - self.prev_error)
        
        angle = p + i + d
        self.prev_error = error
        
        drive_msg = AckermannDriveStamped()
        # TODO: fill in drive message and publish
        # Drive message needs a header? Or just drive properties
        drive_msg.drive.steering_angle = angle
        drive_msg.drive.speed = float(velocity)
        
        self.publisher_.publish(drive_msg)

    def scan_callback(self, msg):
        """
        Callback function for LaserScan messages. Calculate the error and publish the drive message in this function.

        Args:
            msg: Incoming LaserScan message

        Returns:
            None
        """
        error = self.get_error(msg, self.desired_dist) # TODO: replace with error calculated by get_error()
        
        # Calculate speed based on steering angle as requested by the lab writeup
        # 0 to 10 deg -> 1.5 m/s
        # 10 to 20 deg -> 1.0 m/s
        # > 20 deg -> 0.5 m/s
        
        # Need to use the predicted steering angle, but here we calculate error first, then pass to PID control...
        # Wait, the PID control block accepts velocity. So we need to estimate the steering angle?
        # Let's approximate the steering angle with the P term for speed selection, or just use error for speed control.
        # Actually, the spec says "If the steering angle is between 0 degrees and 10 degrees..."
        # So we can calculate the PID angle first, determine velocity, then publish. Let's refactor this slightly.
        # What we can do is: error -> PID -> angle -> velocity -> publish. 
        # Since pid_control takes velocity, maybe we calculate velocity based on the P-term roughly?
        # Or better, let pid_control determine velocity itself. But the skeleton requires `velocity = ...` here.
        
        # Let's roughly estimate angle from P term:
        est_angle_rad = self.kp * error
        abs_est_angle_deg = math.fabs(math.degrees(est_angle_rad))
        
        if abs_est_angle_deg < 10.0:
            velocity = 1.5
        elif abs_est_angle_deg < 20.0:
            velocity = 1.0
        else:
            velocity = 0.5
             
        self.pid_control(error, velocity) # TODO: actuate the car with PID


def main(args=None):
    rclpy.init(args=args)
    print("WallFollow Initialized")
    wall_follow_node = WallFollow()
    rclpy.spin(wall_follow_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    wall_follow_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
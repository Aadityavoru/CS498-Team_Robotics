#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math

class BallPublisher(Node):
    def __init__(self):
        super().__init__('ball_simulator')
        
        # Publisher for ball pose
        self.publisher = self.create_publisher(PoseStamped, 'ball_pose', 10)
        
        # Timer to publish at 10 Hz
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # Ball position - starts at origin, moves at 1 m/s
        self.time = 0.0
        self.velocity = 1.0  # m/s
        
        self.get_logger().info('Ball simulator started - moving at 1 m/s')
    
    def timer_callback(self):
        msg = PoseStamped()
        
        # Header
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        
        # Position - ball moves in a straight line along x-axis at 1 m/s
        # Converting to cm (multiply by 100) to match the frame coordinates
        msg.pose.position.x = self.velocity * self.time
        msg.pose.position.y = 0.0
        msg.pose.position.z = 0.0
        
        # Orientation - identity quaternion (no rotation)
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0
        
        # Publish
        self.publisher.publish(msg)
        
        # Increment time
        self.time += 0.1
        
        # Reset after 10 seconds to prevent going too far
        if self.time > 10.0:
            self.time = 0.0
            self.get_logger().info('Resetting ball position')

def main(args=None):
    rclpy.init(args=args)
    node = BallPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
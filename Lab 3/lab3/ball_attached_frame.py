#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_ros import TransformBroadcaster
import math


class BallAttachedFramePublisher(Node):
    def __init__(self):
        super().__init__('ball_attached_frame_publisher')
        
        # Create a transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscribe to the ball's pose topic
        self.subscription = self.create_subscription(
            PoseStamped,
            'ball_pose',
            self.ball_pose_callback,
            10
        )
        
        self.get_logger().info('Ball attached frame broadcaster started')
    
    def ball_pose_callback(self, msg):
        """
        Callback function that receives the ball's pose and broadcasts
        a frame attached to the ball with an arbitrary offset
        """
        # Create a TransformStamped message
        t = TransformStamped()

        # Set the timestamp from the incoming pose message
        t.header.stamp = msg.header.stamp

        # Parent frame: the world frame (same as ball_pose header)
        t.header.frame_id = 'world'

        # Child frame: the ball's attached frame
        t.child_frame_id = 'ball'

        # Set translation: use the ball's pose + an arbitrary 0.5 m z-offset
        t.transform.translation.x = msg.pose.position.x
        t.transform.translation.y = msg.pose.position.y
        t.transform.translation.z = msg.pose.position.z + 0.5  # arbitrary offset

        # Set rotation: use the ball's orientation (identity = no rotation)
        t.transform.rotation.x = msg.pose.orientation.x
        t.transform.rotation.y = msg.pose.orientation.y
        t.transform.rotation.z = msg.pose.orientation.z
        t.transform.rotation.w = msg.pose.orientation.w

        # Broadcast the transform
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = BallAttachedFramePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

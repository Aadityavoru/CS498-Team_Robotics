#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import math


class FrameListenerNode(Node):
    def __init__(self):
        super().__init__('frame_listener')
        
        # Create a TF2 buffer
        self.tf_buffer = Buffer()

        # Create a TF2 listener (binds to the buffer)
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Create a timer to periodically lookup transforms (1 Hz)
        self.timer = self.create_timer(1.0, self.on_timer)
        
        self.get_logger().info('Frame listener node started')
    
    def on_timer(self):
        """
        Timer callback that looks up the transform from camera to base
        and prints the ball's position relative to the robot base
        """
        # Source frame: the ball; target frame: the robot base
        target_frame = 'base'
        source_frame = 'ball'

        try:
            # Look up the transform from source_frame to target_frame
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                rclpy.time.Time()
            )

            # Extract position information
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z

            # Print the ball's position relative to the base
            self.get_logger().info(
                f'Ball position relative to base: x={x:.3f}, y={y:.3f}, z={z:.3f}'
            )
            
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(
                f'Could not transform {source_frame} to {target_frame}: {str(e)}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = FrameListenerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

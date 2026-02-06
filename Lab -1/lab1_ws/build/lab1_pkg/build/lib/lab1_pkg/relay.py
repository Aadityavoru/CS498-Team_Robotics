import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped

class Relay(Node):
    def __init__(self):
        super().__init__('relay')
        
        # Subscribe to 'drive' topic
        self.subscription = self.create_subscription(
            AckermannDriveStamped,
            'drive',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Create publisher for 'drive_relay' topic
        self.publisher_ = self.create_publisher(AckermannDriveStamped, 'drive_relay', 10)

    def listener_callback(self, msg):
        # Multiply speed and steering angle by 3
        new_speed = msg.drive.speed * 3.0
        new_steering_angle = msg.drive.steering_angle * 3.0

        new_msg = AckermannDriveStamped()
        new_msg.drive.speed = new_speed
        new_msg.drive.steering_angle = new_steering_angle

        # Publish the new message
        self.publisher_.publish(new_msg)
        # self.get_logger().info(f'Relaying: speed={new_speed}, steering_angle={new_steering_angle}')

def main(args=None):
    rclpy.init(args=args)
    relay = Relay()
    rclpy.spin(relay)
    relay.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

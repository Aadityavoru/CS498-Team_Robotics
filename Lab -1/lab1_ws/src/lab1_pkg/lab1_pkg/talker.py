import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        # Declare parameters with default values
        self.declare_parameter('v', 0.0)
        self.declare_parameter('d', 0.0)

        # Create publisher for 'drive' topic
        self.publisher_ = self.create_publisher(AckermannDriveStamped, 'drive', 10)

        # Timer to publish as fast as possible (e.g., 100Hz = 0.01s)
        timer_period = 0.001 
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # Get parameter values
        v = self.get_parameter('v').get_parameter_value().double_value
        d = self.get_parameter('d').get_parameter_value().double_value

        msg = AckermannDriveStamped()
        msg.drive.speed = v
        msg.drive.steering_angle = d

        # Publish message
        self.publisher_.publish(msg)
        # self.get_logger().info(f'Publishing: speed={v}, steering_angle={d}')

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

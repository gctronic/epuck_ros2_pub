import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Int32
from sensor_msgs.msg import Range

class Epuck2Publisher(Node):

    def __init__(self):
        super().__init__('epuck_ros2_publisher')
        self.publisher_led0 = self.create_publisher(Bool, 'led0', 1)
        self.publisher_led2 = self.create_publisher(Bool, 'led2', 1)
        self.publisher_led4 = self.create_publisher(Bool, 'led4', 1)
        self.publisher_led6 = self.create_publisher(Bool, 'led6', 1)
        self.publisher_led3 = self.create_publisher(Int32, 'led3', 1) # RGB led
        self.subscription = self.create_subscription(Range,'ps1', self.listener_callback, 1)
        self.subscription  # prevent unused variable warning
        timer_period = 0.15  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.state = 0

    def listener_callback(self, msg):
        temp = Int32()
        if msg.range < 0.03:
            self.get_logger().info('Prox0 detected: "%f"' % msg.range)
            temp.data = 0x00FFFFFF;
            self.publisher_led3.publish(temp)
        else:
            temp.data = 0x00000000;
            self.publisher_led3.publish(temp)

    def timer_callback(self):
        msg = Bool()
        if self.state == 0:
            msg.data = True
            self.publisher_led0.publish(msg)
            msg.data = False
            self.publisher_led2.publish(msg)
            self.publisher_led4.publish(msg)
            self.publisher_led6.publish(msg)
            self.state = 1
        elif self.state == 1:
            msg.data = True
            self.publisher_led2.publish(msg)
            msg.data = False
            self.publisher_led0.publish(msg)
            self.publisher_led4.publish(msg)
            self.publisher_led6.publish(msg)
            self.state = 2
        elif self.state == 2:
            msg.data = True
            self.publisher_led4.publish(msg)
            msg.data = False
            self.publisher_led0.publish(msg)
            self.publisher_led2.publish(msg)
            self.publisher_led6.publish(msg)
            self.state = 3
        elif self.state == 3:
            msg.data = True
            self.publisher_led6.publish(msg)
            msg.data = False
            self.publisher_led0.publish(msg)
            self.publisher_led2.publish(msg)
            self.publisher_led4.publish(msg)
            self.state = 0

        self.get_logger().info('Publishing state: "%d"' % self.state)


def main(args=None):
    rclpy.init(args=args)

    epuck2_publisher = Epuck2Publisher()

    rclpy.spin(epuck2_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    epuck2_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

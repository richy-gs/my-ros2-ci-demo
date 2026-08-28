"""A minimal publisher node used to exercise the CI pipeline."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    """Publishes an incrementing counter message once a second."""

    def __init__(self) -> None:
        super().__init__('talker')
        self._publisher = self.create_publisher(String, 'chatter', 10)
        self._count = 0
        self.create_timer(1.0, self._on_timer)

    def _on_timer(self) -> None:
        msg = String()
        msg.data = f'hello world {self._count}'
        self._publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self._count += 1


def main(args=None) -> None:
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

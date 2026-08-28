import rclpy

from demo_pkg.talker import Talker


def test_publishes_incrementing_counter():
    rclpy.init()
    node = Talker()
    try:
        assert node._count == 0
        node._on_timer()
        assert node._count == 1
        node._on_timer()
        assert node._count == 2
    finally:
        node.destroy_node()
        rclpy.shutdown()

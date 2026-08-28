from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='demo_pkg',
            executable='talker',
            name='talker',
            output='screen',
        ),
    ])

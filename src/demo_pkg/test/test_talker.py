# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from demo_pkg.talker import Talker
import rclpy


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

if __name__ == "__main__":
    test_publishes_incrementing_counter()
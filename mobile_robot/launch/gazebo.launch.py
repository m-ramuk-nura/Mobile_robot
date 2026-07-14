import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('mobile_robot')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    urdf_path = os.path.join(pkg_share, 'urdf', 'mobile_robot.urdf')

    robot_description = ParameterValue(Command(['cat ', urdf_path]), value_type=str)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        )
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    # ROS2 analog of ROS1's `spawn_model` - spawns the robot into a running
    # Gazebo instance by reading /robot_description.
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        arguments=['-topic', 'robot_description', '-entity', 'mobilr_robot'],
        output='screen',
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
    ])

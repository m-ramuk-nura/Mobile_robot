import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('mobile_robot')
    default_urdf_path = os.path.join(pkg_share, 'urdf', 'mobile_robot.urdf')
    default_rviz_path = os.path.join(pkg_share, 'rviz', 'urdf.rviz')

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=default_urdf_path,
        description='Absolute path to the robot URDF file',
    )

    robot_description = ParameterValue(
        Command(['cat ', LaunchConfiguration('model')]),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_path],
    )

    return LaunchDescription([
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
    ])

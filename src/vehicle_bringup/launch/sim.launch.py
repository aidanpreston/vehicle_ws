import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    bringup = get_package_share_directory('vehicle_bringup')
    description = get_package_share_directory('vehicle_description')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world = os.path.join(bringup, 'worlds', 'basic_world.sdf')
    urdf = os.path.join(description, 'urdf', 'vehicle.urdf')
    with open(urdf) as f:
        robot_desc = f.read()

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items())

    rsp = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}])

    spawn = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'vehicle_blue', '-z', '0.05'])

    return LaunchDescription([gz_sim, rsp, spawn])
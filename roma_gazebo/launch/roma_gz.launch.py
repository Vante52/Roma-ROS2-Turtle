import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    roma_gazebo_share = get_package_share_directory("roma_gazebo")
    roma_description_share = get_package_share_directory("roma_description")
    ros_gz_sim_share = get_package_share_directory("ros_gz_sim")

    world_file = os.path.join(
        roma_gazebo_share,
        "worlds",
        "flat_world.sdf"
    )

    xacro_file = os.path.join(
        roma_description_share,
        "urdf",
        "roma.urdf.xacro"
    )

    robot_description = {
        "robot_description": Command([
            "xacro ",
            xacro_file,
            " mesh_uri_prefix:=file://",
            roma_description_share
        ])
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim_share,
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": f"-r {world_file}"
        }.items()
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="screen"
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-world", "flat_world",
            "-name", "roma",
            "-topic", "robot_description",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "0.15"
        ],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        TimerAction(
            period=3.0,
            actions=[spawn_robot]
        )
    ])
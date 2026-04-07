from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

ARGUMENTS = [
    DeclareLaunchArgument(
        #user interface of the joint state publisher
        name='gui',
        default_value='true',
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui'
    ),
    DeclareLaunchArgument(
        #path to the urdf file
        name='model',
        default_value=PathJoinSubstitution([
            get_package_share_directory('roma_description'),
            'urdf',
            'roma.urdf'
        ]),
    ),
]


def generate_launch_description():
    """
    Launch the urdf_launch display.launch.py with the given arguments
    return: LaunchDescription - the launch description with its arguments
    """
    ld = LaunchDescription(ARGUMENTS)

    ld.add_action(
        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('urdf_launch'),
                'launch',
                'display.launch.py'
            ]),
            launch_arguments={
                'urdf_package': 'roma_description',
                'urdf_package_path': LaunchConfiguration('model'),
                'jsp_gui': LaunchConfiguration('gui')
            }.items()
        )
    )

    return ld
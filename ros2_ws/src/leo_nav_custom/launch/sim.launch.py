import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_leo_nav_custom = get_package_share_directory('leo_nav_custom')
    pkg_leo_gazebo = get_package_share_directory('leo_gz_bringup')

    world_file = os.path.join(pkg_leo_nav_custom, 'worlds', 'flat_empty.world')

    # Gazebo Simulator
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_leo_gazebo, 'launch', 'leo_gz.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    # Autonomy Node
    go_to_goal_node = Node(
        package='leo_nav_custom',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        go_to_goal_node
    ])

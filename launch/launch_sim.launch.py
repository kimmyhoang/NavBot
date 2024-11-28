from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument,
                            IncludeLaunchDescription)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration,
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    package_name = 'navbot' 
    pkg_gazebo_ros = get_package_share_directory('ros_gz_sim')
    pkg_navbot = get_package_share_directory(package_name)
    rsp_launch_path = PathJoinSubstitution([pkg_navbot, 'launch', 'rsp.launch.py'])
    gz_launch_path = PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gz_sim.launch.py'])

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Set use simulation time to True'
    )

    return LaunchDescription([
        use_sim_time_arg,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rsp_launch_path),
            launch_arguments={
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path)
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description', '-entity', 'my_bot'],
            output='screen'
        ),
    ])

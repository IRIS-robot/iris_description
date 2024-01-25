from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    log_level = DeclareLaunchArgument(
        name='log_level', 
        default_value='INFO', 
        choices=['DEBUG','INFO','WARN','ERROR','FATAL'],
        description='Flag to set log level')

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('meu_pkg_py'), '/launch/simulation.launch.py']),
         
           
    )

    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('meu_pkg_py'), '/launch/load.launch.py']),
    )

    # SLAM (SLAM Toolbox ou Cartographer) vem a partir daqui:
    
    slam = Node(
        parameters=[
          '/home/thormeyr/ws_urdf2/src/meu_pkg_py/config/mapper_params_online_async.yaml',
          {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')

    
	

    ld = LaunchDescription()
    ld.add_action(log_level)
    ld.add_action(simulation)
    ld.add_action(robot)
    ld.add_action(slam)

    return ld

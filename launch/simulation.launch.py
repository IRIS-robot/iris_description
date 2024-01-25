from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    gz_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=''
    )

    gz_model_uri = SetEnvironmentVariable(
        name='GAZEBO_MODEL_DATABASE_URI', 
        value=''
    )

    world_path = DeclareLaunchArgument(
        name='world_path', 
        default_value='/home/thormeyr/ws_urdf2/src/meu_pkg_py/worlds/world1.world', 
        description=''
    )

    gzserver = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'), '/launch/gzserver.launch.py']),
            launch_arguments = {
                'verbose': 'false',
                'world': LaunchConfiguration('world_path')
            }.items()
        )

    gzclient = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'), '/launch/gzclient.launch.py']),
            #condition=IfCondition(LaunchConfiguration('simulation_gui'))
        )

    ld = LaunchDescription()
    ld.add_action(gz_model_path)
    # ld.add_action(gz_model_uri)
    ld.add_action(world_path)
    ld.add_action(gzserver)
    ld.add_action(gzclient)

    return ld

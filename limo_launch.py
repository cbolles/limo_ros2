import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    # Get the directory
    model_path = os.path.join(get_package_share_directory('limo_description'),
                            'urdf', 'limo_four_diff.xacro')


    # Get the name of the robot from the environment
    robot_name = os.getenv('ROBOT_NAME')
    print(robot_name)
    if robot_name is None:
        raise Exception('Environment variable ROBOT_NAME is not set')

    # Launch configuration variables
    declare_port_name = DeclareLaunchArgument(
        'port_name',
        default_value='ttyTHS1')

    declare_odom_name = DeclareLaunchArgument(
        name='odom_topic_name',
        default_value=f'/{robot_name}/odom')

    declare_use_mcnamu = DeclareLaunchArgument(
        name='use_mcnamu',
        default_value='false')

    declare_robot_name = DeclareLaunchArgument(
        name='robot_name',
        default_value='unnames')

    declare_odom_frame_arg = DeclareLaunchArgument(
        name='odom_frame',
        default_value='odom',
        description='Odometry frame id')

    declare_base_link_frame_arg = DeclareLaunchArgument(
        name='base_frame',
        default_value='base_link',
        description='Base link frame id')

    declare_odom_topic_arg = DeclareLaunchArgument(
        name='odom_topic_name',
        default_value=f'/{robot_name}/odom',
        description='Odometry topic name')

    declare_sim_control_rate_arg = DeclareLaunchArgument(
        name='control_rate',
        default_value='50',
        description='Simulation control loop update rate')

    declare_use_mcnamu_arg = DeclareLaunchArgument(
        name='use_mcnamu',
        default_value='false',
        description='Use mecanum motion mode')

    declare_pub_odom_tf_arg = DeclareLaunchArgument(
        name='pub_odom_tf',
        default_value='true',
        description='Parameter to publish odom')

    declare_joint_states_topic_arg = DeclareLaunchArgument(
        name='joint_topic_name',
        default_value=f'/{robot_name}/joint_states',
        description='Joint state topic name')

    declare_robot_description_topic_arg = DeclareLaunchArgument(
        name='robot_description_topic',
        default_value=f'/{robot_name}/robot_description',
        description='Robot description topic name')

    declare_tf_topic_arg = DeclareLaunchArgument(
        name='tf_topic_name',
        default_value=f'/{robot_name}/tf',
        description='TF topic name')

    declare_tf_static_topic_arg = DeclareLaunchArgument(
        name='tf_static_topic_name',
        default_value=f'/{robot_name}/tf_static',
        description='TF topic name')


    # Node for IMU static transform
    start_imu_static_transform_pub_cmd = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_imu',
        arguments=[
            '0.0', '0.0', '0.0', '0.0', '0.0', '0.0',
            f'{robot_name}/base_link', f'{robot_name}/imu_link'
        ])

    # LIMO Base node
    start_limo_base = Node(
        package='limo_base',
        executable='limo_base',
        output='screen',
        emulate_tty=True,
        parameters=[{
                'port_name': LaunchConfiguration('port_name'),
                'odom_frame': LaunchConfiguration('odom_frame'),
                'base_frame': LaunchConfiguration('base_frame'),
                'odom_topic_name': LaunchConfiguration('odom_topic_name'),
                'control_rate': LaunchConfiguration('control_rate'),
                'use_mcnamu': LaunchConfiguration('use_mcnamu'),
                'pub_odom_tf': LaunchConfiguration("pub_odom_tf")
        }])

    # LIMO Joint State node
    start_limo_joint_state_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        remappings=[
            ('/joint_state', LaunchConfiguration('joint_topic_name')),
            ('/robot_description', LaunchConfiguration('robot_description_topic'))
        ])

    # Robot state node
    start_limo_robot_state_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command(['xacro ', model_path])}],
        remappings=[
            ('/joint_state', LaunchConfiguration('joint_topic_name')),
            ('/robot_description', LaunchConfiguration('robot_description_topic')),
            ('/tf', LaunchConfiguration('tf_topic_name')),
            ('/tf_static', LaunchConfiguration('tf_static_topic_name'))
        ])

    # Create the launch description to be populated
    launch_desc = LaunchDescription()

    # Declare the launch options
    launch_desc.add_action(declare_odom_name)
    launch_desc.add_action(declare_port_name)
    launch_desc.add_action(declare_use_mcnamu)
    launch_desc.add_action(declare_robot_name)
    launch_desc.add_action(declare_odom_frame_arg)
    launch_desc.add_action(declare_base_link_frame_arg)
    launch_desc.add_action(declare_odom_topic_arg)
    launch_desc.add_action(declare_sim_control_rate_arg)
    launch_desc.add_action(declare_use_mcnamu_arg)
    launch_desc.add_action(declare_pub_odom_tf_arg)
    launch_desc.add_action(declare_joint_states_topic_arg)
    launch_desc.add_action(declare_robot_description_topic_arg)
    launch_desc.add_action(declare_tf_topic_arg)
    launch_desc.add_action(declare_tf_static_topic_arg)

    # Add all of the Nodes to the launch description
    launch_desc.add_action(start_imu_static_transform_pub_cmd)
    launch_desc.add_action(start_limo_base)
    launch_desc.add_action(start_limo_joint_state_node)
    launch_desc.add_action(start_limo_robot_state_node)

    return launch_desc

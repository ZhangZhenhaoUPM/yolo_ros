#!/usr/bin/env python3
"""
Test launch file for YOLO with RViz visualization
Launches:
  - YOLO node for object detection
  - RViz for visualization
  - USB camera or image republisher (optional)
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # RViz configuration
    rviz_config = os.path.join(
        get_package_share_directory('yolo_ros'),
        'rviz',
        'default.rviz'
    )

    # If default config doesn't exist, create basic config path
    if not os.path.exists(rviz_config):
        rviz_config = ''  # Will use RViz defaults

    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'model',
            default_value='yolo11n.pt',
            description='YOLO model (n=nano, s=small, m=medium, l=large)'
        ),
        DeclareLaunchArgument(
            'input_image_topic',
            default_value='/rgb',
            description='Input image topic'
        ),
        DeclareLaunchArgument(
            'threshold',
            default_value='0.5',
            description='Detection threshold'
        ),
        DeclareLaunchArgument(
            'image_reliability',
            default_value='1',  # RELIABLE
            description='QoS reliability (1=RELIABLE, 2=BEST_EFFORT)'
        ),
        DeclareLaunchArgument(
            'device',
            default_value='cuda:0',
            description='Device (cuda:0 or cpu)'
        ),

        # YOLO node
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('yolo_bringup'),
                    'launch',
                    'yolo.launch.py'
                )
            ),
            launch_arguments={
                'model': LaunchConfiguration('model'),
                'input_image_topic': LaunchConfiguration('input_image_topic'),
                'threshold': LaunchConfiguration('threshold'),
                'image_reliability': LaunchConfiguration('image_reliability'),
                'device': LaunchConfiguration('device'),
                'enable': 'True',
                'namespace': 'yolo',
            }.items(),
        ),

        # RViz node
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config] if rviz_config else [],
        ),
    ])

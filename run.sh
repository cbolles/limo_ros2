#!/bin/bash

# Setup for access LIMO ROS2 launch files
. install/setup.bash

# Launch robot base and bringup camera
ros2 launch limo_launch.py

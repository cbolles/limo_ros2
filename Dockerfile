FROM westonrobot/limo_ros:humble_22082023

SHELL ["/bin/bash", "-c"]

WORKDIR /limo

COPY . .

RUN source /opt/ros/humble/setup.sh &&\
    ./build.sh

# Copy over the script to run the robot base
COPY run.sh run.sh
RUN chmod 777 run.sh

# Copy over the custom launch file
COPY limo_launch.py limo_launch.py

CMD ./run.sh

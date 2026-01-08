FROM ros:humble

SHELL ["/bin/bash", "-c"]

# Install supporting packages
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends \
    build-essential \
    python3-pip \
    pkg-config \
    swig \
    python3-rosdep

# Clean installation of libc-bin
RUN rm /var/lib/dpkg/info/libc-bin.* && \
    apt-get clean && \
    apt-get update && \
    apt-get install libc-bin


# Install LIDAR SDK
RUN git clone https://github.com/YDLIDAR/YDLidar-SDK.git &&\
    mkdir -p YDLidar-SDK/build && \
    cd YDLidar-SDK/build &&\
    cmake ..&&\
    make &&\
    make install &&\
    cd .. &&\
    pip install . &&\
    cd .. && rm -r YDLidar-SDK

# Bring over and build LIMO code
WORKDIR /limo
COPY . .
RUN source /opt/ros/humble/setup.sh && \
    rosdep install --from-paths src --ignore-src -r -y && \
    ./build.sh

# Copy over the script to run the robot base
COPY run.sh run.sh
RUN chmod 777 run.sh

# CMD ./run.sh

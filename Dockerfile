FROM osrf/ros:humble-desktop

# Install core utilities and ROS 2 dependencies
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    python3-rosdep \
    nano \
    git \
    wget \
    x11-apps \
    mesa-utils \
    libgl1-mesa-glx \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true
RUN rosdep update

# Create workspace directory
RUN mkdir -p /ros2_ws/src
WORKDIR /ros2_ws

# Setup bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "if [ -f /ros2_ws/install/setup.bash ]; then source /ros2_ws/install/setup.bash; fi" >> ~/.bashrc
# Fix domain id to ensure isolation
RUN echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc

CMD ["bash"]

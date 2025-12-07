# Multi-stage Dockerfile for VLA Integration Module
# Provides ROS 2 Humble + Gazebo Garden + Nav2 + MoveIt 2 + Python VLA dependencies

# Stage 1: Base ROS 2 Humble
FROM ros:humble-ros-base-jammy AS ros2-base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install essential tools
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    vim \
    build-essential \
    python3-pip \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Add Gazebo Garden and ROS 2 Desktop
FROM ros2-base AS simulation-layer

# Install Gazebo Garden
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install ROS 2 Desktop, Gazebo, Nav2, and MoveIt 2
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-desktop \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-navigation2 \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-moveit-visual-tools \
    ros-${ROS_DISTRO}-moveit-ros-planning-interface \
    gz-garden \
    && rm -rf /var/lib/apt/lists/*

# Stage 3: Add VLA Python Dependencies
FROM simulation-layer AS vla-layer

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install VLA dependencies
RUN pip3 install --no-cache-dir \
    openai-whisper==20231117 \
    openai==1.3.0 \
    ultralytics==8.0.221 \
    opencv-python==4.8.1.78 \
    numpy==1.24.3 \
    scipy==1.11.4 \
    matplotlib==3.8.2 \
    jupyter==1.0.0 \
    jupyterlab==4.0.9 \
    pytest==7.4.3 \
    pytest-cov==4.1.0 \
    python-dotenv==1.0.0 \
    pydantic==2.5.2 \
    jsonschema==4.20.0

# Install audio dependencies for Whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pyaudio==0.2.14

# Stage 4: Add Robot Model and Demo Worlds (Example Layer)
FROM vla-layer AS example-layer

# Create workspace
RUN mkdir -p /workspace/vla_ws/src
WORKDIR /workspace/vla_ws

# Copy robot URDF and world files (will be created in subsequent tasks)
# These will be mounted as volumes during container run
RUN mkdir -p /workspace/assets/robot /workspace/assets/worlds /workspace/code-examples

# Source ROS 2 setup in bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /root/.bashrc

# Set working directory
WORKDIR /workspace

# Expose ports for Jupyter and ROS
EXPOSE 8888 11311

# Default command
CMD ["/bin/bash"]

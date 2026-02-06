# Lab 1: Intro to ROS 2 - Deliverable

## Contents

- **talker.py** - Publishes AckermannDriveStamped with speed `v` and steering angle `d`
- **relay.py** - Subscribes to `/drive`, multiplies values by 3, publishes to `/drive_relay`
- **lab1_launch.py** - Launch file for both nodes

## Running

```bash
cd ~/lab1_ws
colcon build --packages-select lab1_pkg
source install/setup.bash
ros2 launch lab1_pkg lab1_launch.py
```

## Verification Commands

```bash
ros2 topic list
ros2 topic info drive
ros2 topic echo drive
ros2 node list
ros2 node info talker
ros2 node info relay
```


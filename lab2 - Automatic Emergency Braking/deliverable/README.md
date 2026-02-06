# Lab 2: Automatic Emergency Braking - Deliverable

## Contents

- **safety_node.py**: The AEB implementation using iTTC (Instantaneous Time to Collision)

## How It Works

The safety node:
1. Subscribes to `/scan` (LaserScan) and `/ego_racecar/odom` (Odometry)
2. Calculates iTTC for each laser beam: `iTTC = range / max(-velocity * cos(angle), 0)`
3. If any iTTC < 0.5 seconds, publishes brake command to `/drive`

## Running

```bash
# In the simulator container
ros2 run safety_node safety_node.py
```


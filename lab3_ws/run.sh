#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lab 3 – run.sh
# Builds the lab3 package and launches all nodes in separate terminal tabs.
# Usage: bash run.sh  (from anywhere)
# ─────────────────────────────────────────────────────────────────────────────

set -e

WS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_BASH="$WS_DIR/install/setup.bash"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Lab 3 – Building package…"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Source ROS2 base if not already sourced
if [ -z "$ROS_DISTRO" ]; then
    # Try common ROS2 distros in order
    for distro in humble iron jazzy foxy galactic rolling; do
        if [ -f "/opt/ros/$distro/setup.bash" ]; then
            source "/opt/ros/$distro/setup.bash"
            echo "  Sourced ROS2 $distro"
            break
        fi
    done
fi

# Build
cd "$WS_DIR"
colcon build --symlink-install --quiet 2>/dev/null || colcon build --symlink-install

echo ""
echo "  Build complete. Launching nodes…"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Helper: open a new gnome-terminal tab with a title and command
open_tab() {
    local title="$1"
    local cmd="$2"
    gnome-terminal --tab --title="$title" -- bash -c "
        source '$SETUP_BASH' 2>/dev/null || true
        echo -e '\033[1;36m[$title]\033[0m'
        $cmd
        echo -e '\033[1;33m[Node exited – press Enter to close]\033[0m'
        read
    " &
    sleep 0.3  # slight stagger so tabs appear in order
}

# ── Static TF Frames ──────────────────────────────────────────────────────────
open_tab "TF: world→base" \
    "ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 world base"

open_tab "TF: base→end_effector" \
    "ros2 run tf2_ros static_transform_publisher 34 34 41 0 0 0 base end_effector_joint"

open_tab "TF: world→camera" \
    "ros2 run tf2_ros static_transform_publisher 34 23 60 0 0 -1 world camera"

# Give static publishers a moment to establish before dynamic nodes start
sleep 1.5

# ── Dynamic Nodes ─────────────────────────────────────────────────────────────
open_tab "Ball Publisher" \
    "ros2 run lab3 ball_publisher"

sleep 0.5

open_tab "Ball Frame" \
    "ros2 run lab3 ball_attached_frame"

sleep 0.5

open_tab "Listener Node" \
    "ros2 run lab3 listener_node"

echo ""
echo "  All nodes launched in separate tabs."
echo "  Watch the 'Listener Node' tab for ball position output."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

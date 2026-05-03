#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lab 3 – run.sh
# Builds the lab3 package and launches all nodes in separate terminal tabs.
# Usage:
#   bash run.sh            – build & launch all nodes
#   bash run.sh --frames   – generate frames.pdf (run AFTER nodes are up)
# ─────────────────────────────────────────────────────────────────────────────

set -e

WS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_BASH="$WS_DIR/install/setup.bash"

# Source ROS2 base if not already sourced
if [ -z "$ROS_DISTRO" ]; then
    for distro in jazzy humble iron foxy galactic rolling; do
        if [ -f "/opt/ros/$distro/setup.bash" ]; then
            source "/opt/ros/$distro/setup.bash"
            break
        fi
    done
fi

source "$SETUP_BASH" 2>/dev/null || true

# ── --frames mode: generate the TF frame PDF ─────────────────────────────────
if [[ "$1" == "--frames" ]]; then
    echo "Listening to /tf for 5 seconds and saving frames.pdf …"
    ros2 run tf2_tools view_frames --wait-time 5 -o frames
    echo "Done! frames.pdf saved to: $(pwd)/frames.pdf"
    exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Lab 3 – Building package…"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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
    sleep 0.3
}

# ── Static TF Frames ──────────────────────────────────────────────────────────
open_tab "TF: world→base" \
    "ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 world base"

open_tab "TF: base→end_effector" \
    "ros2 run tf2_ros static_transform_publisher 34 34 41 0 0 0 base end_effector_joint"

open_tab "TF: world→camera" \
    "ros2 run tf2_ros static_transform_publisher 34 23 60 0 0 -1 world camera"

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
echo ""
echo "  To generate frames.pdf (while nodes are running):"
echo "    bash run.sh --frames"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

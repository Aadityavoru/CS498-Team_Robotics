import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/trvise/CS498-Team_Robotics/Lab -1/lab1_ws/install/safety_node'

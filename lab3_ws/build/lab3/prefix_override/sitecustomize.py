import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/trvise/CS498-Team_Robotics/lab3_ws/install/lab3'

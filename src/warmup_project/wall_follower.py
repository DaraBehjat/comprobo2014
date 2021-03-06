## This is Dara Behjat's code for the wall follower behavior of the neato robot.
## Some of the code was repurposed from wall.py
## This is part of the Warm Up Project for CompRobo

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan

distance_to_wall = 1.0
flag = False

def scan_received(msg):
    """ Callback function for msg of type sensor_msgs/LaserScan """
    global distance_to_wall
    valid_measurements = []
    for i in range(5):
        if msg.ranges[i] != 0 and msg.ranges[i] < 7:
            valid_measurements.append(msg.ranges[i])
    if len(valid_measurements):
        distance_to_wall = sum(valid_measurements)/float(len(valid_measurements))
    else:
        distance_to_wall = -0.5
    print distance_to_wall

def wall():
    """ Run loop for the wall node """
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, scan_received)
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    global flag
    while not rospy.is_shutdown():
        if distance_to_wall == -0.5:
            msg = Twist()
	    flag = True

def follow_wall(msg, pub):
    """ sends angular and linear velocities to the robot depending on distance from wall """
    global distance_to_wall
    velocity_msg = Twist(Vector3(0.3, 0.0, 0.0), Vector3(0.0, 0.0, 1.57))
    valid_measurements = []
    for i in range(5):
        if msg.ranges[i] > 0.0 and msg.ranges[i] < 1:
            valid_measurements.append(msg.ranges[i])
    if len(valid_measurements):
        velocity_msg = Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 1.57))
    else:    
        velocity_msg = Twist(Vector3(0.2, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
    pub.publish(velocity_msg)
    r.sleep()
    for i in range(360):
        if msg.ranges[i] > 45 and msg.ranges[i] < 90:
            valid_measurements.append(msg.ranges[i])
    if len(valid_measurements):
        velocity_msg = Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 1.57))
    else:    
        velocity_msg = Twist(Vector3(0.2, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
    pub.publish(velocity_msg)
    r.sleep()            

def turn():
    """Turn robot when it approcahes wall"""
        
if __name__ == '__main__':
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, follow_wall, pub)
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    try:
        wall()
    except rospy.ROSInterruptException: pass

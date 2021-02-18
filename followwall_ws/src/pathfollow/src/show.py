#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import rospy
import math
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import roslib;roslib.load_manifest('pathfilter')  
from pathfilter.msg import Traj,TargetPoint
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def gettrajectory():
    msg = rospy.wait_for_message('/trajectory', Traj)
    trajectory = [[msg.trajectoryX[i],msg.trajectoryY[i]] for i in range(len(msg.trajectoryX))]
    return trajectory

def getodom():
    odom = rospy.wait_for_message('/odometry/filtered', Odometry)
    x = odom.pose.pose.orientation.x
    y = odom.pose.pose.orientation.y
    z = odom.pose.pose.orientation.z
    w = odom.pose.pose.orientation.w
    robotX = odom.pose.pose.position.x
    robotY = odom.pose.pose.position.y
    robotAngle = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return robotX,robotY,robotAngle
def bspline(trajectory,sampleNum):
    t = range(len(trajectory))
    trajectoryX = np.array(trajectory)[:,0]
    trajectoryY = np.array(trajectory)[:,1]
    x_tup = interpolate.splrep(t, trajectoryX, k=3)
    y_tup = interpolate.splrep(t, trajectoryY, k=3)
    ipl_t = np.linspace(0.0, len(trajectory) - 1, len(trajectory))
    xBspline = interpolate.splev(ipl_t, x_tup)
    yBspline = interpolate.splev(ipl_t, y_tup)
    output = [[xBspline[i],yBspline[i]] for i in range(len(xBspline))]
    return output

def main():
    rospy.init_node('show')
    traj = gettrajectory()
    traj = bspline(traj,1000)
    plt.ion()
    x = []
    y = []
    while not rospy.is_shutdown():
        plt.clf()
        robotX, robotY, robotAngle = getodom()
        x.append(robotX)
        y.append(robotY)
        plt.plot(x,y,color = 'r')
        plt.plot(np.array(traj)[:, 0], np.array(traj)[:, 1], color = 'b')
        plt.pause(0.001)
    plt.show()

if __name__ == '__main__':
    main()
    

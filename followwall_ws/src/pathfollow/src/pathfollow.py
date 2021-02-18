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

class Fox(object):
    def __init__(self):
        self.dt = rospy.get_param("dt")
        self.k1 = rospy.get_param("k1")
        self.k2 = rospy.get_param("k2")
        self.lmde = rospy.get_param("lmde")
        self.fairA = rospy.get_param("fairA")
        self.ktheta = rospy.get_param("ktheta")
        self.targetindex = rospy.get_param("targetindex")
        self.sampleNum = rospy.get_param("sampleNum")
        self.initCloserAngle = rospy.get_param("initCloserAngle")
        self.linearSpeedDesire = rospy.get_param("linearSpeedDesire")
        self.closerAnglelist = [self.initCloserAngle]
        self.lasttargetSpeed = rospy.get_param("inittargetSpeed")
        self.gettrajectory()
        self.getCurvature()
        self.maxLinearSpeed = rospy.get_param("maxLinearSpeed")  ##移动机器人最大行驶速度
        self.minLinearSpeed = rospy.get_param("minLinearSpeed")  ##移动机器人最小行驶速度
        self.maxAcc = rospy.get_param("maxAcc")  ##移动机器人最大加速度
        self.minAcc = -self.maxAcc
        self.maxAngularSpeed = rospy.get_param("maxAngularSpeed")  ##移动机器人最大角速度
        self.minAngluarSpeed = -self.maxAngularSpeed
        self.lastlinearSpeed = 0
        self.lastrobotX = 0
        self.lastrobotY = 0
    
    def gettrajectory(self):
        path_topic = rospy.get_param('path_topic')
        msg = rospy.wait_for_message(path_topic, Traj)
        self.trajectory = [[msg.trajectoryX[i],msg.trajectoryY[i]] for i in range(len(msg.trajectoryX))]

    def getodom(self):
        odom_topic = rospy.get_param('odom_topic')
        odom = rospy.wait_for_message(odom_topic, Odometry)
        x = odom.pose.pose.orientation.x
        y = odom.pose.pose.orientation.y
        z = odom.pose.pose.orientation.z
        w = odom.pose.pose.orientation.w
        self.robotX = odom.pose.pose.position.x
        self.robotY = odom.pose.pose.position.y
        self.robotAngle = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
        self.linearSpeed = odom.twist.twist.linear.x
        self.angularSpeed = odom.twist.twist.angular.z

    ##从全局坐标系转化到Serrent-Frenet坐标系(文档公式13)
    def getSerretFrenetOrd(self,robotX,robotY,robotAngle,targetX,targetY,targetAngle):
        self.sfX =   (robotX - targetX) * math.cos(targetAngle) + (robotY - targetY) * math.sin(targetAngle)
        self.sfY = - (robotX - targetX) * math.sin(targetAngle) + (robotY - targetY) * math.cos(targetAngle)
        self.sfAngle = robotAngle - targetAngle
        if self.sfAngle > math.pi:
            self.sfAngle = self.sfAngle - 2 * math.pi
        elif self.sfAngle <  - math.pi:
            self.sfAngle = 2 * math.pi + self.sfAngle
    ##通过b样条对轨迹进行插值，并且求取每个点的一阶段数和二阶导数
    def bspline(self):
        self.firstOrderCon = [0]
        self.secondOrderCon = [0]
        self.targetAngle = [0]
        t = range(len(self.trajectory))
        trajectoryX = np.array(self.trajectory)[:,0]
        trajectoryY = np.array(self.trajectory)[:,1]
        x_tup = interpolate.splrep(t, trajectoryX, k=3)
        y_tup = interpolate.splrep(t, trajectoryY, k=3)
        ipl_t = np.linspace(0.0, len(self.trajectory) - 1, self.sampleNum)
        xBspline = interpolate.splev(ipl_t, x_tup)
        yBspline = interpolate.splev(ipl_t, y_tup)
        self.traj = [[xBspline[i],yBspline[i]] for i in range(len(xBspline))]
        self.firstOrderCon = self.firstOrderCon + [(self.traj[i + 1][1] - self.traj[i][1]) / (self.traj[i + 1][0] - self.traj[i][0]) for i in range(len(self.traj) - 1)]
        self.secondOrderCon = self.secondOrderCon + [(self.firstOrderCon[i + 1] - self.firstOrderCon[i]) / (self.traj[i + 1][0] - self.traj[i][0]) for i in range(len(self.traj) - 1)]
        self.targetAngle = self.targetAngle + [math.atan2(self.traj[i + 1][1] - self.traj[i][1] ,self.traj[i + 1][0] - self.traj[i][0]) for i in range(len(self.traj) - 1)]
    ##求取每个点的曲率(文档公式12)
    def getCurvature(self):
        self.bspline() 
        self.cs = []
        for i in range(len(self.firstOrderCon)):
            temp = math.sqrt(1 + math.pow(self.firstOrderCon[i],2)) * self.secondOrderCon[i]
            temp1 = math.pow(1 + math.pow(self.firstOrderCon[i],2), 2)
            self.cs.append(temp / temp1)
    ##获取趋近角(文档公式16)
    def getcloserAngle(self,linearSpeed):
        signu = np.sign(linearSpeed)
        self.closerAngle = - signu * self.fairA * (math.exp(2 * self.ktheta * self.sfY) - 1) / (math.exp(2 * self.ktheta * self.sfY) + 1)
        self.firstOrderCA = (self.closerAngle - self.closerAnglelist[-1]) / self.dt
        self.closerAnglelist.append(self.closerAngle)
    ##根据控制量表达式获取控制量(文档公式22)
    def getControl(self,linearSpeed):
        linearSpeedCon = self.linearSpeedDesire * math.cos(self.sfAngle)
        targetSpeedCon = self.k1 * self.sfX + self.linearSpeedDesire * math.cos(self.sfAngle)
        temp = self.firstOrderCA - self.lmde * self.sfY * linearSpeed * (math.sin(self.sfAngle) - math.sin(self.closerAngle)) / (self.sfAngle - self.closerAngle)
        temp1 = self.k2 * (self.sfAngle - self.closerAngle) + self.cs[self.targetindex] * targetSpeedCon
        angularSpeedCon = temp - temp1
        self.lasttargetSpeed = targetSpeedCon
        return linearSpeedCon, angularSpeedCon, targetSpeedCon
    ##更新目标点位置。
    def targetupdata(self,targetSpeedCon):
        temp = self.targetindex
        sumD = 0
        trajlen = len(self.traj)
        for i in range(0,trajlen,1):
            count = int(np.sign(targetSpeedCon) * i + self.targetindex)
            if count == trajlen - 1 and np.sign(targetSpeedCon) > 0:
                self.targetindex = count
                break
            elif count == 0 and np.sign(targetSpeedCon) < 0:
                self.targetindex = count
                break
            dist = math.hypot(self.traj[count][0] - self.traj[temp][0],self.traj[count][1] - self.traj[temp][1])
            sumD = sumD + dist
            temp = count
            if sumD >= (math.fabs(targetSpeedCon) * self.dt):

                self.targetindex = count
                break
            else:
                continue
    ##跟随函数主体框架
    def follow(self,robotX,robotY,robotAngle,linearSpeed):
        self.getSerretFrenetOrd(robotX,robotY,robotAngle,self.traj[self.targetindex][0],self.traj[self.targetindex][1],self.targetAngle[self.targetindex])
        self.getcloserAngle(linearSpeed)
        linearSpeedCon, angularSpeedCon, targetSpeedCon = self.getControl(linearSpeed)
        self.targetupdata(targetSpeedCon)
        return linearSpeedCon,angularSpeedCon,self.traj

    def lineaSpeedcheck(self, linearSpeed):
        acc = (linearSpeed - self.lastlinearSpeed) / self.dt
        if acc > self.maxAcc:
            acc = self.maxAcc
        elif acc < self.minAcc:
            acc = self.minAcc
        else:
            acc = acc
        linearSpeed = self.lastlinearSpeed + acc * self.dt
        if linearSpeed > self.maxLinearSpeed:
            linearSpeed = self.maxLinearSpeed
        elif linearSpeed < self.minLinearSpeed:
            linearSpeed = self.minLinearSpeed
        else:
            linearSpeed = linearSpeed
        self.lastlinearSpeed = linearSpeed
        return linearSpeed

    ##角速度检查，检查角速度控制命令是否在允许范围内
    def angularSpeedcheck(self, angularSpeed):
        if angularSpeed > self.maxAngularSpeed:
            angularSpeed = self.maxAngularSpeed
        elif angularSpeed < self.minAngluarSpeed:
            angularSpeed = self.minAngluarSpeed
        else:
            angularSpeed = angularSpeed
        return angularSpeed
    def robotpU(self,robotX,robotY,robotAngle,linearSpeed,angularSpeed):
        angularup = robotAngle + angularSpeed * self.dt
        robotXup = robotX + linearSpeed * math.cos(angularup) * self.dt
        robotYup = robotY + linearSpeed * math.sin(angularup) * self.dt
        return robotXup,robotYup,angularup

def main():
    rospy.init_node('pathfollow')
    ##获取参数
    cmd_vel_topic = rospy.get_param('cmd_vel_topic')
    cmd_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 1)
    fox = Fox()
    robotX = rospy.get_param('initrobotX')
    robotY = rospy.get_param('initrobotY')
    robotAngle = rospy.get_param('initrobotAngle')
    while not rospy.is_shutdown():
        s1 = time.time()
        fox.getodom()
        linearSpeedCon,angularSpeedCon,traj = fox.follow(fox.robotX, fox.robotY, fox.robotAngle, fox.linearSpeed)
        linearSpeed = fox.lineaSpeedcheck(linearSpeedCon)
        angularSpeed = fox.angularSpeedcheck(angularSpeedCon)
        twist = Twist()
        twist.linear.x = linearSpeed
        twist.angular.z = angularSpeed
        cmd_pub.publish(twist)
        e1 = time.time()
        fox.dt = e1 - s1
if __name__ == '__main__':
    main()


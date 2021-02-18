#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import fitsec as fs
import localpath as lp
import robotcontrol as rc
class Follow():
    def __init__(self):
        self.maxAcc = rospy.get_param("maxAcc")                   ##移动机器人最大加速度
        self.minAcc = -self.maxAcc
        self.dt = rospy.get_param("dt")                          ##采样时间
        self.kv = rospy.get_param("kv")
        self.sensorAngleMax = rospy.get_param("sensorAngleMax")   ##激光传感器的最大测量角度
        self.sensorAngleMin = rospy.get_param("sensorAngleMin")   ##激光传感器的最小测量角度
        self.sensorAngleReso = rospy.get_param("sensorAngleReso") ##激光传感器的角分辨率
        self.followAngleS = rospy.get_param("followAngleS")    ##提取的有效数据开始角度
        self.followAngleE = rospy.get_param("followAngleE")       ##提取的有效数据结束角度
        self.maxLinearSpeed = rospy.get_param("maxLinearSpeed")   ##移动机器人最大行驶速度
        self.minLinearSpeed = rospy.get_param("minLinearSpeed")   ##移动机器人最小行驶速度
        self.adjacentRange = rospy.get_param("adjacentRange")     ##进行计算的传感器探测距离最大值
        self.maxAngularSpeed = rospy.get_param("maxAngularSpeed") ##移动机器人最大角速度
        self.minAngluarSpeed = -self.maxAngularSpeed
        self.followdist = rospy.get_param("followdist")
        self.lookAHeadDist = rospy.get_param("lookAHeadDist")
        self.precision = rospy.get_param("precision")
        self.followside = rospy.get_param("followside")
        self.sidewindowlen = rospy.get_param("sidewindowlen")
        self.orphansNum = rospy.get_param("orphansNum")
        self.fitThreshold = rospy.get_param("fitThreshold")
        self.orphansdist = rospy.get_param("orphansdist")
        self.lastlinearSpeed = 0
        self.globalPointOrd = []
        self.robotlocate = []

    ##获取激光雷达数据，并将激光雷达数据转化成移动机器人坐标系的坐标,移动机器人坐标系：以移动机器人的前进方向为x轴，垂直于x轴向左为y轴
    #文档2.1获取激光传感器输出原始坐标点
    def getScan(self):
        temp = []
        self.sensorPoint = []
        ##订阅话题
        topic_name=rospy.get_param('scan_topic')
        msg = rospy.wait_for_message(topic_name, LaserScan)
        for i in range(len(msg.ranges)):
            tmp = self.sensorAngleMin + i * self.sensorAngleReso
            ##选取有效角度范围内的激光雷达数据
            if tmp >= self.followAngleS and tmp <= self.followAngleE and msg.ranges[i] <= self.adjacentRange:#文档公式1
                if msg.ranges[i] == float('inf') :
                    continue
                else:
                    ##距离转化成坐标
                    x = msg.ranges[i] * math.cos(tmp)
                    y = msg.ranges[i] * math.sin(tmp)
                    temp.append([x,y])
            else:
                continue
        distance = [math.hypot(temp[i][0], temp[i][1]) for i in range(len(temp))]      
        ind = distance.index(min(distance))
        for i in range(ind,len(temp),1):        
            self.sensorPoint.append(temp[i])
            
    ##获取移动机器人角速度和线速度
    def getOdom(self):
        ##订阅话题
        topic_name=rospy.get_param('odom_topic')
        msgodom = rospy.wait_for_message(topic_name,Odometry)
        x = msgodom.pose.pose.orientation.x
        y = msgodom.pose.pose.orientation.y
        z = msgodom.pose.pose.orientation.z
        w = msgodom.pose.pose.orientation.w
        self.vehicleX = msgodom.pose.pose.position.x
        self.vehicleY = msgodom.pose.pose.position.y
        self.vehicleYaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
        self.linearSpeed = msgodom.twist.twist.linear.x
        self.angularSpeed = msgodom.twist.twist.angular.z
        self.robotlocate.append([self.vehicleX, self.vehicleY])

    ##线速度检查，检查线速度控制命令是否在允许的范围内
    def lineaSpeedcheck(self,linearSpeed):
        acc = (linearSpeed - self.lastlinearSpeed) / self.dt 
        if acc > self.maxAcc:
            acc = self.maxAcc
        elif acc < self.minAcc:
            acc = self.minAcc
        else:
            acc = acc
        linearSpeed = self.lastlinearSpeed + acc
        if linearSpeed > self.maxLinearSpeed:
            linearSpeed = self.maxLinearSpeed
        elif linearSpeed < self.minLinearSpeed:
            linearSpeed = self.minLinearSpeed
        else:
            linearSpeed = linearSpeed
        self.lastlinearSpeed = linearSpeed
        return linearSpeed
    ##角速度检查，检查角速度控制命令是否在允许范围内
    def angularSpeedcheck(self,angularSpeed):
        if angularSpeed > self.maxAngularSpeed:
            angularSpeed = self.maxAngularSpeed
        elif angularSpeed < self.minAngluarSpeed:
            angularSpeed = self.minAngluarSpeed
        else:
            angularSpeed = angularSpeed
        return angularSpeed
    ##将每次的局部路径转化成全局路径
    def localToGlobal(self, normalPointList):
        laserx = [normalPointList[i][0] for i in range(len(normalPointList))]
        lasery = [normalPointList[i][1] for i in range(len(normalPointList))]
        ##将每次读取的传感器坐标点，转化成全局坐标系下的。见文档公式10
        for i in range(len(laserx)):
            x = laserx[i] * math.cos(self.vehicleYaw) - lasery[i] * math.sin(self.vehicleYaw) + self.vehicleX
            y = laserx[i] * math.sin(self.vehicleYaw) + lasery[i] * math.cos(self.vehicleYaw) + self.vehicleY
            self.globalPointOrd.append([round(x, 3), round(y, 3)])
    ##将全局路径坐标点写入数据文件
    def writePathToFile(self):
        fileID = open('/home/czp/followwall_ws/src/lqrfollow/path/globalpath.txt', 'w')
        for i in range(len(self.globalPointOrd)):
            fileID.write(str(self.globalPointOrd[i][0]))
            fileID.write(" ")
            fileID.write(str(self.globalPointOrd[i][1]))
            fileID.write("\n")
        fileID.close()
    ##将移动机器人走的实际路径写入数据文件
    def writeLocateToFile(self):
        fileID = open('/home/czp/followwall_ws/src/lqrfollow/path/robotlocate.txt', 'w')
        for i in range(len(self.robotlocate)):
            fileID.write(str(self.robotlocate[i][0]))
            fileID.write(" ")
            fileID.write(str(self.robotlocate[i][1]))
            fileID.write("\n")
        fileID.close()

def main():
    ##初始化节点
    rospy.init_node('followwall')
    ##读取launch文件的参数
    cml_topic = rospy.get_param("cmd_topic")
    cmd_pub = rospy.Publisher(cml_topic, Twist, queue_size=2) ##控制命令的发布话题
    ##类参数初始化
    follow = Follow()
    ##如果没有键盘中断，执行while循环，即跟墙。
    try:
        while True:
            ##读取激光传感器数据
            follow.getScan()
            ##读取移动机器人位置
            follow.getOdom()
            ##对原始数据进行拟合
            sensorPointfit, tangentslope = fs.fitsec(follow.sensorPoint,follow.sidewindowlen, follow.orphansNum,follow.orphansdist,follow.fitThreshold,follow.followside)
            ##将拟合后的数据进行平行处理
            normalPoint = lp.parallelsec(tangentslope, sensorPointfit, follow.followdist, follow.precision)
            ##利用控制算法，生成角速度和线速度控制命令
            linearSpeedCon, angularSpeedCon = rc.followFunc(normalPoint, sensorPointfit, follow.linearSpeed, follow.maxLinearSpeed, follow.lookAHeadDist, follow.kv, follow.followdist)
            ##对生成控制执行进行check
            linearSpeedCon = follow.lineaSpeedcheck(linearSpeedCon)
            angularSpeedCon = follow.angularSpeedcheck(angularSpeedCon)
            ##将每次生成的局部路径转化成全局路径        
            follow.localToGlobal(normalPoint)
            twist = Twist()
            twist.linear.x = linearSpeedCon
            twist.angular.z = angularSpeedCon
            cmd_pub.publish(twist)
    except KeyboardInterrupt:
        ##将全局路径写入txt文件中，用于之后的滤波处理。
        follow.writePathToFile()
        follow.writeLocateToFile()
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        cmd_pub.publish(twist)
if __name__ == '__main__':
    main()


#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy as np
import math
from scipy import interpolate
import roslib;roslib.load_manifest('pathfilter')  
from pathfilter.msg import Traj
import matplotlib.pyplot as plt
class Pathfilter(object):
    def __init__(self):
        self.mapGridSize = rospy.get_param("mapGridSize")
        self.gridNumThres = rospy.get_param("gridNumThres")
        self.fitThreshold = rospy.get_param("fitThreshold")
    ##求点到线段的距离
    def calPointToLineDis(self, poi, poi1, poi2):
        cross = (poi2[0] - poi1[0]) * (poi[0] - poi1[0]) + (poi2[1] - poi1[1]) * (poi[1] - poi1[1])
        if (cross <= 0):
            return math.hypot((poi[0] - poi1[0]), (poi[1] - poi1[1]))
        d2 = (poi2[0] - poi1[0]) * (poi2[0] - poi1[0]) + (poi2[1] - poi1[1]) * (poi2[1] - poi1[1])
        if (cross >= d2):
            return math.hypot((poi[0] - poi2[0]), (poi[1] - poi2[1]))
        r = cross / d2
        px = poi1[0] + (poi2[0] - poi1[0]) * r
        py = poi1[1] + (poi2[1] - poi1[1]) * r
        return math.hypot((poi[0] - px), (poi[1] - py))
    def readpath(self):
        self.globalpath = []
        with open('/home/czp/followwall_ws/src/lqrfollow/path/globalpath.txt', 'r') as f:
            for line in f:
                lineList = list(line.strip('\n').split(' '))
                lineData = []
                for i in range(len(lineList)):
                    if lineList[i] == '':
                        continue
                    else:
                        lineData.append(float(lineList[i]))
                self.globalpath.append(lineData)
    def readrobotlocate(self):
        self.robotlocate = []
        with open('/home/czp/followwall_ws/src/lqrfollow/path/robotlocate.txt', 'r') as f:
            for line in f:
                lineList = list(line.strip('\n').split(' '))
                lineData = []
                for i in range(len(lineList)):
                    if lineList[i] == '':
                        continue
                    else:
                        lineData.append(float(lineList[i]))
                self.robotlocate.append(lineData)
    ##生成栅格地图，并滤波
    def generateGridMap(self):
        self.pathfilter = []
        ##生成栅格地图
        self.gridmap = []
        ##获取栅格地图的x,y的最大最小值，以及栅格地图的每行每列栅格数量多少
        self.maxX = max(np.array(self.globalpath)[:, 0])
        self.minX = min(np.array(self.globalpath)[:, 0])
        self.maxY = max(np.array(self.globalpath)[:, 1])
        self.minY = min(np.array(self.globalpath)[:, 1])
        self.gridNumX = int(math.ceil((self.maxX - self.minX) / self.mapGridSize) + 1)
        self.gridNumY = int(math.ceil((self.maxY - self.minY) / self.mapGridSize) + 1)
        for indy in range(self.gridNumY):
            y = self.minY + self.mapGridSize * indy
            for indx in range(self.gridNumX):
                x = self.minX + indx * self.mapGridSize
                self.gridmap.append([x, y])
        self.correspondence = [[] for i in range(len(self.gridmap))]
        ##将传感器坐标点放到对应的栅格内。 
        for i in range(len(self.globalpath)):
            indexX = int(((self.globalpath[i][1] - self.minY) - self.mapGridSize / 2) / self.mapGridSize) + 1
            indexY = int(((self.globalpath[i][0] - self.minX) - self.mapGridSize / 2) / self.mapGridSize) + 1
            index = indexX * self.gridNumX + indexY
            self.correspondence[index].append(self.globalpath[i])
            if len(self.correspondence[index]) > self.gridNumThres:
                if self.gridmap[index] not in self.pathfilter:
                    self.pathfilter.append(self.gridmap[index])
    def pathgenerate(self):
        path = []
        for i in range(len(self.robotlocate)):
            dist = [math.hypot(self.robotlocate[i][0] - self.pathfilter[j][0], self.robotlocate[i][1] - self.pathfilter[j][1]) for j in range(len(self.pathfilter))]
            path.append(self.pathfilter[dist.index(min(dist))])
        return path

    def segmentfit(self, path):
        ##存放拟合之后的数据和激光点所对应拟合直线斜率
        pathfit = []
        ##拟合直线的初始位置，s表示拟合区间的首端，e表示拟合区间的尾端(文档2.2(3)直线拟合步骤2)
        s, e = 0, len(path) - 1
        while True:
            #求拟合区间直线斜率
            ##斜率角为90角，即slope等于无穷
            if path[s][0] == path[e][0]:
                slope = float('inf')
            ##斜率不等于90度角，求斜率和截距
            else:
                slope = (path[e][1] - path[s][1]) / (path[e][0] - path[s][0])
                b = path[e][1] - path[e][0] * slope
            ##求拟合区间内每个点到拟合直线的距离
            dist = [self.calPointToLineDis(path[i], path[e], path[s]) for i in range(s, e + 1, 1)]
            ##如果距离最大值小于阈值，拟合成功，在首尾两点之间进行插值
            if max(dist) < self.fitThreshold:
                if slope == float('inf'):
                    temp = (path[e][1] - path[s][1]) / (e - s)
                    ##拟合成功步骤4
                    for i in range(0, e - s + 1, 1):
                        x = path[s][0]
                        y = path[s][1] + i * temp
                        pathfit.append([x, y])
                else:
                    temp = (path[e][0] - path[s][0]) / (e - s)
                    for i in range(0, e - s + 1, 1):
                        x = path[s][0] + i * temp
                        y = x * slope + b
                        pathfit.append([x, y])
                if e >= len(path) - 2:#文档2.2(3)直线拟合步骤3
                    break
                else:
                    s = e + 1
                    e = len(path) - 1
            ##如果最大值大于阈值，直线拟合没有成功，尾端直接跳到距离最大值处
            else:
                e = s + dist.index(max(dist))
        return pathfit
def main():
    rospy.init_node('path', anonymous=True)

    ##初始化参数
    pf = Pathfilter()
    ##读取全局路径
    pf.readpath()
    ##读取机器人走的路径
    pf.readrobotlocate()
    ##生成栅格地图，并进行栅格滤波，生成初始全局路径
    pf.generateGridMap()
    ##通过移动机器人的移动轨迹生成最终全局路径
    path = pf.pathgenerate()
    ##利用直线拟合对最终路径进行优化
    path = pf.segmentfit(path)
    globalpathX = [path[i][0] for i in range(len(path))]
    globalpathY = [path[i][1] for i in range(len(path))]
    ##将路径信息通过话题发布出去。
    trajectory = rospy.get_param('trajectory_topic')
    pub = rospy.Publisher(trajectory, Traj, queue_size = 2)
    r = rospy.Rate(40) # 1000hz  
    while not rospy.is_shutdown(): 
        traj = Traj()
        traj.trajectoryX = globalpathX
        traj.trajectoryY = globalpathY
        pub.publish(traj)
        r.sleep
if __name__ == '__main__':
    main()

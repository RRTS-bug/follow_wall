#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import math
import numpy as np
from control.matlab import *
##lqr控制器
##文档2.5lqr控制器
def lqrFunc(angleError,distError,linearSpeed):
    A = np.array([[0, linearSpeed],[0, 0]])
    B = np.array([[0],[-1]])
    Q = np.array([[1.0, 0],[0,2.0]])
    R = np.array([[1]])
    K, P, e = lqr(A, B, Q, R)
    k1 = K.getA()
    r = -(k1[0][0] * distError + k1[0][1] * angleError)
    return r
##选取跟随目标点
def guidepoint(normalPointList,lookAHeadDist):
    distance = [math.hypot(normalPointList[i][0], normalPointList[i][1]) for i in range(len(normalPointList))]
    distIndex = distance.index(min(distance))
    for i in range(distIndex,len(normalPointList), 1):
        if math.hypot(normalPointList[i][0] - normalPointList[distIndex][0], normalPointList[i][1] - normalPointList[distIndex][1]) > lookAHeadDist:
            return normalPointList[i]
        elif i == len(normalPointList) - 1:
            return normalPointList[i]
        else:
            continue
    
def followFunc(normalPointList, fiterData, linearSpeed, maxLinearSpeed, lookAheadDist, kv, followdist):
    '''
    :param normalPointList (list): 法线点列表
    :param fiterData       (list): 拟合点列表
    :param linearSpeed     (float): 移动机器人的速度
    :param maxLinearSpeed  (float): 允许的移动机器人行驶的最大速度
    :param lookAheadDist   (float): 引导距离
    :param kv              (float): 速度系数
    :param followdist      (float): 跟随距离
    :return:
    '''
    distance = [math.hypot(fiterData[i][0], fiterData[i][1]) for i in range(len(fiterData))]
    distError = followdist - min(distance)
    point = guidepoint(normalPointList, lookAheadDist)
    angleError = math.atan2(point[1], point[0])
    linearSpeedCon = maxLinearSpeed * (1.0 / np.exp(kv * angleError))
    angularSpeedCon = lqrFunc(angleError,distError,linearSpeed)
    return linearSpeedCon,angularSpeedCon
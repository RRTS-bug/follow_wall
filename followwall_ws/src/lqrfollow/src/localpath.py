#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import math
import numpy as np
import fitsec as fs
##文档2.3生成局部路径
def getNormalPoint(tangentslope,sensorPointfit,followdist):
    normalPoint = []
    #获取拟合曲线上每个点的法线斜率和截距
    for i in range(len(sensorPointfit)):
        #切线斜率为0
        if tangentslope[i] == 0:
            normalSlope = float('inf')
            x1 = x2 = sensorPointfit[i][0]
            y1, y2 = sensorPointfit[i][1] + followdist, sensorPointfit[i][1] - followdist
        else:
        ##切线斜率不为0
            if tangentslope[i] == float('inf'):
                normalSlope = 0
            else:
                normalSlope = -1 / tangentslope[i]
            normalIntercept = sensorPointfit[i][1] - sensorPointfit[i][0] * normalSlope
            ##文档2.3生成局部路径公式5,公式6
            a = 1 + math.pow(normalSlope,2)
            b = -2 * sensorPointfit[i][0] + 2 * normalSlope * normalIntercept - 2.0 * normalSlope * sensorPointfit[i][1]
            c = math.pow(sensorPointfit[i][0],2) + math.pow(normalIntercept,2) - 2.0 * normalIntercept * sensorPointfit[i][1] + math.pow(sensorPointfit[i][1],2) - math.pow(followdist,2)
            x1,x2 = (-b + math.sqrt(math.pow(b,2.0) - 4.0 * a * c)) / (2.0 * a), (-b - math.sqrt(math.pow(b,2) - 4.0 * a * c)) / (2.0 * a)
            y1,y2 = (normalSlope * x1 + normalIntercept), (normalSlope * x2 + normalIntercept)
        #选到移动机器人近的一组法线点
        if math.hypot(x1, y1) > math.hypot(x2 ,y2) :
            normalPoint.append([x2, y2])
        else:
            normalPoint.append([x1, y1])
    return normalPoint
##对生成的法线点列表进行滤波
##文档2.3生成局部路径，图7
def filterpoint(normalPoint, sensorPointfit, followdist, precision):
    normalpointfilter = []
    for i in range(len(normalPoint)):
        dist = [fs.calPointToLineDis(normalPoint[i], sensorPointfit[j], sensorPointfit[j+1]) for j in range(len(sensorPointfit) - 1)]
        if round(min(dist), 8) < followdist or round(min(dist), 8) > followdist + precision:
            continue
        else:
            normalpointfilter.append(normalPoint[i])
    return normalpointfilter

def parallelsec(tangentslope, sensorPointfit,followdist, precision):
    '''
    :param tangentslope   (list): 拟合曲线的每个点的切线斜率
    :param sensorPointfit (list): 拟合数据
    :param followdist     (float):固定跟随距离
    :param precision      (float):固定跟随距离精度
    :return normalPointList (list): 将拟合曲线进行平移固定跟随距离后的曲线
    '''
    #获取拟合曲线进行平移固定跟随距离后的曲线
    normalPoint = getNormalPoint(tangentslope, sensorPointfit, followdist)
    ##对生成的曲线进行滤波处理
    normalpointfilter = filterpoint(normalPoint, sensorPointfit, followdist, precision)
    return normalpointfilter

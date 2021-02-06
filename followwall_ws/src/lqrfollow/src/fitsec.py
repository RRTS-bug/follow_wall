#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import rospy
import numpy as np
##求点到线段的距离公式
def calPointToLineDis(poi, poi1, poi2):
    cross = (poi2[0] - poi1[0]) * (poi[0] - poi1[0]) + (poi2[1] - poi1[1]) * (poi[1] - poi1[1])
    if (cross <= 0):
        return math.hypot((poi[0] - poi1[0]),(poi[1] - poi1[1]))
    d2 = (poi2[0] - poi1[0]) * (poi2[0] - poi1[0]) + (poi2[1] - poi1[1]) * (poi2[1] - poi1[1])
    if (cross >= d2):
        return math.hypot((poi[0] - poi2[0]),(poi[1] - poi2[1]))
    r = cross / d2
    px = poi1[0] + (poi2[0] - poi1[0]) * r
    py = poi1[1] + (poi2[1] - poi1[1]) * r
    return math.hypot((poi[0] - px) , (poi[1] - py))

##进行孤点滤波
#文档2.2(1)孤点滤波
def filterorphans(data, orphansNum, orphansdist):
    output = []
    for i in range(len(data)):
        count = 0
        s,e = max(i - 2 * orphansNum,0), min(i + 2 * orphansNum, len(data) - 1)
        for j in range(s,e,1):
            dist = math.hypot(data[i][0] - data[j][0], data[i][1] - data[j][1])
            if dist < orphansdist:
                count = count + 1
        if count >= orphansNum:
            output.append(data[i])
    return output

##对激光数据的纵坐标使用滑动窗求平均
##文档2.2(2)滑动窗滤波
def sidewindow(sensorPoint, sidewindowlen):
    ##定义滑动窗左右两端点，滑动窗向右滑动
    l, r = 0, sidewindowlen - 1
    sumlist = [[0, 0] for i in range(len(sensorPoint))]
    while r <= len(sensorPoint) - 1:
        ##滑动窗内求平均(文档2.2(2)滑动窗滤波步骤2)
        sumtemp = sum([sensorPoint[i][1] for i in range(l,r + 1)]) / (r - l + 1)
        for i in range(l, r + 1, 1):
            sumlist[i][0] = sumlist[i][0] + sumtemp
            sumlist[i][1] = sumlist[i][1] + 1
        ##如果滑动窗右端点有没有超出尾端，如果没有滑动窗向右移动一位
        if r <= len(sensorPoint) - 1:
            r = r + 1
            l = l + 1
            ##如果向右移动一位超出尾端，循环结束
            if r > len(sensorPoint) - 1:
                break
    ##当一个纵坐标位置都多个平均值时，对同一个纵坐标位置的多个平均值进行求平均(文档2.2(2)滑动窗滤波步骤3,4)
    sensorPointfilter = [[sensorPoint[i][0], sumlist[i][0] / sumlist[i][1]] for i in range(len(sumlist))]
    return sensorPointfilter

##直线分段拟合
##文档2.2(3)直线拟合
def segmentfit(fitThreshold, sensorPointfilter):
    ##存放拟合之后的数据和激光点所对应拟合直线斜率
    sensorPointfit = []
    tangentslope = []
    ##拟合直线的初始位置，s表示拟合区间的首端，e表示拟合区间的尾端(文档2.2(3)直线拟合步骤2)
    s, e = 0, len(sensorPointfilter) - 1
    while True:
        #求拟合区间直线斜率
        ##斜率角为90角，即slope等于无穷
        if sensorPointfilter[s][0] == sensorPointfilter[e][0]:
            slope = float('inf')
        ##斜率不等于90度角，求斜率和截距
        else:
            slope = (sensorPointfilter[e][1] - sensorPointfilter[s][1]) / (sensorPointfilter[e][0] - sensorPointfilter[s][0])
            b = sensorPointfilter[e][1] - sensorPointfilter[e][0] * slope
        ##求拟合区间内每个点到拟合直线的距离
        dist = [calPointToLineDis(sensorPointfilter[i], sensorPointfilter[e], sensorPointfilter[s]) for i in range(s, e + 1, 1)]
        ##如果距离最大值小于阈值，拟合成功，在首尾两点之间进行插值
        if max(dist) < fitThreshold:
            if slope == float('inf'):
                temp = (sensorPointfilter[e][1] - sensorPointfilter[s][1]) / (e - s)
                ##拟合成功步骤4
                for i in range(0, e - s + 1, 1):
                    x = sensorPointfilter[s][0]
                    y = sensorPointfilter[s][1] + i * temp
                    sensorPointfit.append([x, y])
                    tangentslope.append(slope)
            else:
                temp = (sensorPointfilter[e][0] - sensorPointfilter[s][0]) / (e - s)
                for i in range(0, e - s + 1, 1):
                    x = sensorPointfilter[s][0] + i * temp
                    y = x * slope + b
                    sensorPointfit.append([x, y])
                    tangentslope.append(slope)
            if e >= len(sensorPointfilter) - 2:#文档2.2(3)直线拟合步骤3
                break
            else:
                s = e + 1
                e = len(sensorPointfilter) - 1
        ##如果最大值大于阈值，直线拟合没有成功，尾端直接跳到距离最大值处
        else:
            e = s + dist.index(max(dist))
    return sensorPointfit, tangentslope

def fitsec(sensorPoint, sidewindowlen, orphansNum, orphansdist, fitThreshold, followside):
    """
    :param sensorPoint   (list):  原始传感器数据
    :param sidewindowlen (int):   滑动窗宽度
    :param fitThreshold  (float): 直线拟合阈值
    :param followside    (int):   移动机器人跟随的左侧或者右侧墙，0为右侧，1为左侧
    :return sensroPointfit, tangentslope (list):  直线拟合后的数据和斜率
    """
    ##如果1：表示跟随左侧墙，激光扫描默认逆时针从-179到180,如果跟随左侧，数据需要反转以下
    if followside == 1:
        datatest = list(reversed(sensorPoint))
    ##如果0：表示跟随右侧墙
    else:
        datatest = sensorPoint
    ##将数据通过滑动窗进行降噪
    datatest = filterorphans(datatest ,orphansNum, orphansdist)
    sensorPointfilter = sidewindow(datatest, sidewindowlen)
    ##进行直线分段拟合，并得出拟合后每个点的斜率
    sensorPointfit, tangentslope = segmentfit(fitThreshold, sensorPointfilter)
    return sensorPointfit, tangentslope

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:45:25 2016

@author: ccl
"""
classNums = 2
import numpy
from math import log
import operator
import loadTrainData
import loadDataSet
vis = [{}, {}, {}]
def getH(dataSet):#得到制定数据集的信息熵
    total = len(dataSet)
    classCounts = {}
    for data in dataSet:
        dataClass = data[-1]
        if not classCounts.has_key(dataClass):
            classCounts[dataClass] = 0
        classCounts[dataClass] += 1

    H = 0.0
    for dataClass in classCounts:
        prob = float(classCounts[dataClass]) / total
        H -= (prob * log(prob, 2))
    return H
def initClass(dataSet):#从训练数据集中得到所有的特征切分点
    dataSetClass = []
    for i in range(classNums):
        dataSetClass.append([])
        for data in dataSet:
            dataSetClass[i].append(data[i])
    for i in range(classNums):
        dataSetClass[i] = list(set(dataSetClass[i]))
        dataSetClass[i].sort()
    return dataSetClass

def splitDataSet(dataSet, feature, value):#利用指定的特征及其切分点将数据切分成两部分数据子集
    subDataSet1 = []
    subDataSet2 = []
    for data in dataSet:
        rD = data[:feature]
        rD.extend(data[feature+1:])
        if data[feature] <= value:
            subDataSet1.append(rD)
        else:
            subDataSet2.append(rD)
    return subDataSet1, subDataSet2
def getBestFeature(dataSet, dataSetClass):#利用信息增益比求出最合适的切分点
    featuresNums = len(dataSetClass)
    hD = getH(dataSet)
    bestFeature = -1
    bestFeatureValue = 0.0
    bestGrDA= 0.0
    total = len(dataSet)
    for feature in range(featuresNums):
        for n in range(1, len(dataSetClass[feature])):
            featureValue = float((dataSetClass[feature][n]+dataSetClass[feature][n-1]))/2
            if vis[feature].has_key(featureValue):
                continue
            subDataSet1, subDataSet2 = splitDataSet(dataSet, feature, featureValue)
            if len(subDataSet1)==0 or len(subDataSet2) == 0:
                vis[feature][featureValue] = 1
                continue
            pA1 = float(len(subDataSet1))/total
            pA2 = float(len(subDataSet2))/total
            hDA = pA1*getH(subDataSet1)+pA2*getH(subDataSet2)
            gDA = hD - hDA
            gAD = -(pA1*log(pA1,2)+pA2*log(pA2,2))
            gRDA = gDA / gAD
            if gRDA > bestGrDA:
                bestGrDA = gRDA
                bestFeature = feature
                bestFeatureValue = featureValue
    vis[bestFeature][bestFeatureValue] = 1
    return bestFeature, bestFeatureValue
def getMaxClass(classList):#得到一个集合中占据大多数的信息的类别
    classCounts = {}
    for dataClass in classList:
        if not classCounts.has_key(dataClass):
            classCounts[dataClass] = 0
        classCounts[dataClass] += 1
    sortedClassCount = sorted(classCounts.iteritems(),
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def one(dataSetClass):#判断信息集中是否只有一个类别
    l = 0
    for dataS in dataSetClass:
        l += len(dataS)
    return l <= 1
def decisionTree(dataSet, dataSetClass, labels):#创建决策树
    classList = [data[-1] for data in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if one(dataSetClass):
        return getMaxClass(classList)
 
    bestFeature, bestFeatureValue = getBestFeature(dataSet, dataSetClass)
    bestFTLabel = labels[bestFeature]
    tree = []
    subDataSet1, subDataSet2 = splitDataSet(dataSet, bestFeature, bestFeatureValue)
    if len(subDataSet1) != 0 and len(subDataSet2) != 0:
        tree = [bestFTLabel, bestFeatureValue, [], []]
        tree[2] = decisionTree(subDataSet1, dataSetClass, labels)
        tree[3] = decisionTree(subDataSet2, dataSetClass, labels)
        if tree[2] == tree[3]:
            tree = tree[2]
    else:
        return getMaxClass(classList)
    return tree
def getPos(p):#得到制定特征的编号
    return int(p)
def getRealDataClass(data, tree):#根据决策树对指定的数据进行分类
    if len(tree) == 1:
        return tree[0];
    p = getPos(tree[0])
    left = []
    if isinstance(tree[2], list):
        left = tree[2]
    else:
        left = [tree[2]]
    right = []
    if isinstance(tree[3], list):
        right = tree[3]
    else:
        right = [tree[3]]
    if data[p] <= tree[1]:
        return getRealDataClass(data, left)
    else:
        return getRealDataClass(data, right)
    

def createDataSet():
    dataSet = loadTrainData.getTrainData()
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    return dataSet, labels
def main():
    dataSet, labels = createDataSet()
    dataSetClass = initClass(dataSet)
    tree = decisionTree(dataSet, dataSetClass, labels)
    allData = loadDataSet.finalData()
    res = []
    for i in range(len(allData)):
        res.append(getRealDataClass(allData[i], tree))
if __name__ == '__main__':
    main()
    

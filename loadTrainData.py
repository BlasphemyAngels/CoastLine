# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 20:11:14 2016

@author: ccl
"""
import struct
import loadDataSet
import numpy as np
seaSamples = 654
seaLines   = 299
landSamples = 435
landLines   = 485
bands   = 4
def getSeaData():
    dataSet = np.zeros((seaLines,seaSamples, bands))
    f = open('data/sea.dat', 'rb')
    data = f.read()
    n = 0
    for i in range(bands):
        for j in range(seaLines):
            for k in range(seaSamples):
                num = data[n]+data[n+1]
                n += 2
                num, = struct.unpack('H', num)
                dataSet[j][k][i] = num
    f.close();
    return dataSet    
    
def getLandData():
    dataSet = np.zeros((landLines,landSamples, bands))
    f = open('data/land.dat', 'rb')
    data = f.read()
    n = 0
    for i in range(bands):
        for j in range(landLines):
            for k in range(landSamples):
                num = data[n]+data[n+1]
                n += 2
                num, = struct.unpack('H', num)
                dataSet[j][k][i] = num
    f.close();
    return dataSet
    
def finalSeaData(seaDataSet):
    grayImg = loadDataSet.getGrayImg(seaDataSet)
    lbp = loadDataSet.getLBP(grayImg)
    dataSet = []
    for i in range(1, seaLines-1):
        for j in range(1, seaSamples-1):
            dataSet.append([])
    p = 0
    for i in range(1, seaLines-1):
        for j in range(1, seaSamples-1):
            dataSet[p].append(seaDataSet[i][j][0])
            dataSet[p].append(seaDataSet[i][j][1])
            dataSet[p].append(seaDataSet[i][j][2])
            dataSet[p].append(seaDataSet[i][j][3])
            for u in range(bands):
                for v in range(u+1, bands):
                    dataSet[p].append(seaDataSet[i][j][v]-seaDataSet[i][j][u])
            dataSet[p].append(lbp[i][j])
            dataSet[p].append(0)
            p += 1
    return dataSet
    
def finalLandData(landDataSet):
    grayImg = loadDataSet.getGrayImg(landDataSet)
    lbp = loadDataSet.getLBP(grayImg)
    dataSet = []
    for i in range(1, landLines-1):
        for j in range(1, landSamples-1):
            dataSet.append([])
    p = 0
    for i in range(1, landLines-1):
        for j in range(1, landSamples-1):
            dataSet[p].append(landDataSet[i][j][0])
            dataSet[p].append(landDataSet[i][j][1])
            dataSet[p].append(landDataSet[i][j][2])
            dataSet[p].append(landDataSet[i][j][3])
            for u in range(bands):
                for v in range(u+1, bands):
                    dataSet[p].append(landDataSet[i][j][v]-landDataSet[i][j][u])
            dataSet[p].append(lbp[i][j])
            dataSet[p].append(1)
            p += 1
    return dataSet
def getTrainData():
    seaDataSet = getSeaData()
    print np.shape(seaDataSet)
    landDataSet = getLandData()
    seaData = finalSeaData(seaDataSet)
    landData = finalLandData(landDataSet)
    return seaData + landData
def main():
    data = getTrainData()
    loadDataSet.store('train.txt', data)
if __name__ == '__main__':
    main()
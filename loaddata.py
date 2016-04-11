# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:29:34 2016

@author: ccl
"""
from numpy import *
samples = 654
lines   = 299
seaSamples = 654
seaLines   = 299
seaBands   = 4
landSamples = 435
landLines   = 485
landBands   = 4
import struct
def loadData():
    seaDataSet = []
    graySea = []
    for i in range(seaLines*seaSamples):
        seaDataSet.append([])
    f = open('data/sea.dat', 'rb')
    n = 0
    data = f.read()
    f.close()
    for k in range(seaBands):
        for i in range(seaLines):
            for j in range(seaSamples):
                d = data[n]+data[n+1]
                n += 2
                d, = struct.unpack('H', d)
                seaDataSet[i*seaSamples+j].append(d)
    for i in range(seaLines):
        for j in range(seaSamples):
            
    landDataSet = []
    for i in range(landLines*landSamples):
        landDataSet.append([])
    f = open('data/land.dat', 'rb')
    n = 0
    data = f.read()
    f.close()
    for k in range(landBands):
        for i in range(landLines):
            for j in range(landSamples):
                d = data[n]+data[n+1]
                n += 2
                d, = struct.unpack('H', d)
                landDataSet[i*landSamples+j].append(d)
    dataSet = seaDataSet + landDataSet
    return dataSet
def getGrayImg(dataSet):
    grayImg = []
    m = shape(dataSet)[0]
    for i in range(m):
        
def initDataSet(dataSet):
    m = shape(dataSet)[0]
    n = shape(dataSet)[1]
    for i in range(m):
        for j in range(n):
            for k in range(j+1, n):
                dataSet[i].append(dataSet[i, k] - dataSet[i, j])
def main():
    dataSet = loadData()
if __name__ == '__main__':
    main()

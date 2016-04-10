# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:29:34 2016

@author: ccl
"""
seaSamples = 654
seaLines   = 299
seaBands   = 4
landSamples = 435
landLines   = 485
landBands   = 4
import struct
def loadData():
    seaDataSet = []
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
def main():
    dataSet = loadData()
if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 19:58:44 2016

@author: ccl
"""
import numpy
import struct
samples = 1996
lines   = 1125
bands   = 4
def loadData(fileName):
    dataSet = numpy.zeros((lines,samples, bands))
    f = open(fileName, 'rb')
    data = f.read()
    n = 0
    for i in range(bands):
        for j in range(lines):
            for k in range(samples):
                num = data[n]+data[n+1]
                n += 2
                num, = struct.unpack('H', num)
                dataSet[j][k][i] = num
    f.close();
    return dataSet

def getGrayImg(dataSet):
    m = numpy.shape(dataSet)[0]
    n = numpy.shape(dataSet)[1]
    grayImg = numpy.zeros((m, n))
    for i in range(m):
        for j in range(n):
            grayImg[i][j] = (dataSet[i][j][3]*30+dataSet[i][j][2]*59+dataSet[i][j][1]*11)/100
    return grayImg

def getLBP(grayImg):
    m = numpy.shape(grayImg)[0]
    n = numpy.shape(grayImg)[1]
    lbp = numpy.zeros((m, n))
    for i in range(1, m-1):
        for j in range(1, n-1):
            center = grayImg[i][j]
            code = 0
            code |= (grayImg[i-1][j-1]>=center)<<7
            code |= (grayImg[i-1][j]>=center)<<6
            code |= (grayImg[i-1][j+1]>=center)<<5
            code |= (grayImg[i][j+1]>=center)<<4
            code |= (grayImg[i+1][j+1]>=center)<<3
            code |= (grayImg[i+1][j]>=center)<<2
            code |= (grayImg[i+1][j-1]>=center)<<1
            code |= (grayImg[i][j-1]>=center)<<0
            lbp[i][j] = code
    return lbp

def finalData(dataSet, lbp):
    m = numpy.shape(dataSet)[0]
    n = numpy.shape(dataSet)[1]
    b = numpy.shape(dataSet)[2]
    p = 0
    data = []
    for i in range(1, m-1):
        for j in range(1, n-1):
            data.append([])
    for i in range(1, m-1):
        for j in range(1, n-1):
            data[p].append(dataSet[i][j][0])
            data[p].append(dataSet[i][j][1])
            data[p].append(dataSet[i][j][2])
            data[p].append(dataSet[i][j][3])
            for u in range(b):
                for v in range(u+1, b):
                    data[p].append(dataSet[i][j][v]-dataSet[i][j][u])
            data[p].append(lbp[i][j])
            p += 1
    return data
def store(fileName, data):
    f = open(fileName, 'w')
    m = numpy.shape(data)[0]
    n = numpy.shape(data)[1]
    for i in range(m):
        line = str('')
        for j in range(n):
            if j != 0:
                line += ' '
            line += str(data[i][j])
        f.write(line+'\n')
    f.close()
def main():
    dataSet = loadData('data3.data3')
    grayImg = getGrayImg(dataSet)
    lbp = getLBP(grayImg)
    data = finalData(dataSet, lbp)
    store('alldata.txt', data)
if __name__ == "__main__":
    main()
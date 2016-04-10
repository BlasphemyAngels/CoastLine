# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:29:34 2016

@author: ccl
"""
seaSamples = 654
seaLines   = 299
seaBands   = 4
import struct
def loadData(fileName):
    seaDataSet = []
    for i in range(seaLines*seaSamples):
        seaDataSet.append([])
    f = open(fileName, 'rb')
    n = 0
    data = f.read()
    for k in range(seaBands):
        for i in range(seaLines):
            for j in range(seaSamples):
                d = data[n]+data[n+1]
                n += 2
                d = struct.unpack('H', d)
                
    f.close()
def main():
    loadData('data/sea.dat')
if __name__ == '__main__':
    main()
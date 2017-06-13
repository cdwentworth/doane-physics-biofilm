#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to calculate the average roughness as a function of time of the two-dimensional 
film using simulation data.

Date: 6/5/2017 7:55

@author: Karee Hustedde
@author: Chris Wentworth

"""
import matplotlib.pylab as plt
import numpy as np
import os
import re
from xml.etree import ElementTree as ET
import zipfile as zf

def extractDataFromXML(fileLoc):
    if '.xml' not in fileLoc:
        fileLoc += ".xml"
    tree = ET.parse(fileLoc)
    species = tree.find(".//species[@name='MyPA01']")
    speciesText = species.text
    speciesNames = species.attrib['header']
    speciesNames = speciesNames.split(',')
    grid = tree.find(".//grid")
    resolution = float(grid.attrib['resolution'])
    nI = int(grid.attrib['nI'])
    nJ = int(grid.attrib['nJ'])
    nK = int(grid.attrib['nK'])
    partArray = speciesText.split(';')
    partArray2 = []
    for p in partArray:
        partArray2.append(p.replace('\n',''))
    partArray = partArray2
    partArray.remove('')  
    numCells = len(partArray)
    numDataTypes = len(speciesNames)
    pArray = np.zeros((numCells,numDataTypes))
    for ci in range(numCells):
        npa = np.fromstring(partArray[ci],sep=',')
        pArray[ci]=npa        
    return pArray,nI,nJ,nK,resolution
def findAve(pArray,resolution):
    # Extract (x,y,z) coordinates of cells
    xlist = []
    ylist = []
    zlist = []
    l = 0
    for l in pArray:
        xlist.append(l[9])
        ylist.append(l[10])
        zlist.append(l[11])
    
    # truncate the y-coordiate
    for i in range(len(ylist)):
        ylist[i] = float(int(ylist[i]))
    
    # create numpy array from (y,x) coordinate lists and sort by y value
    yxCells = np.column_stack([ylist,xlist])
    yxCells = yxCells[yxCells[:,0].argsort()]
    
    # find the largest x for each y value
    yThickness = []
    maxy = resolution * nJ
    numCells = len(pArray)
    
    for yi in range(int(maxy)):
        yi1 = findy1(yxCells,yi,numCells)
        if yi1 >= 0:
            yi2 = findy2(yxCells,yi1,numCells)
            if yi2 >=yi1:
                equalyList = getEqualy(yxCells,yi1,yi2)
            else:
                equalyList = [yxCells[yi1,1]]
            xMax = max(equalyList)
            yThickness.append([yi,xMax])
        else:
            yThickness.append([yi,0])
            
    y,x = zip(*yThickness)
    #Vaeriables and calculations for finding the roughness coefficient
    
    Lf = np.mean(x)
    N = len(y)
    Ra = 0
    for r in x:
        a = np.abs(r-Lf)/(Lf)
        Ra = Ra + a
    AveRC = Ra / N
    
        
    y = yxCells[:,0]
    x = yxCells[:,1]
    return AveRC
def findy1(yxCells,yi,numCells):
    """
    This function finds the first row number (or cell number) in the array 
    yxCells for which the y coordinate of the cell is equal to yi.

    """
    yit = 0
    found = False
    while (not found) and (yit<numCells):
        if int(yxCells[yit,0]) == yi:
            found = True
        else:
            yit = yit + 1
    if found:
        y1 = yit
    else:
        y1 = -1
    return y1

def findy2(yxCells,yi1,numCells):
    """
    This function finds the second row number (or cell number) in the array 
    yxCells for which the y coordinate of the cell is equal to yxCells[yi1,0].

    """
    y = yxCells[yi1,0]
    yit = yi1 + 1
    found = True
    while (found) and (yit<numCells):
        if int(yxCells[yit,0]) != y:
            found = False
        else:
            yit = yit + 1
    if not found:
        y2 = yit - 1
    else:
        y2 = -1
    return y2

def getEqualy(yxCells,yi1,yi2):
    equalyList = []
    if yi2 >= 0:
        for i in range(yi1,yi2+1):
            equalyList.append(yxCells[i,1])
    return equalyList

# Main program
fileLoc = 'agent_State.zip'
arc = zf.ZipFile(fileLoc,'r')
arc.extractall()
recordNames = arc.namelist()
recordNames.reverse()
AveRCArray = []
timeArray = []
for f in recordNames:
    pArray,nI,nJ,nK,resolution=extractDataFromXML(f)
    AveRC = findAve(pArray,resolution)
    AveRCArray.append(AveRC)
    m = re.search('\((.+?)\)',f)
    t = int(m.group(1))
    timeArray.append(t)
for f in recordNames:
    os.remove(f)

plt.plot(timeArray, AveRCArray)
plt.xlabel('Time\nHours')
plt.ylabel(' Roughness\nCoefficient')
plt.grid(True)

plt.draw()
plt.show()   

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to calculate surface area to volume ratio of the two-dimensional film 
using simulation data.
Based on work done by Nathan Little.

Date: 6/12/2017 9:41

@author: Karee Hustedde
@author: Chris Wentworth

"""
import numpy as np
from xml.etree import ElementTree as ET

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

def loci(name,fileName):
    xlist = []
    ylist = []
    zlist = []
    # Extract the cell data from the agent_State xml file

    #This section uses the xml output to make arrays
    tree = ET.parse(fileName)
    species = tree.find(".//species[@name='"+name+"']")
    speciesText = species.text
    speciesNames = species.attrib['header']
    speciesNames = speciesNames.split(',')
    grid = tree.find(".//grid")
    resolution = float(grid.attrib['resolution'])
#    nI = int(grid.attrib['nI'])
    nJ = int(grid.attrib['nJ'])
#    nK = int(grid.attrib['nK'])
    partArray = speciesText.split(';')
    partArray.pop()
    numCells = len(partArray)
#    ###
#    testFile.write('length of partArray=' +str(numCells)+'\n')
#    for p in partArray:
#        testFile.writelines(p)
#    ###
    partArray2 = []
    for p in partArray:
        partArray2.append(p.replace('\n',''))
#    ###
#    testFile.write('\npartArray2:\n')
#    for p in partArray2:
#        testFile.write(p)
#        testFile.write('\n')
#    ###
    partArray = partArray2 
    numDataTypes = len(speciesNames)
    pArray = np.zeros((numCells,numDataTypes))
    for ci in range(numCells):
        npa = np.fromstring(partArray[ci],sep=',')
        pArray[ci]=npa
            
    # Extract (x,y,z) coordinates of cells
    locXi = speciesNames.index('locationX')
    locYi = speciesNames.index('locationY')
    locZi = speciesNames.index('locationZ')
            
    #Finding values for x, y, and Z in the xml file
#    data = 0
    for data in pArray:
        x = data[locXi]
        xlist.append(x)
        y = data[locYi]
        ylist.append(y)
        z = data[locZi]
        zlist.append(z)
                
    return (xlist,ylist,zlist,resolution, nJ,numCells)

# Main Program
testFile = open('testFile.txt','w')
fileName = 'agent_State(2).xml'
name = 'MyPA01'
(xlist,ylist,zlist,resolution, nJ,numCells) = loci(name,fileName) 
       
# truncate the y-coordiate
for i in range(len(ylist)):
    ylist[i] = float(int(ylist[i]))

# create numpy array from (y,x) coordinate lists and sort by y value
yxCells = np.column_stack([ylist,xlist])
yxCells = yxCells[yxCells[:,0].argsort()]

# find the largest x for each y value
yThickness = []
maxy = resolution * nJ

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
surfaceArea = 0
for s in x:
    if s != 0.0:
        surfaceArea = surfaceArea + 1
surfaceArea = float(surfaceArea)
volume = len(xlist)
ratio = surfaceArea/volume
print('\nSurface Area to Volume Ratio:',ratio)
testFile.close()
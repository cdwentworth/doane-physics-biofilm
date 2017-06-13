#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to calculate the average roughness of the two-dimensional film using 
simulation data.
Based on work done by Nathan Little.

Date: 6/2/2017 7:55

@author: Karee Hustedde
@author: Chris Wentworth

"""
import matplotlib.pylab as plt
import numpy as np
from xml.etree import ElementTree as ET
from time import sleep

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

# Extract the cell data from the agent_State xml file
flag = False
while flag is False:
    fileLoc = input("Please input the exact name of the xml file to be examined then press enter."
          +"\nNote: the xml file must be in the same folder as this script.\n")

    if '.xml' not in fileLoc:
        fileLoc += ".xml"
        
    try :
        #This section uses the xml output to make arrays
        tree = ET.parse(fileLoc)
        species = tree.find(".//species[@name='MyHeterotroph']")
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
        flag = True
    except IOError:
        print("There was an error accessing the file please try again.\n")
        sleep(0.2)
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



# plot the film thickness
y,x = zip(*yThickness)
plt.plot(y,x,linestyle='',marker='d',markersize=6.0)

#y = yxCells[:,0]
#x = yxCells[:,1]
#plt.plot(y,x,linestyle='',marker='d',markersize=4.0)
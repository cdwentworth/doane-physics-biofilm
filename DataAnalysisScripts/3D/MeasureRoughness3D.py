#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to calculate the average roughness of the three-dimensional film using 
simulation data.

Date: 6/7/2017 7:55

@author: Karee Hustedde
@author: Chris Wentworth

"""
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import roughnessCoefficientLibrary as rcl

outFile = open('TestData.txt','w')

# Extract the cell data from the agent_State xml file


fileName = 'agent_State(24).xml'
speciesName = 'MyPA01'
pArray, speciesNames, numCells = rcl.getSpeciesData(fileName,speciesName)
resolution,nI,nJ,nK = rcl.getGridData(fileName)

# Extract (x,y,z) coordinates of cells
xlist = []
ylist = []
zlist = []
l = 0
locXi = speciesNames.index('locationX')
locYi = speciesNames.index('locationY')
locZi = speciesNames.index('locationZ')
for l in pArray:
    xlist.append(l[locXi])
    ylist.append(l[locYi])
    zlist.append(l[locZi])

# truncate the y,z-coordinates
for i in range(numCells):
    ylist[i] = float(int(ylist[i]))
    zlist[i] = float(int(zlist[i]))
    
# create numpy array from (y,z,x) coordinate lists
yzxCells = np.column_stack([ylist,zlist,xlist])

# sort the yzxCells array by z value
yzxCells = yzxCells[yzxCells[:,1].argsort()]

###
outFile.write('yzxCells:\n')
for i in range(numCells):
    s = str(yzxCells[i,:])+'\n'
    outFile.write(s)
###
# for each unique z value, pull out the cells with that z-value and
# put them in a numpy array, yxCells and then find the largest x value
# for each y value

yzThickness=[]
maxy = nJ*resolution
maxz = nK*resolution
for zi in range(int(maxz)):
    z1 = rcl.findz1(yzxCells,zi)
    z2 = rcl.findz2(yzxCells,z1)
    yxCells = rcl.getEqualz(yzxCells,z1,z2)
    for yi in range(int(maxy)):
        yi1 = rcl.findy1(yxCells,yi)
        if yi1 >= 0:
            yi2 = rcl.findy2(yxCells,yi1)
            if yi2 >=yi1:
                equalyList = rcl.getEqualy(yxCells,yi1,yi2)
            else:
                equalyList = [yxCells[yi1,1]]
            xMax = max(equalyList)
            yzThickness.append([yi,zi,xMax])
        else:
            yzThickness.append([yi,zi,0])


###
outFile.write('\nyzThickness:\n')
for c in yzThickness:
    s = str(c)+'\n'
    outFile.write(s)
###

outFile.close()
###
# Create a 3d scatter plot of the film thickness
numPoints = len(yzThickness)
points = np.zeros([numPoints,3])
for n in range(numPoints):
    points[n,0]=yzThickness[n][0]
    points[n,1]=yzThickness[n][1]
    points[n,2]=yzThickness[n][2]
fig = plt.figure()
ax = fig.gca(projection = '3d')
ax.set_xlabel('y axis')
ax.set_ylabel('z axis')
ax.set_zlabel('x axis')
ax.scatter(points[:, 0], points[:, 1], points[:, 2],color='m')
plt.show()
###

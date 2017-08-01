#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Roughness Coefficient Library
Date: 6/12/2017

@author: Karee Hustedde
@author: Chris Wentworth
"""
import numpy as np
from xml.etree import ElementTree as ET
def findy1(yxCells,yi):
    '''
    This function finds the first row number (or cell number) in the array 
    yxCells for which the y coordinate of the cell is equal to yi.

    '''
    if len(yxCells.shape)>0:
        numyCells = yxCells.shape[0]
    else:
        numyCells = 0
    yit = 0
    found = False
    while (not found) and (yit<numyCells):
        if int(yxCells[yit,0]) == yi:
            found = True
        else:
            yit = yit + 1
    if found:
        y1 = yit
    else:
        y1 = -1
    return y1

def findy2(yxCells,yi1):
    '''
    This function finds the second row number (or cell number) in the array 
    yxCells for which the y coordinate of the cell is equal to yxCells[yi1,0].

    '''
    if len(yxCells.shape)>0:
        numCells = yxCells.shape[0]
        y = yxCells[yi1,0]
    else:
        numCells = 0
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

def findz1(yzxCells,zi):
    '''
    This function finds the first row number (or cell number) in the array 
    yzxCells for which the z coordinate of the cell is equal to zi.

    '''
    numCells = yzxCells.shape[0]
    zit = 0
    found = False
    while (not found) and (zit<numCells):
        if int(yzxCells[zit,1]) == zi:
            found = True
        else:
            zit = zit + 1
    if found:
        z1 = zit
    else:
        z1 = -1
    return z1

def findz2(yzxCells,zi1):
    '''
    This function finds the last row number (or cell number) in the array 
    yzxCells for which the z coordinate of the cell is equal to yzxCells[zi1,1].

    '''
    if zi1>=0:
        numCells = yzxCells.shape[0]
        z = yzxCells[zi1,1]
        zit = zi1 + 1
        found = True
        while (found) and (zit<numCells):
            if int(yzxCells[zit,1]) != z:
                found = False
            else:
                zit = zit + 1
        if (not found) or (zit==numCells):
            z2 = zit - 1
        else:
            z2 = zi1
    else:
        z2 = -1
    return z2

def getEqualy(yxCells,yi1,yi2):
    equalyList = []
    if yi2 >= 0:
        for i in range(yi1,yi2+1):
            equalyList.append(yxCells[i,1])
    return equalyList

def getEqualz(yzxCells,zi1,zi2):
    '''
    This function pulls out the y/x-coordinates for the cells with the
    same z coordinate referenced by yzxCells[zi1,1].  It returns a list
    of [y,x] coordinates for those cells.
    '''
    if (zi1<0):
        yxCells = np.empty([])
        return yxCells
    ylist = []
    xlist = []
    if zi2 >= 0:
        for i in range(zi1,zi2+1):
            ylist.append(yzxCells[i,0])
            xlist.append(yzxCells[i,2])
        yxCells = np.column_stack([ylist,xlist])
    return yxCells

def getGridData(fileName):
    tree = ET.parse(fileName)
    grid = tree.find(".//grid")
    resolution = float(grid.attrib['resolution'])
    nI = int(grid.attrib['nI'])
    nJ = int(grid.attrib['nJ'])
    nK = int(grid.attrib['nK'])    
    return resolution, nI,nJ,nK

def getSimulationData(fileName):
    tree = ET.parse(fileName)   
    simulation = tree.find(".//simulation")
    time = float(simulation.attrib['time'])
    return time

def getSpeciesData(fileName,speciesName):
    '''
    This function reads the text data corresponding to the species
    given in speciesName from the agent_State xml file.
    '''
   #This section uses the xml output to make arrays
    tree = ET.parse(fileName)
    s=".//species[@name='"+speciesName+"']"
    species = tree.find(s)
    speciesText = species.text
    speciesNames = species.attrib['header']
    speciesNames = speciesNames.split(',')
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
    return pArray, speciesNames, numCells
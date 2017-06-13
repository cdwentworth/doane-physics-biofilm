"""
Script to make a 3d contour plot of the eps particles from the simulation.
Original code taken from: http://matplotlib.org/examples/mplot3d/contourf3d_demo2.html
   
Nathan L.
6/25/13
"""

from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from xml.etree import ElementTree as ET
import numpy as np
from time import sleep

flag = False
while flag is False:
    fileLoc = raw_input("Please input the exact name of the xml file to be examined then press enter."
          +"\nNote: the xml file must be in the same folder as this script.\n")

    if '.xml' not in fileLoc:
        fileLoc += ".xml"

    try :
        #This section uses the xml output to make arrays
        tree = ET.parse(fileLoc)
        species = tree.find(".//species[@name='MyHeterotrophEPS']")
        names = species.attrib['header']
        epsArray = np.genfromtxt((line.rstrip(';') for line in species.text.splitlines()), 
            delimiter=',', names=names)
        flag = True
    except IOError:
        print("There was an error accessing the file please try again.\n")
        sleep(0.2)

#Using lists to avoid creating thousands of arrays
xlist = []
ylist = []
zlist = []
l = 0
while l < len(epsArray):
    m = 9
    xlist.append(epsArray[l][m])
    m += 1
    ylist.append(epsArray[l][m])
    m += 1
    zlist.append(epsArray[l][m])
    l += 1

X = np.array(xlist)
Y = np.array(ylist)
Z = np.array(zlist)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(Z, Y, X, cmap=cm.jet, linewidth=0.1)

ax.set_xlabel('Z')
ax.set_ylabel('Y')
ax.set_zlabel('X')

plt.show()


'''
Script to make 2D contour plot of the eps particles from the simulation.
Basis code taken from http://matplotlib.org/examples/pylab_examples/contourf_log.html
and other examples

Nathan L.
6/25/13
'''

from matplotlib import pyplot as plt
import numpy as np
from numpy import ma
from matplotlib import colors, ticker, cm
from xml.etree import ElementTree as ET
from scipy.interpolate import griddata
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

x = np.array(xlist)
y = np.array(ylist)
z = np.array(zlist)

del(xlist)
del(ylist)
del(zlist)

hiZ = 0.0
hiY = 0.0

for tempZ in z:
	if tempZ > hiZ:
		hiZ = tempZ

for tempY in y:
	if tempY > hiY:
		hiY = tempY


shift = 0.9
xi = np.linspace(0,hiZ,len(z)*shift)
yi = np.linspace(0,hiY,len(y)*shift)  

# Grid the data
# Note: using method='nearest' causes a MemoryError
zi = griddata((z,y), x,(xi[None,:],yi[:,None]), method='linear')

# This method can raise a MemoryError
cs = plt.contourf(xi, yi, zi, locator=ticker.AutoLocator(), cmap=cm.PuBu_r)

cbar = plt.colorbar()

# Plot data points
#plt.scatter(z,y,marker='o',c='b',s=5)

plt.xlim(-1,hiZ+1)
plt.ylim(-1,hiY+1)
plt.show()


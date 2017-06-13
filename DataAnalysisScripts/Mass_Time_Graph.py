'''
Script to create a mass/time graph for the sum of the mass of every eps
    particle at each iteration.

6/25/13
Nathan L.
'''
from xml.etree import ElementTree as ET
import matplotlib.pylab as plt
import zipfile as zf
#from os import *
import os

massSums = []
flag = False
fileLoc = 'agent_Sum.zip'
arc = zf.ZipFile(fileLoc,'r')
arc.extractall()
recordNames = arc.namelist()

for f in recordNames:
    tree = ET.parse(f)
    species = tree.find(".//species[@name='MyPA01']")
    line = species.text.split(',')
    m = float(line[1])
    sim = tree.find(".//simulation")
    t = sim.attrib['time']
    t = float(t)
    massSums.append([t,m])

#Dangerous if there are copies of the records stored in the same directory as this script
for f in recordNames:
    os.remove(f)

t,m = zip(*massSums)
plt.plot(t,m,linestyle='',marker='d',markersize=2)
plt.xlabel('Time\nHours')
plt.ylabel('Mass\nmicrograms')
plt.grid(True)

plt.draw()
plt.show()

'''
Script to create a mass/time graph for the sum of the mass of every eps
    particle at each iteration.

6/25/13
Nathan L.
'''
from xml.etree import ElementTree as ET
from pylab import *
from zipfile import *
from os import *
from time import sleep

epsSums = []
flag = False
#fileLoc = "\\Users\\Nathan\\Dropbox\\2013 Summer Research Project\\Sample Output\\agent_Sum.zip"

while flag is False:
    fileLoc = raw_input("Please input the exact name of the zip file to be processed then press enter."
          +"\nNote: the zip file must be in the same folder as this script.\n")

    if '.zip' not in fileLoc:
        fileLoc += ".zip"

    try :
        arc = ZipFile(fileLoc,'r')

        arc.extractall()
        recordNames = arc.namelist()
        flag = True
    except IOError:
        print("There was an error accessing the file please try again.\n")
        sleep(0.2)


for f in recordNames:
    tree = ET.parse(f)
    species = tree.find(".//species[@name='MyHeterotrophEPS']")
    line = species.text.split(',')
    #This line is not necessary, but could be useful later
    line[0] = line[0].strip('\n')
    #insert is used so that the data will be in the correct order
    epsSums.insert(0,line[1])

#Dangerous if there are copies of the records stored in the same directory as this script
for f in recordNames:
    remove(f)
    
plot(epsSums)
xticks(arange(0,len(recordNames),1))
xlabel('Time\nHours')
ylabel('EPS Mass\nunit?')
grid(True)

draw()
show()

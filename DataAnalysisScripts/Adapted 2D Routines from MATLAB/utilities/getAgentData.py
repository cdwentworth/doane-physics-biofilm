'''
 This script is designed to duplicate the MATLAB script of the same name.

 Nathan Little
 7/26/13
 '''
# Partially Converted
# Assume that any strange/nonfunctional code is copied until proven otherwise

# Waiting
#from getEnvData import *
from agentListToGrid import *
from unzipSelect import *
from xml.dom import minidom
import numpy as np
import os.path

def getAgentData(nFile,Type = 'State',skipeps = 0):
    '''This function is similar to the 'loadAgents' routine, but allows one to specify the data output kind.

    getAgentData(nFile,type,skipeps)
 
        nFile is the iterate number or 'last' for the last iterate
 
        type may be:
            'State' for separate data for each agent
 
            'Sum' for data summed by species type
 
            'Grid' to return a solute-sized grid with the agent
 			information copied to it (total biomass per species)
 
            'SplitGrid' to return a solute-sized grid with the agent
 			information split into active, inert, and EPS portions
 
        set skipeps to 1 to ignore any species with EPS or eps in their title

        Returns [adata,time]
  '''

    # default colors that are assigned to each species
    acolor = ('r','b','g','y','m','c','o','k')

    # make lowercase for easier string comparisons
    Type = Type.lower()

    dogrid = False
    dosplit = False
    if Type == 'grid' or Type == 'splitgrid' or Type == 'split':

        dogrid = True

        if Type == 'splitgrid':
            dosplit = True

        Type = 'state'

    if Type == 'state':
        Type = 'State'
        
    if Type == 'sum':
        Type='Sum'

    if nFile.isdigit():
        stateFile = str('agent_%s(%i).xml'%(Type,nFile))
    else:
        stateFile = str('agent_%s(%s).xml'%(Type,nFile))
        if nFile == 'last':
            stateFile = str('lastIter/agent_%s(last).xml'%Type)
        
    # decompress the file if needed
    if not os.path.isfile(stateFile):
        zipFile = str('agent_%s.zip'%Type)
        success = unzipSelect(zipFile,stateFile)

        if not success:
            print('Could not read file "%s"\n'%stateFile)
            print('or unzip it from "%s".\n'%zipFile)
            adata = 0
            time = -1
            return [adata,time]


    # now starts the reading in of XML data    
    xDoc = minidom.parse(stateFile)
    xRoot = xDoc.documentElement

    time = float(xRoot.getElementsByTagName('simulation').item(0).getAttribute('time'))

    grid = xRoot.getElementsByTagName('grid').item(0)
    if grid != []:
            res = float(xRoot.getElementsByTagName('grid').item(0).getAttribute('resolution'))
            nI = float(xRoot.getElementsByTagName('grid').item(0).getAttribute('nI'))
            nJ = float(xRoot.getElementsByTagName('grid').item(0).getAttribute('nJ'))
            nK = float(xRoot.getElementsByTagName('grid').item(0).getAttribute('nK'))
    else:
            # since we don't have the resolution or gridpoint numbers, get them from the solute file
            [s] = getEnvData(nFile)
            res = s(1,1).resolution
            nI = s(1,1).nI
            nJ = s(1,1).nJ
            nK = s(1,1).nK
            del s


    allSpecies = xDoc.getElementsByTagName('species')

    adata = empty((0,0))

    for iSpecies in range(0, allSpecies.getLength):
        speciesName = str(allSpecies.item(iSpecies-1).getAttribute('name'))

        if skipeps and length(strfind(lower(speciesName),'eps')) > 0:
            print('Skipping species %s.\n' % speciesName)
            # Need to 'continue' simulation, somehow
            

        # read the header but then create a record of which column holds
        # each data value
        header = char(allSpecies.item(iSpecies-1).getAttribute('header'))
        labels = regexp(header,'\w*','match')
        labelColumnMap = empty((0,0))
        for i in range(1,length(labels)):
            labelColumnMap = setfield(labelColumnMap,{1},labels[i],i)
            

        # read in the data values
        x = allSpecies.item(iSpecies-1).getFirstChild
        if !isempty(x):
            x = float(x.getData) #command was originally the more flexible 'str2num()'. Watch for problems.
        

        # setfield has been misbehaving in my testing
        adata[iSpecies][1].setfield(speciesName,'name')
        adata[iSpecies][1].setfield(acolor{iSpecies},'color')
        adata[iSpecies][1].setfield(res,'resolution')
        adata[iSpecies][1].setfield(nI,'nI')
        adata[iSpecies][1].setfield(nJ,'nJ')
        adata[iSpecies][1].setfield(nK,'nK')
        adata[iSpecies][1].setfield(labelColumnMap,'header')
        adata[iSpecies][1].setfield(x,'data')

    # when we want the data on a solute-style grid
    if dogrid:
        adata = agentListToGrid(adata,dosplit)
        
    return [adata,time]


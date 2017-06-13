'''
 This script is designed to duplicate the MATLAB script of the same name.
 Description taken from original.

 Judging by the TODO from the original MATLAB script
     and the fact that 'result' is hardcoded to equal 123456 in one instace
     this script may not be finished.

 Nathan Little
 7/22/13
 '''
# First-pass conversion
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

import numpy as np

def result = calcBiofilmData(agentData,theval):
    """result = calcBiofilmData(agentData,theval)

    the agentData structure array is a SOLUTE-STYLE grid of agent information

    perform calculations to find:
     'biomass': gives the total biomass field
     'area': gives the area covered by the biofilm
     'interface': returns a vector of highest interface point for
                   each y location
     'porosity': compares the space taken up by the biofilm total
                   compared to the agent sum
    """


    if strcmp(theval,'biomass')
        # calculate the biomass field: represents biofilm interior
        result = biomass(agentData);

    if strcmp(theval,'area')
        # calculate the area taken up by the biofilm
        result = bioarea(agentData);

    if strcmp(theval,'interface')
        # find the interface location for each horizontal position
        biofield = biomass(agentData);
        res = agentData(1,1).resolution;

        # y is horizontal, x is vertical
        ny = agentData(1,1).nJ;
        nx = agentData(1,1).nI;

        x = ((1:nx) - 0.5)*res;

        # find the interface location at each horizontal position
        result = zeros(ny,1);
            for j=1:ny
                    for ii=1:nx-1
                            i = nx-ii;
                if (biofield(i,j) > 0) && (biofield(i+1,j) == 0.0)
                    result(j) = x(i+1);
                    break;

    if strcmp(theval,'porosity')
        bfarea = bioarea(agentData);

        # now calculate area of the individual agents
        # TODO!!
        result = 123456;



######################################################################
# functions used many places
######################################################################

def result = biomass(adata)
    # create the biomass grid by summing all the biomass contours
    nspec = size(adata,1);
    ntype = size(adata,2);
    result = 0.*adata(1,1).data;
    for i=1:nspec
        for j=1:ntype
            result = result + adata(i,j).data;


########################################################################

def result = bioarea(adata)
    # calculate the area taken up by the biofilm

    # first get a simple grid containing the biomass data
    biofield = biomass(adata);
    res = adata(1,1).resolution;

    # y is horizontal, x is vertical
    ny = adata(1,1).nJ;
    nx = adata(1,1).nI;

    # only add the area that contains biomass
    result = 0;
    for i=1:nx
            for j=1:ny
                if biofield(i,j) > 0
                    result = result + res*res;

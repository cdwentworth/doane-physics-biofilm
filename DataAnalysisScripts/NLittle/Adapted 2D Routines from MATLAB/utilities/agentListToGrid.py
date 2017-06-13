'''
 This script is designed to duplicate the MATLAB script of the same name.
 Description taken from original.

 Nathan Little
 7/25/13
 '''
import numpy as np
# Untested
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

def agentListToGrid(adata,dosplit = False):
    """This function takes individual agent data and converts it to a grid.

    agentListToGrid(adata[,dosplit]) returns a grid

        adata is a numpy array
        dosplit is optional.
        set dosplit to True to split active, inert, and EPS portions"""    

    nspec = np.size(adata);
    ntype = 1;

    # get voxel volume (cube of the resolution)
    res = adata[1][1] #Can't figure out how to include 'resolution'
    vol = res**3

    # now copy new agent data in & create new 'agrid' fields
    agrid = np.zeros(adata.shape)
    for ispec in range(0,nspec):
        agrid[ispec][1]['name']       = adata[ispec]['name']
        agrid[ispec][1]['resolution'] = adata[1][1]['resolution']
        agrid[ispec][1]['nI']         = adata[1][1]['nI']
        agrid[ispec][1]['nJ']         = adata[1][1]['nJ']
        agrid[ispec][1]['nK']         = adata[1][1]['nK']
        agrid[ispec][1]['unit']       = 'g.L-1'; # THIS IS ASSUMED!!
        agrid[ispec][1]['data']       = np.zeros((adata[1][1]['nI'],adata[1][1]['nJ'],
                                                  adata[1][1]['nK']))
    

    if dosplit:
        for ispec in range(0,nspec):
            # iterate over each species and copy the data in each field so that
            # we have it in triplicate, with the spots to be replaced by active
            # biomass, inert biomass, and EPS
            agrid[ispec][2] = agrid[ispec][1]
            agrid[ispec][3] = agrid[ispec][1]

            # now modify the name of each component
            specname = adata[ispec].name
            agrid[ispec][1]['name'] = str('%s-biomass' % specname)
            agrid[ispec][2]['name'] = str('%s-inert' % specname)
            agrid[ispec][3]['name'] = str('%s-capsule' % specname)
        
    

    # now that we have the spots ready, iterate over agents and place the
    # data into the correct field data
    for ispec in range(0,nspec):

            # data locations for this species
            if 'locationX' in adata[ispec]['header']:
                    locx = adata[ispec]['header']['locationX']
                    locy = adata[ispec]['header']['locationY']
                    locz = adata[ispec]['header']['locationZ']
            else:
                    print('*** Using zero location for species %s. ***\n' % adata[ispec]['name'])
                    locx = 0;
                    locy = 0;
                    locz = 0;
            

            havebio = 'biomass' in adata[ispec]['header']
            if havebio:
                    locb = adata[ispec]['header']['biomass']

            havenrt = 'inert' in adata[ispec]['header]
            if havenrt:
                    loci = adata[ispec]['header']['inert']

            havecap = 'capsule' in adata[ispec]['header']
            if havecap:
                    locc = adata[ispec]['header']['capsule']

            # now iterate over all the agents in the structure and copy them to the grid
        for iagent in range(0, np.shape(adata[ispec]['data'])):
            drow = adata[ispec]['data'][iagent]

            # first get the location on the grid
            i = np.floor(drow[locx]/res)+1;
            j = np.floor(drow[locy]/res)+1;
            k = np.floor(drow[locz]/res)+1;

            # do the split method if needed
            # this portion also does not apply for plasmids
            if dosplit and havebio:
                # biomass portion
                agrid[ispec][1]['data'][i,j,k] = agrid[ispec][1]['data'][i,j,k] + drow[locb]/vol;
            
                # only add inert mass if we actually have it
                    if havenrt:
                        # inert biomass portion
                        agrid[ispec][2]['data'][i,j,k] = agrid[ispec][2]['data'][i,j,k] + drow[loci]/vol

                # only add capsule mass if we actually have it
                if havecap:
                    # capsule portion
                    agrid[ispec][3]['data'][i,j,k] = agrid[ispec][3]['data'][i,j,k] + drow[locc]/vol;
                
            else:
                # otherwise we keep all the biomass together
                agrid[ispec][1]['data'][i,j,k] = agrid[ispec][1]['data'][i,j,k] + drow[locb]/vol;

                # only add inert mass if we actually have it
                    if havenrt:
                        # inert biomass portion
                        agrid[ispec][1]['data'][i,j,k] = agrid[ispec][1]['data'][i,j,k] + drow[loci]/vol                            

                # only add capsule mass if we actually have it
                if havecap:
                    # capsule portion
                    agrid[ispec][1]['data'][i,j,k] = agrid[ispec][1]['data'][i,j,k] + drow[locc]/vol;    

    return agrid

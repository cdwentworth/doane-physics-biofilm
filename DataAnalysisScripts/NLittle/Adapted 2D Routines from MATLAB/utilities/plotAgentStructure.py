'''
 This script is designed to duplicate the MATLAB script of the same name.

 Nathan Little
 7/26/13
'''
import numpy as np
# Partially converted
# Assume that any strange/nonfunctional code is copied from MATLAB unless proven otherwise

def plotAgentStructure(a,time,sName=''):
    '''This function plots the agent structure given in 'a'

    plotAgentStructure(a,time[,sName])
        'a' is an array
        'sName' is optional
            To keep previous plot, include legend entry 'sName'.
        '''

    #
    # first remove any species that have no individuals
    #
    rem = []
    keep = []
    
    for i in range(0,np.size(a)):
            if np.shape(a[i][0]['data'][0]) > 0:
                    keep = np.concatenate((keep, i))
            else:
                    rem = np.concatenate((rem, i))
            
    
    for i in range(0,length(rem)):
            print('No individuals of species %s to plot.\n' % a[rem[i]]['name'])
    
    a = a[keep];

    ################################################
    nspec = np.size(a)

    '''
    Note: This section was commented out in MATLAB
    
    sort the species so that those with the most members are plotted first
     
    sorder = zeros(nspec,2);
    for i=1:nspec
    	sorder(i,1) = calcAgentData(a(i),'number');
    	sorder(i,2) = i;
    end
    sorder = sortrows(sorder,-1);
    anew = a;
    for i=1:nspec
    	anew(i) = a(sorder(i,2));
    end
    a = anew;
    '''

    # creat storage arrays for desired values
    xyz = np.zeros(nspec, 1)
    rad = np.zeros(nspec, 1)

    # scale the radius values for more visible plots
    radscale = 4

    # fill storage arrays
    for i in range(0,nspec):
        # copy position columns for all individuals
        xyz[i] = a[i]['data'][:,a[i]['header']['locationX']:a[i]['header']['locationZ']]

        # copy radius column for all individuals and scale the radius
        # (this if statement is used for backwards compatibility)
        if 'totalRadius' in a[i]['header']:
            rad[i] = a[i]['data'][:,a[i]['header']['totalRadius']]*radscale
        else:
            rad[i] = a[i]['data'][:,a[i]['header']['radius']]*radscale

    #
    # adjust data
    #

    # make agent names legible in plots
    for i in range(0,nspec):
        a[i]['name'] = str.replace(a[i]['name'],'_','\_')

    #
    # plot data
    #
    if sName != '':
        hold on #MATLAB function, no direct replacement

    # this sets up the legend by plotting one cell of each type
    # (put the points outside the domain)
    for i in range(0,nspec):
        plot(-10,-10,'o',...
                    'MarkerSize',12,...
                    'MarkerFaceColor',a(i).color,...
                    'MarkerEdgeColor','k');
        hold on;
    
    if sName == '':
        legend(a.name);
    else:
        legend(sName,a.name);

    # now go through and plot the points
    maxht = 0;
    maxrt = 0;
    for i in range(0,nspec):
        nparts = size(xyz{i},1);
        print('Individuals of %s: %i\n' % a[i]['name'],nparts)
        for j in range(1,nparts):
            plot(xyz{i}(j,2),xyz{i}(j,1),'o',
                            'MarkerSize',rad[i][j],
                            'MarkerFaceColor',a[i]['color'],
                            'MarkerEdgeColor','k')
            maxht = max(maxht,xyz{i}(j,1));
            maxrt = max(maxrt,xyz{i}(j,2));


    if sName is '':
            axis equal;
            xlim([0 a(1).nJ*a(1).resolution])
            ylim([0 max([40,1.2*maxht])]);
    else:
            axis equal;
            xlim([0 a(1).nJ*a(1).resolution])
            ylim([0 a(1).nI*a(1).resolution])
    

    xlabel('Y [\mum]');
    ylabel('X [\mum]');
    title(str('Agents at %g Hours' % time));

    drawnow;    

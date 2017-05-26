'''
 This script is designed to duplicate the MATLAB script of the same name.
 Description taken from original.

 Nathan Little
 7/22/13
 '''
# First-pass conversion
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

import numpy as np

def idCleanUp(dirs):
    """takes a cell array of directories and cleans out the following files:

    pass in 'sub' to get all the subdirectories of this one
    pass in 'recursive' to clean ALL subdirectories recursively

    env_Sum(*).xml
    env_State(*).xml
    agent_Sum(*).xml
    agent_State(*).xml
    it(*).pov
    """

    if nargin < 1
            dothecleaning;
            return;

    if strcmp(dirs,'sub')
            dirs = getDirNames('.');

    recursive = 0;
    if strcmp(dirs,'recursive')
            recursive = 1;
            dirs = getDirNames('.');

    for id=1:numel(dirs)
            if strcmp(dirs{id},'lastIter')
                    %fprintf('Skipping lastIter\n');
                    continue;

            cd(dirs{id});

            fprintf('Cleaning %s [%i/%i]\n',dirs{id},id,numel(dirs));
            dothecleaning;

            if recursive
                    idCleanUp('recursive');

            cd ..;

########################################################################

def dothecleaning():

    delete('env_Sum(*).xml');
    delete('env_State(*).xml');
    delete('agent_Sum(*).xml');
    delete('agent_State(*).xml');
    delete('it(*).pov');

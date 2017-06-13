'''
 This script is designed to duplicate the MATLAB script of the same name

 Nathan Little
 7/22/13
'''
# First-pass Conversion
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

# Waiting
#import plotContour, plotAgents
def plotMix(nFile,sName):
    """plotMix(nFile,sName)
    
    plots agents and the solute sName for the given iterate nFile
    (the options for sName are the same as in plotContour)
    """

    if nargin < 1
            help plotMix;
            return;
    end

    if nargin < 2
            fprintf('Need to specify contour to plot.\n');
            showRunInfo(nFile);
            return;
    end

    plotContour(nFile,sName);
    plotAgents(nFile,sName);

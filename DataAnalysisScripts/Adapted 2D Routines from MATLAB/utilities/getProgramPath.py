'''
 This script is designed to duplicate the MATLAB script of the same name.
 Description taken from original.

 Nathan Little
 7/22/13
 '''
# First-pass conversion
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

import numpy as np

def thepath = getProgramPath(theprog):
    """thepath = getProgramPath(theprog)
    returns the path to a few useful programs
    """

    theprog = lower(theprog);

    if strcmp(theprog,'POV-Ray')
            # install location for POV-Ray
            thepath = '/usr/local/bin';

    else if strcmp(theprog,'quietpov')
            # install location for the QuietPOV add-on
            thepath = 'C:\Program Files\POV-Ray for Windows v3.6\guiext\QuietPOV';

    else if strcmp(theprog,'imagemagick')
            # install location for ImageMagick
            thepath = '/home/kieran/Downloads/ImageMagick-6.8.5-8';

    else if strcmp(theprog,'ffmpeg')
            # install location for the ffmpeg library
            thepath = '/usr/bin/ffmpeg';

    else
            thepath = '';
    

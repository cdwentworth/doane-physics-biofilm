'''
 This script is designed to duplicate the MATLAB script of the same name

 Nathan Little
 7/3/13
'''
# Fully Converted

import os
from zipfile import *

def unzipSelect(zipFilename,targetFile):
    '''This function unzips a single file from a zip archive.

    unzipSelect(zipFilename, targetFile)
        zipFilename is the name of the zip file to be accessed.
        
        targetFile is the name of the file in the zip archive to be unzipped.
        
        Returns boolean signifying if the operation was successful.
        '''

    # Formatting help
    if '.zip' not in zipFilename:
        zipFilename += ".zip"
        
    zipFile = ZipFile(zipFilename,'r')
    outputDirectory = os.getcwd()

    # Inflate all entries
    enumeration = zipFile.namelist()
    test=False

    x = 0
    while (x < len(enumeration) and test is False):
        zipEntry = enumeration[x]
        if (zipEntry == targetFile):
            outputName = os.path.join(outputDirectory,targetFile)
            test=True
        x += 1

    if test:
        try:
            open(outputName, 'w+')
        except:
            zipFile.close()
            print ('Could not create "%s".' % outputName)

    else:
        print('File "%s" not found\n'% targetFile)

    # Close zip.
    zipFile.close()
    return test

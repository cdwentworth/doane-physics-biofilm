'''
 plotAgents(nFile,sName)

 'nFile' is the number of the xml file you want to access
 input sName (solute name) to retain previous plot
  (assumes the solute was plotted previously)

 This script is designed to duplicate the MATLAB script of the same name
     described above.

 Nathan Little
 7/12/13
 '''
# Partially Converted

# Waiting
#from utilities import getAgentData, plotAgentStructure

helpString = ("plotAgents(nFile,sName)\n\n"
    +"input sName (solute name) to retain previous plot\n"
    +" (assumes the solute was plotted previously)")

def plotAgents(nFile, sName = ""):
    '''plotAgents(nFile,sName)

    'nFile' is the number of the xml file you want to access
    input 'sName' (solute name) to retain previous plot
        (assumes the solute was plotted previously)'''
    
    if nFile == None and sName == "":
        print(helpString)
    else:
        # make solute name legible in plots
        sName = str.replace(sName,"_","\_")

    [a,time] = getAgentData(nFile,'State')

    # now just call the generic agent plotting routine
    plotAgentStructure(a,time,sName)


    

        

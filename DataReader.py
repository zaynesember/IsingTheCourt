import numpy as np
import csv

class DataReader:
    
    #TODO: Add other courts
    #1994-2005
    #First case is 1994-053, last is 2004-080
    def getRehnquist():
        
        allVotes = np.empty((9,))
        caseVotes = np.empty(9)
        
        with open('SCDB_2019_01_justiceCentered_Citation.csv') as csv_file:
            
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            
            prevCaseID = -1
            
            for row in csv_reader:
                
                #Grab the string with the case ID
                caseIDstr = row[0]
                
                #Remove the dash and convert to an int for better comparison
                caseIDint = int(caseIDstr[0:4] + caseIDstr[5:])
                
                #Check to ensure we're in the Rehnquist court era (with continuity of justices)
                if(caseIDint >= 1994053 and caseIDint <= 2004080):
                    
                    if(prevCaseID == caseIDint):
                        
                        #Note this is using the 'direction' column where votes are categorized by ideology, other measures may be better
                        direction = int(row[58])
                        #Conservative vote
                        if(direction == 1): np.append(caseVotes, -1)
                        #Liberal vote
                        if(direction == 2): np.append(caseVotes, 1)
                        else: np.append(caseVotes, None)
                    
                    else: 
                        np.append(allVotes, caseVotes)
                        caseVotes = np.empty(9)
                        
                prevCaseID = caseIDint
                
            return allVotes 
                    
                    
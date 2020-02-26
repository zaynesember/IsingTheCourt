import numpy as np
import csv

class DataReader:
   
    def directionCheck(caseVotes, direction):
        #Conservative vote
        if(direction == "1"): return np.append(caseVotes,-1.)
        #Liberal vote
        if(direction == "2"): return np.append(caseVotes,1.)
        #No direction
        else: return np.append(caseVotes,0.)
        
    #TODO: Add other courts
    #1994-2005
    #First case is 1994-053, last is 2004-080
    def getRehnquist():
        
        allVotes = np.array([None,None,None,None,None,None,None,None,None])
        #allVotes = np.empty(shape=(9,1))
        caseVotes = np.array([])
        
        with open('SCDB_2019_01_justiceCentered_Citation_utf.csv') as csv_file:
            
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            
            prevCaseID = -1
            idx = 0
            
            for row in csv_reader:
                
                #Grab the string with the case ID
                caseIDstr = row[0]
                
                #Make sure we aren't on row 0 otherwise casting to an int later doesn't work
                if (idx > 0): 
                    
                    #Remove the dash and convert to an int for better comparison
                    caseIDnumstr = str(caseIDstr[0:4]) + str(caseIDstr[5:])
                    caseIDint = int(caseIDnumstr)
      
                
                    #Check to ensure we're in the Rehnquist court era (with continuity of justices)
                    if(caseIDint >= 1994053 and caseIDint <= 2004080):
                        print("Current case ID: ", caseIDint)
                        #print("Previous case ID: ", prevCaseID)
                        if(prevCaseID == caseIDint or prevCaseID == -1):
                            
                            #Note this is using the 'direction' column where votes are categorized by ideology, other measures may be better
                            direction = row[58]
                            #Append the transformed vote direction to the array
                            caseVotes = DataReader.directionCheck(caseVotes, direction)

                        else: 
                            print("All votes: ",allVotes)
                            print("Case votes: ",caseVotes)
                            print("All votes shape: ",allVotes.shape)
                            print("Case votes shape: ",caseVotes.shape)
                            #print("Current case ID: ", caseIDint)
                            if(caseVotes.size == 9):
                                allVotes = np.concatenate([allVotes.reshape(-1,9), caseVotes.reshape(-1,9)],axis=0)
                                caseVotes = np.array([])
                            
                            direction = row[58]
                            caseVotes = DataReader.directionCheck(caseVotes, direction)

                        prevCaseID = caseIDint
                    
                idx+=1
                
            return allVotes 
        
    
    
    
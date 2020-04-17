import numpy as np
import csv

#TODO: Add other courts
class DataReader:
   
    #Takes in existing array of votes for an individual case and direction of a vote and transforms then
    #appends it to array
    def directionCheck(caseVotes, direction):
        #Conservative or dissenting vote
        if(direction == "1"): return np.append(caseVotes,-1.)
        #Liberal or majority vote
        if(direction == "2"): return np.append(caseVotes,1.)
        #No direction
        else: return np.append(caseVotes,0)
        
    #Scrapes vote data for the Rehnquist Court from 1994 to 2005
    def getRehnquist(ideology=False, mm=False):
        if ideology: rowidx=57
        if mm: rowidx=58
        
        allVotes = np.array([None,None,None,None,None,None,None,None,None])
        #allVotes = np.empty(shape=(9,1))
        caseVotes = np.array([])
        
        with open('SCDB_2019_01_justiceCentered_Citation_utf.csv', encoding='utf-8') as csv_file:
            
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
                    
                        if(prevCaseID == caseIDint or prevCaseID == -1):
                            
                            direction = row[rowidx]
                            #Append the transformed vote direction to the array
                            caseVotes = DataReader.directionCheck(caseVotes, direction)

                        else: 
                            #Check for oddball cases where not all justices voted and ignore them
                            if(caseVotes.size == 9):
                                zeroes = False
                                for v in caseVotes:
                                    if v==0: zeroes = True
                                if (not zeroes): allVotes = np.concatenate([allVotes.reshape(-1,9), caseVotes.reshape(-1,9)],axis=0)
                                caseVotes = np.array([])
                            
                            direction = row[rowidx]
                            caseVotes = DataReader.directionCheck(caseVotes, direction)

                        prevCaseID = caseIDint
                    
                idx+=1
            
            #Slice off first row of Nones
            return allVotes[1:] 
        
    
    
    
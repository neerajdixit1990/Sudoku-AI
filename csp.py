import os
import sys
import copy
import time
import random
from Queue import PriorityQueue
from Queue import Queue


###########################################
# you need to implement five funcitons here
###########################################


class SudokuSolver:
    
    def __init__(self, filename):
            
            self.puzzle=[[]] 
            self.blanks=[] 
            self.defArray() 
            self.blankValues={}
            self.constraintChecks=0 
            self.runningTime=0
            self.option=2
            self.N=1
            self.M=1
            self.K=1
            self.conflict=0
	    self.no_false = 0
            self.blanks=self.loadFile(filename)
	    
            
    
    def defArray(self):
        for i in range(100):
            self.puzzle.append([])
            for j in range(100):
                self.puzzle[i].append([])
                self.puzzle[i][j]=0        
    

        
    def loadFile(self, inpFile):
        puzzle=open(inpFile, 'r')
        puzzleText = puzzle.readline().strip().split(';')
        param = puzzleText[0].split(',')
        try:        
            self.N = int(param[0])
            self.M = int(param[1])
            self.K = int(param[2])
            #print "nmk: "+str(self.N)+str(self.M)+str(self.K)
        except ValueError:
            pass 
        try: 
            for row in range (1,self.N+1):
                tok = puzzleText[row].split(',')
                if len(tok)!=self.N:
                    sys.exit(1)
                for col in range(self.N):
                    token=tok[col].split()[0].strip()
                    if token=='-':  
                        token=0 
                    token=int(token)
                    row2 = row-1
                        
                    self.puzzle[row-1][col]=int(token)
        except IndexError:
            print "self.puzzle[row-1][col]:error "
            pass
        emp=[]
        try:   
            for i in range(self.N):
                for j in range(self.N):
                    if self.puzzle[i][j]==0:
                        emp.append((i, j))
        except IndexError:
            pass
        
        return emp
        
        print ""
    
    def getEmptycls_MRV(self, puzzle):
        emptycls=[]
        try:
            for i in range(self.N):
                for j in range(self.N):
                    if self.puzzle[i][j]==0:
                        emptycls.append([0, i, j])
        except IndexError:
            pass

	for i in range(len(emptycls)):
	    for num in range(1, self.N+1):
		if self.checkSud(emptycls[i][1], emptycls[i][2], num, True):
		    emptycls[i][0] = emptycls[i][0] + 1
	emptycls.sort(key=lambda tup: tup[0])
        return emptycls

            
    def backtracking(self, index):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
            #Found a solution if we have gone past the last blank
        if index == len(self.blanks):
	    #import pudb
	    #pudb.set_trace()
            self.endOp()
	    return True
        
        #Haven't found a solution yet; get coords of the blank
        row=self.blanks[index][0]
        col=self.blanks[index][1]
        
        #Try numbers 1-9.
        for num in range(1, self.N+1):
            if self.checkSud(row, col, num, False):   
                #If the number is valid, increment current path by 1.
                #self.currentPathLength+=1 
                self.puzzle[row][col] = num
                val = self.backtracking(index+1)
        
        #No number found...set back to 0 and return to the previous blank
        #self.pathLengths.append(self.currentPathLength) #Add the current path length to the overall list.
        #self.currentPathLength-=1 #-1 from path
		if val == True:
		    return True
		else:
        	    #index-=1
        	    self.puzzle[row][col]=0
        return False

    def endOp(self):
                return True
    
    def checkSud(self, row, col ,num, heur):
        if heur==False:
            self.constraintChecks+=1 #Increment number of constraint checks
        valid=False
        if num==0:
            return True
        else:
            #Return true if row, column, and box have no violations
            rowValid=self.checkRow(row, num)
            colValid=self.checkColumn(col, num)
            boxValid=self.checkBox(row, col, num)                                   
            valid=(rowValid&colValid&boxValid)
        
            return valid
        
        
    def checkRow(self, row, num ):
        for col in range(self.N):
            currentValue=self.puzzle[row][col]
            if num==currentValue:
                return False        
        return True
    
    #    Check for validity 
    
    def checkColumn(self, col, num ):
        for row in range(self.N):
            currentValue=self.puzzle[row][col]
            if num==currentValue:
                return False
        return True

    #    Check for validity
    
    def checkBox(self, row, col, num):       
        row=(row/self.M)*self.M
        col=(col/self.K)*self.K
        
        for r in range(self.M):
            for c in range(self.K):
                if self.puzzle[row+r][col+c]==num:
                    return False
        return True
    
    
    def printPuzzle(self):
        print "____________________" 
        rSs=[]
        try:
            for i in range(self.N):
                rS=[]
                for j in range(self.N):
                    rS.append(str(self.puzzle[i][j])+" ")
                print rS
    
            for i in range(0, self.N):
                for j in range(0, self.N):
                    print rS[i][j]
                print '\n'
                print "--------------------" 
        except IndexError:
            pass

    def find_next_cell(self):
	min_count = 1000
	tup = [-1, -1]
	for i in range(self.N):
	    for j in range(self.N):
		if self.puzzle[i][j] == 0:
		    count = 0
		    for num in range(1, self.N+1):
		        if self.checkSud(i, j, num, False):
			    count = count + 1
		    if min_count > count:
		        min_count = count
		        tup[0] = i
		        tup[1] = j
	return tup

    def backtrackingMRV(self):
        ###
        # use backtracking + MRV to solve sudoku puzzle here,
        # return the solution in the form of list of 
        # list as describe in the PDF with # of consistency
        # checks done
        ###
        
	#Found a solution if we have gone past the last blank
	#import pudb
	#pudb.set_trace()
        tup = self.find_next_cell()
	if tup == [-1,-1]:
		#import pudb
		#pudb.set_trace()
		self.endOp()
		return True	


        #Try numbers 1-9.
        for num in range(1, self.N+1):
            if self.checkSud(tup[0], tup[1], num, False):
                
                self.puzzle[tup[0]][tup[1]] = num
                ret = self.backtrackingMRV()

		if ret == False:
        	    self.puzzle[tup[0]][tup[1]]=0
		else:
		    return True
        return False
 
    
    def backtrackingMRVfwd(self):
        if len(self.blanks)==0:
            self.endOp()
	    self.printPuzzle()
            return True

        blank=self.MRVval()
        row=blank[0]
        col=blank[1]

        valBlanks=copy.deepcopy(self.blankValues[blank])
        #print "blank"+ str(blank)
        #print "blankvalues"+ str(valBlanks)

        for num in valBlanks:
            valCopy=copy.deepcopy(self.blankValues) 
            consistent=self.checInv(blank, num)
            if (consistent==True): 
                self.blanks.remove(blank)
                self.puzzle[row][col] = num

                result=self.backtrackingMRVfwd()

                self.blankValues=valCopy 

                self.blanks.append(blank)
                self.puzzle[row][col]=0
                

        return True


    def MRVval(self):

        q = PriorityQueue()
        for blank in self.blanks:
            possible = self.getAllVal(blank, False)
            q.put((len(possible), blank))

        blanks = []
        blanks.append(q.get())
        minVal = blanks[0][0]

        while not q.empty(): 
            next = q.get()
            if next[0] == minVal:
                blanks.append(next)
            else:
                break

        dmax = len(self.getAssocBlks(blanks[0][1]))
        dmaxBlank = blanks[0]

        for blank in blanks:
            degree = len(self.getAssocBlks(blank[1]))
            if degree > dmax:
                dmaxBlank = blank
                dmax = degree
        return dmaxBlank[1]
 
    def getAssocBlks(self, blank):
        row=blank[0]
        col=blank[1]
        
        nb=[]
        associatedBlanks=self.getRBlks(row)+self.getCBlks(col)+self.getBBlks(row, col)
        for blank in associatedBlanks:
            if blank not in nb and blank!=(row,col): 

                nb.append(blank)
        return nb
    
    def getRBlks(self, row):
        cls = []
        for col in range(self.N):
            if self.puzzle[row][col]==0:
                cls.append((row, col))
        return cls
    
    def getCBlks(self, col ):
        cls=[]
        for row in range(self.N):
            if self.puzzle[row][col]==0:    
                cls.append((row,col))
        
        return cls
    

    def getBBlks(self, row, col):       
        cls=[]
        row=(row/self.M)*self.M
        col=(col/self.K)*self.K
        
        for r in range(self.M):
            for c in range(self.K):
                if self.puzzle[row+r][col+c]==0:
                    cls.append((row+r,col+c))
                    
        return cls
    
    def checInv(self, blank, num):
        
        nb=self.getAssocBlks(blank)
        for nblk in nb:
            ndom=self.blankValues[nblk]
            if num in ndom:
                self.blankValues[nblk].remove(num)
                if len(self.blankValues[nblk])==0: 
                    return False
        return True
    
    def procVar(self):
        
        for blank in self.blanks:
            valPos=self.getAllVal(blank, False)
            self.blankValues[blank]=valPos
    
    def getAllVal(self, cell, heur):
        row=cell[0]
        col=cell[1]
        allowed=[]
        for i in range(1,self.N+1):
            if self.checkSud(row, col, i, heur):
                allowed.append(i)
    
        return allowed

    def cp_consistency(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.puzzle[i][j] == 0:
                    count = 0
                    for num in range(1, self.N+1):
                        if self.checkSud(i, j, num, True):
                            count = count + 1
			    valid_num = num
			    row = i
			    col = j
		    if count == 1:
			self.puzzle[row][col] = valid_num

        for i in range(self.N):
            for j in range(self.N):
                if self.puzzle[i][j] == 0:
                    count = 0
                    for num in range(1, self.N+1):
                        if self.checkSud(i, j, num, True):
                            count = count + 1
                            valid_num = num
                            row = i
                            col = j
                    if count == 0:
                        return False
	return True
	
    
    def backtrackingMRVcp(self):
        ###
        # use backtracking + MRV + cp to solve sudoku puzzle here,
        # return the solution in the form of list of 
        # list as describe in the PDF with # of consistency
        # checks done
        ###
        tup = self.find_next_cell()
        if tup == [-1,-1]:
                #import pudb
                #pudb.set_trace()
                self.endOp()
                return True


        #Try numbers 1-9.
        for num in range(1, self.N+1):
            if self.checkSud(tup[0], tup[1], num, False):
                #If the number is valid, increment current path by 1.
                self.puzzle[tup[0]][tup[1]] = num
		
		#import pudb
		#pudb.set_trace()
		sudoku_cp = copy.deepcopy(self)
		if not sudoku_cp.cp_consistency():
		    self.puzzle[tup[0]][tup[1]]=0
		    #self.no_false = self.no_false + sudoku_cp.no_false
		    continue
		
		#self.no_false = self.no_false + sudoku_cp.no_false
                ret = self.backtrackingMRV()

                if ret == False:
                    self.puzzle[tup[0]][tup[1]]=0
                else:
                    return True
        return False
   
    def find_next_cell_minconflict(self):

	#import pudb
	#pudb.set_trace()	
	mincount = 10
	index = random.randint(0, len(self.blanks)-1)
	row = self.blanks[index][0]
	col = self.blanks[index][1]
	    
	for i in range(1, self.N+1):
	    count = 0
            if not self.checkRow(row, i):                
                count = count + 1
            if not self.checkColumn(col, i):
		count = count + 1
            if not self.checkBox(row, col, i):
		count = count + 1
	    
	    #if count == 0:
		#continue
	    
	    if count < mincount:
		mincount = count
		num = i	
	
	#if count == 0:
	    #return (-1, -1, -1)
	#else:
	return (row, col, num)
 
    def minConflict(self, index):
        
        
	for cnt in range (100000):
            if len(self.blanks)==0:
                #self.endOp()
                self.printPuzzle()
                return True

            min_tup = self.find_next_cell_minconflict()
            if min_tup == (-1, -1, -1):
		continue
	    else:
		if self.checkSud(min_tup[0], min_tup[1], min_tup[2], False):
		    #import pudb
		    #pudb.set_trace()
		    self.puzzle[min_tup[0]][min_tup[1]] = min_tup[2]
		    self.blanks.remove((min_tup[0], min_tup[1]))
   
		if len(self.blanks)==0:
            	    #self.endOp()
            	    self.printPuzzle()
            	    return True
	
	return False
              
    
    def checkConflict(self, row, col ,num, heur):
        if heur==False:
            self.constraintChecks+=1 #Increment number of constraint checks
        valid=False
        if num==0:
            return True
        else:
            #Return true if row, column, and box have no violations
            rcnt=self.checkRow(row, num)
            ccnt=self.checkColumn(col, num)
            bcnt=self.checkBox(row, col, num)                                   
            self.conflict= rcnt+ccnt+bcnt
        
            return self.conflict
        
        
    def checkRowConflict(self, row, num ):
        for col in range(self.N):
            currentValue=self.puzzle[row][col]
            if num==currentValue:
                cnt =cnt+1         
        return cnt
    
    #    Check for validity 
    
    def checkColumnConflict(self, col, num ):
        for row in range(self.N):
            currentValue=self.puzzle[row][col]
            if num==currentValue:
                cnt =cnt+1 
        return cnt

    #    Check for validity
    
    def checkBoxConflict(self, row, col, num):       
        row=(row/self.M)*self.M
        col=(col/self.K)*self.K
        
        for r in range(self.M):
            for c in range(self.K):
                if self.puzzle[row+r][col+c]==num:
                    cnt =cnt+1 
        return cnt



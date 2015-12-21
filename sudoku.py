import argparse
import sys
import csp
import time

###############################################################
# NOTE: Don't edit this file
###############################################################
def main(args):
    ###
    # args.input: this will give you the path to game.txt file
    ###
    
    ##########################################################
    # backtracking
    ##########################################################
	sudoku_obj_1 = csp.SudokuSolver(sys.argv[2])	
	tic = time.clock()
	sudoku_obj_1.backtracking(0)
	toc = time.clock()
	timeItr = toc - tic
	
	print "Backtracking:"
	print "Execution Time: " + str(timeItr)
	print "Consistency Checks: " + str(sudoku_obj_1.constraintChecks)
	print "Solution: "
	sudoku_obj_1.printPuzzle()   
 
    ##########################################################
    # backtracking + MRV
    ##########################################################
	sudoku_obj_2 = csp.SudokuSolver(sys.argv[2])
	tic = time.clock()
	sudoku_obj_2.backtrackingMRV()
	toc = time.clock()
	timeItr = toc - tic
	
	print "backtrackingMRV:"
	print "Execution Time: " + str(timeItr)
	print "Consistency Checks: " + str(sudoku_obj_2.constraintChecks)
	print "Solution: " 
	sudoku_obj_2.printPuzzle()
    
    ##########################################################
    # backtracking + MRV + fwd
    ##########################################################
	sudoku_obj_3 = csp.SudokuSolver(sys.argv[2])    
	tic = time.clock()
	sudoku_obj_3.procVar()
	sudoku_obj_3.backtrackingMRVfwd()
	toc = time.clock()
	timeItr = toc - tic

	print "backtrackingMRVfwd:"
	print "Execution Time: " + str(timeItr)
	print "Consistency Checks: " + str(sudoku_obj_3.constraintChecks)
	print "Solution printed above " + '\n'
    
    ##########################################################
    # backtracking + MRV + CP
    ##########################################################
	sudoku_obj_4 = csp.SudokuSolver(sys.argv[2])
	tic = time.clock()
	sudoku_obj_4.backtrackingMRVcp()
	toc = time.clock()
	timeItr = toc - tic
	
	print "backtrackingMRVcp:"
	print "Execution Time: " + str(timeItr)
	print "Consistency Checks: " + str(sudoku_obj_4.constraintChecks)
	print "Solution: "
	sudoku_obj_4.printPuzzle()
    
    ##########################################################
    # minConflict
    ##########################################################
	#import pudb
	#pudb.set_trace()
	sudoku_obj_5 = csp.SudokuSolver(sys.argv[2])	
	tic = time.clock()
	sudoku_obj_5.minConflict(0)
	toc = time.clock()
	timeItr = toc - tic
	
	print "minConflict:"
	print "Execution Time: " + str(timeItr)
	print "Consistency Checks: " + str(sudoku_obj_5.constraintChecks)
	#print "Solution: " + str(solution) + '\n'
	sudoku_obj_5.printPuzzle()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="HomeWork Three")
	parser.add_argument("--input", type=str)
	args = parser.parse_args()
	main(args)

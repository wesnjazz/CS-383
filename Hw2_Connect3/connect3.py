import sys
from problem import *
from readfile import *

def main():
	if len(sys.argv) != 2:
		print("usage:python", sys.argv[0], "[stateFile.txt]")
		sys.exit()

	initialState, width, height = readInitialStateFile(sys.argv[1])
	problem = Problem(initialState)
	optimalMove = problem.miniMaxDecision(problem.initialState)

	if len(optimalMove[0]) > 0:
		print(optimalMove)
		bestValue = optimalMove[2]
		bestMove = optimalMove[4] + str(optimalMove[3])
		print(bestValue, bestMove)

if __name__ == "__main__":
	main()

import sys
import myqueue
from problem import *
from node import *
from readfile import *
import time

def main():
	if len(sys.argv) != 2: 
		print("usage: python", sys.argv[0], "mapfile.txt")
		sys.exit()
	initialState, width, height = readInitialStateFile(sys.argv[1])

	problem = Problem(initialState, width, height)
	start = time.time()
	solution, totalNumFrontier, totalNumExplored, maxNumQueue = aStarSearch(problem)
	end = time.time()

	printSolution(solution, width)
	printMetrics(totalNumFrontier, totalNumExplored, maxNumQueue, end-start)

def aStarSearch(problem):
	totalNumFrontier = 0
	totalNumExplored = 0
	maxNumQueue = 0

	# node = problem.initialState
	node = Node(problem.initialState, path_cost=heuristic(problem, problem.goalState, problem.initialState))

	# STEP - initialize the frontier using the initial state of problem
	frontier = myqueue.PriorityQueue()	# data structure for BFS: queue of list data type
	frontier.put(node.path_cost + heuristic(problem, problem.goalState, node.state), node)
	totalNumFrontier += 1

	frontierSet = set()
	frontierSet.add(tuple(node.state))

	# STEP - initialize the explored set to be empty (for GRAPH-SEARCH)
	exploredSet = set()

	# STEP - loop do
	while True:
		n = len(frontierSet)
		if (n > maxNumQueue):
			maxNumQueue = n

		if (totalNumExplored >= 100000):
			print("no solution found (100k limit reached)")
			return False, totalNumFrontier, totalNumExplored, maxNumQueue

		# STEP - if the frontier is empty then return failrue
		if frontier.empty():
			return False, totalNumFrontier, totalNumExplored, maxNumQueue

		# STEP - choose a leaf node and remove it from the frontier
		node = frontier.get()
		totalNumExplored += 1
		frontierSet.remove(tuple(node.state))

		if problem.goalTest(node.state):
			return solution(node), totalNumFrontier, totalNumExplored, maxNumQueue

		# STEP - add the node to the explored set (for GRAPH-SEARCH)
		exploredSet.add(tuple(node.state))

		# STEP - expand the chosen node, adding the resulting nodes to the frontier
		availableActions = problem.actions(node.state)	# find available actions of the chosen node
		for action, possible in availableActions.items():
			if possible:
				child = childNode(problem, node, action)
				if tuple(child.state) not in frontierSet and tuple(child.state) not in exploredSet:
					# STEP - if the node contains a goal state then return the sorresponding solution
					frontier.put(child.path_cost + heuristic(problem, problem.goalState, child.state), child)
					totalNumFrontier += 1
					frontierSet.add(tuple(child.state))
				elif frontier.contains(child):
					cost = frontier.getPriority(child)
					if cost > child.path_cost + heuristic(problem, problem.goalState, child.state):
						frontier.update(child, child.path_cost + heuristic(problem, problem.goalState, child.state))
						frontierSet.remove(tuple(child.state))

def heuristic(problem, goalState, currState):
	goalIdx = goalState.index('.')
	currIdx = currState.index('.')
	width, height = problem.width, problem.height
	x_distance = abs((goalIdx % width) - (currIdx % width))
	y_distance = abs((goalIdx // height) - (currIdx // height))
	return x_distance + y_distance

def printSolution(solution, width):
	if solution == False:
		print("No solution")
		return
	for state in solution:
		i = 0
		s = ""
		for x in state:
			if i != 0 and i % width == 0:
				s = s.strip()
				s += '\n'
			s += x
			s += ' '
			i += 1
		print(s, '\n')

def printMetrics(totalNumFrontier, totalNumExplored, maxNumQueue, elapsedTime):
	print("\n[Metrics]")
	print("Total number of search nodes added to the frontier queue:", totalNumFrontier)
	print("Total number of search nodes selected from the frontier queue for expansion:", totalNumExplored)
	print("Maximum size of the search queue at any given time during the search:", maxNumQueue)
	print("Elapsed Time:", elapsedTime)


if __name__ == "__main__":
	main()
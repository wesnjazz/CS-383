import sys
from problem import *
from readfile import *
from stack import *

def main():
	if len(sys.argv) != 2: 
		print("usage: python", sys.argv[0], "mapfile.txt")
		sys.exit()
	initialState, width, height = readInitialStateFile(sys.argv[1])
	print("width: ", width, "height: ", height)
	problem = Problem(initialState, width, height)
	solution, count = dfs(problem)
	print(type(solution))
	printSolution(solution, width)
	print(count)

def dfs(problem):
	# STEP - initialize the frontier using the initial state of problem

	node = problem.initialState
	if problem.goalTest(node):
		return node, 1

	frontier = Stack()	# data structure for DFS: Queue of list data type
	frontier.push(problem.initialState)
	frontierSet = set()
	frontierSet.add(tuple(problem.initialState))



	# STEP - initialize the explored set to be empty (for GRAPH-SEARCH)
	exploredSet = set()

	solution = []

	tries = 0
	# STEP - loop do
	while True:
		tries += 1
		# print(tries)
		# STEP - if the frontier is empty then return failrue
		if frontier.size() == 0:
			print("No Solution")
			return [], tries

		# STEP - choose a leaf node and remove it from the frontier
		node = frontier.pop()
		# if problem.goalTest(node):
		# 	solution.append(node)
		# 	return solution, tries


		# STEP - if the node contains a goal state then return the sorresponding solution
		# if problem.goalTest(node):
		# 	exploredSet.append(problem.goalState)
		# 	return exploredSet

		# STEP - add the node to the explored set (for GRAPH-SEARCH)
		exploredSet.add(tuple(node))
		solution.append(node)
		# print(exploredSet)
		# STEP - expand the chosen node, adding the resulting nodes to the frontier
		availableActions = problem.actions(node)	# find available actions of the chosen node
		# print("************ find possible states **********************")
		# print("from: ", node)
		# frontier.print()
		for direction, possible in availableActions.items():
			if possible:
				child = problem.transitionModel(node, direction)
				# print(type(frontier))
				# print(type(frontier.stack))
				# frontier.print()
				# print("Contains?:", frontier.contains(child))
				if tuple(child) not in frontierSet and tuple(child) not in exploredSet:
					if problem.goalTest(child):
						solution.append(child)
						return solution, tries
					frontier.push(child)
					frontierSet.add(tuple(child))
				# elif child in solution:
					# solution.remove(child)

				# print(direction, "  : ", problem.transitionModel(node, direction))

				# print("---------------------------------------------")
				# print(node)
				# print("goint ", direction, ": ", possible)
				# print("---------------------------------------------")
				# frontier.push(problem.transitionModel(node, direction))	# push the corresponding node(result node) of the available action into the frontier
				# frontier.push(problem.transitionModel(node, direction))	# push the corresponding node(result node) of the available action into the frontier




		# for i in range(0, frontier.size()):
		# 	print(i)
		# for i in range(0, len(exploredSet)):
		# 	print(exploredSet[i])

	print("solution:", exploredSet)

def printSolution(solution, width):
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

if __name__ == "__main__":
	main()
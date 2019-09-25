import queue

class Problem:
	def __init__(self, initialState, width, height):
		self.initialState = initialState
		self.width = width
		self.height = height
		self.goalState = self.setGoalState()
		self.cost = 1

	def transitionModel(self, state, action):
		""" Transition Model """
		""" A description of what each eaction does """
		blankIdx = state.index('.')
		tempState = state[:]
		if self.actions(state).get(action):
			if action == 'N':
				tempState[blankIdx], tempState[blankIdx-self.height] = tempState[blankIdx-self.height], tempState[blankIdx]
			elif action == 'S':
				tempState[blankIdx], tempState[blankIdx+self.height] = tempState[blankIdx+self.height], tempState[blankIdx]
			elif action == 'W':
				tempState[blankIdx], tempState[blankIdx-1] = tempState[blankIdx-1], tempState[blankIdx]
			elif action == 'E':
				tempState[blankIdx], tempState[blankIdx+1] = tempState[blankIdx+1], tempState[blankIdx]
		return tempState

	def actions(self, state):
		""" A description of the possible actions available of the agent """
		blankIdx = state.index('.')
		lastIdx = len(state) - 1

		N = ((blankIdx-self.width) >= 0) and ((blankIdx%self.width)==((blankIdx-self.width)%self.width))
		S = ((blankIdx+self.width) <= lastIdx) and ((blankIdx%self.width)==((blankIdx+self.width)%self.width))
		W = ((blankIdx-1) >= 0) and ((blankIdx//self.width) == ((blankIdx-1)//self.width))
		E = ((blankIdx+1) <= lastIdx) and ((blankIdx//self.width) == ((blankIdx+1)//self.width))
		return dict([('E', E), ('S', S), ('N', N), ('W', W)])
		# return dict([('E', E), ('S', S), ('N', N), ('W', W)])
		# return dict([('E', E), ('S', S), ('N', N), ('W', W)])
		# return dict([('E', E), ('S', S), ('N', N), ('W', W)])

	def goalTest(self, state):
		""" determines whether a given state is a goal state """
		# print("*** GOAL TEST ***")
		# print("GoalState:", self.goalState, "state:", state)
		return state == self.goalState

	def stepCost(self, state, action):
		""" assigns a numeric cost to each path """
		return 1

	def setGoalState(self):
		goalState = []
		for i in range(self.width * self.height):
			if i == 0: goalState.append('.')
			else: goalState.append(str(i))
		return goalState

def solution(node):
	solution = []
	while node != None:
		solution.append(node.state)
		node = node.parent
	return solution[::-1]

if __name__ == "__main__":
	main()
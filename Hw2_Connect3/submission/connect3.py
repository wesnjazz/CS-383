import sys

def readInitialStateFile(file):
	with open(sys.argv[1], 'rt') as f:
		resultStr = ""	# result string from the input
		initialState = []	# list of initial state
		width, height = 0, 0
		while True:
			""" remove leading/ending whitespaces, 
				then also remove newline and space,
				then split into list """
			line = f.readline().strip().replace("\n", "").split()
			for c in line:
				initialState.append(c)
			height += 1
			if width == 0: width = len(line)
			if not line:
				height -= 1
				break	# break if reached EOF

		return initialState, width, height 	# return the resulting list

class Problem:
	def __init__(self, state):
		self.initialState = state
		self.maxPlayer = 'X'
		self.minPlayer = 'O'
		self.emptySlot = '.'
		self.cols = 5
		self.rows = 4
		self.terminalOffset = (
			(0,1,2), (1,2,3), (2,3,4), (5,6,7), (6,7,8), (7,8,9),
			(10,11,12), (11,12,13), (12,13,14),	(15,16,17), (16,17,18), (17,18,19),
			(0,5,10), (5,10,15), (1,6,11), (6,11,16),
			(2,7,12), (7,12,17), (3,8,13), (8,13,18), (4,9,14), (9,14,19),
			(0,6,12), (1,7,13), (2,8,14), (5,11,17), (6,12,18), (7,13,19),
			(2,6,10), (3,7,11), (4,8,12), (7,11,15), (8,12,16), (9,13,17))

	def player(self, state):
		countMaxPlayer, countMinPlayer, countEmptySlots = self.countPlayersAndEmptySlots(state)
		if countMaxPlayer > countMinPlayer:
			return self.minPlayer
		else:
			return self.maxPlayer
		
	def actions(self, state):
		actions = []
		availableColum = True
		for col in range(0, self.cols):
			if state[col] == self.emptySlot:
				actions.append(col)
		return actions

	def result(self, state, action):
		player = self.player(state)
		newState = state[::]
		lastIdx = -1
		for row in range(0, self.rows):
			if state[row * self.cols + action] == self.emptySlot:
				lastIdx = row * self.cols + action
			else:
				break
		if lastIdx == -1:
			return newState
		else:
			newState[lastIdx] = player
			return newState

	def terminalTest(self, state):
		countMaxPlayer, countMinPlayer, countEmptySlots = self.countPlayersAndEmptySlots(state)
		if countEmptySlots == 0:
			return True
		else:
			return self.connectTest(state)
		return False

	def connectTest(self, state):
		for offSet in self.terminalOffset:
				if state[offSet[0]] != self.emptySlot and state[offSet[0]] == state[offSet[1]] == state[offSet[2]]:
					return True
		return False

	def utility(self, state, player):
		countMaxPlayer, countMinPlayer, countEmptySlots = self.countPlayersAndEmptySlots(state)
		if countMaxPlayer > countMinPlayer:
			if player == self.maxPlayer:
				return 1
			elif player == self.minPlayer:
				return -1
		elif countMinPlayer == countMaxPlayer:
			if self.connectTest(state):
				return -1
			else:
				return 0
		else:
			return 0

	def countPlayersAndEmptySlots(self, state):
		countMaxPlayer = state.count(self.maxPlayer)
		countMinPlayer = state.count(self.minPlayer)
		countEmptySlots = state.count(self.emptySlot)
		return countMaxPlayer, countMinPlayer, countEmptySlots

	def printState(self, state):
		i = 0
		s = ""
		for x in state:
			if i != 0 and i % self.cols == 0:
				s = s.strip()
				s += '\n'
			s += x
			s += ' '
			i += 1
		print(s)

	def miniMaxDecision(self, state):
		# self.printState(state)
		# print("Next Turn:", self.player(state))
		values = []
		player = self.player(state)
		maxTemp 	= -999999999
		maxAction 	= -999999999
		maxValue 	= -999999999
		minTemp 	= 999999999
		minAction 	= 999999999
		minValue 	= 999999999
		actionsAvailable = self.actions(state)

		if len(actionsAvailable) > 0:
			if player == self.maxPlayer:
				for a in actionsAvailable:
					s = self.result(state, a)
					# self.printState(s)
					x = self.minValue(s)
					if x > maxTemp:
						maxTemp = x
						maxAction = a
					# print("v:", x, "\n")
					values.append(x)
				maxValue = max(values)
				return values, actionsAvailable, maxValue, maxAction, player

			elif player == self.minPlayer:
				for a in actionsAvailable:
					s = self.result(state, a)
					# self.printState(s)
					x = self.maxValue(s)
					if x < minTemp:
						minTemp = x
						minAction = a
					# print("v:", x, "\n")
					values.append(x)
				minValue = min(values)
				return values, actionsAvailable, minValue, minAction, player
		return values, actionsAvailable, maxValue, maxAction, player


	def maxValue(self, state):
		# self.printState(state)
		if self.terminalTest(state):
			return self.utility(state, self.minPlayer)
		v = -999999999
		for a in self.actions(state):
			v = max(v, self.minValue(self.result(state, a)))
		return v

	def minValue(self, state):
		# self.printState(state)
		if self.terminalTest(state):
			return self.utility(state, self.maxPlayer)
		v = 999999999
		for a in self.actions(state):
			v = min(v, self.maxValue(self.result(state, a)))
		return v

def main():
	if len(sys.argv) != 2:
		print("usage:python", sys.argv[0], "[stateFile.txt]")
		sys.exit()

	initialState, width, height = readInitialStateFile(sys.argv[1])
	problem = Problem(initialState)
	optimalMove = problem.miniMaxDecision(problem.initialState)

	if len(optimalMove[0]) > 0:
		# print(optimalMove)
		bestValue = optimalMove[2]
		bestMove = optimalMove[4] + str(optimalMove[3])
		print(bestValue, bestMove)

if __name__ == "__main__":
	main()

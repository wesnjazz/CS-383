class Node:
	def __init__(self, state, path_cost=0, parent=None, action=None):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost

	def __lt__(self, other):
		return self.state > other.state

def childNode(problem, parent, action):
	state = problem.transitionModel(parent.state, action)
	child = Node(state)
	child.parent = parent
	child.action = action
	child.path_cost = parent.path_cost + problem.stepCost(parent.state, action)
	return child

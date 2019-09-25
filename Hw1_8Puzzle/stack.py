class Stack():
	def __init__(self):
		self.stack = []

	def push(self, item):
		self.stack.append(item)

	def pop(self):
		return self.stack.pop()

	def peek(self):
		return self.stack[-1]

	def size(self):
		return len(self.stack)

	def isEmpty(self):
		return self.stack == []

	def contains(self, item):
		return item in self.stack

	def print(self):
		print("size: ", len(self.stack))
		for x in self.stack:
			print("haha", x)
import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []
        self.hashTable = dict()
    
    def put(self, priority, item):
        heapq.heappush(self.items, (priority, item))
        self.hashTable[item] = priority
    
    def get(self):
        return heapq.heappop(self.items)[1]

    def empty(self):
        return len(self.items) == 0

    def contains(self, item):
    	# print(item, "##test##")
    	return item in self.hashTable

    def getPriority(self, item):
    	return self.hashTable[item]

    def update(self, item, priority):
    	i = self.items.index(tuple([priority, item]))
    	# for x in self.items:
    	# 	if item == x[1] and priority == x[0]:
    	# 		print("found")
    	# 		x[1] = item
    	# 		x[0] = priority

    def printQueue(self):
    	for x in self.items:
    		print(x[0], x[1].state)
    	# print(type(self.items))
    	# print("###", self.items[0])
    	# print("###", type(self.items[0]))
    	# print(type((self.items[0])[1]))
    	# x = (self.items[0])[1].state
    	# print(x)
    	# print(self.hashTable)
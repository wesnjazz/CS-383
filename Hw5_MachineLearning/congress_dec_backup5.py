import sys
import csv
import math
import collections
import re

labels = ["Democrat", "Republican"]
header = ["Vote1", "Vote2", "Vote3", "Vote4", "Vote5", "Vote6", "Vote7", "Vote8", "Vote9", "Vote10",
				"Vote11", "Vote12", "Vote13", "Vote14", "Vote15", "Vote16", "Vote17", "Vote18", "Vote19", "Vote20",
				"Vote21", "Vote22", "Vote23", "Vote24", "Vote25", "Vote26", "Vote27", "Vote28", "Vote29", "Vote30",
				"Vote31", "Vote32", "Vote33", "Vote34", "Vote35", "Vote36", "Vote37", "Vote38", "Vote39", "Vote40",
				"Vote41", "Vote42", "Party"]
num_of_examples = 0
entropy_Goal = 0

class DecisionTree():
	def __init__(self, name):
		self.name = name
		self.subtree = dict()
		self.prob = dict()
		self.column = self.getColumnNum(self.name)

	def getColumnNum(self, name):
		# for s in name.split():
		# 	print(s)
		return int(re.search(r'\d+', name).group())
		# pass
		# return int(s) for s in name.split() if s.isdigit()

	def add_subtree(self, value, subtree):
		self.subtree[value] = subtree


	def getProbability(self, examples):
		count = dict()
		for l in labels:
			count[l] = 0

		for row in examples:
			if row[-1] == labels[0]:
				count[labels[0]] +=1
			elif row[-1] == labels[1]:
				count[labels[1]] +=1
		print(count)
		self.prob[labels[0]] = count[labels[0]] / (count[labels[0]] + count[labels[1]])
		self.prob[labels[1]] = count[labels[1]] / (count[labels[0]] + count[labels[1]])
		print(self.prob)

	def count_tree(self):
		num = dict()
		subnum = dict()
		for i in labels:
			num[i] = 0
			subnum[i] = 0

		dict_str = dict()
		dict_tree = dict()
		for attr in self.subtree:
			item = self.subtree[attr]
			if isinstance(item, str):
				dict_str[attr] = item
			elif isinstance(item, DecisionTree):
				dict_tree[attr] = item

		for attr in dict_str:
			item = self.subtree[attr]
			if item == labels[0]:
				num[labels[0]] += 1
			elif item == labels[1]:
				num[labels[1]] += 1

		for attr in dict_tree:
			item = self.subtree[attr]
			subnum[labels[0]], subnum[labels[1]] = item.count_tree()

		return num[labels[0]]+subnum[labels[0]], num[labels[1]]+subnum[labels[1]]

	def __repr__(self):
		return "<" + self.name + ">"

def Decision_Tree_Learning(examples, attributes, parent_examples):
	if len(examples) == 0:
		return Plurality_Value(parent_examples)
	elif has_only_same_classification(examples):
		return examples[0][-1]	# return the only classification which examples has
	elif len(attributes) == 0:
		return Plurality_Value(examples)
	else:
		attr_A = argmax(examples, attributes)
		print("\nBest info_gain:", attr_A)
		tree = DecisionTree(attr_A)
		tree.getProbability(examples)
		possibleValues = unique_values(examples, header.index(attr_A))
		# possibleValues = set(["Yea", "Nay"])
		# print(examples)
		# print(possibleValues)
		for v in possibleValues:
			# print("VALUE:", v)
			exs = split_examples(examples, attr_A, v)
			sub_attr = attributes[:]
			sub_attr.remove(attr_A)
			subtree = Decision_Tree_Learning(exs, sub_attr, examples)
			# print(subtree)
			tree.add_subtree(v, subtree)

	return tree

def predict(tree, test_example):
	party = labels[0]

	vote_num_node = tree
	print(vote_num_node)
	print(vote_num_node.subtree)
	print(vote_num_node.prob)

	vote_answer = 0

	return party, 0.0
	
def split_examples(examples, attribute, value):
	exs = []
	for e in examples:
		if e[header.index(attribute)] == value:
			# print(e)
			exs.append(e)
	return exs

def Plurality_Value(examples):
	possibleValues = unique_values(examples, len(examples[0]) - 1)
	count = dict()
	# initialize count dictionary
	for v in possibleValues:
		count[v] = 0
	# count for each values in examples
	for row in examples:
		count[row[-1]] += 1
	# return the value of maximum frequency
	return max(count, key=count.get)

def has_only_same_classification(examples):
	s = examples[0][-1]	# get a sample classification
	for row in examples:
		if row[-1] != s:
			return False
	return True

def argmax(examples, attributes):
	# prob = dict()
	max_info_gain = -99.0
	max_a = attributes[0]
	for a in attributes:
		temp_info_gain = Importance(header.index(a), examples)
		# temp_info_gain, prop = Importance(header.index(a), examples)
		# print(prop)
		# prob[a] = prop
		# print(len(prop))
		if temp_info_gain > max_info_gain:
			max_info_gain = temp_info_gain
			max_a = a
	# print(len(prob))
	return max_a

def Importance(a, examples):
	global num_of_examples, entropy_Goal
	# get unique possible values in examples
	possibleValues = unique_values(examples, a)
	# print(possibleValues)
	# initialize subsets dictionary which contains a list of classification
	subsets = dict()
	entropy = dict()
	for v in possibleValues:
		subsets[v] = []
		entropy[v] = 0
	# print(subsets)
	# add each classification to the corresponding subset of subsets
	for row in examples:
		# print(row[a])
		(subsets[row[a]]).append(row[-1])
	# print(subsets)
	
	# prob = dict()
	# for v in subsets:
	# 	prob[v] = 0.0


	information = 0.0
	for s in subsets:
		# print()
		# print(header[a])
		# print(s)
		l = subsets.get(s)
		# print(l)
		d = dict()
		for x in labels:
			d[x] = 0
		total = 0
		for x in l:
			d[x] += 1
			total += 1
		# print(d)

		# print(total)
		prob_labelA = d[labels[0]] / total
		prob_labelB = d[labels[1]] / total
		# prob[s] = prob_labelA
		# prob[s] = (prob_labelA, prob_labelB)
		# print(prob[s])
		# print(prob_labelA)
		# print(prob_labelB)

		# print(d[labels[0]])
		# print(d[labels[1]])

		if prob_labelA == 0.0 and prob_labelB != 0.0:
			entropy[s] = -( (prob_labelB * math.log(prob_labelB, 2.0)) )
		elif prob_labelA != 0.0 and prob_labelB == 0.0:
			entropy[s] = -( (prob_labelA * math.log(prob_labelA, 2.0)) )
		elif prob_labelA == 0.0 and prob_labelB == 0.0:
			entropy[s] = 0.0
		else:
			entropy[s] = -( (prob_labelA * math.log(prob_labelA, 2.0)) + (prob_labelB * math.log(prob_labelB, 2.0)) )

		# print("E({}={}) = -( ({}/{})log2({}/{}) + ({}/{})log2({}/{}) = {}"\
		# 	.format(header[a], s, d[labels[0]], total, d[labels[0]], total,\
		# 		d[labels[1]], total, d[labels[1]], total, entropy[s]))
		information += (total/num_of_examples) * entropy[s]

	gained_information = entropy_Goal - information
	
	# print()
	# print("Entropy of {}: {}".format(header[a], entropy))
	# print("Information from {}: {}".format(header[a], information))
	# print("Information gained from {}: {}".format(header[a], gained_information))
	# print()
	# print(prob)
	# return gained_information, prob
	return gained_information


def entropy_GoalAttribute(examples):
	global num_of_examples, entropy_Goal
	possibleValues = unique_values(examples, len(examples[0]) - 1)
	count = dict()
	# initialize count dictionary
	for v in possibleValues:
		count[v] = 0
	# count for each values in examples
	for row in examples:
		num_of_examples += 1
		count[row[-1]] += 1

	prob_labelA = count[labels[0]] / num_of_examples
	prob_labelB = count[labels[1]] / num_of_examples

	entropy = 0
	if prob_labelA == 0.0 and prob_labelB != 0.0:
		entropy = -( (prob_labelB * math.log(prob_labelB, 2.0)) )
	elif prob_labelA != 0.0 and prob_labelB == 0.0:
		entropy = -( (prob_labelA * math.log(prob_labelA, 2.0)) )
	elif prob_labelA == 0.0 and prob_labelB == 0.0:
		entropy = 0.0
	else:
		entropy = -( (prob_labelA * math.log(prob_labelA, 2.0)) + (prob_labelB * math.log(prob_labelB, 2.0)) )
	entropy_Goal = entropy

def main():
	if len(sys.argv) != 3:
		print("usage: python foo.py foo_train.csv foo_test.csv")
		return

	training_data = read_data(sys.argv[1])
	test_data = read_data(sys.argv[2])

	new_training_data = []
	for row in training_data:
		row = ['Nay' if (x != 'Yea') and (x!= labels[0]) and (x!=labels[1]) else x for x in row]
		new_training_data.append(row)

	new_test_data = []
	for row in test_data:
		row = ['Nay' if (x != 'Yea') and (x!= labels[0]) and (x!=labels[1]) else x for x in row]
		new_test_data.append(row)
	# print(new_training_data)
	# wait()
	# print(training_data)

	# print(has_only_same_classification(training_data))
	# print(Plurality_Value(training_data))

	# entropy_Goal = entropy_GoalAttribute(training_data)
	entropy_GoalAttribute(new_training_data)
	# print(Importance(header.index("Outlook"), training_data, entropy_Goal))

	# select attributes excluding label
	attributes = header[:-1]

	# for a in attributes:
	# 	print(Importance(header.index(a), training_data))

	# print(argmax(training_data, attributes))

	tree = Decision_Tree_Learning(new_training_data, attributes, [])

	print("\n\n*****************************************************")

	# num = dict()
	# num[labels[0]], num[labels[1]] = tree.count_tree()
	# totalnum = 0
	# for i in labels:
	# 	totalnum += num[i]

	# probability = dict()
	# for i in labels:
	# 	probability[i] = num[i] / totalnum
	# print(probability)

	# print_tree(tree)

	for row in new_test_data:
	# 	# print(row)
		party, prob = predict(tree, row)
		print("{},{}".format(party, prob))

def print_tree(tree, depth=0, parent=""):
	# for n in range(0, depth):
		# print("---", end="")
	# print(parent, end="")
	if (depth == 0):
		print(tree)
	subtree = tree.subtree
	# print(subtree)
	leaf = dict()
	nonleaf = dict()
	for x in subtree:
		# print(subtree[x])	
		# print(type(subtree[x]))
		if isinstance(subtree[x], DecisionTree):
			nonleaf[x] = subtree[x]
		else:
			leaf[x] = subtree[x]
	# print(leaf)
	# print(nonleaf)

	for x in leaf:
		for n in range(0, depth+1):
			print("---", end="")
		print("{}.{}: {}".format(tree, x, leaf[x]))
		# print("--{}-- {}: {}".format(tree, x, leaf[x]))
	for x in nonleaf:
		for n in range(0, depth+1):
			print("---", end="")
		# print(x)
		# print(nonleaf[x])
		# print("--{}-- {}: {}".format(tree, x, nonleaf[x]))
		print("{}.{}: {}".format(tree, x, nonleaf[x]))
		print_tree(nonleaf[x], depth+1, str(nonleaf[x]))

def unique_values(rows, col):
	return set([row[col] for row in rows])

import msvcrt as m
def wait():
    m.getch()

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

if __name__ == "__main__":
	main()
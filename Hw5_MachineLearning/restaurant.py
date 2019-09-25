import sys
import csv
import math
import collections

labels = ["Yes", "No"]
header = ["Alternate", "Bar", "Fri/Sat", "Hungry", "Patrons", "Price", "Raining", "Reservation", "Type", "WaitEstimate", "WillWait"]
num_of_examples = 0
entropy_Goal = 0

class DecisionTree():
	def __init__(self, name):
		self.name = name
		self.subtree = dict()

	def add_subtree(self, value, subtree):
		self.subtree[value] = subtree

	def print_tree(self, level=""):
		pass

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
		print(unique_values(examples, header.index(attr_A)))
		print("Best info_gain:", attr_A)
		tree = DecisionTree(attr_A)
		print("TREE: ", tree)
		print("    --subtree: ", tree.subtree)
		print("    --subtree: ", type(tree.subtree))
		print()
		possibleValues = unique_values(examples, header.index(attr_A))
		# print(examples)
		# print(possibleValues)
		for v in possibleValues:
			# print("VALUE:", v)
			exs = split_examples(examples, attr_A, v)
			sub_attr = attributes[:]
			sub_attr.remove(attr_A)
			subtree = Decision_Tree_Learning(exs, sub_attr, examples)
			print("SUBSUBTREE:", type(subtree), subtree)
			tree.add_subtree(v, subtree)

	return tree
	
def split_examples(examples, attribute, value):
	exs = []
	for e in examples:
		if e[header.index(attribute)] == value:
			exs.append(e)
	return exs

def Plurality_Value(examples):
	possibleValues = unique_values(examples, len(examples[0]) - 1)
	# print(examples)
	# print(possibleValues)
	count = dict()
	# initialize count dictionary
	for v in possibleValues:
		count[v] = 0
	# count for each values in examples
	for row in examples:
		count[row[-1]] += 1
	# return the value of maximum frequency
	print(count)
	# print(max(count, key=count.get))
	return max(count, key=count.get)

def has_only_same_classification(examples):
	s = examples[0][-1]	# get a sample classification
	for row in examples:
		if row[-1] != s:
			return False
	return True

def unique_values(rows, col):
	# for row in rows:
		# print("\t\t", row)
	return set([row[col] for row in rows])

def argmax(examples, attributes):
	print()
	print(attributes)
	max_info_gain = -99.0
	max_a = attributes[0]
	for a in attributes:
		temp_info_gain = Importance(header.index(a), examples)
		if temp_info_gain > max_info_gain:
			max_info_gain = temp_info_gain
			max_a = a
	return max_a

def Importance(a, examples):
	global num_of_examples, entropy_Goal
	# get unique possible values in examples
	possibleValues = unique_values(examples, a)
	# initialize subsets dictionary which contains a list of classification
	subsets = dict()
	entropy = dict()
	for v in possibleValues:
		subsets[v] = []
		entropy[v] = 0
	# print(subsets)
	# add each classification to the corresponding subset of subsets
	for row in examples:
		(subsets[row[a]]).append(row[-1])
	# print(subsets)
	
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
	print('{0: <20}'.format(header[a]), "\tentropy_Goal: {0:<10}".format(entropy_Goal), "information: {0:<20}".format(information), "\t gained_information:", gained_information)
	
	# print()
	# print("Entropy of {}: {}".format(header[a], entropy))
	# print("Information from {}: {}".format(header[a], information))
	# print("Information gained from {}: {}".format(header[a], gained_information))
	# print()
	return gained_information


def entropy_GoalAttribute(examples):
	print("****** entropy_GoalAttribute(examples) ******")
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

	print(count)
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
	print("****** entropy_GoalAttribute(examples) ******  finish")

def main():
	if len(sys.argv) != 2:
		print("usage: python foo.py foo_train.csv foo_test.csv")
		return

	training_data = read_data(sys.argv[1])
	# test_data = read_data(sys.argv[2])
	# print(len(training_data))

	# print(has_only_same_classification(training_data))
	# print(Plurality_Value(training_data))

	# entropy_Goal = entropy_GoalAttribute(training_data)
	entropy_GoalAttribute(training_data)
	# print(Importance(header.index("Outlook"), training_data, entropy_Goal))

	# select attributes excluding label
	attributes = header[:-1]

	# for a in attributes:
	# 	print(Importance(header.index(a), training_data))

	# print(argmax(training_data, attributes))

	tree = Decision_Tree_Learning(training_data, attributes, [])
	print("\n\n******************** TREE ****************************")
	print(tree)
	print(tree.subtree)
	print(tree.subtree['Some'])
	print(tree.subtree['None'])
	print(tree.subtree['Full'])
	print(tree.subtree['Full'].subtree)
	print(tree.subtree['Full'].subtree['No'])
	print(tree.subtree['Full'].subtree['Yes'])
	print(tree.subtree['Full'].subtree['Yes'].subtree)
	print("\n\n******************************************************")
	tree.print_tree()
	num = dict()
	num[labels[0]], num[labels[1]] = tree.count_tree()
	totalnum = 0
	for i in labels:
		totalnum += num[i]

	# print(numYes, numNo)

	probability = dict()
	for i in labels:
		probability[i] = num[i] / totalnum

	print(probability)


def print_tree(tree):
	

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

if __name__ == "__main__":
	main()
import sys
import csv
import math
import collections

labels = ["Yes", "No"]
header = ["Alternate", "Bar", "Fri/Sat", "Hungry", "Patrons", "Price", "Raining", "Reservation", "Type", "WaitEstimate", "WillWait"]

def Decision_Tree_Learning(examples, attributes, parent_examples):
	tree = []
	if len(examples) == 0:
		return Plurality_Value(parent_examples)
	elif has_only_same_classification(examples):
		return examples[0][-1]	# return the only classification which examples has
	elif len(attributes) == 0:
		return Plurality_Value(examples)
	else:
		#max_attribute = 
		pass
	return tree
	
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

def Importance(a, examples):
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
	print(subsets)
	
	for s in subsets:
		print(s)
		l = subsets.get(s)
		print(l)
		d = dict()
		for x in labels:
			d[x] = 0
		total = 0
		for x in l:
			d[x] += 1
			total += 1
		print(d)

		# subsets_invert = dict((v, k) for k, v in subsets.items())
		prob_labelA = d[labels[0]] / total
		prob_labelB = d[labels[1]] / total
		# print(prob_labelA)
		# print(prob_labelB)

		print(header[a])
		print(s)
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

		print("E({}={}) = -( ({}/{})log2({}/{}) + ({}/{})log2({}/{}) = {}"\
			.format(header[a], s, d[labels[0]], total, d[labels[0]], total,\
				d[labels[1]], total, d[labels[1]], total, entropy[s]))

		# entropy[s] = -(d[labels[0]])

	print(entropy)

def main():
	if len(sys.argv) != 2:
		print("usage: python foo.py foo_train.csv foo_test.csv")
		return

	training_data = read_data(sys.argv[1])
	# test_data = read_data(sys.argv[2])
	# print(training_data)

	# print(has_only_same_classification(training_data))
	# print(Plurality_Value(training_data))
	print(Importance(header.index("Fri/Sat"), training_data))

	attributes = header[:]
	# print(attributes)
	tree = Decision_Tree_Learning(training_data, attributes, [])


	# # P(WillWait = Yes)
	# # P(WillWait = No)
	# numYes = 0
	# numNo = 0
	# numYesNo = 0
	# for i in range(0, len(training_data)):
	# 	numYesNo += 1
	# 	if training_data[i][-1] == Yes:
	# 		numYes += 1
	# 	elif training_data[i][-1] == No:
	# 		numNo += 1
	# P_WillWait_Yes = numYes / numYesNo
	# P_WillWait_No = numNo / numYesNo
	# print("P(WillWait = {}) = {}\t\tP(WillWait = {}) = {}".format(Yes, P_WillWait_Yes, No, P_WillWait_No))

	# # get attributes
	# attributes = header[:]
	# print(attributes)
	# for i in range(0, len(attributes) - 1):
	# 	possibleValues = unique_values(training_data, i)
	# 	print(possibleValues)
	# 	for i in range(0, len(possibleValues)):
	# 		print(i)

	# entropy_S = -( ((P_WillWait_Yes) * math.log(P_WillWait_Yes, 2)) + ((P_WillWait_No) * math.log(P_WillWait_No, 2)) )
	# print("entropy(S) = {}".format(entropy_S))



def unique_values(rows, col):
	return set([row[col] for row in rows])

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

if __name__ == "__main__":
	main()
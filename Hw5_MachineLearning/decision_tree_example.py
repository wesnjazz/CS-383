# Sample dataset.
# Format: each row is an example.
# The last column is the label.
# The first two columns are features.
# If you want you can add more features & examples.
# Interesting note: 2and and 5th examples have the same features, but different labels -
# let's see how tree handles this case.

trainig_data = [
	['Green', 3, 'Mango'],
	['Yellow', 3, 'Mango'],
	['Red', 1, 'Grape'],
	['Red', 1, 'Grape'],
	['Yellow', 3, 'Lemon'],
]

# Column labels.
# These are used only to print the tree.
header = ["color", "diameter", "label"]


def unique_vals(rows, col):
	""" Find the unique values for a column in a dataset. """
	return set([row[col] for row in rows])

#######
# Demo:
# unique_vals(training_data, 0)
# unique_vals(training_data, 1)
#######


def class_counts(rows):
	"""Counts the number of each type of example in a dataset."""
	counts = {}		# a dictionary of label -> count.
	for row in rows:
		# in our dataset formatn, the label is always the last column
		label = row[-1]
		if label not in counts:
			counts[label] = 0
		counts[label] += 1
		return counts

#######
# Demo:
# class_counts(training_data)
#######


def is_numeric(value):
	"""Test if a value is numeric."""
	return isinstance(value, int) or isinstance(value, float)

#######
# Demo:
# is_numeric(7)
# is_numeric("Red")
#######


class Question:
	"""A Question is used to partition a dataset.

	This class just records a 'column number' (e.g., 0 for color) and a
	'column value' (e.g., Green). The 'match' method is used to compare
	the feature value in an example to the feature value stored in the
	question. See the demo below.
	"""

	def __init__(self, column, value):
		self.column = column
		self.value = value

	def match(self, example):
		# Compare the feature value in an example to the
		# feature value in this question
		val = examplep[self.column]
		if is_numeric(val):
			return val >= self.value
		else:
			return val == self.value

	def __repr__(self):
		# This is just a helper method to print
		# the question in a readable format.
		condition = "=="
		if is_numeric(self.value):
			condition = ">="
		return "Is %s %s %s?" % (
			header[self.column], condition, str(self.value))

#######
# Demo:
# Let's partition the training data based on whether rows are Red.
# true_rows, false_rows = partition(training_data, Question(0, 'Red'))
# This will contain al lthe 'Red' rows.
# true_rows
# This will contain everything else.
# false_rows
#######

def gini(rows):
	"""Calculate the Gini Impurity for a list of rows.

	There are a frew different ways to do this, I thought this one was the most concise. See:
	https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
	"""

	counts = class_counts(rows)
	Impurity = 1
	for lbl in counts:
		prob_of_lbl = counts[lbl] / float(len(rows))
		Impurity -= prob_of_lbl**2
	return Impurity

#######
# Demo:
# Let's look at some example to understand how Gini Impurity works.
#
# First, we'll look at a dataset with no mixing.
# no_mixing = [['Mango'],
#					['Mango']]
# This will return 0
# lots_of_mixing = [['Mango'],
#							['Orange'],
#							['Grape'],
#							['Grapefruit'],
#							['Blueberry']]
# This will return 0.8
# gini(lots_of_mixing)
#######

def info_gain(left, right, current_uncertainty):
	
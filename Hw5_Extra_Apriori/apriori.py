import sys
import csv
import math
from decimal import *

Yes = "Yea"
No = "Nay"

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

def repurpose(data):
	data_set = []
	for x in data:
		temp = set()
		for i in range(0, len(x)):
			if x[i] == 'Yea' and x[i] != 'Republican' and x[i] != 'Democrat':
				temp.add(i)
		data_set.append(temp)
	return data_set

supple=dict()

def count(data, col_num):
	vote_num = []
	vote_cnt = []
	for i in range(0, col_num):
		temp = set()
		temp.add(i)
		vote_num.append(temp)
		vote_cnt.append(0)
	# print(vote_num)
	for x in data:
		for y in x:
			temp = set()
			temp.add(y)
			if temp in vote_num:
				vote_cnt[y]+=1
	# print(vote_cnt)

	for i in range(0, col_num):
		supple[tuple(vote_num[i])] = vote_cnt[i]
	return vote_num, vote_cnt


def pruning(vote_num, vote_cnt, min_support=2):
	# print("-----------------------Pruning")
	# print(vote_num)
	# print(vote_cnt)
	newVote_num = []
	newVote_cnt = []
	for i in range(0, len(vote_num)):
		if vote_cnt[i] >= min_support:
			# print(vote_num[i])
			# x = set()
			# x.add(i)
			newVote_num.append(vote_num[i])
			newVote_cnt.append(vote_cnt[i])
	# print(newVote_num)
	# print(newVote_cnt)
	# print("------------------------Pruning--------------FINISH---------------")
	return newVote_num, newVote_cnt

def Apriori(vote_num, vote_cnt, min_support=2):
	# print("======== Apriori ==========")
	furVote_num = []
	furVote_cnt = []
	for i in range(0, len(vote_num)):
		supple[tuple(vote_num[i])] = vote_cnt[i]
	newVote_num, newVote_cnt = pruning(vote_num, vote_cnt, min_support)
	# print(newVote_num)
	# print(newVote_cnt)
	if(len(newVote_num) <= 1):
		# print(newVote_num)
		# print(newVote_cnt)
		return newVote_num, newVote_cnt
	for i in range(0, len(newVote_num)):
		for j in range(i+1, len(newVote_num)):
			union = newVote_num[i] | newVote_num[j]
			# joint = newVote_num[i] & newVote_num[j]
			# print(union)
			# print(joint)
			if union not in furVote_num:
				furVote_num.append(union)
	# print(furVote_num)
	for i in range(0, len(furVote_num)):
		cnt = 0
		for j in range(0, len(data_set)):
			# print("furVote_num[{}]:{}, data_set[{}]:{}".format(i, furVote_num[i], j, data_set[j]))
			a = furVote_num[i] & data_set[j]
			if len(a) >= len(furVote_num[i]):
				cnt+=1
				# print(a, cnt)
		furVote_cnt.append(cnt)


	# print(furVote_num)
	# print(furVote_cnt)
	frequent_further = False
	for x in furVote_cnt:
		if x >= min_support:
			frequent_further = True
			break

	# print("======== Apriori   finish ==========")
	if frequent_further == False:
		return newVote_num, newVote_cnt
	# input()
	return Apriori(furVote_num, furVote_cnt, min_support)

def Confidence(finalNum, finalCnt, confidence):
	for x in finalNum:
		subsets = powerset(set(x))
		for y in subsets:
			if len(y) <= 0:
				continue
			one = set(y)
			two = x - set(y)
			three = one | two
			if len(two) <= 0:
				continue

			if tuple(one) in supple and tuple(three) in supple:
				con_val = supple[tuple(three)] / supple[tuple(one)]
				if con_val >= confidence:
					print(str(one)[1:-1], "->", str(two)[1:-1])
					# print(str(one)[1:-1], "->", str(two)[1:-1], con_val)
				# print(str(one)[1:-1], "->", str(two)[1:-1], ":", supple[tuple(one)], supple[tuple(two)], supple[tuple(three)], supple[tuple(three)] / supple[tuple(one)])

from itertools import chain, combinations
def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

import time
start = time.time()

train_data = read_data(sys.argv[1])

col_num = len(train_data[0])
# print("col_num:", col_num)
min_support = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

data_set = repurpose(train_data)
vote_num, vote_cnt = count(data_set, col_num)
finalNum, finalCnt = Apriori(vote_num, vote_cnt, min_support)

confidence = 0.80
Confidence(finalNum, finalCnt, confidence)

end = time.time()
elapsed = end - start
# print("Time elapsed:", elapsed)
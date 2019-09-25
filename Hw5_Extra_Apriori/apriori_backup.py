import sys
import csv
import math
from decimal import *

Yes = "Yea"
No = "Nay"

def get_list_for_clustering(data, jd_data):
	cluster = []
	for i in range(0, len(data)):
		temp_list = []
		temp_list.append(str(i))
		cluster.append(temp_list)
	return cluster

def clustering(cluster_init, num_clutser = 5):
	# print("----------------------")
	# print(cluster_init)
	# print("num_clutser:", num_clutser)
	# print("len:", len(cluster_init))
	if(len(cluster_init)==num_clutser or len(cluster_init) == 1):
		return cluster_init

	avg_jd_min = 999
	min_x = -1
	min_y = -1
	for i in range(0, len(cluster_init)):
		for j in range(i+1, len(cluster_init)):
			# print(cluster_init[i], cluster_init[j])
			total_jd = 0
			total_n = 0
			for k in range(0, len(cluster_init[i])):
				for l in range(0, len(cluster_init[j])):
					x = cluster_init[i][k]
					y = cluster_init[j][l]
					if(int(x)>int(y)):
						temp = x
						x = y
						y = temp
					s = x+"-"+y
					# print(s)
					# print("x:", x, "\ty:", y, "\t", s, ":", jd_data[s])
					total_jd += jd_data[s][1]
					total_n += 1
					# if jd_data[s][1] < jd_min:
						# jd_min = jd_data[s][1]
						# min_x = int(x)
						# min_y = int(y)
					# jd_min = jd_data[s][1] if jd_data[s][1] < jd_min else jd_min
					# print("min: ", jd_min, "x:", min_x, "y:", min_y)
			# print()
			average_link = total_jd / total_n
			if average_link < avg_jd_min:
				avg_jd_min = average_link
				min_x = i
				min_y = j
			# print("total_jd:", total_jd, "\ttotal_n:", total_n)
			# print("average_link:", average_link, "\tmin_avg:", avg_jd_min, "\tx:", min_x, "\ty:", min_y)

	# print(cluster_init)
	# print(cluster_init[min_x], cluster_init[min_y])
	cluster_init[min_x] = cluster_init[min_x] + cluster_init[min_y]
	del cluster_init[min_y]
	# print(cluster_init)
	# print("Recursive Call")
	# print(cluster_init)
	# print("-----------------------\n\n")
	return clustering(cluster_init, num_clutser)

def store_jd(data):
	jd_data = dict()
	for i in range(0, len(data)):
		for j in range(i+1, len(data)):
			s = str(i)+"-"+str(j)
			# print("s: ", s, get_jaccard_index(data[i], data[j]))
			jd_data[s] = get_jaccard_index(data[i], data[j])
	# for x in jd_data:
	# 	print(x, jd_data[x])
	return jd_data

def get_jaccard_index(A, B):
	setAe = set(A)
	setBe = set(B)
	# print("setAe: ")
	# print(setAe)
	# print("setBe: ")
	# print(setBe)
	AjointB = setAe & setBe
	AunionB = setAe | setBe
	lenAjB = len(AjointB)
	lenAuB = len(AunionB)
	if (lenAjB == 0 and lenAuB == 0):
		return 0, 0
	# print("A joint B:", AjointB, lenAjB)
	# print("A union B:", AunionB, lenAuB)
	ji = 0 if lenAuB == 0 else (lenAjB/lenAuB)
	jd = 1 - ji
	# print("ji:{}\tjd:{}".format(ji, jd))
	return ji, jd

# def pruning_data(data, frequency, min_support=5):
	# pass
	# TB_before = dict()
	# for x in data:
	# 	for y in x:
	# 		set_y = set()
	# 		set_y.add(y)
	# 		print(set_y)
	# 		if y in TB_before:
	# 			TB_before[y] = TB_before[y] + 1
	# 		else:
	# 			TB_before[y] = 1
	# # print(TB_before)
	# for x in TB_before:
	# 	if(TB_before[x] < min_support):
	# 		TB_before[x] = 0
	# # print(TB_before)
	# TB_after = { k:v for k, v in TB_before.items() if v != 0 }
	# # print(TB_after)

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


import itertools
def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def Confidence(finalNum, finalCnt, confidence):
	# print(finalNum)

	for x in finalNum:
		# print(x)
		subsets = powerset(set(x))
		for y in subsets:
			if len(y) <= 0:
				continue
			one = set(y)
			two = x - set(y)
			three = one | two
			if len(two) <= 0:
				continue
			con_val = supple[tuple(three)] / supple[tuple(one)]
			if con_val >= confidence:
				# print(str(one)[1:-1], "->", str(two)[1:-1])
				print(str(one)[1:-1], "->", str(two)[1:-1], con_val)
			# print(str(one)[1:-1], "->", str(two)[1:-1], ":", supple[tuple(one)], supple[tuple(two)], supple[tuple(three)], supple[tuple(three)] / supple[tuple(one)])

	# print(supple)
	# ss = findsubsets(finalNum[0], 2)
	# print(ss)
	# print(type(ss))
	# xx = all_subsets(finalNum[0])
	# print(set(x))

from itertools import chain, combinations
 
def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))


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
print("col_num:", col_num)

data_set = repurpose(train_data)
# print(data_set)

min_support = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

vote_num, vote_cnt = count(data_set, col_num)
# print(vote_num)
# print(vote_cnt)

# pruning(vote_num, vote_cnt, min_support)
finalNum, finalCnt = Apriori(vote_num, vote_cnt, min_support)
# print(finalNum)
# print(finalCnt)

confidence = 0.5
Confidence(finalNum, finalCnt, confidence)
# c, d = Apriori(a, b, min_support)
# print(c)
# print(d)
# d, f = Apriori(c, d, min_support)
# print(d)
# print(f)


# data, frequency = count(data_set)
# pruning_data(data_set, min_support)




# jd_data = store_jd(data_set)
# num_clutser = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

# cluster_init = get_list_for_clustering(data_set, jd_data)
# print(cluster_init)
# cluster = clustering(cluster_init, num_clutser)
# print(cluster)

end = time.time()
elapsed = end - start
print("Time elapsed:", elapsed)
import sys
import csv
import math
from decimal import *

"""
P(democrat) = count(democrat) / (count(democrat) + count(republican))
"""

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

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

def repurpose(data):
	data_set = []
	for x in data:
		temp = []
		for i in range(0, len(x)):
			if x[i] == 'Yea' and x[i] != 'Republican' and x[i] != 'Democrat':
				temp.append(i)
		data_set.append(temp)
	return data_set

# import time
# start = time.time()

train_data = read_data(sys.argv[1])
data_set = repurpose(train_data)
jd_data = store_jd(data_set)
num_clutser = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

cluster_init = get_list_for_clustering(data_set, jd_data)
# print(cluster_init)
cluster = clustering(cluster_init, num_clutser)
# print(cluster)
for i in range(0, len(cluster)):
	# cluster[i]=sorted(cluster[i])
	cluster[i].sort(key=int)
# print(cluster)
for x in cluster:
	for y in range(0, len(x)):
		if(y+1 == len(x)):
			print(x[y], end="")
			continue;
		print(x[y], end=", ")
		# print(", ".join([y]))
		# print(y,  sep=", ", end=", ")
		# print(", ".join(y))
	print()

# end = time.time()
# elapsed = end - start
# print("Time elapsed:", elapsed)
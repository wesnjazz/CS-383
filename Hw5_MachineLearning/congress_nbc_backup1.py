import sys
import csv
import math

"""
P(democrat) = count(democrat) / (count(democrat) + count(republican))
"""

Republican = "Republican"
Democrat = "Democrat"
Yes = "Yea"
No = "Nay"

def main():
	train_data = read_data(sys.argv[1])
	test_data = read_data(sys.argv[2])
	numR, numD = countParty(train_data)
	totalRD = numR + numD
	pR = numR / totalRD
	pD = numD / totalRD

	# print("Total:", totalRD, "\t# of", Republican, ":", numR, "\t# of", Democrat, ":", numD)

	trainedR, trainedD = train(train_data, numR, numD)
	predict(test_data, trainedR, trainedD, pR, pD)

def countParty(data):
	"""
	count number of Democrats and Republicans
	"""
	numR = numD = 0
	for x in data:
		if x[-1] == Republican:
			numR += 1
		elif x[-1] == Democrat:
			numD += 1
	return numR, numD

def marginalCount(data, vote, party, answer):
	c = 0
	for x in data:
		if x[-1] == party and x[vote] == answer:
			c += 1
	return c

def train(data, numR, numD):
	trainedR = []	# marginal CPT for each votes(e.g, P(vote1=Yes|party=Republican) ) of Republican
	trainedD = []	# marginal CPT of Democrat
	for i in range(0, len(data[0]) - 1):	# loop from 0 to max number of votes
		trainedR.append([0,0,0])	# initialize trained set of Republican
		trainedD.append([0,0,0])	# initialize trained set of Democrat
	# print("**************************************")
	# print(trainedR)
	# print(trainedD)

	for cols in range(0, len(data[0]) - 1):	# loop from 0 to max number of votes
		validvoteR = 0
		validvoteD = 0
		for rows in range(0, len(data)):	# loop from 0 to
			if data[rows][cols] == Yes or data[rows][cols] == No:
				if data[rows][-1] == Republican:
					validvoteR += 1
					if data[rows][cols] == Yes:
						trainedR[cols][0] += 1
					else:
						trainedR[cols][1] += 1
				elif data[rows][-1] == Democrat:
					validvoteD += 1
					if data[rows][cols] == Yes:
						trainedD[cols][0] += 1
					else:
						trainedD[cols][1] += 1

		trainedR[cols][2] = validvoteR
		trainedD[cols][2] = validvoteD
		# trainedR[cols] /= validvoteR
		# trainedD[cols] /= validvoteD

	# print(trainedR)
	# print(trainedD)
	# print("**************************************")
	# for i in range(0, len(trainedR)):
	# 	print("P(Vote={}|{}) = {}\t\t\t\tP(Vote={}|{}) = {}".format(i+1, Republican, trainedR[i][0]/trainedR[i][2], i+1, Democrat, trainedD[i][0]/trainedD[i][2]))


	return trainedR, trainedD

def predict(test_data, trainedR, trainedD, pR, pD):
	# predict_result = []
	for i in range(0, len(trainedR)):
		rr = (trainedR[i][0]/trainedR[i][2]) * pR
		dd = (trainedD[i][0]/trainedD[i][2]) * pD
		# print("P({}|Vote={}) = {}\t\t\t\tP({}|Vote={}) = {}".format(Republican, i+1, rr, Democrat, i+1, dd))
	numR = numD = 0
	for r in test_data:
		numYea = 0
		numNay = 0
		for x in range(0, len(r)):
			if r[x] == Yes:
				numYea += 1
			elif r[x] == No:
				numNay += 1
		numYeaNay = numYea + numNay
		# print(numYea, numNay, numYeaNay)
		isR = 1.0
		isD = 1.0
		isRlog = 0
		isDlog = 0
		# print(r)
		for x in range(0, len(r)):
			if r[x] == Yes:
				# print("R=Yes", (trainedR[x][0]+1), "divide by", (trainedR[x][2]+1))
				isR = isR * ( (trainedR[x][0]+1) / (trainedR[x][2]+numYeaNay) )
				isRlog = isRlog + math.log( (trainedR[x][0]+1) / (trainedR[x][2]+numYeaNay) )
				# print("D=Yes", (trainedD[x][0]+1), "divide by", (trainedD[x][2]+1))
				isD = isD * ( (trainedD[x][0]+1) / (trainedD[x][2]+numYeaNay) )
				isDlog = isDlog + math.log( (trainedD[x][0]+1) / (trainedD[x][2]+numYeaNay) )
			if r[x] == No:
				# print("R=Nay", (trainedR[x][1]+1), "divide by", (trainedR[x][2]+1))
				isR = isR * ( (trainedR[x][1]+1) / (trainedR[x][2]+numYeaNay) )
				isRlog = isRlog + math.log( (trainedR[x][1]+1) / (trainedR[x][2]+numYeaNay) )
				# print("D=Nay", (trainedD[x][1]+1), "divide by", (trainedD[x][2]+1))
				isD = isD * ( (trainedD[x][1]+1) / (trainedD[x][2]+numYeaNay) )
				isDlog = isDlog + math.log( (trainedD[x][1]+1) / (trainedD[x][2]+numYeaNay) )

	# for r in test_data:
	# 	isR = 0
	# 	isD = 0
	# 	print(r)
	# 	for x in range(0, len(r)):
	# 		if r[x] == Yes:
	# 			# print("R=Yes", (trainedR[x][0]+1), "divide by", (trainedR[x][2]+1))
	# 			isR = isR + math.log( (trainedR[x][0]+1) / (trainedR[x][2]+1) )
	# 			# print("R=Yes", isR)
	# 			# print("D=Yes", (trainedD[x][0]+1), "divide by", (trainedD[x][2]+1))
	# 			isD = isD + math.log( (trainedD[x][0]+1) / (trainedD[x][2]+1) )
	# 			# print("D=Yes", isD)
	# 		if r[x] == No:
	# 			# print("R=Nay", (trainedR[x][1]+1), "divide by", (trainedR[x][2]+1))
	# 			isR = isR + math.log( (trainedR[x][1]+1) / (trainedR[x][2]+1) )
	# 			# print("R=Nay", isR)
	# 			# print("D=Nay", (trainedD[x][1]+1), "divide by", (trainedD[x][2]+1))
	# 			isD = isD + math.log( (trainedD[x][1]+1) / (trainedD[x][2]+1) )
	# 			# print("D=Nay", isD)

		# print("isR:", isR, "\tisD:", isD)
		# print("isRlog:", isRlog, "\tisDlog:", isDlog)
		isR *= pR
		isD *= pD
		isRlog += math.log(pR)
		isDlog += math.log(pD)
		# print("isR:", isR, "\tisD:", isD)
		# print("isRlog:", isRlog, "\tisDlog:", isDlog)
		# isR = math.log(isR)
		# isD = math.log(isD)
		# print("isR:", isR, "\tisD:", isD)
		normalR = isR / (isR + isD)
		normalD = isD / (isR + isD)
		normalRlog = math.exp(isRlog) / (math.exp(isRlog) + math.exp(isDlog))
		normalDlog = math.exp(isDlog) / (math.exp(isRlog) + math.exp(isDlog))
		# print("normalRlog: {}% \tnormalDlog: {}%".format(normalRlog, normalDlog))
		# print("normalR:", normalR, "\tnormalD:", normalD)
		# print("normalR: {}% \tnormalD: {}%".format(normalR, normalD))

		if isRlog >= isDlog:
			print("{},{}".format(Republican, normalR))
			numR += 1
		else:
			print("{},{}".format(Democrat, normalD))
			numD += 1
	# print("{}/{}".format(numD, numR))

def read_data(filename):
	with open(filename) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
	return data

if __name__ == "__main__":
	main()
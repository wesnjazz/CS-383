'''
class RV
	- name: {Rain, Late}
	- status: {True, False}
	- cpt table given markov blanket
	- getProbability(selfStatus=, givenStatus=):
			P(R|T) if self.name == "Rain":
						if self.status == +r: 0.470588235
						elif self.status == -r: 0.529411765
			P(L|T) if   +l: 0.3
							-l: 0.7

	- resample(probability):
		u = uniform distribution random number [0, 1]
		if u <= pobability:
			self.status = True
		else:
			self.status = False







0.47058823529411764
0.4
0.42
0.476

hw3

Algorithm:
function GIBBS-ASK(X, e, bn, N ) returns an estimate of P(X|e)
	local variables: 	N, a vector of counts for each value of X , initially zero
						Z, the nonevidence variables in bn
						x, the current state of the network, initially copied from e

	initialize x with random values for the variables in Z
	for j = 1 to N do
		for each Zi in Z do
			set the value of Zi in x by sampling from P(Zi|mb(Zi))
			N[x] ← N[x] + 1 where x is the value of X in x
	return NORMALIZE(N)

Data structure:
X:	class Node
e:
bn:
N:
locN:
locZ:
locx:

'''

'''
class RV
	- name: {Rain, Late}
	- status: {True, False}
	- cpt table given markov blanket
	- getProbability(selfStatus=, givenStatus=):
			P(R|T) if self.name == "Rain":
						if self.status == +r: 0.470588235
						elif self.status == -r: 0.529411765
			P(L|T) if   +l: 0.3
							-l: 0.7

	- resample(probability):
		u = uniform distribution random number [0, 1]
		if u <= pobability:
			self.status = True
		else:
			self.status = False
'''
import random

class RV():
	def __init__(self, name):
		self.name = name
		u = random.random()
		if u <= 0.50:
			self.status = True
		else:
			self.status = False

	def getProbability(self, selfStatus):	# givenStatus = True, because Traffic=True is given
		if self.name == "Rain":
			if selfStatus == True: return 0.470588235	# P(+r|+t) = By Bayes' Rule, it is calculated as 0.470588235
			else:	return 0.529411765						# P(-r|+t) = By Bayes' Rule, it is calculated as 0.529411765
		elif self.name == "Late":
			if selfStatus == True: return 0.3			# P(+l|+t) = By its given CPT, it is 0.3
			else: return 0.7									# P(-l|+t) = By its given CPT, it is 0.7

	def resample(self, givenProbability):
		'''
		Resample self.status by its given probability.
		Divide the range from 0.0 to 1.0 by its given probability and then choose True of False based upon the u value
		ex) if given probability is 0.3, then 	if u <= 0.3 -> it is True
															if u > 0.3 -> it is False
		'''
		u = random.random()	# get a uniformly distributed random number in range [0, 1)
		# print("random u:", u)
		if u <= givenProbability:
			self.status = True
		else:
			self.status = False

	def printSelf(self):
		print("name:", self.name, "\tstatus:", self.status)


class SampleCounter():
	def __init__(self):
		self.stateDict = {
			"True, True, True": 0,	"True, True, False": 0,
			"True, False, True": 0, "True, False, False": 0,
			"False, True, True": 0, "False, True, False": 0,
			"False, False, True": 0, "False, False, False": 0 }

	def countUp(self, status):
		self.stateDict[status] = self.stateDict[status] + 1

	def printSelf(self):
		print(self.stateDict)

def MCMC(N):
	# initialize all random variables randomly
	Rain = RV("Rain")
	Traffic = RV("Traffic")
	Late = RV("Late")

	# set the evidence variable, Traffic = True
	Traffic.status = True

	nonEvidence = [Rain, Late]

	sc = SampleCounter()
	for i in range(N):
		print(i)
		newState = ["True", "True", "True"]
		for r in nonEvidence:
			r.resample(r.getProbability(r.status))
			r.printSelf()
			if r.name == Rain.name:
				newState[0] = str(r.status)
			elif r.name == Late.name:
				newState[2] = str(r.status)
		print(newState)
		newStateStr = str(newState[0]) + ", " + str(newState[1]) + ", " + str(newState[2])
		sc.countUp(newStateStr)

	sc.printSelf()

def main():
	# mc = SampleCounter("True, True, True")
	# mc.countUp("True, True, True")
	# mc.countUp("True, True, True")
	# mc.countUp("True, True, True")
	# mc.countUp("False, True, True")
	# mc.countUp("False, True, False")
	# mc.countUp("False, False, False")
	# mc.countUp("False, False, False")
	# mc.countUp("False, False, False")
	# mc.countUp("False, False, False")
	# mc.countUp("False, False, False")
	# mc.countUp("False, False, False")
	# mc.printSelf()

	MCMC(10)

	# Rain = RV("Rain")
	# Rain.printSelf()
	# Traffic = RV("Traffic", True)
	# Late = RV("Late", True)

	# print(Rain.getProbability(True))
	# Rain.resample(Rain.getProbability(True))
	# Rain.printSelf()
	# print(Rain.getProbability(False))
	# Rain.resample(Rain.getProbability(False))
	# Rain.printSelf()
	# print(Late.getProbability(True))
	# Late.resample(Late.getProbability(True))
	# Late.printSelf()
	# print(Late.getProbability(False))
	# Late.resample(Late.getProbability(False))
	# Late.printSelf()
	
	# print(Rain.getProbability(False))
	# print(Rain.getProbability(True) + Rain.getProbability(False))
	# print(Late.getProbability(True))
	# print(Late.getProbability(False))
	# print(Late.getProbability(True) + Late.getProbability(False))

	# print(0.470588235)
	# print(0.4)
	# print(0.43)
	# print(0.475)

if __name__ == "__main__":
	main()

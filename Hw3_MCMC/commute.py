'''
Name: DongWon Park
Work by: alone
Last update: 2018.10.25.
CS 383 Homework #3
Markov Chain Monte Carlo (Gibbs sampling)
'''

'''
class BayesNode
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

class BayesNode():
	"""
	name: {"Rain", "Traffic", "Late"}
	status: {True, False}
	"""
	def __init__(self, name):
		# set the name and initialize the status randomly with the probability of 0.5
		self.name = name
		u = random.random()
		if u <= 0.50:
			self.status = True
		else:
			self.status = False

	def getProbability(self, selfStatus):	# givenStatus = True, because Traffic=True is given
		# ex) P(Rain|Traffic=true) = P(+r|+t) = Rain.getProbability(Rain)
		#		P(Late=False|Traffic=True) = P(-l|+t) = Late.getProbability(Late)  # Late.status = False
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
		if u <= givenProbability:
			self.status = True
		else:
			self.status = False

	def printSelf(self):
		print("name:", self.name, "\tstatus:", self.status)


class SampleCounter():
	"""
	Container class for tracking the number of each generated samples
	"""
	def __init__(self):
		self.stateDict = {
			"True, True, True": 0,	"True, True, False": 0,
			"True, False, True": 0, "True, False, False": 0,
			"False, True, True": 0, "False, True, False": 0,
			"False, False, True": 0, "False, False, False": 0 }

	def countUp(self, status):
		# count up the given sample
		self.stateDict[status] = self.stateDict[status] + 1

	def query(self, nodeName, status):
		if nodeName == "Rain":
			if status == True:
				return self.stateDict["True, True, True"] + self.stateDict["True, True, False"] + self.stateDict["True, False, True"] + self.stateDict["True, False, False"]
			elif status == False:
				return self.stateDict["False, True, True"] + self.stateDict["False, True, False"] + self.stateDict["False, False, True"] + self.stateDict["False, False, False"]
		elif nodeName == "Late":
			if status == True:
				return self.stateDict["True, True, True"] + self.stateDict["True, False, True"] + self.stateDict["False, True, True"] + self.stateDict["False, False, True"]
			elif status == False:
				return  + self.stateDict["True, True, False"] + self.stateDict["True, False, False"] + self.stateDict["False, True, False"] + self.stateDict["False, False, False"]

	def printSelf(self):
		print(self.stateDict)


def MCMC(nodeName, N):
	# print("\n# of samples:", N)

	# initialize all random variables randomly
	Rain = BayesNode("Rain")
	Traffic = BayesNode("Traffic")
	Late = BayesNode("Late")

	# set the evidence variable, Traffic = True
	Traffic.status = True

	# set the non-evidence variable list
	nonEvidence = [Rain, Late]

	# create a container which keep tracks of number of each sampling
	sc = SampleCounter()

	# MCMC (Gibbs Sampling) algorithm
	for i in range(N):
		newState = ["True", "True", "True"]
		for r in nonEvidence:
			r.resample(r.getProbability(r.status))
			if r.name == Rain.name:
				newState[0] = str(r.status)
			elif r.name == Late.name:
				newState[2] = str(r.status)
		newStateStr = str(newState[0]) + ", " + str(newState[1]) + ", " + str(newState[2])
		sc.countUp(newStateStr)

	# count samplings
	trueCount = sc.query(nodeName, True)
	falseCount = sc.query(nodeName, False)
	# normalize
	normalizedTrue = trueCount / (trueCount + falseCount)	
	normalizedFalse = falseCount / (trueCount + falseCount)
	# print the result
	print(normalizedTrue)

def main():
	exactProbability = ( 0.8 * 0.1 ) / ( 0.8 * 0.1 + 0.1 * 0.9)
	print(exactProbability)
	MCMC("Rain", 10)
	MCMC("Rain", 100)
	MCMC("Rain", 1000)

if __name__ == "__main__":
	main()

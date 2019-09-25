import sys

def readInitialStateFile(file):
	with open(sys.argv[1], 'rt') as f:
		resultStr = ""	# result string from the input
		initialState = []	# list of initial state
		width, height = 0, 0
		while True:
			""" remove leading/ending whitespaces, 
				then also remove newline and space,
				then split into list """
			line = f.readline().strip().replace("\n", "").split()
			for c in line:
				initialState.append(c)
			height += 1
			if width == 0: width = len(line)
			if not line:
				height -= 1
				break	# break if reached EOF

		return initialState, width, height 	# return the resulting list

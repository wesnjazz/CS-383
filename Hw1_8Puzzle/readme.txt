Name: DongWon Park

Fun fact:
	- I am new to python. Most stuck point was dealing with python data structures.

Work with:
	- alone

Uninformed search:
	- I did BFS and Uniform Cost Search for extra credit

Heuristic:
	- I used the manhattan distance

Instructions:
	- python bfs.py puzzle.txt
	- python uniformcost.py puzzle.txt
	- python astar.py puzzle.txt

Summary of performance:
	Mine works better on BFS which I used the hashSet for finding nodes instead of iterating through whole data structure.
	Mine works okay on Uniform Cost Search and A* Search.
	- puzzle_2x2_1.txt
		- no solution
	- puzzle_3x3_1.txt
		- the test case given in the homework sheet
		- BFS: max expanded node: 43,062
		- Uniform: 174,082
		- A*: 153,383

Notes or warning:
	- I think BFS works fine, but I am not sure of uniform and A*
	- Actually, BFS works much faster than UniformCost and A*
	- I think it is the matter of how I implement a queue in python
	- my program works on any size puzzle, even not a square
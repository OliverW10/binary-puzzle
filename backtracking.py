import math
import numpy as np

test1 = np.array(
	[[1, 0, 0, 1, 1, 0],
	[0, 1, 1, 0, 0, 1],
	[0, 1, 0, 1, 1, 0],
	[1, 0, 0, 1, 0, 1],
	[0, 1, 1, 0, 1, 0],
	[1, 0, 1, 0, 0, 1]])

test2 = np.array(
	[[1, 0, 0, 1, 1, 0],
	[0, 1, 1, 0, 0, 1],
	[0, 1, 0, 1, 1, 0],
	[1, 0, 0, 1, 1, 0],
	[0, 1, 1, 0, 1, 0],
	[1, 0, 1, 0, 0, 1]])

size = 6

# define starting configuration here
start_board = np.full((size, size), 2)
start_board[1, 1] = 1
start_board[5, 1] = 1
start_board[1, 2] = 1
start_board[3, 2] = 1
start_board[2, 3] = 0
start_board[5, 3] = 1
start_board[1, 4] = 1
start_board[3, 5] = 0
start_board[4, 5] = 0
# start_board[5, 5] = 0

threes = [[1, 1, 1], [0, 0, 0]]

placements = []
def checkBoard(board):
	# check number per row
	for i in range(size):
		row = board[i]
		if len([x for x in row if x == 0]) > 3 or len([x for x in row if x == 1]) > 3:
			return False

		col = np.rot90(board)[i]
		if len([x for x in col if x == 0]) > 3 or len([x for x in col if x == 1]) > 3:
			return False

	# check threes in a rows		
	for i in range(1, size-1):
		for j in range(size):
			horz = [board[i-1][j], board[i][j], board[i+1][j]]
			if horz == threes[0] or horz == threes[1]:
				return False

	# check threes in cols
	for i in range(size):
		for j in range(1, size-1):
			vert = [board[i][j-1], board[i][j], board[i][j+1]]
			if vert == threes[0] or vert == threes[1]:
				return False

	# # checks to see if all the rows and unique
	if len(np.unique(board, axis=0)) != size:
		return False
	# # checks to see if all the columns are unique
	if len(np.unique(board, axis=1)) != size:
		return False

	return True

def findEmpty(board):
	# finds the first square with a two from left to right top to bottom
	allPos = np.where(board==2)
	if len(allPos[1]) == 0:
		return False
	return (allPos[0][0], allPos[1][0])

def branch(board, callback = lambda *x:x):
	callback(board)
	# checks if we filled every square, meaning we found a solution
	pos = findEmpty(board)
	if type(pos) == bool and checkBoard(board) == True:
		return True, board

	# sets the next undecided square to 0
	board[pos[0], pos[1]] = 0
	# checks if its valid (so far)
	if checkBoard(board):
		# if it is continue recursively branching down
		out = branch(board, callback)
		if out[0] == True: # found a solution in this branch
			return True, out[1]

	# sets the next undecided square to 1
	board[pos[0], pos[1]] = 1
	# checks if its valid (so far)
	if checkBoard(board):
		# if it is continue recursively branching down
		out = branch(board, callback)
		if out[0] == True: # found a solution in this branch
			return True, out[1]

	board[pos[0], pos[1]] = 2
	return False, [] # didnt find a solution in this branch

def printBoard(board):
	for i in range(size):
		for j in range(size):
			print(board[i][j], end="")
		print("")

printBoard(branch(start_board, printBoard)[1])
	
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
	[1, 0, 0, 1, 0, 1],
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
	return True

def findEmpty(board):
	allPos = np.where(board==2)
	if len(allPos[1]) == 0:
		return False
	return (allPos[0][0], allPos[1][0])

def branch(board):
	pos = findEmpty(board)
	if pos == False:
		return True, board

	board[pos[0], pos[1]] = 0
	if checkBoard(board):
		out = branch(board)
		if out[0] == True:
			return True, out[1]

	board[pos[0], pos[1]] = 1
	if checkBoard(board):
		out = branch(board)
		if out[0] == True:
			return True, out[1]

	board[pos[0], pos[1]] = 2
	return False, []

def printBoard(board):
	for i in range(size):
		for j in range(size):
			print(board[i][j], end="")
		print("")

printBoard(branch(start_board)[1])
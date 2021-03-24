import numpy as np
import time

class BinaryPuzzle:
	def __init__(self):
		self.board = []
		self.initilized = False

	def readAidensFormat(self, string: str):
		# reads start config in the format "1xx\nx1x\nx00"
		# defines the full array flattened with x as undefined and \n as seperators
		rows = string.split("\n")
		self.board = []
		for i in rows:
			self.board.append([])
			for j in i:
				if j == "0":
					self.board[-1].append(0)
				elif j == "1":
					self.board[-1].append(1)
				else:
					self.board[-1].append(-1)

		self.board = np.array(self.board, dtype=np.int8)
		self.initilized = True

	def readFullArr(self, arr):
		# reads start confiig in the format [[1, -1, -1], [-1, 1, -1], [-1, 0, 0]
		# defines to the full 2d array with -1 as undefined
		self.board = np.array(arr, dtype=np.int8)
		self.initilized = True

	def readPosArr(self, arr, size = 6):
		# reads the config in the format [ *[x, y, n] ]
		# defines the starting numbers as positions everything else is undefined
		# is size x size in size
		self.board = np.full((size, size), -1, dtype=np.int8)
		for i in arr:
			self.board[i[1]][i[0]] = i[2]

		self.initilized = True

	@staticmethod
	def checkBoard(board):
		maxNum = len(board)//2 # maximum number of each letter per row and col
		# check count of each number per per row
		for i in range(len(board)):
			row = board[i]
			col = np.rot90(board)[i]

			for line in [row, col]:
				if len([x for x in line if x == 0]) > maxNum or len([x for x in line if x == 1]) > maxNum:
					return False

		# check threes in a rows
		# goes through every grid square except all the edge ones
		for i in range(1, len(board)-1):
			for j in range(len(board)):
				# gets gets the squares one left, this one and one right
				horz = [board[i-1][j], board[i][j], board[i+1][j]]
				# gets gets the squares one up, this one and one down
				vert = [board[j][i-1], board[j][i], board[j][i+1]]

				# for both horz and vert
				for line in [horz, vert]:
					# check if they are either three zeros of three ones
					if line == [0]*3 or line == [1]*3:
						return False

		if not np.any(board[:, 0] == -1): # only cares about uniqueness for full boards

			# # checks to see if all the rows and unique
			# np.unique returns the given array with duplicates removed
			if len(np.unique(board, axis=0)) != len(board):
				return False
			# # checks to see if all the columns are unique
			if len(np.unique(board, axis=1)) != len(board):
				return False

		# none of the checks failed
		return True

	@staticmethod
	def findEmpty(board):
		# finds the first square with a -1 from left to right top to bottom
		allPos = np.where(board==-1)
		if len(allPos[1]) == 0:
			return False
		return (allPos[0][0], allPos[1][0])

	@staticmethod
	def printBoard(board):
		for row in board:
			for num in row:
				if num == -1:
					print(" ", end="")
				else:
					print(num, end="")
			print("")
		print("\n\n")
		time.sleep(0.05)

	def branch(self, board, callback):
		callback(board)

		# checks if we filled every square, meaning we found a solution
		pos = self.findEmpty(board)
		if pos == False and self.checkBoard(board) == True:
			return True, board

		for test in [0, 1]:
			# sets the next undecided square to both 0 and 1
			board[pos[0], pos[1]] = test
			# checks if its valid (so far)
			if self.checkBoard(board):
				# if it is continue recursively branching down
				out = self.branch(board, callback)
				if out[0] == True: # found a solution
					return True, out[1]

		# if this branch isnt valid revert the changes and back out
		board[pos[0], pos[1]] = -1
		return False, []

	def solve(self, display=False):
		if display:
			func = self.printBoard
		else:
			func = lambda *x:x

		if self.initilized:
			return self.branch(self.board, func)[1]
		else:
			raise Exception("Not initilized yet")			

if __name__ == "__main__":
	import json

	with open(r"examples.json") as f:
		examples = json.loads(f.read())

	for n, puz in enumerate(examples["puzzles"]):
		print(f"Puzzle {n+1}")
		puzzle = BinaryPuzzle()
		puzzle.readAidensFormat(puz)
		puzzle.printBoard(puzzle.solve(display=False))

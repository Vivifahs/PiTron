class Grid(object):
	def __init__(self, len):
		self.board = [[0 for i in range(len)] for i in range(len)]
	def flip(self, x, y, colorNum):
		if self.board[x - 1][y - 1] == str(colorNum):
                        self.board[x - 1][y - 1] = 0
		else:
                        self.board[x - 1][y - 1] = colorNum
	def read(self, x, y):
		return self.board[x - 1][y - 1]
	def __str__(self):
		stri = ""
		for row in range(len(self.board)):
			for col in range(len(self.board)):
				stri = stri + str(self.board[row][col]) + " "
			stri = stri + "\n"
		return stri

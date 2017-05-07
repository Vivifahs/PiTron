from gameobject import GameObject

class Grid(object):
	def __init__(self, cols, rows, cellsize):
		self.board = [[None for i in range(cols)] for i in range(rows)]
		self.rows = rows
		self.cols = cols

		# Used by GameObjects to set their graphics
		self.cellsize = cellsize

	def setCell(self, item, col, row):
		self.board[row][col] = item

	def getCell(self, col, row):
		return self.board[row][col]

	def cellOccupied(self, col, row):
		return self.board[row][col] is not None

	def render(self, surface):
		for row in range(self.rows):
			for col in range(self.cols):
				item = self.getCell(col, row)

				if isinstance(item, GameObject):
					item.render(surface)

	def __str__(self):
		gstr = ''

		for row in range(self.rows):
			for col in range(self.cols):
				item = self.board[row][col]

				if item is None:
					item = '~'

				gstr += str(item)

			gstr += '\n'

		return gstr

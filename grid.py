from gameobject import GameObject
import pygame

class Grid(object):
	def __init__(self, cols, rows, cellsize, offsetx, offsety):
		self.board = [[None for i in range(cols)] for i in range(rows)]
		self.rows = rows
		self.cols = cols

		# Used by GameObjects to set their graphics
		self.cellsize = cellsize

		# Positioning
		self.offsetx = offsetx
		self.offsety = offsety

		# Rendering
		self.image = pygame.Surface((cols * cellsize, rows * cellsize))
		self.image.set_colorkey((0,0,0))
		
		self.grid_bgnd_a = pygame.image.load("grid.png").convert()
		self.grid_bgnd_b = pygame.image.load("inv_grid.png").convert()
		self.grid_bgnd_c = pygame.image.load("off_grid.png").convert()

		self.grid_bgnd = self.grid_bgnd_a

		self.grid_rect = self.image.get_rect()

	def setCell(self, item, col, row):
		self.board[row][col] = item

	def getCell(self, col, row):
		return self.board[row][col]

	def cellOccupied(self, col, row):
		return self.board[row][col] is not None

	def clear(self):
		for row in range(self.rows):
			for col in range(self.cols):
				self.setCell(None, col, row)

	def setImage(self, image):
		if self.grid_bgnd is not image:
			self.grid_bgnd = image

	def render(self, surface, hide=False):
		self.image.blit(self.grid_bgnd, (0, 0))

		for row in range(self.rows):
			
			#s1 = (self.offsetx, self.cellsize * row + self.offsety)
			#e1 = (self.cols * self.cellsize + self.offsetx, s1[1])
			#pygame.draw.line(surface, (128, 0, 255), s1, e1)

			for col in range(self.cols):

				#s2 = (self.cellsize * col + self.offsetx, self.offsety)
				#e2 = (s2[0], self.rows * self.cellsize + self.offsety)
				#pygame.draw.line(surface, (128, 0, 255), s2, e2)

				item = self.getCell(col, row)

				if item is not None:
					if not hide:
						item.render(self.image)

		return self.image

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

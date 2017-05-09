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

		#self.image = pygame.Surface((cols * cellsize, rows * cellsize))
		#self.image.set_alpha(128)
		#self.image.fill((50, 0, 255))
		self.image = pygame.image.load("grid2.png").convert()
		self.img_rect = self.image.get_rect()

		self.img_rect[0] += self.offsetx
		self.img_rect[1] += self.offsety

	def setCell(self, item, col, row):
		self.board[row][col] = item

	def getCell(self, col, row):
		return self.board[row][col]

	def cellOccupied(self, col, row):
		return self.board[row][col] is not None

	def render(self, surface):
		#pygame.draw.rect(surface, (10,0,255), self.rect)

		renderitems = []

		for row in range(self.rows):
			
			s1 = (self.offsetx, self.cellsize * row + self.offsety)
			e1 = (self.cols * self.cellsize + self.offsetx, s1[1])
			#pygame.draw.line(surface, (128, 0, 255), s1, e1)

			for col in range(self.cols):

				s2 = (self.cellsize * col + self.offsetx, self.offsety)
				e2 = (s2[0], self.rows * self.cellsize + self.offsety)
				#pygame.draw.line(surface, (128, 0, 255), s2, e2)

				item = self.getCell(col, row)

				if isinstance(item, GameObject):
					#item.render(surface)
					renderitems.append(item)

		#surface.blit(self.image, (self.offsetx, self.offsety))
		surface.blit(self.image, self.img_rect)

		for item in renderitems:
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

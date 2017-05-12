from random import randint
import pygame

# Base class for all Game Objects
class GameObject(object):
	def __init__(self, x, y, board, color=[255, 255, 255]):
		self.x = x
		self.y = y

		# Keep reference to main board and insert self at (x, y)
		self.board = board
		self.board.setCell(self, x, y)

		# Create image square and keep reference to original color
		self.image = pygame.Surface((self.board.cellsize, self.board.cellsize))
		self.color = color

		self.image.fill(self.color)

	def randposition(self):
		self.board.setCell(None, self.x, self.y)

		empty = False
		while not empty:
			self.x = randint(0, self.board.cols - 1)
			self.y = randint(0, self.board.rows - 1)

			if not self.board.cellOccupied(self.x, self.y):
				empty = True

		self.board.setCell(self, self.x, self.y)

	# Change color of image
	def setColor(self, color):
		self.image.fill(color)

    # Change color back to original
	def resetColor(self):
		self.image.fill(self.color)

	# Update logic
	def update(self, delta):
		raise NotImplementedError

	# Draw to screen
	def render(self, surface):
		x = self.x * self.board.cellsize
		y = self.y * self.board.cellsize

		surface.blit(self.image, (x, y))

	def __str__(self):
		return 'O'

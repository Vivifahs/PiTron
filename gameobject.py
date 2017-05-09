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
		x = self.x * self.board.cellsize + self.board.offsetx
		y = self.y * self.board.cellsize + self.board.offsety

		#print 'drawing {} at ({},{})'.format(str(self), x, y)
		surface.blit(self.image, (x, y))

	def __str__(self):
		return 'O'

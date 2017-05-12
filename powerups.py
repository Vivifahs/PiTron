from random import randint
from gameobject import GameObject
import pygame

class Powerup(GameObject):

	FONT = None

	def __init__(self, board, lifetime=5000, color=[255,255,255]):
		GameObject.__init__(self, 0, 0, board, color)

		Powerup.FONT = pygame.font.SysFont("system", board.cellsize + 5)
		self.image.blit(Powerup.FONT.render(str(self), 0, (255,255,255)), (1,0))

		self.lifetime = lifetime
		self.currtime = self.lifetime
		self.used = False

		self.randposition()

	def applyEffectTo(self, snake):
		raise NotImplementedError

	def update(self, delta):
		self.currtime -= delta

		if self.currtime <= 0:
			self.used = True

	def __str__(self):
		return 'P'

class GhostPU(Powerup):
	def __init__(self, board):
		Powerup.__init__(self, board, lifetime=2500, color=[150, 150, 150])

	def applyEffectTo(self, snake):
		snake.addTimer('ghost1', 5000, snake.enableCollision)
		snake.addTimer('ghost2', 5000, snake.resetColor)
		snake.disableCollision()
		snake.setColor([200,200,200])

		self.used = True

	def __str__(self):
		return 'G'

class SpeedPU(Powerup):
	def __init__(self, board):
		Powerup.__init__(self, board, lifetime=5000, color=[255, 0, 255])

	def applyEffectTo(self, snake):
		snake.addTimer('speed', 5000, snake.resetDelay)
		snake.setDelay(snake.getDelay() / 2)

		self.used = True

	def __str__(self):
		return 'S'

class PortalPU(Powerup):
	def __init__(self, board):
		Powerup.__init__(self, board, lifetime=7500, color=[0,255,255])

	def applyEffectTo(self, snake):
		snake.randposition()

		self.used = True

	def __str__(self):
		return 'P'

class WidthPU(Powerup):
	def __init__(self, board):
		Powerup.__init__(self, board, lifetime=5000, color=[0,255,0])

	def applyEffectTo(self, snake):
		snake.addTimer('width', 5000, snake.thin)
		snake.widen()

		self.used = True

	def __str__(self):
		return 'W'


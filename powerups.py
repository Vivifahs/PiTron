from random import randint
from gameobject import GameObject
import pygame

class Powerup(GameObject):
	def __init__(self, board, lifetime=5000, color=[255,255,255]):
		GameObject.__init__(self, 0, 0, board, color)

		self.lifetime = lifetime
		self.currtime = self.lifetime
		self.used = False

		self.randposition()

	def randposition(self):
		self.board.setCell(None, self.x, self.y)

		self.x = randint(1, self.board.cols - 1)
		self.y = randint(1, self.board.rows - 1)

		self.board.setCell(self, self.x, self.y)

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
		snake.setColor([150,150,150])

		self.used = True

	def __str__(self):
		return 'G'

class SpeedPU(Powerup):
	def __init__(self, board):
		Powerup.__init__(self, board, lifetime=5000, color=[255, 0, 255])

	def applyEffectTo(self, snake):
		snake.addTimer('speed', 5000, snake.resetDelay)
		snake.setDelay(50)

		self.used = True

	def __str__(self):
		return 'D'

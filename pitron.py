from pygame.locals import *
from grid import Grid
from powerups import *
from snake import Snake

import pygame
import sys

WINDOW_W = 800
WINDOW_H = 600

GRIDSIZE = 8

GRID_W = WINDOW_W / GRIDSIZE
GRID_H = WINDOW_H / GRIDSIZE

class Game(object):
	def __init__(self):
		self.display = pygame.display.set_mode((WINDOW_W,WINDOW_H), pygame.HWSURFACE)
		pygame.display.set_caption('PiTron')

		self.board = Grid(GRID_W, GRID_H, GRIDSIZE)

		self.powerups = []
		self.players = []
		#self.player = Snake(2, 2, self.board)

		self.clock = pygame.time.Clock()

		self.running = False

		self.lpressed = False
		self.rpressed = False

	def start(self):
		self.players.append(Snake(0, 0, self.board))
		self.players.append(Snake(GRID_W - 1, GRID_H - 1, self.board, Snake.LEFT, [0,0,255]))
		self.powerups.append(GhostPU(self.board))
		self.powerups.append(SpeedPU(self.board))

		self.running = True

		print self.board
		self.loop()

	def loop(self):
		while self.running:
			delta = self.clock.tick()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cleanup()

			keys = pygame.key.get_pressed()

			if keys[K_RIGHT]:
				self.players[1].move(Snake.RIGHT)
			if keys[K_LEFT]:
				self.players[1].move(Snake.LEFT)
			if keys[K_UP]:
				self.players[1].move(Snake.UP)
			if keys[K_DOWN]:
				self.players[1].move(Snake.DOWN)

			if keys[K_d]:
				self.players[0].move(Snake.RIGHT)
			if keys[K_a]:
				self.players[0].move(Snake.LEFT)
			if keys[K_w]:
				self.players[0].move(Snake.UP)
			if keys[K_s]:
				self.players[0].move(Snake.DOWN)

			if keys[K_ESCAPE]:
				self.running = False

			self.update(delta)

			self.draw()

		self.cleanup()

	def update(self, delta):
		for snake in self.players:
			snake.update(delta)
		
		for powerup in self.powerups:
			powerup.update(delta)

			if powerup.used:
				self.powerups.remove(powerup)
				self.board.setCell(None, powerup.x, powerup.y)

	def draw(self):
		self.display.fill((0,0,0))

		self.board.render(self.display)
		
		pygame.display.update()

	def cleanup(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

if __name__ == '__main__':
	pygame.init()

	game = Game()
	game.start()

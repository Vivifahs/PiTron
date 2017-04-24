# PiTron v0.0.1a
# Snake controlled with two GPIO switches
from random import randint
from pygame.locals import *
import RPi.GPIO as GPIO
import pygame
import sys
import time

# Window dimensions
WINDOW_W = 640
WINDOW_H = 480

# Movement step
# Coordinates are scaled by this
GRIDSIZE = 32

# Number of grid cells in window
GRID_W = WINDOW_W / GRIDSIZE
GRID_H = WINDOW_H / GRIDSIZE

# GPIO keys
KLEFT = 26
KRIGHT = 21

# Info strings
VERSION = 'PiTron v0.0.1a'
IMAGEDR = 'img/'

# Returns true if the coordinates match up
# i.e, they're on the same grid spot
def sameGrid(x1, y1, x2, y2):
	return x1 == x2 and y1 == y2

# Increases length of player when 'eaten'
class Apple(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.reposition()

		self.img = pygame.image.load(IMAGEDR + "apple.png").convert()

	# Repositions apple to a random spot on the grid
	def reposition(self):
		self.x = randint(1, GRID_W - 1) * GRIDSIZE
		self.y = randint(1, GRID_H - 1) * GRIDSIZE

	def draw(self, surface):
		surface.blit(self.img, (self.x, self.y))

# Player class
class Player(object):
	# Direction constants
	LEFT, RIGHT, UP, DOWN = range(4)

	def __init__(self):
		# Direction stuff
		self.direction = Player.RIGHT
		self.changeDir = None
		
		# Setup start length
		self.length = 3
		self.x = [0, 1, 2]
		self.y = [0, 0, 0]

		# Counters used to step updates
		self.updateDelay = 45
		self.updateCount = 0

		self.img = pygame.image.load(IMAGEDR + "snake.png").convert()

	# main update method
	def update(self):
		self.updateCount += 1

		if self.updateCount > self.updateDelay:
			# Change direction if needed
			if self.changeDir != None:
				self.direction = self.changeDir
				self.changeDir = None

			# Update previous positions
			for i in range(self.length - 1, 0, -1):
				self.x[i] = self.x[i - 1]
				self.y[i] = self.y[i - 1]

			# Update current position
			if self.direction == Player.LEFT:
				self.x[0] -= GRIDSIZE
			elif self.direction == Player.RIGHT:
				self.x[0] += GRIDSIZE
			elif self.direction == Player.UP:
				self.y[0] -= GRIDSIZE
			elif self.direction == Player.DOWN:
				self.y[0] += GRIDSIZE

			# Reset delay count
			self.updateCount = 0

	# Add another tail block
	def increase(self):
		self.x.append(self.x[self.length - 1])
		self.y.append(self.y[self.length - 1])
		self.length += 1

	# Direction setters 
	def moveLeft(self):
		if self.direction != Player.RIGHT:
			self.changeDir = Player.LEFT

	def moveRight(self):
		if self.direction != Player.LEFT:
			self.changeDir = Player.RIGHT

	def moveUp(self):
		if self.direction != Player.DOWN:
			self.changeDir = Player.UP

	def moveDown(self):
		if self.direction != Player.UP:
			self.changeDir = Player.DOWN

	def draw(self, surface):
		for i in range(0, self.length):
			surface.blit(self.img, (self.x[i], self.y[i]))

# Main game class
class Game(object):
	def __init__(self):
		self.running = False
		self.display = None
		self.player = None
		self.apple = None

		# Keep track of GPIO presses
		self.lpressed = False
		self.rpressed = False

	def on_init(self):
		pygame.init()
		self.display = pygame.display.set_mode((WINDOW_W, WINDOW_H), \
							pygame.HWSURFACE)
		pygame.display.set_caption(VERSION)

		self.player = Player()
		self.apple = Apple()

		self.running = True

	def on_event(self, event):
		if event.type == QUIT:
			self.running = False

	def on_loop(self):
		self.player.update()

		# Check player-apple collision
		for i in range(self.player.length):
			if sameGrid(self.apple.x, self.apple.y, \
					self.player.x[i], self.player.y[i]):
				self.apple.reposition()
				self.player.increase()

		# Check player collision with self
		for i in range(2, self.player.length):
			if sameGrid(self.player.x[0], self.player.y[0], \
					self.player.x[i], self.player.y[i]):
				print "You lose"
				self.on_cleanup()

		# Check if player is offscreen
		if self.player.x[0] < 0 or self.player.x[0] > GRID_W * GRIDSIZE or \
			self.player.y[0] < 0 or self.player.y[0] > GRID_H * GRIDSIZE:
			print "You lose"
			self.on_cleanup()

	def on_render(self):
		self.display.fill((0,0,0))
		self.player.draw(self.display)
		self.apple.draw(self.display)
		pygame.display.update()

	def on_cleanup(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

	def on_execute(self):
		self.on_init()

		while self.running:
			# Get pygame events
			pygame.event.pump()
			keys = pygame.key.get_pressed()

			if GPIO.input(KLEFT):
				if not self.lpressed:
					self.lpressed = True

					if self.player.direction == Player.UP:
						self.player.moveLeft()
					elif self.player.direction == Player.DOWN:
						self.player.moveRight()
					elif self.player.direction == Player.LEFT:
						self.player.moveDown()
					elif self.player.direction == Player.RIGHT:
						self.player.moveUp()
			else:
				self.lpressed = False

			if GPIO.input(KRIGHT):
				if not self.rpressed:
					self.rpressed = True

					if self.player.direction == Player.UP:
						self.player.moveRight()
					elif self.player.direction == Player.DOWN:
						self.player.moveLeft()
					elif self.player.direction == Player.LEFT:
						self.player.moveUp()
					elif self.player.direction == Player.RIGHT:
						self.player.moveDown()
			else:
				self.rpressed = False		

			if keys[K_LEFT]:
				self.player.moveLeft()
			elif keys[K_RIGHT]:
				self.player.moveRight()
			elif keys[K_UP]:
				self.player.moveUp()
			elif keys[K_DOWN]:
				self.player.moveDown()
			if keys[K_ESCAPE]:
				self.running = False

			self.on_loop()
			self.on_render()

		self.on_cleanup()

# Entrypoint
if __name__ == '__main__':
	# Setup GPIO stuff
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(KLEFT, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(KRIGHT, GPIO.IN, GPIO.PUD_DOWN)

	# Start game
	game = Game()
	game.on_execute()

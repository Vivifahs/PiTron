from pygame.locals import *
from random import randint
from grid import Grid
from powerups import *
from snake import Snake

import pygame
import sys

# Window dimensions
WINDOW_W = 1024
WINDOW_H = 768

# Grid dimensions
CELL_SIZE = 8
GRID_W = 75
GRID_H = 75

GRID_OFFSET_X = (WINDOW_W - GRID_W * CELL_SIZE) / 2
GRID_OFFSET_Y = (WINDOW_H - GRID_H * CELL_SIZE) / 2

BACKGROUND = "space.png"

# Player start positions
POS_1 = (GRID_W / 2, 0) # Top
POS_2 = (GRID_W - 1, GRID_H / 2) # Right
POS_3 = (GRID_W / 2, GRID_H - 1) # Bottom
POS_4 = (0, GRID_H / 2) # Left

# GPIO input pins
PINS = [4, 17, 27, 22, 5, 6, 13, 19]

WHITE = (255,255,255)

class Game(object):
	def __init__(self):
		# Set up display
		flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN

		if 'fullscreen' in sys.argv:
			flags = flags | pygame.FULLSCREEN

		self.display = pygame.display.set_mode((WINDOW_W,WINDOW_H), flags)
		self.display.set_alpha(None)
		pygame.display.set_caption('PiTron')

		# Main grid
		self.board = Grid(GRID_W, GRID_H, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)

		# Game lists
		self.powerupclasses = []
		self.powerups = []
		self.players = []

		# Game timer
		self.clock = pygame.time.Clock()

		# Key inputs
		# Key = player index
		# Val = [left button, right button, left pressed, right pressed]
		self.inputs = {}
		self.returnpressed = False

		# Text rendering
		self.font = pygame.font.SysFont("monospace", 15)
		self.winfont = pygame.font.SysFont("monospace", 32)
		
		# Background image
		self.background = pygame.image.load(BACKGROUND).convert()
		self.background_rect = self.background.get_rect()

		# Gamestate
		self.running = False
		self.twoplayer = False

		self.won = False
		self.winner = None

	def start(self):
		self.powerupclasses.append(GhostPU)
		self.powerupclasses.append(SpeedPU)
		self.powerupclasses.append(PortalPU)
		self.powerupclasses.append(WidthPU)

		self.players.append(Snake(POS_1[0], POS_1[1], self.board, Snake.DOWN))
		self.players.append(Snake(POS_3[0], POS_3[1], self.board, Snake.UP, [0,0,255]))

		self.inputs[0] = [pygame.K_a, pygame.K_d, False, False]
		self.inputs[1] = [pygame.K_LEFT, pygame.K_RIGHT, False, False]

		if not self.twoplayer:
			self.players.append(Snake(POS_2[0], POS_2[1], self.board, Snake.LEFT, [225, 0, 225]))
			self.players.append(Snake(POS_4[0], POS_4[1], self.board, Snake.RIGHT, [255,255,0]))

			self.inputs[2] = [pygame.K_j, pygame.K_l, False, False]
			self.inputs[3] = [pygame.K_f, pygame.K_h, False, False]

		# Board rotation
		self.boardangle = 0.0
		self.rotationtimer = 7500
		self.rotating = False
		
		# Input flipping
		self.fliptimer = 5000
		self.flipped = False

		# Render blanking
		self.blanktimer = 15000
		self.blankdelay = 2000
		self.renderblanked = False

		# Powerup spawning
		self.spawnfreq = 20

		# Effect delays
		self.thresholdA = 10000
		self.thresholdB = 15000

		self.canrotate = False
		self.canflip = False
		self.canblank = False

		self.running = True

		#print self.board
		self.loop()

	def reset(self):
		self.running = False
		self.twoplayer = not self.twoplayer

		self.won = False
		self.winner = None

		del self.players[:]
		del self.powerupclasses[:]
		del self.powerups[:]
		self.inputs.clear()
		self.board.clear()

		self.start()

	def loop(self):
		while self.running:
			# Get time between frames
			delta = self.clock.tick()

			if not self.canrotate:
				self.thresholdA -= delta

				if self.thresholdA <= 0:
					self.canrotate = True
					self.canflip = True
			elif not self.canblank:
				self.thresholdB -= delta

				if self.thresholdB <= 0:
					self.canblank = True

			# Handle board rotation
			if self.canrotate:
				if not self.rotating:
					self.rotationtimer -= delta

					if self.rotationtimer <= 0:
						self.rotationtimer = randint(3000, 10000)
						self.rotating = True

			# Handle input flipping
			if self.canflip:
				self.fliptimer -= delta

				if self.fliptimer <= 0:
					self.fliptimer = randint(2500, 5000)
					self.flipped = not self.flipped

			# Handle render pausing
			if self.canblank:
				if not self.renderblanked:
					self.blanktimer -= delta

					if self.blanktimer <= 0:
						self.blanktimer = 15000
						self.renderblanked = True

						self.flipped = False
				else:
					self.blankdelay -= delta
				
					if self.blankdelay <= 0:
						self.blankdelay = 1500
						self.renderblanked = False

			# Spawn powerups
			spawn = randint(1, 1000)

			if spawn >= 1000 - self.spawnfreq:
				ptype = randint(0, len(self.powerupclasses) - 1)

				self.powerups.append(self.powerupclasses[ptype](self.board))

			# Handle 'x' being clicked
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cleanup()
			
			# Handle input
			keys = pygame.key.get_pressed()

			for key in self.inputs.keys():
				value = self.inputs[key]

				left = value[0]
				right = value[1]
				lpressed = value[2]
				rpressed = value[3]
				
				if keys[left]:
					if not lpressed:
						self.inputs[key][2] = True
						self.players[key].changeDirection(-1 if not self.flipped else 1)
				else:
					self.inputs[key][2] = False
					
				if keys[right]:
					if not rpressed:
						self.inputs[key][3] = True
						self.players[key].changeDirection(1 if not self.flipped else -1)
				else:
					self.inputs[key][3] = False
				
				
			if keys[K_ESCAPE]:
				self.running = False

			if keys[K_RETURN]:
				if not self.returnpressed:
					self.returnpressed = True
					self.reset()
					break
			else:
				self.returnpressed = False

			# Update and render everything
			self.update(delta)
			self.draw()

		# Quit
		self.cleanup()

	def update(self, delta):
		for snake in self.players:
			snake.update(delta)

		alive = [x for x in self.players if x.alive]
		if len(alive) == 1 and self.winner is None:
			self.won = True

			for i in range(len(self.players)):
				if self.players[i].alive:
					self.winner = i

		for powerup in self.powerups:
			powerup.update(delta)

			if powerup.used:
				self.powerups.remove(powerup)
				self.board.setCell(None, powerup.x, powerup.y)

	def draw(self):
		# Background
		self.display.fill((0,0,0))
		self.display.blit(self.background, self.background_rect)

		# Draw everything to grid
		if self.flipped:
			self.board.setImage(self.board.grid_bgnd_b)
		elif self.renderblanked:
			self.board.setImage(self.board.grid_bgnd_c)
		else:
			self.board.setImage(self.board.grid_bgnd_a)

		boardsurf = self.board.render(self.display, hide=self.renderblanked)
		boardrect = boardsurf.get_rect()

		boardrect.topleft = (GRID_OFFSET_X, GRID_OFFSET_Y)

		# Increase board rotation
		if self.rotating:
			self.boardangle += 0.5

			if self.boardangle % 90.0 == 0.0:
				self.rotating = False

			if self.boardangle >= 360:
				self.boardangle = 0

		# Rotate and display board
		rotsurf = pygame.transform.rotate(boardsurf, self.boardangle)
		rotrect = rotsurf.get_rect()
		rotrect.center = boardrect.center

		self.display.blit(rotsurf, rotrect)

		# Display player status
		for i in range(len(self.players)):
			string = "Player {}: {}".format(i + 1, 'Alive' if self.players[i].alive else 'Dead ')
			img = self.font.render(string, 1, self.players[i].color)
			pos = (i * (self.font.size(string)[0] + 10) + GRID_OFFSET_X, 0)
			self.display.blit(img, pos)

		# Display FPS
		fps = self.font.render("FPS: {}".format(round(self.clock.get_fps(), 2)), 1, WHITE)
		self.display.blit(fps, (0,0))

		# Display rotation status
		rotatestr = 'Rotating!'
		if not self.canrotate:
			thresholdtime = int(self.thresholdA / 1000)
			rotatestr = 'Rotation enabled in: {}'.format(thresholdtime)
		elif not self.rotating:
			rottime = int(self.rotationtimer / 1000)
			rotatestr = 'Next rotation: {}'.format(rottime)
			
		rot = self.font.render(rotatestr, 1, WHITE)
		self.display.blit(rot, (0,15))

		# Display flip status
		flipstr = 'Inputs flipped!'
		if not self.canflip:
			thresholdtime = int(self.thresholdA / 1000)
			flipstr = 'Flipping enabled in: {}'.format(thresholdtime)
		elif not self.flipped:
			fliptime = int(self.fliptimer / 1000)
			flipstr = 'Next flip: {}'.format(fliptime)

		flip = self.font.render(flipstr, 1, WHITE)
		self.display.blit(flip, (0,30))

		# Display render pause status
		pausestr = 'Rendering stopped'
		if not self.canblank:
			thresholdtime = int(self.thresholdB / 1000)
			pausestr = 'Blanking enabled in: {}'.format(thresholdtime)
		elif not self.renderblanked:
			pausetime = int(self.blanktimer / 1000)
			pausestr = 'Next blank: {}'.format(pausetime)

		ps = self.font.render(pausestr, 1, WHITE)
		self.display.blit(ps, (0,45))

		# Did someone win?
		if self.won:
			winstr = "Player {} wins!".format(self.winner + 1)

			wn = self.winfont.render(winstr, 1, self.players[self.winner].color)
			sz = self.winfont.size(winstr)
			self.display.blit(wn, (WINDOW_W / 2 - sz[0] / 2, WINDOW_H - GRID_OFFSET_Y / 2))

		pygame.display.update()

	# Close everything
	def cleanup(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

# Entrypoint
if __name__ == '__main__':
	args = sys.argv
	print args

	#GPIO.setmode(GPIO.BCM)
	
	#for pin in PINS:
	#	GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)

	pygame.init()

	game = Game()
	game.start()


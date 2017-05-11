from pygame.locals import *
from grid import Grid
from powerups import *
from snake import Snake

import pygame
import sys

WINDOW_W = 1024
WINDOW_H = 768

GRID_OFFSET_X = 152
GRID_OFFSET_Y = 24
CELL_SIZE = 8

GRID_W = (WINDOW_W - GRID_OFFSET_X * 2) / CELL_SIZE
GRID_H = (WINDOW_H - GRID_OFFSET_Y * 2) / CELL_SIZE

BACKGROUND = "space.png"

UPDATE_GRID = (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_W * CELL_SIZE, GRID_H * CELL_SIZE)

# Player start positions
POS_1 = (GRID_W / 2, 0) # Top
POS_2 = (GRID_W - 1, GRID_H / 2) # Right
POS_3 = (GRID_W / 2, GRID_H - 1) # Bottom
POS_4 = (0, GRID_H / 2) # Left

class Game(object):
	def __init__(self):
		# Set up display
		flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
		self.display = pygame.display.set_mode((WINDOW_W,WINDOW_H), flags)
		self.display.set_alpha(None)
		pygame.display.set_caption('PiTron')

		# Main grid
		self.board = Grid(GRID_W, GRID_H, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)

		# Game lists
		self.powerups = []
		self.players = []

		# Game timer
		self.clock = pygame.time.Clock()

		# Key inputs
		# Key = player index
		# Val = [left button, right button, left pressed, right pressed]
		self.inputs = { 0 : [pygame.K_a, pygame.K_d, False, False], \
						1 : [pygame.K_LEFT, pygame.K_RIGHT, False, False]}

		# Text rendering
		self.font = pygame.font.SysFont("monospace", 15)
		
		# Background image
		self.background = pygame.image.load(BACKGROUND).convert()
		self.background_rect = self.background.get_rect()

		# Board rotation
		self.boardangle = 0.0
		self.rotationtimer = 7500
		self.rotating = False
		
		# Input flipping
		self.fliptimer = 5000
		self.flipped = False

		# Gamestate
		self.running = False

	def start(self):
		self.powerups.append(GhostPU(self.board))
		self.powerups.append(SpeedPU(self.board))

		self.players.append(Snake(POS_1[0], POS_1[1], self.board, Snake.DOWN))
		#self.players.append(Snake(POS_2[0], POS_2[1], self.board, Snake.LEFT, [0,0,255]))
		self.players.append(Snake(POS_3[0], POS_3[1], self.board, Snake.UP, [225, 0, 225]))
		#self.players.append(Snake(POS_4[0], POS_4[1], self.board, Snake.RIGHT, [255,255,0]))

		self.running = True

		#print self.board
		self.loop()

	def loop(self):
		while self.running:
			# Get time between frames
			delta = self.clock.tick()

			# Handle board rotation
			if not self.rotating:
				self.rotationtimer -= delta

				if self.rotationtimer <= 0:
					self.rotationtimer = 7500
					self.rotating = True

			# Handle input flipping
			self.fliptimer -= delta

			if self.fliptimer <= 0:
				self.fliptimer = 5000
				self.flipped = not self.flipped

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

			# Update and render everything
			self.update(delta)
			self.draw()

		# Quit
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
		# Background
		self.display.fill((0,0,0))
		self.display.blit(self.background, self.background_rect)

		boardsurf = self.board.render(self.display)
		boardrect = boardsurf.get_rect()

		boardrect.topleft = (GRID_OFFSET_X, GRID_OFFSET_Y)

		if self.rotating:
			self.boardangle += 0.5

			if self.boardangle % 90.0 == 0.0:
				self.rotating = False

			if self.boardangle >= 360:
				self.boardangle = 0

		if self.flipped:
			inv = pygame.Surface(boardrect.size, pygame.SRCALPHA)
			inv.fill((255,255,255,255))
			inv.blit(boardsurf, (0,0), None, pygame.BLEND_RGB_SUB)
			boardsurf = inv

		rotsurf = pygame.transform.rotate(boardsurf, self.boardangle)
		rotrect = rotsurf.get_rect()
		rotrect.center = boardrect.center

		#if self.flipped:
		#	inv = pygame.Surface(rotsurf.get_rect().size, pygame.SRCALPHA)
		#	inv.fill((255,255,255,255))
		#	inv.blit(rotsurf, (0,0), None, pygame.BLEND_RGB_SUB)
		#	rotsurf = inv

		self.display.blit(rotsurf, rotrect)

		# Display player status
		for i in range(len(self.players)):
			string = "Player {}: {}".format(i + 1, 'Alive' if self.players[i].alive else 'Dead ')
			img = self.font.render(string, 1, self.players[i].color)
			pos = (i * (self.font.size(string)[0] + 10) + GRID_OFFSET_X, 0)
			self.display.blit(img, pos)

		# Display FPS
		fps = self.font.render("FPS: {}".format(round(self.clock.get_fps(), 2)), 1, (255,255,255))
		self.display.blit(fps, (0,0))

		# Display rotation status
		rotatestr = 'Rotating!'
		if not self.rotating:
			rottime = int(self.rotationtimer / 1000)
			rotatestr = 'Next rotation: {}'.format(rottime)
			
		rot = self.font.render(rotatestr, 1, (255,255,255))
		self.display.blit(rot, (0,15))

		# Display flip status
		flipstr = 'Inputs flipped!'
		if not self.flipped:
			fliptime = int(self.fliptimer / 1000)
			flipstr = 'Next flip: {}'.format(fliptime)

		flip = self.font.render(flipstr, 1, (255,255,255))
		self.display.blit(flip, (0,30))

		pygame.display.update()

	def cleanup(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

if __name__ == '__main__':
	pygame.init()

	game = Game()
	game.start()

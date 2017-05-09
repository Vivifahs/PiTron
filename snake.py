from gameobject import GameObject
from powerups import Powerup

# Pieces that create a Snake's tail
class SnakeCell(GameObject):
	def __init__(self, x, y, board, color=[255,0,0]):
		GameObject.__init__(self, x, y, board, color)

	# Nothing to update
	def update(self, delta):
		pass

	def __str__(self):
		return 'X'

# Player object
class Snake(GameObject):
	# Direction enum
	LEFT, UP, RIGHT, DOWN = range(4)
    # Default delay between updates in ms
	DELAY = 100

	def __init__(self, x, y, board, direction=RIGHT, color=[255,0,0]):
		GameObject.__init__(self, x, y, board, color)

		# Direction
		self.direction = direction
		self.changedir = None

		# Flags
		self.collision = True
		self.alive = True

		# List of SnakeCells belonging to this Snake
		self.cells = []

		# Timers
		self.timers = {}
		self.addTimer('update', Snake.DELAY, self.doUpdate, resetTime=Snake.DELAY)

    # Various functions used by powerups
	def disableCollision(self):
		self.collision = False

	def enableCollision(self):
		self.collision = True

	def setDelay(self, delay):
		self.timers['update'][0] = delay
		self.timers['update'][1] = delay

	def resetDelay(self):
		self.setDelay(Snake.DELAY)

	# Add a timer
	# time: duration of timer
    # callback: function to call when time runs out
    # resetTime: if not 0, then the timer will reset to this upon running out
	def addTimer(self, name, time, callback, resetTime=0):
		self.timers[name] = [time, resetTime, callback]

	# Set new direction
    # Doesn't change if the direction is opposite from the current direction
	def move(self, direction):
		if direction == Snake.LEFT:
			if self.direction != Snake.RIGHT:
				self.changedir = Snake.LEFT

		elif direction == Snake.RIGHT:
			if self.direction != Snake.LEFT:
				self.changedir = Snake.RIGHT

		elif direction == Snake.UP:
			if self.direction != Snake.DOWN:
				self.changedir = Snake.UP

		elif direction == Snake.DOWN:
			if self.direction != Snake.UP:
				self.changedir = Snake.DOWN

	# Kill this Snake and remove its SnakeCells
	def die(self):
		self.alive = False

		#for cell in self.cells:
		#	self.board.setCell(None, cell.x, cell.y)

		self.setDelay(1)

		print 'Dead!'

    # Tick each timer and call their callbacks if necessary
	def update(self, delta):
		for key in self.timers.keys():
			timer = self.timers[key]
			timer[0] -= delta

			if timer[0] <= 0:
				if timer[1] == 0:
					del self.timers[key]
				else:
					timer[0] = timer[1]

				timer[2]()

	# Actuall update the Snake
	def doUpdate(self):
		# Change direction
		if self.changedir is not None:
			self.direction = self.changedir
			self.changedir = None

		if self.alive:
            # Leave SnakeCell behind
			snakecell = SnakeCell(self.x, self.y, self.board, self.color)
			self.cells.append(snakecell)
	
            # Update position
			if self.direction == Snake.LEFT:
				self.x -= 1
			elif self.direction == Snake.RIGHT:
				self.x += 1
			elif self.direction == Snake.UP:
				self.y -= 1
			elif self.direction == Snake.DOWN:
				self.y += 1

			# Check if Snake if out of bounds
			if self.x >= self.board.cols or self.x < 0:
				self.die()
				return
			if self.y >= self.board.rows or self.y < 0:
				self.die()
				return

			# Check if current grid cell is already filled
			if self.collision:
				if self.board.cellOccupied(self.x, self.y):
					item = self.board.getCell(self.x, self.y)

                    # Apply effect if item is a Powerup, otherwise die
					if isinstance(item, Powerup):
						item.applyEffectTo(self)
					else:
						self.die()
						return

			# Update board
			self.board.setCell(self, self.x, self.y)
		else:
			if len(self.cells) > 0:
				cell = self.cells[len(self.cells) - 1]
				self.board.setCell(None, cell.x, cell.y)
				self.cells.remove(cell)

	def __str__(self):
		return 'S'

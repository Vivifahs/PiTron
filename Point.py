import math
class Point(object):
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)    
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    def dist(self, other):
        return math.sqrt(((other.x - self.x) ** 2) + ((other.y - self.y) ** 2))
    def midpt(self, other):
        return Point(((self.x + other.x) / 2), ((self.y + other.y) / 2))

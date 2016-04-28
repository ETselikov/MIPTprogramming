from pygame import *
import os

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32
ROAD_COLOR = "#BAA44B"
BZ_COLOR = "#4BBA4D"
ICON_DIR = os.path.dirname(__file__)
 
class Road(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(Color(ROAD_COLOR))
        self.image = image.load("%s/images/blocks/road.png" % ICON_DIR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

class Build_Zone(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(Color(BZ_COLOR))
        self.image = image.load("%s/images/blocks/grass.png" % ICON_DIR)        
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)


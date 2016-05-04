from pygame import *
import os

EN_WIDTH = 96
EN_HEIGHT = 96
EN_COLOR = "#E61793"
ICON_DIR = os.path.dirname(__file__)

class Tower1(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((EN_WIDTH, EN_HEIGHT))
        self.image.fill(Color(EN_COLOR))
        self.image = image.load("%s/images/towers/1.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.damage = 2
        


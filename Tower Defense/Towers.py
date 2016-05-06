from pygame import *
import os

ICON_DIR = os.path.dirname(__file__)
  
class Tower1(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/towers/1.png" % ICON_DIR) 
        self.rect = Rect(x, y, 96, 96)
        self.damage = 2
        self.cost = 250

class Tower2(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/towers/2.png" % ICON_DIR) 
        self.rect = Rect(x, y, 160, 160)
        self.slow = 2
        self.cost = 600

class Tower3(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/towers/3.png" % ICON_DIR) 
        self.rect = Rect(x, y, 160, 160)
        self.damage = 10
        self.cost = 1250

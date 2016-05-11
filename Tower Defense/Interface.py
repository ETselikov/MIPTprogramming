from pygame import *
import os

ICON_DIR = os.path.dirname(__file__)
  
class Frame(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/frame.png" % ICON_DIR) 
        self.rect = Rect(x, y, 800, 32)

class Background(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, 800, 800)

class Icon1(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/icons/1.png" % ICON_DIR) 
        self.rect = Rect(x, y, 150, 50)

class Icon2(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/icons/2.png" % ICON_DIR) 
        self.rect = Rect(x, y, 150, 50)

class Icon3(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/icons/3.png" % ICON_DIR) 
        self.rect = Rect(x, y, 150, 50)

class Select_Icon(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/icons/selected.png" % ICON_DIR) 
        self.rect = Rect(x, y, 150, 50)

from pygame import *
import os

ICON_DIR = os.path.dirname(__file__)
  
class Frame(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/frame.png" % ICON_DIR) 
        self.rect = Rect(x, y, 800, 800)

class Background(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/interface/Menu_Background.png" % ICON_DIR) 
        self.rect = Rect(x, y, 800, 800)

from pygame import *
import os

WIDTH = 2
HEIGHT = 2
COLOR = "#FF0000" 

class Cams(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   
        self.startX = x 
        self.startY = y
        self.yvel = 0
        
        self.image = Surface((WIDTH,HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  

    def update(self, left, right, up, down, MOVE_SPEED_X, MOVE_SPEED_Y):
        if self.rect.x >= 1600 - 400:
            right = False
            self.rect.x = 1600 - 400
        if self.rect.x <= 0 + 400:
            left = False
            self.rect.x = 0 + 400
        if self.rect.y <= 0 + 400:
            up = False
            self.rect.y = 0 + 400
        if self.rect.y >= 1632 - 400:
            down = False
            self.rect.y = 1632 - 400
            
        if up:
            self.yvel = -MOVE_SPEED_Y
        if down:
            self.yvel = MOVE_SPEED_Y     
        if left:
            self.xvel = -MOVE_SPEED_X
        if right:
            self.xvel = MOVE_SPEED_X
        if not(left or right): 
            self.xvel = 0
        if not(up or down):
            self.yvel = 0
            
        self.rect.y += self.yvel
        self.rect.x += self.xvel 
   

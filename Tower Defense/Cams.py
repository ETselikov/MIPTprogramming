from pygame import *
import os

MOVE_SPEED = 7
WIDTH = 2
HEIGHT = 2
COLOR =  "#FF6262" 

class Cams(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   
        self.startX = x 
        self.startY = y
        self.yvel = 0 
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) 
        self.image.set_colorkey(Color(COLOR)) 

    def update(self, left, right, up, down, MOVE_SPEED_X, MOVE_SPEED_Y):
        if self.rect.x > 1600 - 400:
            right = False
        if self.rect.x < 0 + 400:
            left = False
        if self.rect.y < 0 + 400:
            up = False
        if self.rect.y > 1600 - 400:
            down = False
            
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
   

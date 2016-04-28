from pygame import *
import os

MOVE_SPEED = 3
EN_WIDTH = 32
EN_HEIGHT = 32
EN_COLOR = "#E61793"

class Enemy1(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((EN_WIDTH, EN_HEIGHT))
        self.image.fill(Color(EN_COLOR))       
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.hp = 100
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.prev = 'u'

    def update(self, buildzones):
        if self.up:
            self.yvel = -MOVE_SPEED

        if self.down:
            self.yvel = MOVE_SPEED     
                       
        if self.left:
            self.xvel = -MOVE_SPEED
 
        if self.right:
            self.xvel = MOVE_SPEED
         
        if not(self.left or self.right): 
            self.xvel = 0
        if not(self.up or self.down):
            self.yvel = 0
            
        self.rect.y += self.yvel
        self.collide(buildzones)
        
        self.rect.x += self.xvel
        self.collide(buildzones)
        
    def collide(self, buildzones):
        for c in buildzones:
            if sprite.collide_rect(self, c):
                if self.right:                      
                    self.rect.right = c.rect.left
                    self.right = False
                    if self.prev == 'u' or self.prev == 'd':
                        self.up = True
                        self.prev = 'r'
                        break

                if self.left:                      
                    self.rect.left = c.rect.right
                    self.left = False
                    if self.prev == 'u' or self.prev == 'd':
                        self.up = True
                        self.prev = 'l'
                        break

                if self.down:                      
                    self.rect.bottom = c.rect.top 
                    self.down = False
                    if self.prev == 'l' or self.prev == 'r':
                        self.left = True
                        break

                if self.up:                      
                    self.rect.top = c.rect.bottom 
                    self.up = False
                    if self.prev == 'l' or self.prev == 'r':
                        self.down = True
                        break
                    
                    

from pygame import *
import os

MOVE_SPEED = 2
EN_WIDTH = 32
EN_HEIGHT = 32
EN_COLOR = "#E61793"
ICON_DIR = os.path.dirname(__file__)

class Enemy1(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((EN_WIDTH, EN_HEIGHT))
        self.image.fill(Color(EN_COLOR))
        self.image = image.load("%s/images/enemies/1.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.hp = 1000
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.f = open('Turns.txt', 'r')
        self.turn = self.f.readline()
        self.k = 0
        self.death = False

    def update(self, buildzones, towers):
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
        self.collide(buildzones, towers)
        
        self.rect.x += self.xvel
        self.collide(buildzones, towers)
        
    def collide(self, buildzones, towers):
        for c in buildzones:
            if sprite.collide_rect(self, c):
                if self.right:                      
                    self.rect.right = c.rect.left
                    self.right = False    

                if self.left:                      
                    self.rect.left = c.rect.right
                    self.left = False
                    
                if self.down:                      
                    self.rect.bottom = c.rect.top 
                    self.down = False
                    
                if self.up:                      
                    self.rect.top = c.rect.bottom 
                    self.up = False
                    
                if self.turn[self.k] == 'r':
                    self.right = True
                if self.turn[self.k] == 'l':
                    self.left = True
                if self.turn[self.k] == 'u':
                    self.up = True
                if self.turn[self.k] == 'd':
                    self.down = True
                self.k = self.k + 1
                
        for c in towers:
            if sprite.collide_rect(self, c):
                self.hp = self.hp - c.damage
                if self.hp == 0:
                    self.death = True
                        

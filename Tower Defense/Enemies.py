from pygame import *
import os

EN_WIDTH = 32
EN_HEIGHT = 32
EN_COLOR = "#E61793"
ICON_DIR = os.path.dirname(__file__)

class Enemy(sprite.Sprite):
    def update(self, buildzones, towers, castle):
        if self.up:
            self.yvel = -self.speed

        if self.down:
            self.yvel = self.speed     
                       
        if self.left:
            self.xvel = -self.speed
 
        if self.right:
            self.xvel = self.speed
         
        if not(self.left or self.right): 
            self.xvel = 0
        if not(self.up or self.down):
            self.yvel = 0
            
        self.rect.y += self.yvel
        self.collide(buildzones, towers, castle)
        
        self.rect.x += self.xvel
        self.collide(buildzones, towers, castle)
        
    def collide(self, buildzones, towers, castle):
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
        if sprite.collide_rect(self, castle):
            castle.hp = castle.hp - self.damage
            self.castle = True

class Enemy1(Enemy):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/enemies/1.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.f = open('Turns.txt', 'r')
        self.turn = self.f.readline()
        self.k = 0
        self.death = False
        self.castle = False
        
        self.speed = 2
        self.hp = 1000
        self.cost = 75
        self.damage = 75

class Enemy2(Enemy):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/enemies/2.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.f = open('Turns.txt', 'r')
        self.turn = self.f.readline()
        self.k = 0
        self.death = False
        self.castle = False
        
        self.speed = 4
        self.hp = 5000
        self.cost = 200
        self.damage = 200

class Enemy3(Enemy):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/enemies/3.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.f = open('Turns.txt', 'r')
        self.turn = self.f.readline()
        self.k = 0
        self.death = False
        self.castle = False
        
        self.speed = 7
        self.hp = 10000
        self.cost = 1000
        self.damage = 1000

class BOSS(Enemy):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/images/enemies/BOSS.png" % ICON_DIR) 
        self.rect = Rect(x, y, EN_WIDTH, EN_HEIGHT)
        self.up = self.down = self.right = self.left = False
        self.right = True
        self.f = open('Turns.txt', 'r')
        self.turn = self.f.readline()
        self.k = 0
        self.death = False
        self.castle = False
        
        self.speed = 3
        self.hp = 200000
        self.cost = 0
        self.damage = self.hp

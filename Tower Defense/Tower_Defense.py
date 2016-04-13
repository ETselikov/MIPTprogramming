import pygame
from pygame import *
from Cams import *
from Blocks import *
from Camera_Moving import*

relx = rely = 0
WIN_WIDTH = 800 
WIN_HEIGHT = 800 
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "#4BBA4D"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           
    l = max(-(camera.width-WIN_WIDTH), l)   
    t = max(-(camera.height-WIN_HEIGHT), t) 
    t = min(0, t)                           

    return Rect(l, t, w, h)        


def main():
    pygame.init()  
    screen = pygame.display.set_mode(DISPLAY) 
    pygame.display.set_caption("Tower Defense") 
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) 
                                         
    bg.fill(Color(BACKGROUND_COLOR))     
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    entities = pygame.sprite.Group() 
    roads = []
    buildzones = []
    

    f = open('Level.txt', 'r')
    level = f.readlines()
       
    timer = pygame.time.Clock()
    x=y=0 
    for row in level: 
        for col in row: 
            if col == "#":
                ro = Road(x,y)
                entities.add(ro)
                roads.append(ro)
            if col == " ":
                bz = Build_Zone(x,y)
                entities.add(bz)
                buildzones.append(bz)
                
            x += BLOCK_WIDTH 
        y += BLOCK_HEIGHT    
        x = 0                   
    
    total_level_width  = len(level[0])*BLOCK_WIDTH 
    total_level_height = len(level)*BLOCK_HEIGHT   
    
    Cam1 = Cams(int(total_level_width/4),int(total_level_height/4)) 
    left = right = False 
    up = down = False
    entities.add(Cam1)
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    pygame.mouse.set_pos(int(total_level_width/4),int(total_level_height/4))
    mos = Mouse(relx, rely)
    
    while 1: 
        timer.tick(60)
        
        mos.update(Cam1.rect.x, Cam1.rect.y)
        if mos.relx > 0:
            left = False
            right = True
        if mos.relx < 0:
            right = False
            left = True
        if mos.rely > 0:
            down = True
            up = False
        if mos.rely < 0:
            up = True
            down = False
        for e in pygame.event.get(): 
            if e.type == QUIT:
                pygame.quit()
                return(0)
            
        screen.blit(bg, (0,0))       
        
        camera.update(Cam1) 
        Cam1.update(left, right, up, down, abs(mos.relx), abs(mos.rely))
        
        for e in entities:
            screen.blit(e.image, camera.apply(e))
         
        pygame.display.update()     

if __name__ == "__main__":
    main()

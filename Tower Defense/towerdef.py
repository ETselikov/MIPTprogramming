import pygame
from pygame import *
from Cams import *
from blocks import *
relx = rely = 0
WIN_WIDTH = 800 
WIN_HEIGHT = 640 
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "#004400"

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
    
    Cam1 = Cams(70,70) 
    left = right = False 
    up = down = False
    
    entities = pygame.sprite.Group() 
    platforms = [] 
    
    entities.add(Cam1)
           
    level = [
       "-------------------------------------------------------",
       "-                               --------------------- -",
       "-                       --  ---- ------ --- ----      -",
       "-               ----   ---------------------          -",
       "-            --                                       -",
       "-                      ---------------------          -",
       "--            ---------------------                   -",
       "-    ---------------------                            -",
       "-   -- -- - ---- -- -- -                 ----     --- -",
       "-                                                     -",
       "--     --- -- -- -- -- -- -                           -",
       "-                            -  -  -  -  -  -  -      -",
       "-                -- - -   - -  -  -  -            --- -",
       "-    - -   - - - --- - -                              -",
       "-                        - -- -- -- -- -              -",
       "-      ---                                            -",
       "-                                                     -",
       "-   -------         -----       ------------          -",
       "-                       -                             -",
       "-          ---------    ----  --               -      -",
       "-                                                 --  -",
       "-                                                     -",
       "-                                                     -",
       "-------------------------------------------------------"]
       
    timer = pygame.time.Clock()
    x=y=0 
    for row in level: 
        for col in row: 
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH 
        y += PLATFORM_HEIGHT    
        x = 0                   
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH 
    total_level_height = len(level)*PLATFORM_HEIGHT   
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 

    pygame.mouse.set_pos(70,70)
    pygame.mouse.get_rel()
    while 1: 
        timer.tick(60)
        for e in pygame.event.get(): 
            if e.type == QUIT:
                pygame.quit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False

        screen.blit(bg, (0,0))       

        camera.update(Cam1) 
        Cam1.update(left, right, up, down)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
         
        pygame.display.update()     

if __name__ == "__main__":
    main()

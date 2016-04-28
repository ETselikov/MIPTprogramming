import pygame, time
from Camera_Moving import *
from Scene import *
from Transparent import *
from pygame import *
from Cams import *
from Blocks import *
from Enemies import*


relx = rely = 0
WIN_WIDTH = 800 
WIN_HEIGHT = 800 
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "#4BBA4D"
ICON_DIR = os.path.dirname(__file__)

class WaitScene(Scene):
    def __init__(self, time = 1000, *argv):
        Scene.__init__(self, *argv)
        self.run = 0
        self.time = time

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                self.the_end()
                self.set_next_scene(MenuScene())

        if not self.run < self.time:
            self.the_end()

    def _update(self, dt):
        self.run += dt

class ShowScene(Scene):
    def _start(self):
        sprite = pygame.image.load("%s/images/logo.png" % ICON_DIR)
        self.sprite = sprite

        self.plambir = Transparent(3000)
        self.plambir.start()

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                self.the_end()
                self.set_next_scene(MenuScene())

        if not self.plambir.is_start():
            self.the_end()

    def _update(self, dt):
        self.plambir.update(dt)

    def _draw(self, dt):
        self.display.fill((255,255,255))
        self.display.blit(self.plambir.get_sprite(self.sprite),
                          get_center(self.display.get_rect(),
                                     self.sprite.get_rect()))

class HideScene(ShowScene):
    def _start(self):
        ShowScene._start(self)

        self.plambir.toggle()
        self.plambir.set_time(1000)

class Menu:
    def __init__(self, position = (0,0), loop = True):
        self.index = None
        self.x = position[0]
        self.y = position[1]
        self.menu = list()

    def first(self):
        self.index = 0

    def second(self):
        self.index = 1

    def none(self):
        self.index = None

    def add_menu_item(self, no_select, select, func):
        self.menu.append({ 'no select' : no_select, 'select' : select, 'func' : func })

    def call(self):
        self.menu[self.index]['func']()

    def draw(self, display):
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                display.blit(item['select'], (x, y))
                y += item['select'].get_rect().h
            else:
                display.blit(item['no select'], (x, y))
                y += item['no select'].get_rect().h
            index += 1

class MenuScene(Scene):
    def New_Game(self):
        self.the_end()
        self.set_next_scene(GameScene())
        pygame.event.post(pygame.event.Event(const.END_SCENE))

    def Exit_Game(self):
        self.set_next_scene(None)
        self.the_end()

    def Settings(self):
        self.set_next_scene(None)
        self.the_end()
        
    def _start(self):
        self.menu = Menu((500,600))
        font      = pygame.font.SysFont("Monospace", 40, bold = False, italic = False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold = True, italic = True)
        item = u"Новая игра"
        self.menu.add_menu_item(font.render(item, True, (0, 0, 0)),
                                font_bold.render(item, True, (0, 0, 0)),
                                self.New_Game)
        #item = u"Настройки"
        #self.menu.add_menu_item(font.render(item, True, (0, 0, 0)),
        #                       font_bold.render(item, True, (0, 0, 0)),
        #                        self.Settings)
        item = u"Выход"
        self.menu.add_menu_item(font.render(item, True, (0, 0, 0)),
                                font_bold.render(item, True,(0, 0, 0)),
                                self.Exit_Game)

    def _event(self, event):
        (mosx, mosy) = pygame.mouse.get_pos()
        for e in event.get():
            if mosx > 500 and mosx < 750 and mosy > 600 and mosy < 640:
                self.menu.first()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.menu.call()
            elif mosx > 500 and mosx < 620 and mosy > 660 and mosy < 685:
                self.menu.second()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.menu.call()
            else:
                self.menu.none()
            if e.type == QUIT:
                self.the_end()
                self.set_next_scene(None)           
            
    def _draw(self, dt):
        self.display.fill((255,255,255))
        self.menu.draw(self.display)

class GameScene(Scene):
    def _start(self):
        self.k = 0
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode(DISPLAY) 
        pygame.display.set_caption("Tower Defense") 
        self.bg = Surface((800,800))
        self.entities = pygame.sprite.Group() 
        self.roads = []
        self.buildzones = []
        self.enemies = []
        

        f = open('Level.txt', 'r')
        level = f.readlines()
           
        x=y=0 
        for row in level: 
            for col in row: 
                if col == "#":
                    ro = Road(x,y)
                    self.entities.add(ro)
                    self.roads.append(ro)
                if col == " ":
                    bz = Build_Zone(x,y)
                    self.entities.add(bz)
                    self.buildzones.append(bz)
                    
                x += BLOCK_WIDTH 
            y += BLOCK_HEIGHT    
            x = 0                   

        
        total_level_width  = len(level[0])*BLOCK_WIDTH 
        total_level_height = len(level)*BLOCK_HEIGHT   
        
        self.Cam1 = Cams(int(total_level_width/2),int(total_level_height/2)) 
        self.left = self.right = False 
        self.up = self.down = False
        self.entities.add(self.Cam1)
        
        self.camera = Camera(camera_configure, total_level_width, total_level_height) 
        
        self.mos = Mouse(relx, rely)
    def _event(self, event):
        self.timer.tick(60)
            
        self.mos.update(self.Cam1.rect.x, self.Cam1.rect.y)
        if self.mos.relx > 0:
            self.left = False
            self.right = True
        if self.mos.relx < 0:
            self.right = False
            self.left = True
        if self.mos.rely > 0:
            self.down = True
            self.up = False
        if self.mos.rely < 0:
            self.up = True
            self.down = False
        for e in pygame.event.get(): 
            if e.type == QUIT:
                self.the_end()
                self.set_next_scene(None)
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.the_end()
                    self.set_next_scene(MenuScene())  

    def _draw(self, dt):
        self.screen.blit(self.bg, (0,0))       

        if self.k % 300 == 0:
            self.en = Enemy1(0,64)
            self.entities.add(self.en)
            self.enemies.append(self.en)
        self.k += 1
            
        self.camera.update(self.Cam1) 
        self.Cam1.update(self.left, self.right, self.up, self.down, abs(self.mos.relx), abs(self.mos.rely))
        for i in self.enemies:
            i.update(self.buildzones)
            
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
             
        pygame.display.update()

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

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()
class Game():
    def __init__(self, width, height, color , scene   = None):
        pygame.init()       
        self.scene     = scene
        self.__display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense")
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        self.__display.fill((255,255,255))
        pygame.display.flip() 

    def game_loop(self):
        
        while self.scene != None:
                clock = pygame.time.Clock()
                dt    = 0
                
                self.scene.start(self.__display)

                while not self.scene.is_end():
                    self.scene.loop(dt)

                    pygame.display.flip()

                    dt = clock.tick(60)

                self.scene = self.scene.next()
                

def get_center(surface, sprite):
    return (surface.w/2 - sprite.w/2,
            surface.h/2 - sprite.h/2)

scene = WaitScene(1000, ShowScene(WaitScene(500, HideScene(WaitScene(1000,MenuScene())))))
game = Game(WIN_WIDTH, WIN_HEIGHT, BACKGROUND_COLOR, scene)
game.game_loop()
pygame.quit()

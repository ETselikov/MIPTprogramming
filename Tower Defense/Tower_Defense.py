import pygame, time
from Camera_Moving import *
from Scene import *
from Transparent import *
from pygame import *
from Cams import *
from Blocks import *
from Enemies import *
from Towers import *
from Interface import *
from Menu import *


relx = rely = 0
WIN_WIDTH = 800 
WIN_HEIGHT = 800 
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "#4BBA4D"
DIR = os.path.dirname(__file__)

class Wait_Scene(Scene):
    def __init__(self, time = 1000, *argv):
        Scene.__init__(self, *argv)
        self.run = 0
        self.time = time

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    self.the_end()
                    self.set_next_scene(Main_Menu_Scene())

        if not self.run < self.time:
            self.the_end()

    def _update(self, dt):
        self.run += dt

class Show_Scene(Scene):
    def _start(self):
        sprite = pygame.image.load("%s/images/logo.png" % DIR)
        self.sprite = sprite

        self.plambir = Transparent(3000)
        self.plambir.start()

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    self.the_end()
                    self.set_next_scene(Main_Menu_Scene())

        if not self.plambir.is_start():
            self.the_end()

    def _update(self, dt):
        self.plambir.update(dt)

    def _draw(self, dt):
        self.display.fill((255,255,255))
        self.display.blit(self.plambir.get_sprite(self.sprite),
                          get_center(self.display.get_rect(),
                                     self.sprite.get_rect()))

class Hide_Scene(Show_Scene):
    def _start(self):
        Show_Scene._start(self)

        self.plambir.toggle()
        self.plambir.set_time(1000)

class Main_Menu_Scene(Scene):
    def New_Game(self):
        self.the_end()
        self.set_next_scene(Game_Scene())
        pygame.event.post(pygame.event.Event(const.END_SCENE))

    def Exit_Game(self):
        self.set_next_scene(None)
        self.the_end()
        
    def _start(self):
        self.bg = Background(0, 0)
        self.menu = Menu((500,550))
        font      = pygame.font.SysFont("Monospace", 40, bold = False, italic = False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold = True, italic = True)
        item = u"Новая игра"
        self.menu.add_menu_item(font.render(item, True, (0, 0, 0)),
                                font_bold.render(item, True, (0, 0, 0)),
                                self.New_Game)
        item = u"Выход"
        self.menu.add_menu_item(font.render(item, True, (0, 0, 0)),
                                font_bold.render(item, True,(0, 0, 0)),
                                self.Exit_Game)

    def _event(self, event):
        (mosx, mosy) = pygame.mouse.get_pos()
        for e in event.get():
            if mosx > 500 and mosx < 750 and mosy > 550 and mosy < 590:
                self.menu.index = 0
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    pygame.mixer.music.stop()
                    self.menu.call()
            elif mosx > 500 and mosx < 620 and mosy > 600 and mosy < 640:
                self.menu.index = 1
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    pygame.mixer.music.stop()
                    self.menu.call()
            else:
                self.menu.index = None
            if e.type == QUIT:
                pygame.mixer.music.stop()
                self.the_end()
                self.set_next_scene(None)           
            
    def _draw(self, dt):
        self.display.blit(self.bg.image, (0, 0))
        self.menu.draw(self.display)

class Game_Scene(Scene):
    def _start(self):
        self.money = 1000
        self.k = 0
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode(DISPLAY) 
        pygame.display.set_caption("Tower Defense")
        pygame.mixer.music.load("%s/sounds/Game.mp3" % DIR)
        pygame.mixer.music.play(-1)
        self.entities = pygame.sprite.Group()
        self.rdgr = pygame.sprite.Group()
        self.bzgr = pygame.sprite.Group()
        self.engr = pygame.sprite.Group()
        self.selection = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.interface = pygame.sprite.Group()
        self.building = None
        self.BOSS = False

        f = open('Level.txt', 'r')
        level = f.readlines()

        self.font = pygame.font.SysFont("Monospace", 25, bold = False, italic = False)
        frame = Frame(0, 0)
        self.interface.add(frame)
           
        x = y = 0 
        for row in level: 
            for col in row: 
                if col == "#":
                    ro = Road(x,y)
                    self.entities.add(ro)
                    self.rdgr.add(ro)
                if col == " ":
                    bz = Build_Zone(x,y)
                    self.entities.add(bz)
                    self.bzgr.add(bz)
                if col == "c":
                    self.castle = Castle(x,y)
                    self.entities.add(self.castle)
                    self.rdgr.add(self.castle)
                
                x += BLOCK_WIDTH 
            y += BLOCK_HEIGHT    
            x = 0                   

        
        total_level_width  = len(level[0])*BLOCK_WIDTH 
        total_level_height = len(level)*BLOCK_HEIGHT   
        
        self.Cam1 = Cams(int(total_level_width/2),int(total_level_height/2)) 
        self.left = self.right = False 
        self.up = self.down = False
        
        self.camera = Camera(camera_configure, total_level_width, total_level_height) 
        
        self.mos = Mouse(relx, rely)

        (self.cursor_posx, self.cursor_posy) = mouse.get_pos()
        self.cursor = Cursor(self.cursor_posx, self.cursor_posy)
        

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

        (self.cursor_posx, self.cursor_posy) = mouse.get_pos()
        self.cursor.update(self.cursor_posx + self.Cam1.rect.x - 400, self.cursor_posy + self.Cam1.rect.y - 400)
        for c in self.bzgr:
            if sprite.collide_rect(self.cursor, c):
                self.select = Selected(c.rect.x, c.rect.y)
                self.selection.add(self.select)
                self.building = c
        for c in self.rdgr:
            if sprite.collide_rect(self.cursor, c):
                self.building = None
        for c in self.towers:
            if sprite.collide_rect(self.cursor, c):
                self.building = None
        if sprite.collide_rect(self.cursor, self.castle):
                self.building = None
                
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.mixer.music.stop()
                self.the_end()
                self.set_next_scene(None)

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("%s/sounds/Main_Menu.mp3" % DIR)
                    pygame.mixer.music.play(-1)
                    self.the_end()
                    self.set_next_scene(Main_Menu_Scene())
            if e.type == MOUSEBUTTONDOWN and e.button == 1 and self.building != None:
                tower = Tower1(self.building.rect.x - 32, self.building.rect.y - 32)
                if self.money >= tower.cost:
                    self.towers.add(tower)
                    self.building = None
                    self.money = self.money - tower.cost

    def _draw(self, dt):       
        if self.k > 0 and self.k < 30000:
            if self.k % 400 == 0:
                self.en = Enemy1(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
        if self.k >= 5000 and self.k < 30000:
            if self.k % 200 == 0:
                self.en = Enemy1(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
        if self.k >= 8000 and self.k < 30000:
            if self.k % 300 == 0:
                self.en = Enemy2(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
        if self.k >= 15000 and self.k < 30000:
            if self.k % 500 == 0:
                self.en = Enemy3(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
            if self.k % 200 == 0:
                self.en = Enemy2(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
        if self.k >= 25000 and self.k < 30000:
            if self.k % 200 == 0:
                self.en = Enemy3(0,96)
                self.entities.add(self.en)
                self.engr.add(self.en)
        if self.k == 30000:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("%s/sounds/BOSS.mp3" % DIR)
            pygame.mixer.music.play(-1)
            self.boss = BOSS(0,96)
            self.entities.add(self.boss)
            self.engr.add(self.boss)
            self.BOSS = True
        self.k += 1
        
        for e in self.engr:
            if e.castle or e.death:
                self.engr.remove(e)
                if e.death:
                    self.money = self.money + e.cost
            
            
        self.camera.update(self.Cam1) 
        self.Cam1.update(self.left, self.right, self.up, self.down, abs(self.mos.relx), abs(self.mos.rely))
        for i in self.engr:
            i.update(self.bzgr, self.towers, self.castle)
            
        for e in self.bzgr:
            self.screen.blit(e.image, self.camera.apply(e))
        for e in self.rdgr:
            self.screen.blit(e.image, self.camera.apply(e))
        for e in self.towers:
            self.screen.blit(e.image, self.camera.apply(e))
        for e in self.engr:
            self.screen.blit(e.image, self.camera.apply(e))
        for e in self.selection:
            self.screen.blit(e.image, self.camera.apply(e))
            self.selection.remove(e)
        for i in self.interface:
            self.screen.blit(i.image, (0, 0))
        self.screen.blit(self.font.render("Money = " + str(self.money), True, (255, 226, 0)), (575, 1))
        self.screen.blit(self.font.render("Castle hp = " + str(self.castle.hp), True, (0 + (100000 - self.castle.hp)/395, 255 - (100000 - self.castle.hp)/395, 0)), (10, 1))
        if self.BOSS:
            self.screen.blit(self.font.render("BOSS hp = " + str(self.boss.hp), True, (255, 255, 255)), (300, 1))
                    
class Cursor(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((1,1))
        self.rect = Rect(x, y, 1, 1)
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

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
        pygame.mixer.music.load("%s/sounds/Main_Menu.mp3" % DIR)
        pygame.mixer.music.play(-1)

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

scene = Wait_Scene(1000, Show_Scene(Wait_Scene(500, Hide_Scene(Wait_Scene(1000,Main_Menu_Scene())))))
game = Game(WIN_WIDTH, WIN_HEIGHT, BACKGROUND_COLOR, scene)
game.game_loop()
pygame.quit()

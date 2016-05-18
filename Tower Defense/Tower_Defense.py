import pygame
from Scenes import *

class Game():
    def __init__(self, width, height, color , scene   = None):
        pygame.init()       
        self.scene = scene
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
                dt = 0
                self.scene.start(self.__display)
                
                while not self.scene.is_end():
                    self.scene.loop(dt)
                    pygame.display.flip()
                    dt = clock.tick(60)

                self.scene = self.scene.next()

scene = Wait_Scene(1500, Show_Scene_logo(Wait_Scene(500, Hide_Scene(Wait_Scene(500, Show_Scene_menu(Wait_Scene(500, Main_Menu_Scene())))))))
game = Game(WIN_WIDTH, WIN_HEIGHT, BACKGROUND_COLOR, scene)
game.game_loop()
pygame.quit()

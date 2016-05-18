import pygame

class Mouse(object):
    def __init__(self, relx, rely):
        self.relx = 0
        self.rely = 0
    def update(self, camx, camy):
        (mosx, mosy) = pygame.mouse.get_pos()
        if mosx > 780 or mosx < 20:
            self.relx = int((mosx - 400) / 25)
        else:
            self.relx = 0
        if mosy > 780 or mosy < 20:
            self.rely = int((mosy - 400) / 25)
        else:
            self.rely = 0

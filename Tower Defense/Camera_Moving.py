import pygame

class Mouse(object):
    def __init__(self, relx, rely):
        self.relx = 0
        self.rely = 0
    def update(self, camx, camy):
        (mosx, mosy) = pygame.mouse.get_pos()
        if mosx > 750 or mosx < 50:
            self.relx = int((mosx - 400)/20)
        else:
            self.relx = 0
        if mosy > 750 or mosy < 50:
            self.rely = int((mosy - 400)/20)
        else:
            self.rely = 0

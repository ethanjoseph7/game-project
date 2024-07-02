import pygame
from pygame.locals import *
from os.path import join

class Background(pygame.sprite.Sprite):
    def __init__(self, displaysurface):
        super().__init__()
        self.screen = displaysurface
        self.bgimage = pygame.image.load(join("backgrounds", "nightsky_2.png"))
        self.bgimage = pygame.transform.scale(self.bgimage, self.screen.get_size())

    def render(self):
        self.screen.blit(self.bgimage, (0, 0))
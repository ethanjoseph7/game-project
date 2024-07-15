import pygame
from pygame.locals import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, displaysurface):
        super().__init__()
        ground_url = "assets/platforms/water_2.png"
        self.image = pygame.image.load(ground_url)
        self.screen = displaysurface
        width = self.screen.get_width()
        height = self.screen.get_height()
        self.rect = self.image.get_rect(center = (width/2, height-25))
        
    def render(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))  
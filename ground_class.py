import pygame
from pygame.locals import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, displaysurface):
        super().__init__()
        ground_url = "platforms/water_2.png"
        self.image = pygame.image.load(ground_url)
        self.rect = self.image.get_rect(center = (850, 875))
        self.screen = displaysurface
                                        
    def render(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))  
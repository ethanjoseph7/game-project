import pygame
from pygame.locals import *

class Background(pygame.sprite.Sprite):
      def __init__(self, displaysurface):
            super().__init__()
            bg_url = "backgrounds/nightsky_6.png"
            self.bgimage = pygame.image.load(bg_url)        
            self.bgY = -100
            self.bgX = -100
            self.screen = displaysurface
 
      def render(self):
            self.screen.blit(self.bgimage, (self.bgX, self.bgY))
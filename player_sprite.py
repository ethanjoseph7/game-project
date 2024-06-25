import pygame
from pygame.locals import *
from IPython.display import Image
import sys
        
def get_image(width, height, color):
    image_url = "character_sprites/Fighter/idle.png"
    sheet = pygame.image.load(image_url).convert_alpha()
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet, (0, 0), (0,0, width, height))
    image.set_colorkey(color)
    return image
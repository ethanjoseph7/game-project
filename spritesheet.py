import pygame
from pygame.locals import *
from IPython.display import Image
import sys
        
def get_image(image_url, frame, width, height, color):
    sheet = pygame.image.load(image_url).convert_alpha()
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame*width),0, width, height))
    image.set_colorkey(color)
    return image

def update_animation(screen, sprite_list, x, y):
    last_update = pygame.time.get_ticks
    animation_cooldown = 500
    frame = 0
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(sprite_list):
            frame = 0
    screen.blit(sprite_list[frame], (x, y))

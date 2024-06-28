import pygame
from pygame.locals import *
from IPython.display import Image
import sys
from PIL import Image
import spritesheet

mv_animation_right_url = "character_sprites/Fighter/Run_right.png"
mv_animation_left_url = "character_sprites/Fighter/Run_left.png"
attack_animation_right_url = "character_sprites/Fighter/Attack_1_right.png"
attack_animation_left_url = "character_sprites/Fighter/Attack_1_left.png"
width = 128
height = 128
BG = (0,0,0)



def get_idle_animation_group() -> list:
    return 

def moving_animation_right_list() -> list:
    return animate(mv_animation_right_url)

def moving_animation_left_list() -> list:
    return animate(mv_animation_left_url)

def attack_animation_right_list() -> list:
    return animate(attack_animation_right_url)

def attack_animation_left_list() -> list:
    return animate(attack_animation_left_url)    

def animate(url):
    sprite_sheet = Image.open(url)
    image_width = sprite_sheet.size[0]
    image_height = sprite_sheet.size[1]
    array_of_animations = []
    for i in range(0, image_width, width):
        frame = spritesheet.get_image(url, i, width, height, BG)
        array_of_animations.append(frame)
    return array_of_animations
    


def get_image(frame, type):
    if type == "idle":
        return spritesheet.get_image(idle_animation_url, frame, width, height, BG)
    elif type == "attack_right":
        return spritesheet.get_image(attack_animation_right_url, frame, width, height, BG)
    elif type == "attack_left":
        return spritesheet.get_image(attack_animation_left_url, frame, width, height, BG)




    
def get_idle_frame():
    return spritesheet.get_image(idle_animation_url, 0, width, height, BG)



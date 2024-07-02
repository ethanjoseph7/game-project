import pygame
from pygame.locals import *
from IPython.display import Image
import fighter_sprite
import samurai_sprite


sprites = []

def load_sprites(type):
    if type == "fighter":
        load_fighter_sprite()
        return sprites
    elif type == "samurai":
        load_samurai_sprite()
        return sprites
    
def load_fighter_sprite():
    sprites.append(fighter_sprite.get_idle_images()[0])
    sprites.append(fighter_sprite.get_idle_images()[1])

    sprites.append(fighter_sprite.get_running_images()[0])
    sprites.append(fighter_sprite.get_running_images()[1])

    sprites.append(fighter_sprite.get_attack_1_images()[0])
    sprites.append(fighter_sprite.get_attack_1_images()[1])

    sprites.append(fighter_sprite.get_attack_2_images()[0])
    sprites.append(fighter_sprite.get_attack_2_images()[1])

    sprites.append(fighter_sprite.get_jump_images()[0])
    sprites.append(fighter_sprite.get_jump_images()[1])

    return sprites

def load_samurai_sprite():
    sprites.append(samurai_sprite.get_idle_images()[0])
    sprites.append(samurai_sprite.get_idle_images()[1])

    sprites.append(samurai_sprite.get_idle_images()[0])
    sprites.append(samurai_sprite.get_idle_images()[1])

    sprites.append(samurai_sprite.get_running_images()[0])
    sprites.append(samurai_sprite.get_running_images()[1])

    sprites.append(samurai_sprite.get_attack_1_images()[0])
    sprites.append(samurai_sprite.get_attack_1_images()[1])

    sprites.append(samurai_sprite.get_attack_2_images()[0])
    sprites.append(samurai_sprite.get_attack_2_images()[1])

    sprites.append(samurai_sprite.get_jump_images()[0])
    sprites.append(samurai_sprite.get_jump_images()[1])

    return sprites
import pygame
from pygame.locals import *
from IPython.display import Image
import fighter_sprite
import samurai_sprite
import shinobi_sprite
import skeleton_sprite




def load_sprites(type):
    if type == "fighter":
        return load_fighter_sprite()
    elif type == "samurai":
        return load_samurai_sprite()
    elif type == "shinobi":
        return load_shinobi_sprite()
    elif type == "skeleton":
        return load_skeleton_sprite()
        
    
def load_fighter_sprite():
    sprites = []
    sprites.append(fighter_sprite.get_idle_images()[0])
    sprites.append(fighter_sprite.get_idle_images()[1])

    sprites.append(fighter_sprite.get_running_images()[0])
    sprites.append(fighter_sprite.get_running_images()[1])

    sprites.append(fighter_sprite.get_attack_1_images()[0])
    sprites.append(fighter_sprite.get_attack_1_images()[1])

    sprites.append(fighter_sprite.get_attack_2_images()[0])
    sprites.append(fighter_sprite.get_attack_2_images()[1])

    sprites.append(fighter_sprite.get_attack_3_images()[0])
    sprites.append(fighter_sprite.get_attack_3_images()[1])

    sprites.append(fighter_sprite.get_jump_images()[0])
    sprites.append(fighter_sprite.get_jump_images()[1])

    return sprites

def load_samurai_sprite():
    sprites = []
    sprites.append(samurai_sprite.get_idle_images()[0])
    sprites.append(samurai_sprite.get_idle_images()[1])

    sprites.append(samurai_sprite.get_running_images()[0])
    sprites.append(samurai_sprite.get_running_images()[1])

    sprites.append(samurai_sprite.get_attack_1_images()[0])
    sprites.append(samurai_sprite.get_attack_1_images()[1])

    sprites.append(samurai_sprite.get_attack_2_images()[0])
    sprites.append(samurai_sprite.get_attack_2_images()[1])

    sprites.append(samurai_sprite.get_attack_3_images()[0])
    sprites.append(samurai_sprite.get_attack_3_images()[1])

    sprites.append(samurai_sprite.get_jump_images()[0])
    sprites.append(samurai_sprite.get_jump_images()[1])

    return sprites

def load_shinobi_sprite():
    sprites = []
    sprites.append(shinobi_sprite.get_idle_images()[0])
    sprites.append(shinobi_sprite.get_idle_images()[1])

    sprites.append(shinobi_sprite.get_running_images()[0])
    sprites.append(shinobi_sprite.get_running_images()[1])

    sprites.append(shinobi_sprite.get_attack_1_images()[0])
    sprites.append(shinobi_sprite.get_attack_1_images()[1])

    sprites.append(shinobi_sprite.get_attack_2_images()[0])
    sprites.append(shinobi_sprite.get_attack_2_images()[1])

    sprites.append(shinobi_sprite.get_attack_3_images()[0])
    sprites.append(shinobi_sprite.get_attack_3_images()[1])

    sprites.append(shinobi_sprite.get_jump_images()[0])
    sprites.append(shinobi_sprite.get_jump_images()[1])

    return sprites


def load_skeleton_sprite():
    sprites = []
    sprites.append(skeleton_sprite.get_idle_images()[0])
    sprites.append(skeleton_sprite.get_idle_images()[1])

    sprites.append(skeleton_sprite.get_running_images()[0])
    sprites.append(skeleton_sprite.get_running_images()[1])

    sprites.append(skeleton_sprite.get_attack_1_images()[0])
    sprites.append(skeleton_sprite.get_attack_1_images()[1])

    sprites.append(skeleton_sprite.get_attack_2_images()[0])
    sprites.append(skeleton_sprite.get_attack_2_images()[1])

    sprites.append(skeleton_sprite.get_attack_3_images()[0])
    sprites.append(skeleton_sprite.get_attack_3_images()[1])

    sprites.append(skeleton_sprite.get_jump_images()[0])
    sprites.append(skeleton_sprite.get_jump_images()[1])

    return sprites
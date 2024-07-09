import pygame
from pygame.locals import *
from PIL import Image
import spritesheet

SIZE_MULTIPLIER = 1.9


def get_idle_images():
    samurai_idle_right_images = []
    samurai_idle_left_images = []
    for i in range(6):
        load_url = "character_sprites/Samurai/idle_right_images/Idle_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_idle_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_idle_left_images.append(bigger_img)

    return (samurai_idle_right_images, samurai_idle_left_images)


def get_running_images():
    samurai_running_right_images = []
    samurai_running_left_images = []
    for i in range (8):
        load_url = "character_sprites/Samurai/run_right_images/Walk_right_" + str(i+1) + ".png"

        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_running_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_running_left_images.append(bigger_img)

    return (samurai_running_right_images, samurai_running_left_images)

def get_attack_1_images():
    samurai_attack_1_right_images = []
    samurai_attack_1_left_images = []
    for i in range (10):
        load_url = "character_sprites/Samurai/attack_1_right_images/Attack_1_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_attack_1_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_attack_1_left_images.append(bigger_img)

    return (samurai_attack_1_right_images, samurai_attack_1_left_images)

def get_attack_2_images():
    samurai_attack_2_right_images = []
    samurai_attack_2_left_images = []
    for i in range (12):
        load_url = "character_sprites/Samurai/attack_2_right_images/Attack_2_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_attack_2_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_attack_2_left_images.append(bigger_img)

    return (samurai_attack_2_right_images, samurai_attack_2_left_images)

def get_attack_3_images():
    samurai_attack_3_right_images = []
    samurai_attack_3_left_images = []
    for i in range (12):
        load_url = "character_sprites/Samurai/attack_3_right_images/Attack_3_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_attack_3_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_attack_3_left_images.append(bigger_img)

    return (samurai_attack_3_right_images, samurai_attack_3_left_images)

def get_jump_images():    
    samurai_jump_right_images = []
    samurai_jump_left_images = []
    for i in range(1):
        load_url = "character_sprites/Samurai/jump_right_images/Jump_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        samurai_jump_right_images.append(bigger_img)

        bigger_img = pygame.transform.flip(bigger_img, True, False)
        samurai_jump_left_images.append(bigger_img)

        return (samurai_jump_right_images, samurai_jump_left_images)

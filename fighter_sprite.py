import pygame
from pygame.locals import *

SIZE_MULTIPLIER = 1.9

def get_idle_images():
    fighter_idle_right_images = []
    fighter_idle_left_images = []
    for i in range(6):
        load_url = "character_sprites/Fighter/idling_right_images/idle_right_" + str(i+1)+ ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_idle_right_images.append(bigger_img)

        load_url = "character_sprites/Fighter/idling_left_images/idle_left_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_idle_left_images.append(bigger_img)

    return (fighter_idle_right_images, fighter_idle_left_images)

def get_running_images():
    fighter_running_right_images = []
    fighter_running_left_images = []
    for i in range (8):
        load_url = "character_sprites/Fighter/run_right_images/Run_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_running_right_images.append(bigger_img)

        load_url = "character_sprites/Fighter/run_left_images/Run_left_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_running_left_images.append(bigger_img)

    return (fighter_running_right_images, fighter_running_left_images)

def get_attack_1_images():
    fighter_attack_1_right_images = []
    fighter_attack_1_left_images = []
    for i in range (10):
        load_url = "character_sprites/Fighter/attack_1_right_images/Attack_1_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_attack_1_right_images.append(bigger_img)

        load_url = "character_sprites/Fighter/attack_1_left_images/Attack_1_left_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_attack_1_left_images.append(bigger_img)

    return (fighter_attack_1_right_images, fighter_attack_1_left_images)

def get_attack_2_images():
    fighter_attack_2_right_images = []
    fighter_attack_2_left_images = []
    for i in range (3):
        load_url = "character_sprites/Fighter/attack_2_right_images/Attack_2_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_attack_2_right_images.append(bigger_img)

        load_url = "character_sprites/Fighter/attack_2_left_images/Attack_2_left_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_attack_2_left_images.append(bigger_img)

    return (fighter_attack_2_right_images, fighter_attack_2_left_images)

def get_jump_images():    
    fighter_jump_right_images = []
    fighter_jump_left_images = []
    for i in range(1):
        load_url = "character_sprites/Fighter/jump_right_images/Jump_right_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_jump_right_images.append(bigger_img)

        load_url = "character_sprites/Fighter/jump_left_images/Jump_left_" + str(i+1) + ".png"
        image = pygame.image.load(load_url).convert_alpha()
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        fighter_jump_left_images.append(bigger_img)
        return (fighter_jump_right_images, fighter_jump_left_images)
    





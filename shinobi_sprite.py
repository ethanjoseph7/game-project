import pygame
from pygame.locals import *
import spritesheet

SIZE_MULTIPLIER = 1.9
BG = (0,0,0)
X_DIM = 96
Y_DIM = 84

def get_idle_images():
    shinobi_idle_right_images = []
    shinobi_idle_left_images = []
    for i in range(6):
        ss_url = "character_sprites/Shinobi/Idle.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_idle_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_idle_left_images.append(bigger_img)

    return (shinobi_idle_right_images, shinobi_idle_left_images)

def get_running_images():
    shinobi_running_right_images = []
    shinobi_running_left_images = []
    for i in range (8):
        ss_url = "character_sprites/Shinobi/Run.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_running_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_running_left_images.append(bigger_img)

    return (shinobi_running_right_images, shinobi_running_left_images)

def get_attack_1_images():
    shinobi_attack_1_right_images = []
    shinobi_attack_1_left_images = []
    for i in range (5):
        ss_url = "character_sprites/Shinobi/Attack_1.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_attack_1_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_attack_1_left_images.append(bigger_img)

    return (shinobi_attack_1_right_images, shinobi_attack_1_left_images)

def get_attack_2_images():
    shinobi_attack_2_right_images = []
    shinobi_attack_2_left_images = []
    for i in range (3):
        ss_url = "character_sprites/Shinobi/Attack_2.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_attack_2_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_attack_2_left_images.append(bigger_img)


    return (shinobi_attack_2_right_images, shinobi_attack_2_left_images)

def get_attack_3_images():
    shinobi_attack_3_right_images = []
    shinobi_attack_3_left_images = []
    for i in range (4):
        ss_url = "character_sprites/Shinobi/Attack_3.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_attack_3_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_attack_3_left_images.append(bigger_img)


    return (shinobi_attack_3_right_images, shinobi_attack_3_left_images)

def get_jump_images():    
    shinobi_jump_right_images = []
    shinobi_jump_left_images = []
    for i in range (12):
        ss_url = "character_sprites/Shinobi/Jump.png"
        ss = spritesheet.spritesheet(ss_url)
        x_coord = (X_DIM/4 + i*X_DIM*4/3)
        y_coord = 128-Y_DIM
        coords = (x_coord,y_coord, X_DIM,Y_DIM)
        image = ss.image_at(coords).convert_alpha()
        image.set_colorkey(BG)
        bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
        shinobi_jump_right_images.append(bigger_img)
        bigger_img = pygame.transform.flip(bigger_img, True, False)
        shinobi_jump_left_images.append(bigger_img)

    return (shinobi_jump_right_images, shinobi_jump_left_images)
    





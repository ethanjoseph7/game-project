import pygame
from pygame.locals import *
import spritesheet
from PIL import Image

SIZE_MULTIPLIER = 1.9
BG = (0,0,0,0)
X_DIM = 96
Y_DIM = 84
FRAME_WIDTH = 128

class sprite_class():

    def __init__(self, sprite_type):
        self.sprite_type = sprite_type

    def get_idle_images(self):
        fighter_idle_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Idle.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range(int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_idle_images.append(bigger_img)

        return fighter_idle_images

    def get_running_images(self):
        fighter_running_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Run.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range (int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_running_images.append(bigger_img)

        return fighter_running_images

    def get_attack_1_images(self):
        fighter_attack_1_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Attack_1.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range (int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_attack_1_images.append(bigger_img)

        return fighter_attack_1_images

    def get_attack_2_images(self):
        fighter_attack_2_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Attack_2.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range (int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_attack_2_images.append(bigger_img)


        return fighter_attack_2_images

    def get_attack_3_images(self):
        fighter_attack_3_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Attack_3.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range (int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_attack_3_images.append(bigger_img)


        return fighter_attack_3_images

    def get_jump_images(self):    
        fighter_jump_images = []
        ss_url = "character_sprites/" + str(self.sprite_type) + "/Jump.png"
        ss = spritesheet.spritesheet(ss_url)
        img = Image.open(ss_url)
        for i in range (int(img.width/FRAME_WIDTH)):
            x_coord = (X_DIM/4 + i*X_DIM*4/3)
            y_coord = 128-Y_DIM
            coords = (x_coord,y_coord, X_DIM,Y_DIM)
            image = ss.image_at(coords).convert_alpha()
            image.set_colorkey(BG)
            bigger_img = pygame.transform.scale(image, (image.get_width()*SIZE_MULTIPLIER, image.get_height()*SIZE_MULTIPLIER))
            fighter_jump_images.append(bigger_img)

        return fighter_jump_images
    
    def load_sprites(self):
        return (self.get_idle_images(), self.get_running_images(), self.get_attack_1_images(),
                self.get_attack_2_images(), self.get_attack_3_images(), self.get_jump_images())
        





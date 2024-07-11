import pygame
from pygame.locals import *
import sprites_class

class Enemy(pygame.sprite.Sprite):
    def __init__(self, vec, screen, type):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.vec = vec
        self.screen = screen
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        
        # Sprite
        self.type = type
        
        self.idle_right_images = []
        self.idle_left_images = []

        self.running_right_images = []
        self.running_left_images = []

        self.attack_1_right_images = []
        self.attack_1_left_images = []

        self.attack_2_right_images = []
        self.attack_2_left_images = []

        self.attack_3_right_images = []
        self.attack_3_left_images = []

        self.jump_right_images = []
        self.jump_left_images = []

        self.load_sprites(type)

    def load_sprites(type):
        pass
        
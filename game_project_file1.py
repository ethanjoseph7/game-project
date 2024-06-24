import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import player

 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
#print(pygame.get_init())
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()      
 
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
     
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()


class Player(player.Player_Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec((10, self.SCREEN_HEIGHT-30))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
                
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

running = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
            # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
            pass
    




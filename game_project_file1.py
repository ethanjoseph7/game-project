import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import samurai_sprite
import fighter_sprite
import ground_class
import background_class


 
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
BG = (0,0,0)
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
import player_class

# load samurai images
samurai_idle_right_images = samurai_sprite.get_idle_images()[0]
samurai_idle_left_images = samurai_sprite.get_idle_images()[1]
 

background = background_class.Background(displaysurface)
ground = ground_class.Ground(displaysurface)
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = player_class.Player(vec, displaysurface, "fighter")
player_2 = player_class.Player_2(vec, displaysurface, "samurai")


player_group = pygame.sprite.Group()
player_group.add(player)
player_2_group = pygame.sprite.Group()
player_2_group.add(player_2)



while True:
    FPS_CLOCK.tick(FPS)
    player.idle()
    player_2.idle()
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
            # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump(ground_group)
            if event.key == pygame.K_RSHIFT:
                if player.attacking == FALSE:
                    player.attack()
                    hits = pygame.sprite.spritecollide(player, player_2_group, False)
                    if hits:
                        print("player hits")
            
            if event.key == pygame.K_w:
                player_2.jump(ground_group)
            if event.key == pygame.K_LSHIFT:
                if player_2.attacking == FALSE:
                    player_2.attack()
                    hits = pygame.sprite.spritecollide(player_2, player_group, False)
                    if hits:
                        print("player 2 hits")
                
                
            


    player.gravity_check(player, ground_group)
    player_2.gravity_check(player_2, ground_group)
    # Render Functions ------
    background.render() 
    ground.render()
    player_2.update()
    player.update()
    if player.attacking:
        player.attack()
    if player_2.attacking:
        player_2.attack()
    player.move()
    player_2.move()
    displaysurface.blit(player.image, player.rect)
    displaysurface.blit(player_2.image, player_2.rect)
    player_2.move()
    player.move()
    player.update()
    player_2.update()
    pygame.display.update() 
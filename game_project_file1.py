import pygame
from pygame.locals import *
import sys
import random
import ctypes
from tkinter import filedialog
from tkinter import *
import ground_class
import background_class
import platforms
from ctypes import *

pygame.init()

HEIGHT = 900
WIDTH = 1700
ACC = 0.3
FRIC = -0.10
FPS = 90
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0, 0, 0)
SIZE_MULTIPLIER = 1.9 * 1.5
RED = (255, 0, 0)
<<<<<<< HEAD
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
=======
#YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
>>>>>>> origin/main

'''
def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
<<<<<<< HEAD
=======
        pass
>>>>>>> origin/main
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")
'''


def main():
    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    #bring_window_to_front()
    
    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(displaysurface, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(displaysurface, RED, (x, y, 400, 30))
        pygame.draw.rect(displaysurface, YELLOW, (x, y, 400 * ratio, 30))

    # Delayed imports and initializations
    import player_class
    background = background_class.Background(displaysurface)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    player1_type = "fighter"  # input("player one, fighter or samurai? ")
    player2_type = "samurai"  # input("player two, fighter or samurai? ")
    player = player_class.Player(vec, displaysurface, player1_type)
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)

    player_group = pygame.sprite.Group()
    player_group.add(player)
    player_2_group = pygame.sprite.Group()
    player_2_group.add(player_2)

    platform_width = 100 * SIZE_MULTIPLIER * 1.3
    platform_height = 30 * SIZE_MULTIPLIER
    platform1 = platforms.Platform(WIDTH * 0.1, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform2 = platforms.Platform(WIDTH * 0.40, HEIGHT / 2.8, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform3 = platforms.Platform(WIDTH * 0.70, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform_group = pygame.sprite.Group()
    platform_group.add(platform1, platform2, platform3)

    fullscreen = False
    
    font = pygame.font.SysFont('Arial', 24)

<<<<<<< HEAD
    # Game loop
=======
    players = (player, player_2)
<<<<<<< HEAD
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(displaysurface, WHITE, (x - 3, y - 2, 404, 34))
        pygame.draw.rect(displaysurface, RED, (x, y, 400, 30))
        pygame.draw.rect(displaysurface, BLACK, (x, y, 400 * ratio, 30))
=======

    last = pygame.time.get_ticks()

>>>>>>> 86f7154 (three attack combo added for samurai and fighter sprites and player class)

    # game loop
>>>>>>> origin/main
    while True:
        FPS_CLOCK.tick(FPS)
        player.idle()
        player_2.idle()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == VIDEORESIZE:
                if not fullscreen:
                    displaysurface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        displaysurface = pygame.display.set_mode((displaysurface.get_width(), displaysurface.get_height()), pygame.FULLSCREEN)
                    else:
                        displaysurface = pygame.display.set_mode((displaysurface.get_width(), displaysurface.get_height()), pygame.RESIZABLE)
                if event.key == pygame.K_UP:
                    player.jump(ground_group, platform_group)
                if event.key == pygame.K_DOWN:
                    player.fall(platform_group)
                if event.key == pygame.K_RSHIFT:
<<<<<<< HEAD
                    if not player.attacking:
=======
                    if player.attacking == FALSE:
                        if(pygame.time.get_ticks() - 750 > last):
                            player.attack_sheet = 0
                            player.attack_frame = 0
>>>>>>> origin/main
                        player.attack()
                        hits = pygame.sprite.spritecollide(player, player_2_group, False)
                        if hits:
                            print("player hits")
<<<<<<< HEAD
                            player_2.health =- 1 
=======
                        last = pygame.time.get_ticks()
                            
                
>>>>>>> origin/main
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_s:
                    player_2.fall(platform_group)
                
                if event.key == pygame.K_LSHIFT:
                    if not player_2.attacking:
                        player_2.attack()
                        hits = pygame.sprite.spritecollide(player_2, player_group, False)
                        if hits:
                            print("player 2 hits")
                            player.health =- 1

        player.gravity_check(player, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)

        # Render Functions ------
        background.render()
        ground.render()
        platform_group.draw(displaysurface)
        draw_health_bar(player.health, 20, 30)
        draw_health_bar(player_2.health, 1280, 30)
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
        
        
        # Render player numbers above each player
        player_text_surface = font.render("Player 1", True, (255, 255, 255))
        player_text_rect = player_text_surface.get_rect(center=(player.rect.centerx, player.rect.top - 20))
        displaysurface.blit(player_text_surface, player_text_rect)

        player_2_text_surface = font.render("Player 2", True, (255, 255, 255))
        player_2_text_rect = player_2_text_surface.get_rect(center=(player_2.rect.centerx, player_2.rect.top - 20))
        displaysurface.blit(player_2_text_surface, player_2_text_rect)
        
        draw_health_bar(player.health, 20, 40)
        draw_health_bar(player_2.health, 1280, 40)
        
        pygame.display.update()

if __name__ == "__main__":
    main()

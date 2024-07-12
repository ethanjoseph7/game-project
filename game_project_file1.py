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
import player_class

pygame.init()

HEIGHT = 900
WIDTH = 1700
ACC = 0.3
FRIC = -0.7
FPS = 90
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
SIZE_MULTIPLIER = 1.9*1.5
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)


def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")



def play_two_player():
    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    bring_window_to_front()

    # Delayed imports and initializations
    
    background = background_class.Background(displaysurface)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    player1_type = "Plent"  # input("player one, fighter or samurai? ")
    player2_type = "Fire_Spirit"  # input("player two, fighter or samurai? ")
    player_1 = player_class.Player(vec, displaysurface, player1_type)
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)

    player_group = pygame.sprite.Group()
    player_group.add(player_1)
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



    players = (player_1, player_2)


    # Function for creating health bar
    def draw_health_bar(player, x, y):
        ratio = player.health / 100
        if(ratio  <= 0):
            if player.number == 1:
                print("player 2 wins")
            else:
                print("player 1 wins")
            pygame.quit()
            sys.exit()
            
        if player.number == 1:
            pygame.draw.rect(displaysurface, WHITE, (x - 3, y - 2, 404, 34))
            pygame.draw.rect(displaysurface, RED, (x, y, 400, 30))
            pygame.draw.rect(displaysurface, BLACK, (x, y, 400*(1-ratio), 30))
        elif player.number == 2:
            pygame.draw.rect(displaysurface, WHITE, (x - 3, y - 2, 404, 34))
            pygame.draw.rect(displaysurface, BLACK, (x, y, 400, 30))
            pygame.draw.rect(displaysurface, RED, (x, y, 400*ratio, 30))


    def update_health():
        draw_health_bar(player_2, 20, 30)
        draw_health_bar(player_1, 1280, 30)


    player_1_last_attack = pygame.time.get_ticks()
    player_2_last_attack = pygame.time.get_ticks()

    player_1_last_frame = -1
    player_2_last_frame = -1



    # game loop

    while True:
        FPS_CLOCK.tick(FPS)
        player_1.idle()
        player_2.idle()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #Player 1 controls
                if event.key == pygame.K_UP:
                    player_1.jump(ground_group, platform_group)

                if event.key == pygame.K_DOWN:
                    player_1.fall(platform_group)

                if event.key == pygame.K_RSHIFT:
                    if(pygame.time.get_ticks() - 550 > player_1_last_attack):
                        player_1.attack_sheet = 0
                        player_1.attack_frame = 0
                        player_1_last_frame = -1

                    player_1.attack()
                    hits = pygame.sprite.spritecollide(player_1, player_2_group, False)
                    diff_frame = player_1.attack_sheet != player_1_last_frame
                    legit_attack = hits and diff_frame
                    if legit_attack and player_1.facing(player_2):

                        
                        player_2.health -= player_1.damage
                        update_health()

                    player_1_last_attack = pygame.time.get_ticks()
                    player_1_last_frame = player_1.attack_sheet
                            
                #Player 2 controls
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_s:
                    player_2.fall(platform_group)
                
                if event.key == pygame.K_LSHIFT:
                    if(pygame.time.get_ticks() - 550 > player_2_last_attack):
                        player_2.attack_sheet = 0
                        player_2.attack_frame = 0
                        player_2_last_frame = -1
                    player_2.attack()
                    hits = pygame.sprite.spritecollide(player_2, player_group, False)
                    diff_frame = player_2.attack_sheet != player_2_last_frame
                    legit_attack = hits and diff_frame
                    if legit_attack and player_2.facing(player_1):
                        player_1.health -= player_2.damage
                        update_health
                    player_2_last_attack = pygame.time.get_ticks()
                    player_2_last_frame = player_2.attack_sheet

        player_1.gravity_check(player_1, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)

        # Render Functions ------
        background.render()
        ground.render()
        platform_group.draw(displaysurface)
        
        update_health()
        player_2.update()
        player_1.update()
        if player_1.attacking:
            player_1.attack()
        if player_2.attacking:
            player_2.attack()
        player_1.move()
        player_2.move()
        displaysurface.blit(player_1.image, player_1.rect)
        displaysurface.blit(player_2.image, player_2.rect)
        player_2.move()
        player_1.move()
        player_1.update()
        player_2.update()
        
        
        # Render player numbers above each player
        player_text_surface = font.render("Player 1", True, (255, 255, 255))
        player_text_rect = player_text_surface.get_rect(center=(player_1.rect.centerx, player_1.rect.top - 20))
        displaysurface.blit(player_text_surface, player_text_rect)

        player_2_text_surface = font.render("Player 2", True, (255, 255, 255))
        player_2_text_rect = player_2_text_surface.get_rect(center=(player_2.rect.centerx, player_2.rect.top - 20))
        displaysurface.blit(player_2_text_surface, player_2_text_rect)
    
        
        pygame.display.update()

def play_one_player():
    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    #bring_window_to_front()

    # Delayed imports and initializations
    
    background = background_class.Background(displaysurface)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    player1_type = "Fighter"  # input("player one, fighter or samurai? ")
    player2_type = "Samurai"  # input("player two, fighter or samurai? ")
    player_1 = player_class.Player(vec, displaysurface, player1_type)
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)

    player_group = pygame.sprite.Group()
    player_group.add(player_1)
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



    players = (player_1, player_2)


    # Function for creating health bar
    def draw_health_bar(player, x, y):
        ratio = player.health / 100
        if(ratio  <= 0):
            if player.number == 1:
                print("player 2 wins")
            else:
                print("player 1 wins")
            pygame.quit()
            sys.exit()
            
        if player.number == 1:
            pygame.draw.rect(displaysurface, WHITE, (x - 3, y - 2, 404, 34))
            pygame.draw.rect(displaysurface, RED, (x, y, 400, 30))
            pygame.draw.rect(displaysurface, BLACK, (x, y, 400*(1-ratio), 30))
        elif player.number == 2:
            pygame.draw.rect(displaysurface, WHITE, (x - 3, y - 2, 404, 34))
            pygame.draw.rect(displaysurface, BLACK, (x, y, 400, 30))
            pygame.draw.rect(displaysurface, RED, (x, y, 400*ratio, 30))


    def update_health():
        draw_health_bar(player_2, 20, 30)
        draw_health_bar(player_1, 1280, 30)


    player_1_last_attack = pygame.time.get_ticks()
    player_2_last_attack = pygame.time.get_ticks()

    player_1_last_frame = -1
    player_2_last_frame = -1



    # game loop

    while True:
        FPS_CLOCK.tick(FPS)
        player_1.idle()
        player_2.idle()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #Player 1 controls
                if event.key == pygame.K_UP:
                    player_1.jump(ground_group, platform_group)

                if event.key == pygame.K_DOWN:
                    player_1.fall(platform_group)

                if event.key == pygame.K_RSHIFT:
                    if(pygame.time.get_ticks() - 550 > player_1_last_attack):
                        player_1.attack_sheet = 0
                        player_1.attack_frame = 0
                        player_1_last_frame = -1

                    player_1.attack()
                    hits = pygame.sprite.spritecollide(player_1, player_2_group, False)
                    diff_frame = player_1.attack_sheet != player_1_last_frame
                    legit_attack = hits and diff_frame
                    if legit_attack and player_1.facing(player_2):

                        
                        player_2.health -= player_1.damage
                        update_health()

                    player_1_last_attack = pygame.time.get_ticks()
                    player_1_last_frame = player_1.attack_sheet
                            
                #Player 2 controls
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_s:
                    player_2.fall(platform_group)
                
                if event.key == pygame.K_LSHIFT:
                    if(pygame.time.get_ticks() - 550 > player_2_last_attack):
                        player_2.attack_sheet = 0
                        player_2.attack_frame = 0
                        player_2_last_frame = -1
                    player_2.attack()
                    hits = pygame.sprite.spritecollide(player_2, player_group, False)
                    diff_frame = player_2.attack_sheet != player_2_last_frame
                    legit_attack = hits and diff_frame
                    if legit_attack and player_2.facing(player_1):
                        player_1.health -= player_2.damage
                        update_health
                    player_2_last_attack = pygame.time.get_ticks()
                    player_2_last_frame = player_2.attack_sheet

        player_1.gravity_check(player_1, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)

        # Render Functions ------
        background.render()
        ground.render()
        platform_group.draw(displaysurface)
        
        update_health()
        player_2.update()
        player_1.update()
        if player_1.attacking:
            player_1.attack()
        if player_2.attacking:
            player_2.attack()
        player_1.move()
        player_2.move()
        displaysurface.blit(player_1.image, player_1.rect)
        displaysurface.blit(player_2.image, player_2.rect)
        player_2.move()
        player_1.move()
        player_1.update()
        player_2.update()
        
        
        # Render player numbers above each player
        player_text_surface = font.render("Player 1", True, (255, 255, 255))
        player_text_rect = player_text_surface.get_rect(center=(player_1.rect.centerx, player_1.rect.top - 20))
        displaysurface.blit(player_text_surface, player_text_rect)

        player_2_text_surface = font.render("Player 2", True, (255, 255, 255))
        player_2_text_rect = player_2_text_surface.get_rect(center=(player_2.rect.centerx, player_2.rect.top - 20))
        displaysurface.blit(player_2_text_surface, player_2_text_rect)
    
        
        pygame.display.update()



def main():
    play_two_player()

if __name__ == "__main__":
    main()
    


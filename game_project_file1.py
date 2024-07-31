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
import enemy_class

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

'''
def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")
'''


def play_two_player():
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
    player1_type = "Plent"  # input("player one, fighter or samurai? ")
    player2_type = "Fighter"  # input("player two, fighter or samurai? ")
    

    platform_width = 100 * SIZE_MULTIPLIER * 1.3
    platform_height = 30 * SIZE_MULTIPLIER
    platform1 = platforms.Platform(WIDTH * 0.1, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform2 = platforms.Platform(WIDTH * 0.40, HEIGHT / 2.8, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform3 = platforms.Platform(WIDTH * 0.70, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform_group = pygame.sprite.Group()
    platform_group.add(platform1, platform2, platform3)

    player_1 = player_class.Player(vec, displaysurface, player1_type, ground_group, platform_group)
    player_2 = player_class.Player_2(vec, displaysurface, player2_type, ground_group, platform_group)

    player_1_group = pygame.sprite.Group()
    player_1_group.add(player_1)
    player_2_group = pygame.sprite.Group()
    player_2_group.add(player_2)
 
    fullscreen = False
    
    font = pygame.font.SysFont('Arial', 24)



    players = (player_1, player_2)


    # Function for creating health bar


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
                    player_1.jump()

                if event.key == pygame.K_DOWN:
                    player_1.fall()

                if event.key == pygame.K_RSHIFT:
                    player_1.attack()
                    print(str(player_2.health))
                            
                #Player 2 controls
                if event.key == pygame.K_w:
                    player_2.jump()
                if event.key == pygame.K_s:
                    player_2.fall()
                
                if event.key == pygame.K_LSHIFT:
                    player_2.attack()

        player_1.gravity_check()
        player_2.gravity_check()

        # Render Functions ------
        background.render()
        ground.render()
        platform_group.draw(displaysurface)
        
        update_health(player_1, displaysurface)
        update_health(player_2, displaysurface)
        player_2.update()
        player_1.update()

        if player_1.attacking:
            register_attack(player_1, player_2, player_2_group, displaysurface)
            player_1.attack()

        if player_2.attacking:
            register_attack(player_2, player_1, player_1_group, displaysurface)
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
    player_type = "Fighter"
    enemy_type = "Skeleton"
    

    platform_width = 100 * SIZE_MULTIPLIER * 1.3
    platform_height = 30 * SIZE_MULTIPLIER
    platform1 = platforms.Platform(WIDTH * 0.1, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform2 = platforms.Platform(WIDTH * 0.40, HEIGHT / 2.8, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform3 = platforms.Platform(WIDTH * 0.70, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)

    platform_group = pygame.sprite.Group()
    platform_group.add(platform1, platform2, platform3)

    player = player_class.Player(vec, displaysurface, player_type, ground_group, platform_group)
    enemy = enemy_class.Enemy(vec, displaysurface, enemy_type, ground_group, platform_group, player)

    player_group = pygame.sprite.Group()
    player_group.add(player)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    fullscreen = False
    
    font = pygame.font.SysFont('Arial', 24)

    # game loop

    while True:
        FPS_CLOCK.tick(FPS)
        player.idle()
        enemy.idle()
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
                    player.jump()

                if event.key == pygame.K_DOWN:
                    player.fall()

                if event.key == pygame.K_RSHIFT:
                    player.attack()
                    
                            
                
        player.gravity_check()
        enemy.gravity_check()

        # Render Functions ------
        background.render()
        ground.render()
        platform_group.draw(displaysurface)
        
        update_health(player, displaysurface)
        update_health(enemy, displaysurface)
        enemy.update()
        player.update()

        
        if player.attacking:
            register_attack(player, enemy, enemy_group, displaysurface)
            player.attack()
            

        enemy.attack()
        if enemy.attacking:
            register_attack(enemy, player, player_group, displaysurface)

        player.move()
        enemy.move()

        enemy.warp()
        enemy.jump()

        displaysurface.blit(player.image, player.rect)
        displaysurface.blit(enemy.image, enemy.rect)

        enemy.move()
        player.move()

        

        enemy.fall()

        player.update()
        enemy.update()
        
        
        # Render player numbers above each player
        player_text_surface = font.render("Player", True, (255, 255, 255))
        player_text_rect = player_text_surface.get_rect(center=(player.rect.centerx, player.rect.top - 20))
        displaysurface.blit(player_text_surface, player_text_rect)

        enemy_text_surface = font.render("Enemy", True, (255, 255, 255))
        enemy_text_rect = enemy_text_surface.get_rect(center=(enemy.rect.centerx, enemy.rect.top - 20))
        displaysurface.blit(enemy_text_surface, enemy_text_rect)
    
        
        pygame.display.update()

def register_attack(fighter, opponent, opponent_sprite_group, displaysurface):
    hits = pygame.sprite.spritecollide(fighter, opponent_sprite_group, False)
    diff_frame = fighter.attack_sheet != fighter.last_frame
    legit_attack = hits and diff_frame

    if legit_attack and fighter.facing(opponent) and fighter.attack_spaced:
            opponent.health -= fighter.damage
            update_health(opponent, displaysurface)

    fighter.last_frame = fighter.attack_sheet
    return

def draw_health_bar(player, x, y, displaysurface):
        ratio = player.health / 100
        
        if(player.health <= 1):
            if player.number == 1:
                print("enemy wins")
            else:
                print("player wins")
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

def update_health(character, displaysurface):
    if character.number == 1:
        draw_health_bar(character, 1280, 30, displaysurface)
    else:
        draw_health_bar(character, 20, 30, displaysurface)


def main():
    number_of_players = 1 #input("how many players: ")
    if int(number_of_players) == 1:
        play_one_player()
    elif int(number_of_players) == 2:
        play_two_player()
    else:
        print("need to input 1 or 2")

if __name__ == "__main__":
    main()
    


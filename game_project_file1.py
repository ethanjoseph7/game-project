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
from bat_swarm import BatSwarm
import player_class
import player_class

pygame.init()

HEIGHT = 900
WIDTH = 1700
ACC = 0.3
FRIC = -0.7
FPS = 90
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0, 0, 0)
SIZE_MULTIPLIER = 1.9 * 1.5

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
dark_red = (139, 0, 0)
grey = (64, 64, 64)
outline_color = (105, 100, 100)  # Light grey color for the outline

# Health bar constants
max_health = 100
bar_width = 400
bar_height = 30
outline_thickness = 1
corner_radius = 15

def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")



def play_game():
    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    bring_window_to_front()
    

    background = background_class.Background(displaysurface)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    bat_swarm = BatSwarm(displaysurface)
    player1_type = "fighter"  # input("player one, fighter or samurai? ")
    player2_type = "samurai"  # input("player two, fighter or samurai? ")
    player = player_class.Player(vec, displaysurface, player1_type)
    player.health = 100
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)
    player_2.health = 100

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


    last = 0
   

    def draw_rounded_rect(surface, color, rect, corner_radius):
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def draw_vertical_gradient_rect(surface, rect, color1, color2, middle_color):
        x, y, width, height = rect
        half_height = height // 2
        for i in range(half_height):
            factor_up = i / half_height
            factor_down = i / half_height
            color_up = tuple(int(middle_color[j] + (color1[j] - middle_color[j]) * factor_up ) for j in range(3))
            color_down = tuple(int(middle_color[j] + (color2[j] - middle_color[j]) * factor_down) for j in range(3))
            line_rect_up = (x, y + half_height - i - 1, width, 1)
            line_rect_down = (x, y + half_height + i, width, 1)
            pygame.draw.rect(surface, color_up, line_rect_up)
            pygame.draw.rect(surface, color_down, line_rect_down)

    def draw_health_bar(screen, health, x, y):
        # Background bar
        bg_rect = pygame.Rect(x - bar_width // 2, y - bar_height // 2, bar_width, bar_height)
        draw_rounded_rect(screen, dark_red, bg_rect, corner_radius)

        # Health bar
        current_width = int((health / max_health) * bar_width)
        health_rect = pygame.Rect(x - bar_width // 2, y - bar_height // 2, current_width, bar_height)
        draw_vertical_gradient_rect(screen, health_rect, black, black, grey)

        # Outline
        outline_rect = pygame.Rect(x - bar_width // 2 - outline_thickness, y - bar_height // 2 - outline_thickness,
                                   bar_width + 2 * outline_thickness, bar_height + 2 * outline_thickness)
        pygame.draw.rect(screen, outline_color, outline_rect, border_radius=corner_radius + outline_thickness, width=outline_thickness)
        
    # game loop
    while True:
        FPS_CLOCK.tick(FPS)
        player_1.idle()
        player_2.idle()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
            # Event handling for a range of different key presses
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        displaysurface = pygame.display.set_mode((displaysurface.get_width(), displaysurface.get_width()), pygame.FULLSCREEN)
                    else:
                        displaysurface = pygame.display.set_mode((displaysurface.get_width(), displaysurface.get_width()), pygame.FULLSCREEN)

                if event.key == pygame.K_UP:
                    player_1.jump(ground_group, platform_group)

                if event.key == pygame.K_DOWN:
                    player_1.fall(platform_group)

                if event.key == pygame.K_RSHIFT:
                    if not player_1.attacking:
                        if(pygame.time.get_ticks() - 750 > last):
                            player_1.attack_sheet = 0
                            player_1.attack_frame = 0

                        player_1.attack()
                        hits = pygame.sprite.spritecollide(player_1, player_2_group, False)
                        if hits and player_1.facing(player_2):

                            player_2.health -= 10  
                        last = pygame.time.get_ticks()
                            
                #Player 2 controls
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_s:
                    player_2.fall(platform_group)

                if event.key == pygame.K_LSHIFT:
                    if not player_2.attacking:
                        player_2.attack()
                        hits = pygame.sprite.spritecollide(player_2, player_group, False)
                        if hits and player_2.facing(player_1):
                            player_1.health -= 10
                            update_health

        player_1.gravity_check(player_1, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)

        # Render Functions ------
        background.render()
        bat_swarm.update()
        bat_swarm.render()
        ground.render()
        platform_group.draw(displaysurface)

        draw_health_bar(displaysurface, player.health, 220, 40)
        draw_health_bar(displaysurface, player_2.health, 1480, 40)
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
        assign_player_tags(displaysurface, font, players)

        pygame.display.update()

def assign_player_tags(displaysurface, font, players):
    player = players[0]
    player_2 = players[1]
    player_text_surface = font.render("Player 1", True, (255, 255, 255))
    player_text_rect = player_text_surface.get_rect(center=(player.rect.centerx, player.rect.top - 20))
    displaysurface.blit(player_text_surface, player_text_rect)

    player_2_text_surface = font.render("Player 2", True, (255, 255, 255))
    player_2_text_rect = player_2_text_surface.get_rect(center=(player_2.rect.centerx, player_2.rect.top - 20))
    displaysurface.blit(player_2_text_surface, player_2_text_rect)
    
        
    pygame.display.update()



def main():
    play_game()

if __name__ == "__main__":
    main()
    


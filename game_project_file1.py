import pygame
from pygame.locals import *
import sys
import random
import ctypes
import imageio
from PIL import Image as PilImage
from tkinter import filedialog
from tkinter import *
import ground_class
import background_class
import platforms
from bat_swarm import BatSwarm
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
blue = (0, 0, 255)
outline_color = (105, 100, 100)  # Light grey color for the outline

# Health bar constants
max_health = 100
bar_width = 400
bar_height = 30
outline_thickness = 1
corner_radius = 15
heart_size = (30, 30)
heart_sprite_sheet = pygame.image.load('heart_lives.png')

def extract_heart_images(sprite_sheet, heart_size):
    heart_images = []
    for i in range(3):
        heart_image = sprite_sheet.subsurface(pygame.Rect(i * heart_size[0], 0, heart_size[0], heart_size[1]))
        heart_images.append(pygame.transform.scale(heart_image, heart_size))
    return heart_images

full_heart_image, half_heart_image, empty_heart_image = extract_heart_images(heart_sprite_sheet, heart_size)

def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")

def reset_round(player_1, player_2):
    player_1.health = max_health
    player_2.health = max_health
    player_1.rect.topleft = (100, HEIGHT - 150)  # Reset player positions as needed
    player_2.rect.topleft = (WIDTH - 200, HEIGHT - 150)
    player_1.velocity = pygame.math.Vector2(0, 0)
    player_2.velocity = pygame.math.Vector2(0, 0)

def load_gif_frames(filename):
    gif = imageio.mimread(filename)
    frames = []
    for frame in gif:
        # Convert the frame to a PIL Image
        pil_image = PilImage.fromarray(frame)

        # Convert the PIL Image to a mode that pygame can use (RGBA)
        pil_image = pil_image.convert("RGBA")

        # Convert the PIL Image to a format pygame can use
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()

        # Create a pygame Surface from the PIL Image data
        frame_surface = pygame.image.fromstring(data, size, mode)
        
        # Scale the frame to the screen size
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        
        frames.append(frame_surface)
    return frames

def menu_screen():
    vec = pygame.math.Vector2
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Menu")

    # Load GIF frames
    gif_frames = load_gif_frames('menu.gif')
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    font = pygame.font.SysFont('Arial', 50)

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def button(text, font, color, rect, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            if click[0] == 1 and action is not None:
                action()

        pygame.draw.rect(displaysurface, color, rect, border_radius=15)
        pygame.draw.rect(displaysurface, blue, rect, 2, border_radius=15)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        displaysurface.blit(text_surface, text_rect)

    def start_game():
        play_game()

    def quit_game():
        pygame.quit()
        sys.exit()

    while True:
        FramePerSec.tick(FPS)

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_text('Game Menu', font, (255, 255, 255), displaysurface, WIDTH // 2 - 100, HEIGHT // 4)

        start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        button('Start', font, red, start_button_rect, start_game)
        button('Exit', font, red, exit_button_rect, quit_game)

        pygame.display.update()

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
    player1_type = "shinobi"
    player2_type = "samurai"
    player_1 = player_class.Player(vec, displaysurface, player1_type)
    player_1.health = 100
    player_1.lives = 3  # Initial lives
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)
    player_2.health = 100
    player_2.lives = 3  # Initial lives

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
    round_number = 1
    round_start_time = None

    def draw_rounded_rect(surface, color, rect, corner_radius):
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def draw_vertical_gradient_rect(surface, rect, color1, color2, middle_color):
        x, y, width, height = rect
        for i in range(height):
            ratio = i / height
            if ratio < 0.5:
                new_color = (
                    int(color1[0] + (middle_color[0] - color1[0]) * ratio * 2),
                    int(color1[1] + (middle_color[1] - color1[1]) * ratio * 2),
                    int(color1[2] + (middle_color[2] - color1[2]) * ratio * 2)
                )
            else:
                new_color = (
                    int(middle_color[0] + (color2[0] - middle_color[0]) * (ratio - 0.5) * 2),
                    int(middle_color[1] + (color2[1] - middle_color[1]) * (ratio - 0.5) * 2),
                    int(middle_color[2] + (color2[2] - middle_color[2]) * (ratio - 0.5) * 2)
                )
            pygame.draw.line(surface, new_color, (x, y + i), (x + width, y + i))

    def draw_health_bar(screen, health, x, y, align="left"):
        bg_rect = pygame.Rect(x - bar_width // 2, y - bar_height // 2, bar_width, bar_height)
        draw_rounded_rect(screen, grey, bg_rect, corner_radius)
        draw_rounded_rect(screen, red, pygame.Rect(x - bar_width // 2, y - bar_height // 2, bar_width, bar_height), corner_radius)
        if align == "left":
            health_rect = pygame.Rect(x - bar_width // 2, y - bar_height // 2, int((health / max_health) * bar_width), bar_height)
        else:
            health_rect = pygame.Rect(x - bar_width // 2 + (bar_width - int((health / max_health) * bar_width)), y - bar_height // 2, int((health / max_health) * bar_width), bar_height)
        draw_rounded_rect(screen, dark_red, health_rect, corner_radius)
        outline_rect = pygame.Rect(x - bar_width // 2, y - bar_height // 2, bar_width, bar_height)
        pygame.draw.rect(screen, outline_color, outline_rect, outline_thickness, border_radius=corner_radius)

    def draw_lives(screen, health, lives, x, y):
        max_hearts = 5
        hearts_to_draw = min(lives, max_hearts)

        for i in range(hearts_to_draw):
            if health <= 0 and i == hearts_to_draw - 1:
                screen.blit(empty_heart_image, (x + i * heart_size[0], y))
            else:
                screen.blit(full_heart_image, (x + i * heart_size[0], y))

    def display_round_text(round_number):
        text = f"Round {round_number}"
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        displaysurface.blit(text_surface, text_rect)
        pygame.display.update()

    while True:
        FPS_CLOCK.tick(FPS)
        current_time = pygame.time.get_ticks()

        if round_start_time and current_time - round_start_time < 3000:
            display_round_text(round_number)

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
                        if(pygame.time.get_ticks() - 550 > player_1_last):
                            player_1.attack_sheet = 0
                            player_1.attack_frame = 0

                        player_1.attack()
                        hits = pygame.sprite.spritecollide(player_1, player_2_group, False)
                        if hits and player_1.facing(player_2):

                            player_2.health -= player_1.damage
                            update_health()

                        player_1_last = pygame.time.get_ticks()
                            
                #Player 2 controls
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_s:
                    player_2.fall(platform_group)

                if event.key == pygame.K_LSHIFT:
                    if not player_2.attacking:
                        if(pygame.time.get_ticks() - 550 > player_2_last):
                            player_2.attack_sheet = 0
                            player_2.attack_frame = 0
                        player_2.attack()
                        hits = pygame.sprite.spritecollide(player_2, player_group, False)
                        if hits and player_2.facing(player_1):
                            player_1.health -= player_2.damage
                            update_health
                        player_2_last = pygame.time.get_ticks()

        player_1.gravity_check(player_1, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)

        if player_1.health <= 0:
            player_1.lives -= 1
            if player_1.lives > 0:
                round_number += 1
                round_start_time = pygame.time.get_ticks()
            else:
                print("Player 1 is out of lives!")
                menu_screen()
                return
        if player_2.health <= 0:
            player_2.lives -= 1
            if player_2.lives > 0:
                round_number += 1
                round_start_time = pygame.time.get_ticks()
            else:
                print("Player 2 is out of lives!")
                menu_screen()
                return

        background.render()
        bat_swarm.update()
        bat_swarm.render()
        ground.render()
        platform_group.draw(displaysurface)

        draw_health_bar(displaysurface, player_1.health, 220, 40, align="left")
        draw_lives(displaysurface, player_1.health, player_1.lives, 50, 80)
        draw_health_bar(displaysurface, player_2.health, 1480, 40, align="right")
        draw_lives(displaysurface, player_2.health, player_2.lives, 1600, 80)
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
    menu_screen()

if __name__ == "__main__":
    main()

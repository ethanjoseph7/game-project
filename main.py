import pygame
from pygame.locals import *
import sys
import random
import ctypes
from tkinter import *
import player_class
import imageio
import enemy_class
import os
from utils import load_gif_frames
from PIL import Image

pygame.init()

HEIGHT = 900
WIDTH = 1700
ACC = 0.3
FRIC = -0.7
FPS = 90
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
SIZE_MULTIPLIER = 1.9 * 1.5
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

vec = pygame.math.Vector2
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

player1_type = "fighter"
player2_type = "fighter"
background_name = None

play_single= False
play_double = False
game_over = False


# Method to bring the game window to the front
def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")

def setting_menu():
        menu_font = pygame.font.SysFont('Arial', 30)
        menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 128))

        resume_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/resume_button.png'), (300, 150))
        brightness_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/brightness_button.png'), (300, 150))
        home_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/home_button.png'), (300, 150))
        key_bindings_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/key_bindings_button.png'), (300, 150))
        restart_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/restart_button.png'), (300, 150))

        def image_button(image, pos, action=None):
            rect = image.get_rect(topleft=pos)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if rect.collidepoint(mouse):
                if click[0] == 1 and action is not None:
                    action()

            menu_surface.blit(image, rect)

        image_button(resume_button_img, (WIDTH // 2 - resume_button_img.get_width() // 2, 50))
        image_button(key_bindings_button_img, (WIDTH // 2 - key_bindings_button_img.get_width() // 2, 212.5))
        image_button(brightness_button_img, (WIDTH // 2 - brightness_button_img.get_width() // 2, 375))
        image_button(restart_button_img, (WIDTH // 2 - restart_button_img.get_width() // 2, 537.5))
        image_button(home_button_img, (WIDTH // 2 - home_button_img.get_width() // 2, 700))

        displaysurface.blit(menu_surface, (0, 0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button_img.get_rect(topleft=(WIDTH // 2 - resume_button_img.get_width() // 2, 50)).collidepoint(event.pos):
                        return
                    elif key_bindings_button_img.get_rect(topleft=(WIDTH // 2 - key_bindings_button_img.get_width() // 2, 212.5)).collidepoint(event.pos):
                        print("Key Bindings button clicked")
                    elif brightness_button_img.get_rect(topleft=(WIDTH // 2 - brightness_button_img.get_width() // 2, 375)).collidepoint(event.pos):
                        print("Brightness button clicked")
                    elif restart_button_img.get_rect(topleft=(WIDTH // 2 - restart_button_img.get_width() // 2, 537.5)).collidepoint(event.pos):
                        play_two_player()
                        return
                    elif home_button_img.get_rect(topleft=(WIDTH // 2 - home_button_img.get_width() // 2, 700)).collidepoint(event.pos):
                        menu_screen()
                        return


# Method for the menu screen at the start of the game
def menu_screen():
    gif_frames = load_gif_frames('assets/menu.gif', WIDTH, HEIGHT)
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    start_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/play_button.png'), (295, 150))
    exit_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/exit_button.png'), (275, 150))
    setting_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/setting_button.png'), (150, 150))

    rotation_angle = 0

  
    def draw_button_with_shadow(image, pos, offset=(5, 5), shadow_color=(50, 50, 50)):
        shadow_image = image.copy()
        shadow_image.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)
        displaysurface.blit(shadow_image, (pos[0] + offset[0], pos[1] + offset[1]))
        displaysurface.blit(image, pos)

    def image_button(image, pos, action=None, rotate=False, jump=False):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            if click[0] == 1 and action is not None:
                action()
            if rotate:
                rotated_image = pygame.transform.rotate(image, rotation_angle)
                rect = rotated_image.get_rect(center=rect.center)
                draw_button_with_shadow(rotated_image, rect.topleft)
            elif jump:
                jump_pos = (pos[0], pos[1] - 10)
                draw_button_with_shadow(image, jump_pos)
            else:
                draw_button_with_shadow(image, rect.topleft)
        else:
            draw_button_with_shadow(image, rect.topleft)

    def start_game():
        select_play_type()
        return

    def quit_game():
        pygame.quit()
        sys.exit()

    while True:
        FramePerSec.tick(FPS)

        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        rotation_angle += 1
        if rotation_angle >= 360:
            rotation_angle = 0

        image_button(start_button_img, (WIDTH // 2 - start_button_img.get_width() // 2, HEIGHT // 2 - 100), start_game, jump=True)
        image_button(exit_button_img, (WIDTH // 2 - exit_button_img.get_width() // 2, HEIGHT // 2), quit_game, jump=True)
        image_button(setting_button_img, (25, 25), setting_menu, rotate=True)

        pygame.display.update()


def select_play_type():
    global single_play, double_play


    # Load GIF frames
    gif_frames = load_gif_frames('assets/menu.gif', WIDTH, HEIGHT)
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    # Load button images
    single_player_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/single_play.png'), (475, 275))
    double_player_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/double_play.png'), (475, 275))
    back_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/back_button.png'), (150, 150))

    # Method to draw a button with a shadow
    def draw_button_with_shadow(image, pos, offset=(5, 5), shadow_color=(50, 50, 50)):
        shadow_image = image.copy()
        shadow_image.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)
        displaysurface.blit(shadow_image, (pos[0] + offset[0], pos[1] + offset[1]))
        displaysurface.blit(image, pos)

    # Method to create buttons with images
    def image_button(image, pos, action=None):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            jump_offset = -10  # How much the button should "jump" when hovered
            draw_button_with_shadow(image, (pos[0], pos[1] + jump_offset))
            if click[0] == 1 and action is not None:
                action()
        else:
            draw_button_with_shadow(image, pos)

    def single_play():
        global play_single, play_double
        play_single = True
        play_double = False
        select_back()
        return
        
    def double_play():
        global play_double, play_single
        play_double = True
        play_single = False
        select_back()
        return
    
    def go_back():
        menu_screen()
        return

    while True:
        FramePerSec.tick(FPS)

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()

        # Display buttons
        image_button(single_player_button_img, (WIDTH // 3 - single_player_button_img.get_width(), HEIGHT // 2.5), single_play)
        image_button(double_player_button_img, (WIDTH // 2 + double_player_button_img.get_width() - double_player_button_img.get_width() // 3, HEIGHT // 2.5), double_play)
        image_button(back_button_img, (25, 25), go_back)

        pygame.display.update()
        






# Load GIF frames once and cache them
def ld_gif_frames(file_path):
    pil_image = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = pil_image.copy().convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_image)
            pil_image.seek(pil_image.tell() + 1)
    except EOFError:
        pass
    return frames

# Caching background images and GIF frames
def cache_backgrounds():
    backgrounds = [f for f in os.listdir('assets/backgrounds') if os.path.isfile(os.path.join('assets/backgrounds', f))]
    background_images = {bg: pygame.image.load(os.path.join('assets/backgrounds', bg)).convert_alpha() for bg in backgrounds if bg.endswith('.png')}
    background_gifs = {bg: ld_gif_frames(os.path.join('assets/backgrounds', bg)) for bg in backgrounds if bg.endswith('.gif')}
    background_thumbnails = {bg: pygame.transform.scale(background_images[bg], (180, 120)) for bg in background_images}
    background_thumbnails.update({bg: pygame.transform.scale(background_gifs[bg][0], (180, 120)) for bg in background_gifs})  # Use the first frame of GIF for thumbnail
    return backgrounds, background_images, background_gifs, background_thumbnails

backgrounds, background_images, background_gifs, background_thumbnails = cache_backgrounds()

# Main function to handle the background selection
def select_back():
    global background_name


    # Load GIF frames
    gif_frames = load_gif_frames('assets/menu.gif', WIDTH, HEIGHT)
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0
    
    # Load button images
    back_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/back_button.png'), (150, 150))
    play_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/play_button.png'), (300, 150))
    random_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/random_button.png'), (300, 150))

    # Initialize variables for scrolling and selected background
    scroll_offset = 0
    max_scroll = max(0, (len(backgrounds) // 4 + (1 if len(backgrounds) % 4 != 0 else 0)) * 135 - 450)
    scroll_surface_pos = (200, 200)
    
    box_size = (400, 200)
    box_gif_frames = ld_gif_frames("assets/backgrounds/aldo.gif")
    box_gif_frames = [pygame.transform.scale(frame, box_size) for frame in box_gif_frames]
    box_rect = box_gif_frames[0].get_rect(topleft=(WIDTH - 440, 200))
    box_frame_index = 0
    box_frame_time = 0


    def draw_button_with_shadow(image, pos, surface, offset=(5, 5), shadow_color=(50, 50, 50)):
        shadow_image = image.copy()
        shadow_image.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(shadow_image, (pos[0] + offset[0], pos[1] + offset[1]))
        surface.blit(image, pos)

    def image_button(image, pos, surface, action=None):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if surface == displaysurface:
            mouse_rel = mouse
        else:
            mouse_rel = (mouse[0] - scroll_surface_pos[0], mouse[1] - scroll_surface_pos[1])

        if rect.collidepoint(mouse_rel):
            jump_offset = -7  # How much the button should "jump" when hovered
            draw_button_with_shadow(image, (pos[0], pos[1] + jump_offset), surface)
            if click[0] == 1 and action is not None:
                action()
                pygame.time.wait(200)  # Add a short delay to prevent multiple clicks
        else:
            draw_button_with_shadow(image, pos, surface)

    def go_back():
        select_play_type()
        return

    def select_character():
        if background_name:
            select_char()
        else:
            show_warning("Select a background first!")
        return

    def set_background(name):
        global background_name
        background_name = name
        return

    def select_random_background():
        global background_name
        background_name = random.choice(backgrounds)
        return

    def show_warning(message):
        font = pygame.font.SysFont(None, 36)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH - play_button_img.get_width() / 2, 750 + play_button_img.get_height() / 2))
        displaysurface.blit(text, text_rect)
        pygame.display.update(text_rect)  # Update only the warning text area
        pygame.time.wait(2000)

    selected_background_img = None
    selected_background_gif_frames = []
    selected_background_is_gif = False

    while True:
        FramePerSec.tick(FPS)

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        current_time = pygame.time.get_ticks()

        # Update box animation
        if current_time - box_frame_time >= 100:
            box_frame_index = (box_frame_index + 1) % len(box_gif_frames)
            box_frame_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_offset = max(scroll_offset - 30, 0)
                elif event.button == 5:  # Scroll down
                    scroll_offset = min(scroll_offset + 30, max_scroll)
                    
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()

        # Display buttons
        image_button(back_button_img, (25, 25), displaysurface, go_back)
        image_button(play_button_img, (WIDTH - play_button_img.get_width() * 3, 750), displaysurface, select_character)
        image_button(random_button_img, (WIDTH - random_button_img.get_width() * 4.5, 750), displaysurface, select_random_background)

        # Create a surface for the scrollable area
        scroll_surface = pygame.Surface((1000, 450), pygame.SRCALPHA)

        # Render background image buttons in a grid format (4 per row)
        for i, background in enumerate(backgrounds):
            x = (i % 4) * 240 + 15
            y = (i // 4) * 135 - scroll_offset
            image_button(background_thumbnails[background], (x, y), scroll_surface, action=lambda bg=background: set_background(bg))

        displaysurface.blit(scroll_surface, scroll_surface_pos)

        # Draw the scrollbar
        if max_scroll > 0:
            scroll_bar_y = scroll_surface_pos[1] + int((scroll_offset / max_scroll) * (450 - 75))
        else:
            scroll_bar_y = scroll_surface_pos[1]

        pygame.draw.rect(displaysurface, (100, 100, 100), (scroll_surface_pos[0] + 1000, scroll_bar_y, 30, 75))

        # Display selected background on the right side
        if background_name:
            base_name = background_name.rsplit('.', 1)[0].replace('_', ' ')  # Extract base name without extension and replace underscores with spaces
            
            if background_name.endswith('.png'):
                selected_background_img = pygame.transform.scale(background_images[background_name], box_size)
                selected_background_is_gif = False
            elif background_name.endswith('.gif'):
                selected_background_gif_frames = background_gifs[background_name]
                selected_background_gif_frames = [pygame.transform.scale(frame, box_size) for frame in selected_background_gif_frames]
                selected_background_is_gif = True
            
            if selected_background_is_gif:
                box_gif_frame_index = (current_time // 100) % len(selected_background_gif_frames)
                displaysurface.blit(selected_background_gif_frames[box_gif_frame_index], box_rect.topleft)
            else:
                displaysurface.blit(selected_background_img, box_rect.topleft)
            
            # Add a thick outline to the box
            pygame.draw.rect(displaysurface, (255, 255, 255), box_rect, 5)

            # Render the background name below the box
            font = pygame.font.SysFont(None, 32)  # Choose a font and size
            text_surface = font.render(base_name, True, (255, 255, 255))  # Render the text
            text_rect = text_surface.get_rect(midtop=(box_rect.centerx, box_rect.bottom + 10))  # Position the text
            displaysurface.blit(text_surface, text_rect)  # Blit the text surface onto the display surface

        pygame.display.update()




def select_char():
    # This method allows the players to select their characters for the game by dragging circles onto character buttons.
    # The selected characters are then used in the two-player game.
    
    global player1_type, player2_type
    screen = displaysurface


    # Load GIF frames
    gif_frames = load_gif_frames('assets/menu.gif', WIDTH, HEIGHT)
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    # Load the button images and names
    characters = [
        {"name": "fighter", "image": pygame.transform.scale(pygame.image.load('assets/players/fighter.png'), (260, 260))},
        {"name": "samurai", "image": pygame.transform.scale(pygame.image.load('assets/players/samurai.png'), (260, 260))},
        {"name": "shinobi", "image": pygame.transform.scale(pygame.image.load('assets/players/shinobi.png'), (260, 260))},
        {"name": "skeleton", "image": pygame.transform.scale(pygame.image.load('assets/players/skeleton.png'), (260, 260))}
    ]

    # Define button positions
    button_rects = [
        characters[0]["image"].get_rect(topleft=(200, 150)),
        characters[1]["image"].get_rect(topleft=(550, 150)),
        characters[2]["image"].get_rect(topleft=(900, 150)),
        characters[3]["image"].get_rect(topleft=(1250, 150))
    ]

    # Set up the font for the subheading
    font = pygame.font.SysFont('Arial', 24)
    subheading_texts = [char["name"] for char in characters]
    subheading_surfaces = [font.render(text, True, (255, 255, 255)) for text in subheading_texts]

    # Player selection variables
    selected_player_1 = None
    selected_player_2 = None
    player_1_name = None
    player_2_name = None

    # Draggable circles
    p1_circle = pygame.Rect(50, 50, 80, 80)
    p2_circle = pygame.Rect(150, 50, 80, 80)
    p1_dragging = False
    p2_dragging = False

    # Images button
    start_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/play_button.png'), (295, 150))
    back_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/back_button.png'), (150, 150))
    
    def image_button(image, pos, action=None):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            if click[0] == 1 and action is not None:
                action()

        displaysurface.blit(image, rect)

    # Function to draw the buttons and player indicators
    def draw_buttons():
        for i, rect in enumerate(button_rects):
            screen.blit(characters[i]["image"], rect)
            subheading_rect = subheading_surfaces[i].get_rect(center=(rect.centerx, rect.bottom + 30))
            screen.blit(subheading_surfaces[i], subheading_rect)
        
        # Draw draggable circles
        pygame.draw.ellipse(screen, (0, 0, 255), p1_circle)  # Blue circle for P1
        p1_text = font.render("P1", True, (255, 255, 255))
        screen.blit(p1_text, (p1_circle.centerx - p1_text.get_width() // 2, p1_circle.centery - p1_text.get_height() // 2))
        
        pygame.draw.ellipse(screen, (255, 0, 0), p2_circle)  # Red circle for P2
        p2_text = font.render("P2", True, (255, 255, 255))
        screen.blit(p2_text, (p2_circle.centerx - p2_text.get_width() // 2, p2_circle.centery - p2_text.get_height() // 2))

    def start_game():
        if player_1_name and player_2_name:  # Check if both players have selected their characters
            global player1_type, player2_type
            player1_type = player_1_name
            player2_type = player_2_name
            if play_single:
                play_one_player()
                
            else:
                play_two_player()
                
            return
        else:
            error_text = font.render("Both players must select a character before starting the game!", True, (255, 0, 0))
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT - start_button_img.get_height() - 100))
            pygame.display.flip()
            pygame.time.delay(5000)
            error_text = font.render(" ", True, (0, 0, 0))
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT - start_button_img.get_height() - 100))

    def go_back():
        select_back()
        return

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if p1_circle.collidepoint(event.pos):
                    p1_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = p1_circle.x - mouse_x
                    offset_y = p1_circle.y - mouse_y
                elif p2_circle.collidepoint(event.pos):
                    p2_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = p2_circle.x - mouse_x
                    offset_y = p2_circle.y - mouse_y
            if event.type == pygame.MOUSEBUTTONUP:
                if p1_dragging:
                    p1_dragging = False
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            selected_player_1 = i
                            player_1_name = characters[i]["name"]
                            p1_circle.center = (rect.centerx - 60, rect.centery)  
                elif p2_dragging:
                    p2_dragging = False
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            selected_player_2 = i
                            player_2_name = characters[i]["name"]
                            p2_circle.center = (rect.centerx + 60, rect.centery)  
            if event.type == pygame.MOUSEMOTION:
                if p1_dragging:
                    mouse_x, mouse_y = event.pos
                    p1_circle.x = mouse_x + offset_x
                    p1_circle.y = mouse_y + offset_y
                elif p2_dragging:
                    mouse_x, mouse_y = event.pos
                    p2_circle.x = mouse_x + offset_x
                    p2_circle.y = mouse_y + offset_y

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        # Draw the buttons and player indicators
        draw_buttons()

        # Ensure circles don't overlap
        if p1_circle.colliderect(p2_circle):
            if p1_circle.centerx < p2_circle.centerx:
                p1_circle.right = p2_circle.left - 10
            else:
                p2_circle.right = p1_circle.left - 10

        # Draw the start button
        image_button(start_button_img, (WIDTH // 2 - start_button_img.get_width() // 2, HEIGHT - start_button_img.get_height() - 50), start_game)
        image_button(back_button_img, (25, HEIGHT - start_button_img.get_height() - 50), go_back)

        # Display selected character names
        if player_1_name:
            p1_char_text = font.render(f"P1: {player_1_name}", True, (0, 255, 0))
            screen.blit(p1_char_text, (50, 10))
        if player_2_name:
            p2_char_text = font.render(f"P2: {player_2_name}", True, (0, 255, 0))
            screen.blit(p2_char_text, (WIDTH - p2_char_text.get_width() - 50, 10))

        # Update the display
        pygame.display.flip()

import ground_class
import background_class
import platforms

#in game menu

def show_menu():
        menu_font = pygame.font.SysFont('Arial', 30)
        menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 128))  # Semi-transparent black background

        # Load images for buttons
        resume_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/resume_button.png'), (300, 150))
        brightness_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/brightness_button.png'), (300, 150))
        home_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/home_button.png'), (300, 150))
        key_bindings_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/key_bindings_button.png'), (300, 150))
        restart_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/restart_button.png'), (300, 150))

        def image_button(image, pos, action=None):
            rect = image.get_rect(topleft=pos)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if rect.collidepoint(mouse):
                if click[0] == 1 and action is not None:
                    action()

            menu_surface.blit(image, rect)

        # Display buttons
        image_button(resume_button_img, (WIDTH // 2 - resume_button_img.get_width() // 2, 50))
        image_button(key_bindings_button_img, (WIDTH // 2 - key_bindings_button_img.get_width() // 2, 212.5))
        image_button(brightness_button_img, (WIDTH // 2 - brightness_button_img.get_width() // 2, 375))
        image_button(restart_button_img, (WIDTH // 2 - restart_button_img.get_width() // 2, 537.5 ))
        image_button(home_button_img, (WIDTH // 2 - home_button_img.get_width() // 2, 700))


        displaysurface.blit(menu_surface, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button_img.get_rect(topleft=(WIDTH // 2 - resume_button_img.get_width() // 2, 50 )).collidepoint(event.pos):
                        return
                    elif key_bindings_button_img.get_rect(topleft=(WIDTH // 2 - key_bindings_button_img.get_width() // 2, 212.5)).collidepoint(event.pos):
                        print("Key Bindings button clicked")  # Add key bindings functionality here
                    elif brightness_button_img.get_rect(topleft=(WIDTH // 2 - brightness_button_img.get_width() // 2, 375)).collidepoint(event.pos):
                        print("Brightness button clicked")  # Add brightness control functionality here
                    elif restart_button_img.get_rect(topleft=(WIDTH // 2 - restart_button_img.get_width() // 2, 537.5)).collidepoint(event.pos):
                        if play_double:
                            play_two_player()  # Ensure play_two_player() is defined
                        else:
                            play_one_player()
                        return  
                    elif home_button_img.get_rect(topleft=(WIDTH // 2 - home_button_img.get_width() // 2, 700)).collidepoint(event.pos):
                        menu_screen()  # Ensure menu_screen() is defined
                        return


def play_two_player():

    #bring_window_to_front()

    # Delayed imports and initializations

    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    #bring_window_to_front()

    # Delayed imports and initializations
    
    background = background_class.Background(displaysurface, background_name)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    

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
                    show_menu()

                #Player 1 controls
                if event.key == pygame.K_UP:
                    player_1.jump()

                if event.key == pygame.K_DOWN:
                    player_1.fall()

                if event.key == pygame.K_RSHIFT:
                    player_1.attack()
                            
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

# Method to call when player chooses to play a single player game against a Bot
def play_one_player():

    #bring_window_to_front()

    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    #bring_window_to_front()

    # Delayed imports and initializations
    
    background = background_class.Background(displaysurface, background_name)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    

    platform_width = 100 * SIZE_MULTIPLIER * 1.3
    platform_height = 30 * SIZE_MULTIPLIER
    platform1 = platforms.Platform(WIDTH * 0.1, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform2 = platforms.Platform(WIDTH * 0.40, HEIGHT / 2.8, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform3 = platforms.Platform(WIDTH * 0.70, HEIGHT / 1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)

    platform_group = pygame.sprite.Group()
    platform_group.add(platform1, platform2, platform3)

    player = player_class.Player(vec, displaysurface, player1_type, ground_group, platform_group)
    enemy = enemy_class.Enemy(vec, displaysurface, player2_type, ground_group, platform_group, player)

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
                    show_menu()

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
        global play_single, play_double
        ratio = player.health / 100
        
        if(player.health <= -7):
            if player.number == 2:
                if play_single:
                    show_message("player wins")
                else:
                    show_message("player 1 wins")
                select_back()
                
            else:
                if play_single:
                    show_message("enemy wins")
                else:
                    show_message("player 2 wins")
                select_back()
                
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

def show_message(message):
        print("here")
        font = pygame.font.SysFont(None, 36)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, 100))
        displaysurface.blit(text, text_rect)
        pygame.display.update(text_rect)
        pygame.time.wait(2000)
        

def main():
    menu_screen()


if __name__ == "__main__":
    main()
    


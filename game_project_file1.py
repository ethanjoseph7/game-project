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
import imageio
from PIL import Image as PilImage

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


player1_type = "fighter"  # input("player one, fighter or samurai? ")
player2_type = "fighter"  # input("player two, fighter or samurai? ")

single_play = False
double_play = False


# method to load the game to the front of the window on start 
def bring_window_to_front():
    wm_info = pygame.display.get_wm_info()
    if 'window' in wm_info:
        hwnd = wm_info['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        print("Warning: 'window' key not found in wm_info. Unable to bring window to front.")
        

# This method loads a GIF file, converts each frame to a pygame Surface, scales each frame to the screen size, 
# and returns a list of pygame Surfaces representing each frame of the GIF.
def load_gif_frames(filename):
    gif = imageio.mimread(filename)
    frames = []
    for frame in gif:
        pil_image = PilImage.fromarray(frame)
        pil_image = pil_image.convert("RGBA")
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        frame_surface = pygame.image.fromstring(data, size, mode)
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        frames.append(frame_surface)
    return frames

# Method for the menu screen at the start of the game
def menu_screen():
    vec = pygame.math.Vector2
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Menu")

    # Load GIF frames
    gif_frames = load_gif_frames('assets/menu.gif')
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    # Load button images
    start_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/play_button.png'), (295, 150))
    exit_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/exit_button.png'), (275, 150))
    setting_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/setting_button.png'), (150, 150))

    # Method to create buttons with images
    def image_button(image, pos, action=None):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            if click[0] == 1 and action is not None:
                action()

        displaysurface.blit(image, rect)

    def start_game():
        # Replace this with your actual game starting function
        select_play_type()

    def quit_game():
        pygame.quit()
        sys.exit()
    def setting_menu():
        pass

    while True:
        FramePerSec.tick(FPS)

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Display buttons
        image_button(start_button_img, (WIDTH // 2 - start_button_img.get_width() // 2, HEIGHT // 2 - 50), start_game)
        image_button(exit_button_img, (WIDTH // 2 - exit_button_img.get_width() // 2, HEIGHT // 2 + 50), quit_game)
        image_button(setting_button_img, (25, 25), setting_menu)

        pygame.display.update()
        
def select_play_type():
    global single_play, double_play
    vec = pygame.math.Vector2
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Menu")

    # Load GIF frames
    gif_frames = load_gif_frames('assets/menu.gif')
    gif_frame_count = len(gif_frames)
    gif_frame_index = 0

    # Load button images
    single_player_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/single_play.png'), (400, 275))
    double_player_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/double_play.png'), (400, 275))
    back_button_img = pygame.transform.scale(pygame.image.load('assets/buttons/back_button.png'), (150, 150))

    # Method to create buttons with images
    def image_button(image, pos, action=None):
        rect = image.get_rect(topleft=pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect.collidepoint(mouse):
            if click[0] == 1 and action is not None:
                action()

        displaysurface.blit(image, rect)

    def single_play():
        global single_play
        single_play = True
        select_char()
        
    def double_play():
        global double_play
        double_play = True
        select_char()
    
    def go_back():
        menu_screen()
        


    while True:
        FramePerSec.tick(FPS)

        # Display GIF frame
        displaysurface.blit(gif_frames[gif_frame_index], (0, 0))
        gif_frame_index = (gif_frame_index + 1) % gif_frame_count

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Display buttons
        image_button(single_player_button_img, (WIDTH // 3 - single_player_button_img.get_width(), HEIGHT // 2.5), single_play)
        image_button(double_player_button_img, (WIDTH // 2 + double_player_button_img.get_width() - double_player_button_img.get_width() //3, HEIGHT // 2.5 ), double_play)
        image_button(back_button_img, (25, 25), go_back)

        pygame.display.update()
        

def select_back():
    # This method allows the players to select their characters for the game by dragging circles onto character buttons.
    # The selected characters are then used in the two-player game.
    
    global player1_type, player2_type
    
    vec = pygame.math.Vector2
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = displaysurface
    pygame.display.set_caption("Character Selection")
    
    

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

    # Start button
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

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
        if player_1_name:
            global player1_type
            player1_type = player_1_name
        if player_2_name:
            global player2_type
            player2_type = player_2_name
        play_two_player()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                elif start_button_rect.collidepoint(event.pos):
                    start_game()
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

        # Clear the screen
        screen.fill((0, 0, 0))  # Black background

        # Draw the buttons and player indicators
        draw_buttons()

        # Ensure circles don't overlap
        if p1_circle.colliderect(p2_circle):
            if p1_circle.centerx < p2_circle.centerx:
                p1_circle.right = p2_circle.left - 10
            else:
                p2_circle.right = p1_circle.left - 10

        # Draw the start button
        pygame.draw.rect(screen, (255, 0, 0), start_button_rect)  # Red start button
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (start_button_rect.centerx - start_text.get_width() // 2, start_button_rect.centery - start_text.get_height() // 2))

        # Display selected character names
        if player_1_name:
            p1_char_text = font.render(f"P1: {player_1_name}", True, (0, 255, 0))
            screen.blit(p1_char_text, (50, 10))
        if player_2_name:
            p2_char_text = font.render(f"P2: {player_2_name}", True, (0, 255, 0))
            screen.blit(p2_char_text, (WIDTH - p2_char_text.get_width() - 50, 10))

        # Update the display
        pygame.display.flip()



def select_char():
    # This method allows the players to select their characters for the game by dragging circles onto character buttons.
    # The selected characters are then used in the two-player game.
    
    global player1_type, player2_type
    
    vec = pygame.math.Vector2
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = displaysurface
    pygame.display.set_caption("Character Selection")

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
            play_two_player()
        else:
            print("Both players must select a character before starting the game!")

    def go_back():
        menu_screen()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

        # Clear the screen
        screen.fill((0, 0, 0))  # Black background

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


   




# Method to call when player chooses to play a 2 player game against friend
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
    #player1_type = "Plent"  # input("player one, fighter or samurai? ")
    #player2_type = "Fire_Spirit"  # input("player two, fighter or samurai? ")
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


# Method to call when player chooses to play a single player game against a Bot
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
    #player1_type = "Fighter"  # input("player one, fighter or samurai? ")
   # player2_type = "Samurai"  # input("player two, fighter or samurai? ")
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
    menu_screen()

if __name__ == "__main__":
    main()
    


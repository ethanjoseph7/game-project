import pygame

from ntpath import join  # Import the 'join' function from the 'ntpath' module
import pygame  # Import the 'pygame' library
from pygame.locals import *  # Import constants from 'pygame.locals' module
import sys  # Import the 'sys' module
import random  # Import the 'random' module
from tkinter import filedialog  # Import the 'filedialog' module from 'tkinter'
from tkinter import *  # Import everything from 'tkinter'
import spritesheet  # Import the 'spritesheet' module
import fighter_sprite  # Import the 'fighter_sprite' module
import platforms

pygame.init()  # Initialize the pygame library
vec = pygame.math.Vector2  # Create a 2-dimensional vector object

# Set up some constants
HEIGHT = 350
WIDTH = 700
ACC = 2
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0, 0, 0)

FramePerSec = pygame.time.Clock()

# Create the game window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Load the images for the player's idle, running, and attacking animations
idle_right_images = [
    pygame.image.load(f"character_sprites/Fighter/idling_right_images/idle_right_{i}.png").convert_alpha()
    for i in range(1, 7)
]

idle_left_images = [
    pygame.image.load(f"character_sprites/Fighter/idling_left_images/idle_left_{i}.png").convert_alpha()
    for i in range(1, 7)
]

running_right_images = [
    pygame.image.load(f"character_sprites/Fighter/run_right_images/Run_right_{i}.png").convert_alpha()
    for i in range(1, 9)
]

running_left_images = [
    pygame.image.load(f"character_sprites/Fighter/run_left_images/Run_left_{i}.png").convert_alpha()
    for i in range(1, 9)
]

attack_1_right_images = [
    pygame.image.load(f"character_sprites/Fighter/attack_1_right_images/Attack_1_right_{i}.png").convert_alpha()
    for i in range(1, 8)
]

attack_1_left_images = [
    pygame.image.load(f"character_sprites/Fighter/attack_1_left_images/Attack_1_left_{i}.png").convert_alpha()
    for i in range(1, 5)
]

# Define the Background class
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bg_url = "backgrounds/nightsky_2.png"
        self.bgimage = pygame.image.load(bg_url)
        self.bgY = 0
        self.bgX = 0
        self.pos = pygame.Vector2(0, 0)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

# Define the Ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ground_url = "platforms/water_1.png"
        self.image = pygame.image.load(ground_url)
        self.rect = self.image.get_rect(center=(350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

# Define the Player class

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Player class.

        This method sets up the player's attributes and initializes variables.
        """
        super().__init__()
        BG = (0, 0, 0)
        self.image = pygame.Surface((63, 81)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(idle_right_images[0], self.rect)
        self.image.set_colorkey(BG)

        # Initialize player attributes
        self.jumping = False
        self.running = False
        self.last_update = pygame.time.get_ticks()
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"
        self.jumping = False
        self.attacking = False
        self.attack_frame = 0
        self.idle_frame = 0
        self.jumping = False
        self.running = False
        self.move_frame = 0

    def idle(self, current_time):
        """
        Perform the idle animation.

        This method updates the player's image based on the current idle frame.
        """
        if self.idle_frame > len(idle_right_images):
            self.idle_frame = 0
        if self.idle_frame > len(idle_left_images):
            self.idle_frame = 0
        if self.direction == "RIGHT":
            self.image = idle_right_images[int(self.idle_frame)]
        else:
            self.image = idle_left_images[int(self.idle_frame)]
        self.idle_frame += 0.1

    def move(self):
        """
        Move the player.

        This method handles the player's movement logic based on user input.
        """
        self.acc = vec(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()

        # Player acceleration
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # Velocity calculations
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Player warping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
 
    def gravity_check(self):
        """
        Check for gravity and collision with ground and platforms.

        This method checks if the player is affected by gravity and handles collision with the ground and platforms.
    
        """

        hits_ground = pygame.sprite.spritecollide(player, ground_group, False)
        hits_platform = pygame.sprite.spritecollide(player, platform_group, False)
        
        if self.vel.y > 0:
            if hits_ground:
                lowest = hits_ground[0]
                if self.pos.y < lowest.rect.bottom + self.vel.y:
                    self.pos.y = lowest.rect.top + 1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = 2
            elif hits_platform:
                lowest = hits_platform[0]
                if self.pos.y <= lowest.rect.bottom + self.vel.y:
                    self.pos.y = lowest.rect.top + 1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = 2
            

    def jump(self):
        """
        Make the player jump.

        This method handles the player's jumping logic and animation.
        """
        self.rect.x += 1 
        self.d_jump = False
        # Check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        hits_platform = pygame.sprite.spritecollide(self, platform_group, False)
        self.rect.x -= 1
        
        # Double jump enabled
        if (hits or hits_platform) and not self.jumping:
            self.vel.y = -12
            self.jumping = True
            self.double_jump -= 1
        # Condition to double jump
        elif not hits and not hits_platform and self.double_jump > 0:
            self.jumping = True
            self.vel.y = -12
            self.double_jump -= 1
   
    def update(self):
        """
        Update the player's animation.

        This method updates the player's image based on the current animation frame.
        """
        # Return to base frame at the end of animation
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        # When idling

        # Change image when jumping
        if self.jumping == True:
            if self.direction == "RIGHT":
                self.image = running_right_images[1]
            else:
                self.image = running_left_images[1] 

        # Frame change when moving
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = running_right_images[int(self.move_frame)]
                self.direction = "RIGHT"
            else:
                self.image = running_left_images[int(self.move_frame)] 
                self.direction = "LEFT"
            self.move_frame += 0.1

        # Return to base frame if still
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = running_right_images[int(self.move_frame)]
            else:
                self.image = running_left_images[int(self.move_frame)] 

    def attack(self):
        """
        Perform the attack animation.

        This method updates the player's image based on the current attack frame.
        """
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame >= len(attack_1_left_images):
            self.attack_frame = 0
        
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_1_right_images[int(self.attack_frame)]
        elif self.direction == "LEFT":
            self.image = attack_1_left_images[int(self.attack_frame)]

        # Update the current attack frame
        self.attack_frame += 0.5

    def correction(self):
        """
        Correct an error with character position on left attack frames.

        This method corrects the player's position when the attack frame is at a specific value.
        """
        # Function is used to correct an error with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == -10:
            self.pos.x += 20
 


                        
background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
platform1 = platforms.Platform(150, 250, 100, 30)
platform2 = platforms.Platform(300, 150, 100, 30)
platform3 = platforms.Platform(450, 200, 100, 30)
platform_group = pygame.sprite.Group()
platform_group.add(platform1, platform2, platform3)


while True:
    FPS_CLOCK.tick(FPS)
    current_time = pygame.time.get_ticks()
    player.idle(current_time)
    
    FPS_CLOCK.tick(FPS)

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
            # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_RSHIFT:
                if player.attacking == FALSE:
                    player.attack()
                    player.attack()
                    player.attacking == TRUE

    player.gravity_check()
    
    # Adding some platform blocks with block size (width=50, height=20)

    
    # Render Functions ------
    background.render() 
    background = Background()
    ground = Ground()
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    ground.render()
   


    
    platform_group.draw(displaysurface)
    

    player.update()
    if player.attacking == TRUE:
        player.attack()
    player.move()
    displaysurface.blit(player.image, player.rect)
    player.move()
    player.update()
    pygame.display.update()

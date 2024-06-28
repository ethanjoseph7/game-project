import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import spritesheet
import fighter_sprite

 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
#print(pygame.get_init())
HEIGHT = 350
WIDTH = 700
ACC = 2
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0,0,0)
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

idle_right_images = []
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_1.png").convert_alpha())
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_2.png").convert_alpha())
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_3.png").convert_alpha())
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_4.png").convert_alpha())
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_5.png").convert_alpha())
idle_right_images.append(pygame.image.load("character_sprites/Fighter/idling_right_images/idle_right_6.png").convert_alpha())

idle_left_images = []
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_1.png").convert_alpha())
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_2.png").convert_alpha())
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_3.png").convert_alpha())
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_4.png").convert_alpha())
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_5.png").convert_alpha())
idle_left_images.append(pygame.image.load("character_sprites/Fighter/idling_left_images/idle_left_6.png").convert_alpha())

running_right_images = []
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_1.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_2.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_3.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_4.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_5.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_6.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_7.png").convert_alpha())
running_right_images.append(pygame.image.load("character_sprites/Fighter/run_right_images/Run_right_8.png").convert_alpha())

running_left_images = []
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_1.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_2.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_3.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_4.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_5.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_6.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_7.png").convert_alpha())
running_left_images.append(pygame.image.load("character_sprites/Fighter/run_left_images/Run_left_8.png").convert_alpha())

attack_1_right_images = []
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_1.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_2.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_3.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_4.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_5.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_6.png").convert_alpha())
attack_1_right_images.append(pygame.image.load("character_sprites/Fighter/attack_1_right_images/Attack_1_right_7.png").convert_alpha())



attack_1_left_images = []
attack_1_left_images.append(pygame.image.load("character_sprites/Fighter/attack_1_left_images/Attack_1_left_1.png").convert_alpha())
attack_1_left_images.append(pygame.image.load("character_sprites/Fighter/attack_1_left_images/Attack_1_left_2.png").convert_alpha())
attack_1_left_images.append(pygame.image.load("character_sprites/Fighter/attack_1_left_images/Attack_1_left_3.png").convert_alpha())
attack_1_left_images.append(pygame.image.load("character_sprites/Fighter/attack_1_left_images/Attack_1_left_4.png").convert_alpha())




class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            bg_url = "backgrounds/nightsky_2.png"
            self.bgimage = pygame.image.load(bg_url)        
            self.bgY = 0
            self.bgX = 0
            
            if self.pos.x > WIDTH:
             self.pos.x = 0
            if self.pos.x < 0:
             self.pos.x = WIDTH
 
      def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ground_url = "platforms/water_1.png"
        self.image = pygame.image.load(ground_url)
        self.rect = self.image.get_rect(center = (350, 350))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))  
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()


class Player(pygame.sprite.Sprite):
    

    def __init__(self):
        super().__init__()
        BG = (0,0,0)
        self.image = pygame.Surface((63,81)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(idle_right_images[0], self.rect)
        self.image.set_colorkey(BG)
        
        

        self.jumping = False
        self.running = False
        self.last_update = pygame.time.get_ticks()
 
        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"
        self.jumping = False
        
        # Combat
        self.attacking = False
        self.attack_frame = 0

        # Idle
        self.idle_frame = 0
        
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0



    def idle(self, current_time):
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
        self.acc = vec(0,0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        #returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        #player acceleration
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #velocity calculations
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #player warping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
 
    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False

    def jump(self):
        self.rect.x +=1 
        #check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
            

    def update(self):
        # return to base frame at the end of animation
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        # when idling

        # change image when jumping
        if self.jumping == True:
            if self.direction == "RIGHT":
                self.image = running_right_images[1]
            else:
                self.image = running_left_images[1] 

          # frame change when moving
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = running_right_images[int(self.move_frame)]
                self.direction = "RIGHT"
            else:
                self.image = running_left_images[int(self.move_frame)] 
                self.direction = "LEFT"
            self.move_frame += 0.1

        # return to base frame if still
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = running_right_images[int(self.move_frame)]
            else:
                self.image = running_left_images[int(self.move_frame)] 

    
    def attack(self):
        # if attack frame has reached end of sequence, return to base frame
        if self.attack_frame >= len(attack_1_left_images):
            self.attack_frame = 0
        
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_1_right_images[int(self.attack_frame)]
        elif self.direction == "LEFT":
            self.image = attack_1_left_images[int(self.attack_frame)]


        # update the current attack frame
        self.attack_frame += 0.5

    def correction(self):
        # function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -=20
        if self.attack_frame == -10:
            self.pos.x += 20



                        
background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()


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
    
    # Render Functions ------
    background.render() 
    ground.render()

    player.update()
    if player.attacking == TRUE:
        player.attack()
    player.move()
    displaysurface.blit(player.image, player.rect)
    player.move()
    player.update()
    pygame.display.update() 
        
    




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
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0,0,0)
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

idle_right_images = []
idle_left_images = []
for i in range(6):
    load_url = "character_sprites/Fighter/idling_right_images/idle_right_" + str(i+1)+ ".png"
    idle_right_images.append(pygame.image.load(load_url).convert_alpha())

    load_url = "character_sprites/Fighter/idling_left_images/idle_left_" + str(i+1) + ".png"
    idle_left_images.append(pygame.image.load(load_url).convert_alpha())
    

running_right_images = []
running_left_images = []
for i in range (8):
    load_url = "character_sprites/Fighter/run_right_images/Run_right_" + str(i+1) + ".png"
    running_right_images.append(pygame.image.load(load_url).convert_alpha())

    load_url = "character_sprites/Fighter/run_left_images/Run_left_" + str(i+1) + ".png"
    running_left_images.append(pygame.image.load(load_url).convert_alpha())

attack_1_right_images = []
attack_1_left_images = []
for i in range (10):
    load_url = "character_sprites/Fighter/attack_1_right_images/Attack_1_right_" + str(i+1) + ".png"
    attack_1_right_images.append(pygame.image.load(load_url).convert_alpha())

    load_url = "character_sprites/Fighter/attack_1_left_images/Attack_1_left_" + str(i+1) + ".png"
    attack_1_left_images.append(pygame.image.load(load_url).convert_alpha())
    

jump_right_images = []
jump_left_images = []
for i in range(1):
    load_url = "character_sprites/Fighter/jump_right_images/Jump_right_" + str(i+1) + ".png"
    jump_right_images.append(pygame.image.load(load_url).convert_alpha())

    load_url = "character_sprites/Fighter/jump_left_images/Jump_left_" + str(i+1) + ".png"
    jump_left_images.append(pygame.image.load(load_url).convert_alpha())

samurai_idle_right_images = []
samurai_idle_left_images = []
for i in range(6):
    load_url = "character_sprites/Samurai/idle_right_images/Idle_right_" + str(i+1) + ".png"
    samurai_idle_right_images.append(pygame.image.load(load_url).convert_alpha())

    load_url = "character_sprites/Samurai/idle_left_images/Idle_left_" + str(i+1) + ".png"
    samurai_idle_left_images.append(pygame.image.load(load_url).convert_alpha())




class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            bg_url = "backgrounds/nightsky_2.png"
            self.bgimage = pygame.image.load(bg_url)        
            self.bgY = 0
            self.bgX = 0
 
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
        BG = (0,0,0)
        self.image = pygame.Surface((63,81)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(samurai_idle_left_images[0], self.rect)
        self.image.set_colorkey(BG)

        self.vx = 0
        self.pos = vec((440, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "LEFT"
        self.jumping = False
        self.running = False
        self.move_frame = 0

        # idling
        self.idle_frame = 0

    def move(self):
        self.acc = vec(0,0.5)
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()
        
        # Accelerates the player in the direction of the key press
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC 

        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos  # Update rect with new pos   

    def idle(self):
        if self.idle_frame > len(samurai_idle_right_images):
            self.idle_frame = 0
        if self.idle_frame > len(samurai_idle_left_images):
            self.idle_frame = 0
        if self.direction == "RIGHT":
                self.image = samurai_idle_right_images[int(self.idle_frame)]
        else:
                self.image = samurai_idle_left_images[int(self.idle_frame)] 
        self.idle_frame += 0.1

    def update(self):
           # frame change when moving
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                #self.image = running_right_images[int(self.move_frame)]
                self.direction = "RIGHT"
            else:
                #self.image = running_left_images[int(self.move_frame)] 
                self.direction = "LEFT"
            self.move_frame += 0.1

        # return to base frame if still
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                #self.image = running_right_images[int(self.move_frame)]
                pass
            else:
                #self.image = running_left_images[int(self.move_frame)]
                pass


    def attack(self):
        pass

    def jump(self):
        self.rect.x += 1
    
        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        
        self.rect.x -= 1
    
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(enemy, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False
 

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
        self.cooldown = False
        self.attack_frame = 0

        # Idle
        self.idle_frame = 0
        
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0



    def idle(self):
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
                self.image = jump_right_images[0]
            else:
                self.image = jump_left_images[0] 

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
        self.attacking = True
        if self.attack_frame >= len(attack_1_right_images):
            self.attack_frame = 0
            self.attacking = False

        
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_1_right_images[int(self.attack_frame)]
        elif self.direction == "LEFT":
            #self.correction()
            self.image = attack_1_left_images[int(self.attack_frame)]


        # update the current attack frame
        self.attack_frame += 0.5
        

    def correction(self):
        # function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -=20
        if self.attack_frame == 4:
            self.pos.x += 20



background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
enemy = Enemy()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)



while True:
    FPS_CLOCK.tick(FPS)
    player.idle()
    enemy.idle()
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
            # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_RSHIFT:
                if player.attacking == FALSE:
                    player.attack()
                    hits = pygame.sprite.spritecollide(player, enemy_group, False)
                    if hits:
                        print("hit")
            
            if event.key == pygame.K_w:
                enemy.jump()


    player.gravity_check()
    enemy.gravity_check()
    # Render Functions ------
    background.render() 
    ground.render()
    enemy.update()
    player.update()
    if player.attacking:
        player.attack()
    player.move()
    enemy.move()
    displaysurface.blit(player.image, player.rect)
    displaysurface.blit(enemy.image, enemy.rect)
    enemy.move()
    player.move()
    player.update()
    enemy.update()
    pygame.display.update() 
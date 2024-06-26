import pygame
from pygame.locals import *
import spritesheet
import sys


ACC = 0.3
FRIC = -0.10
HEIGHT = 350
WIDTH = 700

class Player(pygame.sprite.Sprite):
    
    def __init__(self, vec, screen, type):
        super().__init__()
        # Sprite
        self.type = type
        self.idle_right_images = []
        self.idle_left_images = []

        self.running_right_images = []
        self.running_left_images = []

        self.attack_1_right_images = []
        self.attack_1_left_images = []

        self.attack_2_right_images = []
        self.attack_2_left_images = []

        self.jump_right_images = []
        self.jump_left_images = []
        self.load_sprites(type)


        BG = (0,0,0)
        self.image = pygame.Surface((63,81)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self.idle_right_images[0], self.rect)
        self.image.set_colorkey(BG)
        self.displaysurface = screen
        self.vec = vec


        self.jumping = False
        self.running = False
        self.last_update = pygame.time.get_ticks()
 
        # Position and direction
        self.vx = 0
        self.pos = vec((500, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "LEFT"
        self.jumping = False
        self.double_jump = False
        
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

        


    def load_sprites(self, type):
        sprites = spritesheet.load_sprites(type)

        self.idle_right_images = sprites[0]
        self.idle_left_images = sprites[1]
        

        self.running_right_images = sprites[2]
        self.running_left_images = sprites[3]

        self.attack_1_right_images = sprites[4]
        self.attack_1_left_images = sprites[5]
        
        self.attack_2_right_images = sprites[6]
        self.attack_2_left_images = sprites[7]

        self.jump_right_images = sprites[8]
        self.jump_left_images = sprites[9]



    def idle(self):
        if self.idle_frame > len(self.idle_right_images):
            self.idle_frame = 0
        if self.idle_frame > len(self.idle_right_images):
            self.idle_frame = 0
        if self.direction == "RIGHT":
                self.image = self.idle_right_images[int(self.idle_frame)]
        else:
                self.image = self.idle_left_images[int(self.idle_frame)] 
        self.idle_frame += 0.1

    def move(self):
        self.acc = self.vec(0,0.5)

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
    
    def gravity_check(self, player, ground_group):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False

    def jump(self, ground_group):
        self.rect.x +=1 
        #check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

        elif self.jumping and not self.double_jump:
            self.double_jump = True
            self.vel.y = -8

            

    def update(self):
        # return to base frame at the end of animation
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        # when idling

        # change image when jumping
        if self.jumping == True:
            if self.direction == "RIGHT":
                self.image = self.jump_right_images[0]
            else:
                self.image = self.jump_left_images[0] 

          # frame change when moving
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = self.running_right_images[int(self.move_frame)]
                self.direction = "RIGHT"
            else:
                self.image = self.running_left_images[int(self.move_frame)] 
                self.direction = "LEFT"
            self.move_frame += 0.1

        # return to base frame if still
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.running_right_images[int(self.move_frame)]
            else:
                self.image = self.running_left_images[int(self.move_frame)] 
    
    def attack(self):
        # if attack frame has reached end of sequence, return to base frame
        self.attacking = True
        if self.attack_frame >= len(self.attack_1_right_images):
            self.attack_frame = 0
            self.attacking = False

        
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = self.attack_1_right_images[int(self.attack_frame)]
        elif self.direction == "LEFT":
            #self.correction()
            self.image = self.attack_1_left_images[int(self.attack_frame)]


        # update the current attack frame
        self.attack_frame += 0.5
        

    def correction(self):
        # function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -=20
        if self.attack_frame == 4:
            self.pos.x += 20

class Player_2(Player):
    def __init__(self, vec, screen, type):
        super().__init__(vec, screen, type)
        self.pos = vec((200, 240))
        self.direction = "RIGHT"
    

    def gravity_check(self, player_2, ground_group):
        hits = pygame.sprite.spritecollide(player_2, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False

    def move(self):
        self.acc = self.vec(0,0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        #returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        #player acceleration
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
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

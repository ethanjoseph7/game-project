import pygame
from pygame.locals import *
import spritesheet


ACC = 0.5
FRIC = -0.10
HEIGHT = 900
WIDTH = 1700
SIZE_MULTIPLIER = 1.9

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

        self.attack_3_right_images = []
        self.attack_3_left_images = []

        self.jump_right_images = []
        self.jump_left_images = []

        self.load_sprites(type)

        self.all_attack_images_right = []
        self.all_attack_images_right.append(self.attack_1_right_images)
        self.all_attack_images_right.append(self.attack_2_right_images)
        self.all_attack_images_right.append(self.attack_3_right_images)


        self.all_attack_images_left = []
        self.all_attack_images_left.append(self.attack_1_left_images)
        self.all_attack_images_left.append(self.attack_2_left_images)
        self.all_attack_images_left.append(self.attack_3_left_images)

        BG = (0,0,0)
        self.image = pygame.Surface((63*SIZE_MULTIPLIER,81*SIZE_MULTIPLIER)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self.idle_right_images[0], self.rect)
        self.image.set_colorkey(BG)
        self.displaysurface = screen
        self.vec = vec
        self.number = 1


        self.jumping = False
        self.running = False
        self.falling = False
        self.last_update = pygame.time.get_ticks()
 
        # Position and direction
        self.vx = 0
        self.pos = vec((1400, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "LEFT"
        self.jumping = False
        self.double_jump = False
        
        # Combat
        self.attacking = False
        self.cooldown = False
        self.attack_frame = 0
        self.attack_sheet = 0

        # Idle
        self.idle_frame = 0
        
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0

        # Health
        self.health = 100

        


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

        self.attack_3_right_images = sprites[8]
        self.attack_3_left_images = sprites[9]

        self.jump_right_images = sprites[10]
        self.jump_left_images = sprites[11]



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
        self.acc = self.vec(0,0.3)

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
        self.pos += self.vel + 0.9 * self.acc

        #player warping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
    
    def gravity_check(self, player, ground_group, platform_group):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        hits_platform = pygame.sprite.spritecollide(player, platform_group, False)
        if self.vel.y < 0:
            self.falling = False
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False
                    player.falling = False
            elif hits_platform and not self.falling:
                lowest = hits_platform[0]
                if self.pos.y <= lowest.rect.bottom + self.vel.y:
                    self.pos.y = lowest.rect.top + 1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False
                    player.falling = False

    def jump(self, ground_group, platform_group):
        self.rect.x +=1 
        self.falling = False
        self.attacking = False
        #check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        hits_platform = pygame.sprite.spritecollide(self, platform_group, False)

        self.rect.x -= 1

        if (hits or hits_platform) and not self.jumping:
            self.jumping = True
            self.vel.y = -16

        elif self.jumping and not self.double_jump:
            self.double_jump = True
            self.vel.y = -12
            
    def fall(self, platform_group):
        hits_platform = pygame.sprite.spritecollide(self, platform_group, False)
        if hits_platform and not self.falling:
            self.falling = True
            self.vel.y = 3
            self.jumping = False
            

    def update(self):
        # return to base frame at the end of animation
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        # change image when jumping or falling
        if self.jumping == True or self.falling:
            if self.direction == "RIGHT":
                self.image = self.jump_right_images[0]
            else:
                self.image = self.jump_left_images[0] 

          # frame change when moving
        if self.jumping == False and self.running == True and not self.attacking:
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
        if self.attack_frame >= len(self.all_attack_images_right[self.attack_sheet]):
            self.attack_frame = 0
            self.attacking = False
            self.attack_sheet += 1
        if self.attack_sheet > 2:
            self.attack_sheet = 0
            self.attack_frame = 0
        if self.jumping and self.attack_sheet != 2:
            self.attack_sheet = 2
            self.attack_frame = 0

        current_attack_list_right = self.all_attack_images_right[self.attack_sheet]
        current_attack_list_left = self.all_attack_images_left[self.attack_sheet]
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = current_attack_list_right[int(self.attack_frame)]
        elif self.direction == "LEFT":
            #self.correction()
            self.image = current_attack_list_left[int(self.attack_frame)]


        # update the current attack frame
        self.attack_frame += 0.4
        
        

    def correction(self):
        # function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -=20
        if self.attack_frame == 4:
            self.pos.x += 20
    
    def facing(self,player2):
        if self.direction == "RIGHT" and player2.pos.x > self.pos.x:
            return True
        elif self.direction == "LEFT" and player2.pos.x < self.pos.x:
            return True
        return False
    

    def __str__(self):
        return f"{self.type}"    


class Player_2(Player):
    def __init__(self, vec, screen, type):
        super().__init__(vec, screen, type)
        self.load_sprites(type)
        self.pos = vec((300, 240))
        self.direction = "RIGHT"
        self.type = type
        self.number = 2
        self.load_sprites(self.type)

    def move(self):
        self.acc = self.vec(0,0.3)

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
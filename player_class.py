import pygame
from pygame.locals import *
import sprites_class


ACC = 0.5
FRIC = -0.10
HEIGHT = 900
WIDTH = 1700
SIZE_MULTIPLIER = 1.9

class Player(pygame.sprite.Sprite):
    
    def __init__(self, vec, screen, type, ground_group, platform_group):
        super().__init__()
        # Sprite
        self.type = type
        self.idle_images = []

        self.running_images = []

        self.attack_1_images = []

        self.attack_2_images = []

        self.attack_3_images = []

        self.jump_images = []

        self.load_sprites(type)

        self.all_attack_images = []
        self.all_attack_images.append(self.attack_1_images)
        self.all_attack_images.append(self.attack_2_images)
        self.all_attack_images.append(self.attack_3_images)


        self.image = pygame.Surface((64*SIZE_MULTIPLIER,84*SIZE_MULTIPLIER)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self.idle_images[0], self.rect)
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
        self.raw_damage = 7
        self.damage_multiplier = 1
        self.damage = 0
        self.last_frame = -1
        self.last_attack = pygame.time.get_ticks()
        self.attack_spaced = False


        # Idle
        self.idle_frame = 0
        
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.jump_frame = 0

        # Health
        self.health = 100

        # Platform and Ground
        self.platform_group = platform_group
        self.ground_group = ground_group

        


    def load_sprites(self, type):
        curr_sprites = sprites_class.sprite_class(type)
        sprites = curr_sprites.load_sprites()

        self.idle_images = sprites[0]
        
        self.running_images = sprites[1]

        self.attack_1_images = sprites[2]
        
        self.attack_2_images = sprites[3]

        self.attack_3_images = sprites[4]

        self.jump_images = sprites[5]

    def idle(self): 
        if not self.running:
            if self.idle_frame >= len(self.idle_images):
                self.idle_frame = 0
            if self.direction == "RIGHT":
                    self.image = self.idle_images[int(self.idle_frame)]
            else:
                    temp = self.idle_images[int(self.idle_frame)]
                    self.image = self.image = pygame.transform.flip(temp, True, False)
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
        if self.attacking:
            self.acc.x = 0
        elif pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        elif pressed_keys[K_RIGHT]:
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
    
    def gravity_check(self):
        hits = pygame.sprite.spritecollide(self, self.ground_group, False)
        hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
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
                    self.falling = False
            elif hits_platform and not self.falling:
                lowest = hits_platform[0]
                if self.pos.y <= lowest.rect.bottom + self.vel.y:
                    self.pos.y = lowest.rect.top + 1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False
                    self.falling = False

    def jump(self):
        self.rect.x +=1 
        self.falling = False
        self.attacking = False
        #check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, self.ground_group, False)
        hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)

        self.rect.x -= 1

        if (hits or hits_platform) and not self.jumping:
            self.jumping = True
            self.vel.y = -14

        elif self.jumping and not self.double_jump:
            self.double_jump = True
            self.vel.y = -12
            
    def fall(self):
        hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
        if hits_platform and not self.falling and not self.jumping:
            self.falling = True
            self.vel.y = 3
            self.jumping = False
            

    def update(self):
        # return to base frame at the end of animation
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        if self.jump_frame > len(self.jump_images):
            self.jump_frame = 0
            return
        
        # attack delay
        if pygame.time.get_ticks() - 150 < self.last_attack:
            self.attack_spaced = True
            
        else:
            self.attack_spaced = False
        
        # change image when jumping or falling
        if self.jumping or self.falling:
            if self.direction == "RIGHT":
                self.image = self.jump_images[int(self.jump_frame)]
            else:
                temp = self.jump_images[int(self.jump_frame)]
                self.image = pygame.transform.flip(temp, True, False)
            self.jump_frame += 0.07 

          # frame change when moving
        if self.jumping == False and self.running == True and not self.attacking:
            if self.vel.x > 0:
                self.image = self.running_images[int(self.move_frame)]
                self.direction = "RIGHT"
            else:
                temp = self.running_images[int(self.move_frame)]
                self.image = pygame.transform.flip(temp, True, False)
                self.direction = "LEFT"
            self.move_frame += 0.1

        # return to base frame if still
        '''
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.running_images[int(self.move_frame)]
            else:
                self.image = self.running_left_images[int(self.move_frame)] 
        '''
    
    def attack(self):
        # if attack frame has reached end of sequence, return to base frame
        if pygame.time.get_ticks() - 550 > self.last_attack:
            self.attack_sheet = 0
            self.attack_frame = 0
            self.last_frame = -1


        self.attacking = True
        if self.vel.y == 0: 
            self.vel.x /= 1.5
        if self.attack_frame >= len(self.all_attack_images[self.attack_sheet]):
            self.attack_frame = 0
            self.attacking = False
            self.attack_sheet += 1
        if self.attack_sheet > 2:
            self.attack_sheet = 0
            self.attack_frame = 0
        if self.jumping and self.attack_sheet != 2:
            self.attack_sheet = 2
            self.attack_frame = 0
        
        if self.attack_sheet < 2:
            self.damage_multiplier = 1
        else:
            self.damage_multiplier = 1.5

        self.damage = self.raw_damage * self.damage_multiplier

        current_attack_list = self.all_attack_images[self.attack_sheet]
        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = current_attack_list[int(self.attack_frame)]
        elif self.direction == "LEFT":
            #self.correction()
            temp = current_attack_list[int(self.attack_frame)]
            self.image = pygame.transform.flip(temp, True, False)


        # update the current attack frame
        self.attack_frame += 0.15
        self.last_attack = pygame.time.get_ticks()
       
        
        
        

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
    def __init__(self, vec, screen, type, ground_group, platform_group):
        super().__init__(vec, screen, type, ground_group, platform_group)
        self.load_sprites(type)
        self.pos = vec((300, 240))
        self.direction = "RIGHT"
        self.number = 2
        self.platform_group = platform_group

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

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(self, self.ground_group, False)
        hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
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
                    self.falling = False
            elif hits_platform and not self.falling:
                lowest = hits_platform[0]
                if self.pos.y > lowest.rect.top:
                    self.pos.y = lowest.rect.top+1 
                    self.vel.y = 0
                    self.jumping = False
                    self.double_jump = False
import pygame
from pygame.locals import *
import sprites_class
import player_class
import platforms

ACC = 0.3
FRIC = -0.10
HEIGHT = 900
WIDTH = 1700
SIZE_MULTIPLIER = 1.9

class Enemy(player_class.Player_2):
    def __init__(self, vec, screen, type, ground_group, platform_group, player):
        super().__init__(vec, screen, type, ground_group, platform_group)
        self.warping = False
        self.find_right_platform = False
        self.find_left_platform = False
        self.player = player
        self.raw_damage = 5
        
    def move(self):
        self.face_player()
        self.acc = self.vec(0,0.4)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        super().update()

        #player acceleration
        if self.attacking:
            self.acc.x = 0
        elif not self.warping and (self.find_left_platform or self.player.pos.x + 30 < self.pos.x):
            self.acc.x = -ACC
        elif not self.warping and (self.find_right_platform or self.player.pos.x-30 > self.pos.x):
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

    def jump(self):
        if (self.near_a_platform()
             and self.below_player() 
             and not self.falling):
            
            self.face_player()
            self.rect.x +=1 
            self.attacking = False
            #check to see if player contacts ground
            hits = pygame.sprite.spritecollide(self, self.ground_group, False)
            hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)

            self.rect.x -= 1

            if self.find_left_platform and hits_platform:
                self.jumping = True
                self.vel.y = -16
                self.vel.x = 2
                self.find_left_platform = False

            if self.find_right_platform and hits_platform:
                self.jumping = True
                self.vel.y = -16
                self.vel.x = -2
                self.find_left_platform = True


            if ((hits or hits_platform) and not self.jumping):
                self.jumping = True
                self.vel.y = -16

            if self.vel.y > -1 and self.double_jump:
                self.double_jump = False
            
            

    def gravity_check(self):
        return super().gravity_check()
            
    def attack(self):
        if self.near_player():
            self.face_player()
            super().attack()
            self.vel.x = 0
            self.attacking = True
            self.last_attack = pygame.time.get_ticks()
        else:
            self.attacking = False

    def face_player(self):
        if not super().facing(self.player):
            if self.direction == "RIGHT":
                self.direction == "LEFT"
            else:
                self.direction == "RIGHT"

    def near_player(self):
        if abs(self.player.pos.x - self.pos.x) < 100 and abs(self.player.pos.y - self.pos.y) < 30:
            self.moving = False
            return True
        return False
    
    def below_player(self):
        return self.pos.y > self.player.pos.y + 250
    
    def above_player(self):
        return self.pos.y < self.player.pos.y - 50
    
    def fall(self):
        if self.above_player():   
                if not self.falling:
                    self.falling = True
                    self.vel.y = 1
                hits_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
                hits_ground = pygame.sprite.spritecollide(self, self.ground_group, False)
                if hits_ground:
                    self.falling = False


    def warp(self):
        warp = self.should_warp()
        if warp == "right":
            self.acc.x = ACC*2.2
            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.9 * self.acc
            self.warping = True
        elif warp == "left":
            self.acc.x = -ACC*2.2
            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.9 * self.acc
            self.warping = True
        else:
            self.warping = False
        


    def should_warp(self):
        if self.pos.x > 900 and self.player.pos.x < 500:
            return "right"
        elif self.pos.x < 500 and self.player.pos.x > 900:
            return "left"
        else:
            return ""


    def near_a_platform(self):
        for platform in self.platform_group:
            if self.near_platform(platform):
                return True
        return False

    def near_platform(self, platform):
        width = platform.get_width()
        height = platform.get_height()
        x_chord = platform.get_x_coord()
        y_chord = platform.get_y_coord()

        
        within_height = self.pos.y - y_chord < 300 + height
        within_width = abs(self.pos.x - (x_chord+width/2)) < abs(width/2+25)

        if not within_height:
            if self.pos.x < WIDTH/2:
                self.find_left_platform = True
                self.find_right_platform = False
            else:
                self.find_left_platform = False
                self.find_right_platform = True
        
        if within_height:
            self.find_left_platform = False
            self.find_right_platform = False

        return within_height and within_width
    
            
        

                


import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import ground_class
import background_class
import platforms

 
pygame.init()

 
HEIGHT = 900
WIDTH = 1700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
BG = (0,0,0)
SIZE_MULTIPLIER = 1.9 * 1.5



def main():
    vec = pygame.math.Vector2  # 2 for two dimensional
    FramePerSec = pygame.time.Clock()
    
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    import player_class
    background = background_class.Background(displaysurface)
    ground = ground_class.Ground(displaysurface)
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    player1_type = "fighter" #input("player one, fighter or samurai? ")
    player2_type = "samurai" #input("player two, fighter or samurai? ")
    player = player_class.Player(vec, displaysurface, player1_type)
    player_2 = player_class.Player_2(vec, displaysurface, player2_type)


    player_group = pygame.sprite.Group()
    player_group.add(player)
    player_2_group = pygame.sprite.Group()
    player_2_group.add(player_2)


    platform_width = 100 * SIZE_MULTIPLIER * 1.3
    platform_height = 30 * SIZE_MULTIPLIER
    platform1 = platforms.Platform(WIDTH * 0.1, HEIGHT/1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform2 = platforms.Platform(WIDTH * 0.40, HEIGHT/2.8, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform3 = platforms.Platform(WIDTH * 0.70, HEIGHT/1.65, platform_width, platform_height, displaysurface, SIZE_MULTIPLIER)
    platform_group = pygame.sprite.Group()
    platform_group.add(platform1, platform2, platform3)

    fullscreen = False

        # game loop
    while True:
        FPS_CLOCK.tick(FPS)
        player.idle()
        player_2.idle()
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == VIDEORESIZE:
                if not fullscreen:
                    displaysurface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
                # Event handling for a range of different key presses    
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        displaysurface = pygame.display.set_mode( (displaysurface.get_width(), displaysurface.get_width()), pygame.FULLSCREEN)
                    else:
                        displaysurface = pygame.display.set_mode( (displaysurface.get_width(), displaysurface.get_width()), pygame.FULLSCREEN)

                if event.key == pygame.K_UP:
                    player.jump(ground_group, platform_group)
                if event.key == pygame.K_RSHIFT:
                    if player.attacking == FALSE:
                        player.attack()
                        hits = pygame.sprite.spritecollide(player, player_2_group, False)
                        if hits:
                            print("player hits")
                
                if event.key == pygame.K_w:
                    player_2.jump(ground_group, platform_group)
                if event.key == pygame.K_LSHIFT:
                    if player_2.attacking == FALSE:
                        player_2.attack()
                        hits = pygame.sprite.spritecollide(player_2, player_group, False)
                        if hits:
                            print("player 2 hits")
                    
                    
                


        player.gravity_check(player, ground_group, platform_group)
        player_2.gravity_check(player_2, ground_group, platform_group)
        # Render Functions ------
        background.render() 
        ground.render()
        platform_group.draw(displaysurface)
        player_2.update()
        player.update()
        if player.attacking:
            player.attack()
        if player_2.attacking:
            player_2.attack()
        player.move()
        player_2.move()
        displaysurface.blit(player.image, player.rect)
        displaysurface.blit(player_2.image, player_2.rect)
        player_2.move()
        player.move()
        player.update()
        player_2.update()
        pygame.display.update() 


if __name__=="__main__": 
    main() 
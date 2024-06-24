import pygame
from pygame.locals import *
from IPython.display import Image
import sys

class Player_Sprite(pygame.sprite.Sprite):
    player_spritesheet_idle = ""
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1200

    def __init__(self):
        super().__init__() 

        image_url = "images/Fighter/idle.png"
        self.player_spritesheet_idle = pygame.image.load(image_url).convert_alpha()
        self.surf = self.get_image(128, 128)
        self.rect = self.surf.get_rect(center = (100, self.SCREEN_HEIGHT-90))
        
    def get_image(self, width, height):
        sheet = self.player_spritesheet_idle
        image = pygame.Surface((width,height)).convert_alpha()
        BG = (0, 0, 0)
        image.fill(BG)
        image.blit(sheet, (0, 0), (0,0, width, height))
        return image


def main(): 
    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional
    
    #print(pygame.get_init())
    HEIGHT = 800
    WIDTH = 1200
    ACC = 0.5
    FRIC = -0.12
    FPS = 60
    
    FramePerSec = pygame.time.Clock()
    
    BG = (0, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite")
    screen.fill(BG)
    p1 = Player_Sprite()
    while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        
            screen.blit(p1.surf, (550, 400))
            pygame.display.flip();
            
  
  
if __name__=="__main__": 
    main() 
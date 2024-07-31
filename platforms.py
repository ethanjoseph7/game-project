import pygame




class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, displaySurface, SIZE_MULTIPLIER):
        super().__init__()
        self.image = pygame.Surface((width, height))
        platform_url = "assets/platforms/ground6.png"
        platform_image = pygame.image.load(platform_url)  # Load the image for the platform
        platform_image = pygame.transform.scale(platform_image, (platform_image.get_width()* SIZE_MULTIPLIER * 1.3, platform_image.get_height()*SIZE_MULTIPLIER))
        self.image.blit(platform_image, (0, 0), (0, 0, width, height))  # Crop the image to the specified width and height
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        platform_url = "assets/platforms/ground6.png"
        platform_image = pygame.image.load(platform_url).convert_alpha()  # Load the image for the platform
        self.image = pygame.transform.scale(platform_image, (platform_image.get_width()* SIZE_MULTIPLIER*1.4, platform_image.get_height()*SIZE_MULTIPLIER))

        self.rect = self.image.get_rect()
        self.rect.width -= 90
        self.rect.height = 10
        self.rect.x = x  # Set the x-coordinate of the platform
        self.rect.y = y  # Set the y-coordinate of the platform
        self.displaysurface = displaySurface
        BG = (0,0,0)
        self.image.set_colorkey(BG)

    def get_x_coord(self):
        return self.x
    
    def get_y_coord(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def render(self):
        self.displaysurface.blit(self.image, (self.rect.x, self.rect.y))
        
        

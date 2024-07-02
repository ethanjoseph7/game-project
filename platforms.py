import pygame




class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        platform_url = "platforms/Ground2.png"
        platform_image = pygame.image.load(platform_url)  # Load the image for the platform
        self.image.blit(platform_image, (0, 0), (0, 0, width, height))  # Crop the image to the specified width and height
        self.rect = self.image.get_rect()
        self.rect.x = x  # Set the x-coordinate of the platform
        self.rect.y = y  # Set the y-coordinate of the platform

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))
        

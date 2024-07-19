import pygame
from pygame.locals import *
import imageio
from PIL import Image, ImageSequence
import os

class Background(pygame.sprite.Sprite):
    def __init__(self, displaysurface, background_file):
        super().__init__()
        self.screen = displaysurface
        self.bgX = 0
        self.bgY = 0
        self.bg_frames = []
        self.bg_frame_index = 0
        self.load_background(background_file)

    def load_background(self, background_file):
        bg_url = os.path.join("assets", "backgrounds", background_file)
        if not os.path.exists(bg_url):
            raise FileNotFoundError(f"Background file not found: {bg_url}")

        if background_file.endswith('.gif'):
            self.bg_frames = self.load_gif(bg_url)
        else:
            try:
                self.bg_frames = [pygame.image.load(bg_url)]
            except pygame.error as e:
                raise ValueError(f"Error loading image: {bg_url} - {e}")
    
    def load_gif(self, bg_url):
        frames = load_gif_frames(bg_url, self.screen.get_size())
        return frames

    def render(self):
        self.screen.blit(self.bg_frames[self.bg_frame_index], (self.bgX, self.bgY))
        self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)

def load_gif_frames(filename, screen_size):
    gif = imageio.mimread(filename)
    frames = []
    for frame in gif:
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.convert("RGBA")
        mode = pil_image.mode
        data = pil_image.tobytes()
        frame_surface = pygame.image.fromstring(data, pil_image.size, mode)
        frame_surface = pygame.transform.scale(frame_surface, screen_size)
        frames.append(frame_surface)
    return frames
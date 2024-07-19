# helpers.py
import imageio
from PIL import Image as PilImage
import pygame

def load_gif_frames(filename, width, height):
    gif = imageio.mimread(filename)
    frames = []
    for frame in gif:
        pil_image = PilImage.fromarray(frame)
        pil_image = pil_image.convert("RGBA")
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        frame_surface = pygame.image.fromstring(data, size, mode)
        frame_surface = pygame.transform.scale(frame_surface, (width, height))
        frames.append(frame_surface)
    return frames

import pygame
import random

HEIGHT = 900
WIDTH = 1700

class BatSwarm:
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface
        self.bats = []
        self.spawn_timer = 0
        self.spawn_interval = random.randint(100, 200)  # Increased interval for less frequent appearance

        # Load bat sprite (assuming you have a sprite sheet with bat frames)
        self.bat_images = []
        bat_sprite_sheet = pygame.image.load('bat_spritesheet.png').convert_alpha()
        sprite_width = 32
        sprite_height = 32
        for row in range(4):
            bat_row_images = []
            for col in range(4):
                frame = pygame.transform.scale(
                    bat_sprite_sheet.subsurface((col * sprite_width, row * sprite_height, sprite_width, sprite_height)),
                    (64, 64)
                )
                bat_row_images.append(frame)
            self.bat_images.append(bat_row_images)

    def spawn_bats(self):
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x = -50
            y = random.randint(50, HEIGHT - 50)
            speed_x = random.uniform(2, 5)
            speed_y = random.uniform(-1, 1)
            row_index = 1
        elif side == 'right':
            x = WIDTH + 50
            y = random.randint(50, HEIGHT - 50)
            speed_x = -random.uniform(2, 5)
            speed_y = random.uniform(-1, 1)
            row_index = 3
        elif side == 'top':
            x = random.randint(50, WIDTH - 50)
            y = -50
            speed_x = random.uniform(-1, 1)
            speed_y = random.uniform(2, 5)
            row_index = 0
        else:  # bottom
            x = random.randint(50, WIDTH - 50)
            y = HEIGHT + 50
            speed_x = random.uniform(-1, 1)
            speed_y = -random.uniform(2, 5)
            row_index = 2

        num_bats = random.choice([1, random.randint(2, 3)])  # Single bat or small group, max 3
        self.bats.append([x, y, speed_x, speed_y, 0, num_bats, row_index])

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_bats()
            self.spawn_timer = 0
            self.spawn_interval = random.randint(100, 200)  # Increased interval for less frequent appearance

        for bat in self.bats:
            bat[0] += bat[2]
            bat[1] += bat[3]
            bat[4] = (bat[4] + 1) % 4  # Update animation frame (assuming 4 frames per bat type)
            if bat[0] < -50 or bat[0] > WIDTH + 50 or bat[1] < -50 or bat[1] > HEIGHT + 50:
                self.bats.remove(bat)

    def render(self):
        for bat in self.bats:
            row_index = bat[6]  # Retrieve the bat type (row index)
            for i in range(bat[5]):
                offset_x = i * random.randint(50, 70)  # Varied horizontal offset to avoid overlap
                offset_y = random.randint(-20, 20)
                frame = self.bat_images[row_index][bat[4]]
                self.displaysurface.blit(frame, (bat[0] + offset_x, bat[1] + offset_y))


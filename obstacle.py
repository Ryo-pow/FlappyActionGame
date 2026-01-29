import random
import math
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_SPEED

class Obstacle(pygame.sprite.Sprite):
    last_gap_center = SCREEN_HEIGHT // 2
    current_random_gap = 140

    def __init__(self, *groups, is_top, mode):
        super().__init__(*groups)
        self.mode = mode
        self.is_top = is_top

        if self.mode == "spike":
            self.width = 80
            if self.is_top:
                margin = 100
                Obstacle.last_gap_center = random.randint(margin, SCREEN_HEIGHT - margin)
                Obstacle.current_random_gap = random.randint(110, 160)
        else:
            self.width = 60
            if self.is_top:
                Obstacle.last_gap_center = random.randint(100, SCREEN_HEIGHT - 100)
                Obstacle.current_random_gap = random.randint(80, 160)

        self.gap_size = Obstacle.current_random_gap
        self.gap_center_y = Obstacle.last_gap_center
        self.timer = pygame.time.get_ticks() * 0.005
        self.move_range = 35

        self.image = pygame.Surface((self.width, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH + 60, 0))
        self.update_appearance()
        self.mask = pygame.mask.from_surface(self.image)

    def update_appearance(self):
        self.image.fill((0, 0, 0, 0))
        color = (220, 60, 60)
        gap_top = self.gap_center_y - (self.gap_size // 2)
        gap_bottom = self.gap_center_y + (self.gap_size // 2)

        if self.mode == "square":
            if self.is_top:
                pygame.draw.rect(self.image, color, (0, 0, self.width, gap_top))
                pygame.draw.rect(self.image,(255, 255, 255),(0, 0, self.width, gap_top),1)
            else:
                pygame.draw.rect(self.image, color, (0, gap_bottom, self.width, SCREEN_HEIGHT - gap_bottom))
                pygame.draw.rect(self.image, (255, 255, 255), (0, gap_bottom, self.width, SCREEN_HEIGHT - gap_bottom),1)

        elif self.mode == "spike":
            offset = math.sin(self.timer) * self.move_range

            if self.is_top:
                tip_y = gap_top + offset
                points = [(0, 0), (self.width, 0), (self.width // 2, tip_y)]
                pygame.draw.polygon(self.image, color, points)
                pygame.draw.polygon(self.image, (255, 255, 255), points, 2)
            else:
                tip_y = gap_bottom - offset
                points = [(0, SCREEN_HEIGHT), (self.width, SCREEN_HEIGHT), (self.width // 2, tip_y)]
                pygame.draw.polygon(self.image, color, points)
                pygame.draw.polygon(self.image, (255, 255, 255), points, 2)

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.mode == "spike":
            self.timer += 0.1
            self.update_appearance()
            self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0:
            self.kill()

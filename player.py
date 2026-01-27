import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PLAYER_COLOR, (0, 0, 34, 34))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 34, 34), 2)
        
        self.rect = self.image.get_rect(center=(150, SCREEN_HEIGHT // 2))
        
        self.pos_y = float(self.rect.y)
        self.velocity = 0
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.velocity = JUMP_POWER

    def update(self):
        self.velocity += GRAVITY
        self.pos_y += self.velocity
        self.rect.y = int(self.pos_y)
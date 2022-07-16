import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.x += self.setting.alien_speed * self.setting.move_direction
        self.rect.x = self.x

    def check_edge(self) -> bool:
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            return True

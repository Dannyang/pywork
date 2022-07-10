import pygame
from pygame.sprite import Sprite
from settings import Setting


class Alien(Sprite):
    def __init__(self):
        super().__init__()
        self.setting = Setting() 
        self.screen = self.setting.screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.setting.alien_speed * self.setting.move_direction
        self.rect.x = self.x

    def check_edge(self):
        self.screen.get_rect()

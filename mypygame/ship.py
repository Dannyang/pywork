import pygame
from settings import Setting


class Ship:
    def __init__(self, ai_game):  # ai_game是AlienInvasion的实例
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = Setting()
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False
        self.x = float(self.rect.x)
        # pygame 中左上定点坐标是（0,0),往右下走横纵坐标增长
        self.y = float(self.rect.y)

    def biteme(self):
        self.screen.blit(self.image, self.rect)

    # 飞船被创思时重新将飞船置于屏幕下方
    def recreate_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update_position(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.speed_set
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.speed_set
        if self.moving_top and self.rect.top > 0:
            self.y -= self.setting.speed_set
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.setting.speed_set
        self.rect.x = self.x
        self.rect.y = self.y

    # def shoot_bullet(self):


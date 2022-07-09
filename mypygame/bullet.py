import pygame
from pygame.sprite import Sprite
from settings import Setting


# 引入alien_invasion 对象
class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = Setting()
        self.color = self.setting.bullet_color
        # 使用pygame新建一个碰撞体
        self.bullet_rec = pygame.Rect((0, 0), self.setting.bullet_width, self.setting.bullet_height)
        # 矫正位置从船头顶部中间发出
        self.bullet_rec.midbottom = ai_game.ship.image_rect.mid_top

import pygame
from pygame.sprite import Sprite


# 引入alien_invasion 对象
class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.color = self.setting.bullet_color
        # 使用pygame新建一个碰撞体
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        # 矫正位置从船头顶部中间发出
        self.rect.midbottom = self.ship.rect.midtop
        self.y = float(self.rect.y)

    # 需要重写父类Sprite update方法更新rec位置
    def update(self):
        # 向上移动式y坐标减小
        self.y -= self.setting.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # 把生成的子弹生成在画布上
        pygame.draw.rect(self.screen, self.setting.bullet_color, self.rect)

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
        self.bullet_rec = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        # 矫正位置从船头顶部中间发出
        self.bullet_rec.midbottom = ai_game.ship.image_rect.midtop
        self.y = float(self.bullet_rec.y)

    # 需要重写父类Sprite update方法更新rec位置
    def update(self):
        # 向上移动式y坐标减小
        self.y -= self.setting.bullet_speed
        self.bullet_rec.y = self.y

    def draw_bullet(self):
        # 把生成的子弹生成在画布上
        pygame.draw.rect(self.screen, self.setting.bullet_color, self.bullet_rec)

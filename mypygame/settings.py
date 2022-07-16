import pygame


class Setting:
    def __init__(self):
        # python与java的区别python在init方法中定义类属性
        self.screen = 1200
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.speed_set = 0.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 200
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_amount_allowed = 30

        # alien_settings
        # 右移动速度
        self.alien_speed = 0.5
        # 下落速度
        self.drop_down_speed = 0.5
        # 敌人移动方向1 represents right; -1 represents left
        self.move_direction = 1

        # 初始化游戏窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # 创建游戏窗口游戏窗口大小
        pygame.display.set_caption('woah alien!!!!')  # 游戏标题

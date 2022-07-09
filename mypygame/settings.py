class Setting:
    def __init__(self):
        # python与java的区别python在init方法中定义类属性
        self.screen = 1200
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.speed_set = 1.0

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_amount_allowed = 30

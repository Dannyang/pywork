import sys
import pygame
from settings import Setting
from ship import Ship
from bullet import Bullet


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))  # 创建游戏窗口游戏窗口大小
        pygame.display.set_caption('woah alien!!!!')  # 游戏标题
        self.bg_color = self.setting.bg_color
        self.ship = Ship(self)
        # pygame.sprite.Group用于管理所有已经发射的子弹
        self.bullets = pygame.sprite.Group()

    def listen_to_keyboard(self):
        # 监听鼠标和键盘时间
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_evnet(event)

    def check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            # event.key只有在event.type= KEYDOWN时才会有
        elif event.key == pygame.K_UP:
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def check_keyup_evnet(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    def fire_bullet(self):
        # 每发射一枚子弹都需要生成一个bullet实例
        if len(self.bullets) < self.setting.bullet_amount_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def remove_unnecessary_bullet(self, bullets):
        for bullet in bullets:
            if bullet.bullet_rec.top <= 0:
                bullets.remove(bullet)
        print(len(bullets))

    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.biteme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 刷新屏幕
        pygame.display.flip()

    def run_game(self):
        #  Make the most recently drawn screen visible
        while True:
            self.listen_to_keyboard()
            self.ship.update_position()
            self.bullets.update()
            self.remove_unnecessary_bullet(self.bullets)
            self.update_screen()

        # 监听键盘事件


if __name__ == '__main__':
    ai_game = AlienInvasion()
    ai_game.run_game()

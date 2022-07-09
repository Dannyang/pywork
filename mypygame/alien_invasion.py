import sys
import pygame
from settings import Setting
from ship import Ship


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))  # 创建游戏窗口游戏窗口大小
        pygame.display.set_caption('woah alien!!!!')  # 游戏标题
        self.bg_color = self.setting.bg_color
        self.ship = Ship(self)

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

    def check_keyup_evnet(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    # 刷新屏幕
    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.biteme()
        pygame.display.flip()

    def run_game(self):
        #  Make the most recently drawn screen visible
        while True:
            self.listen_to_keyboard()
            self.ship.update_position()
            self.update_screen()

        # 监听键盘事件


if __name__ == '__main__':
    ai_game = AlienInvasion()
    ai_game.run_game()

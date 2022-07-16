import sys
import pygame

from mypygame.alien import Alien
from mypygame.stats import GameStats
from settings import Setting
from ship import Ship
from bullet import Bullet
from time import sleep


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.screen = self.setting.screen  # 创建游戏窗口游戏窗口大小
        self.bg_color = self.setting.bg_color
        self.ship = Ship(self)
        # pygame.sprite.Group用于管理所有已经发射的子弹
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # 先初始化敌人
        self.create_fleet_aliens()
        self.stats = GameStats(self)

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet_aliens()
            self.ship.recreate_ship()
            sleep(1)
        else:
            self.stats.game_active = False

    def listen_to_keyboard(self) -> None:
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

    def move_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("ship hit")
            self.ship_hit()

    def remove_unnecessary_bullet(self, bullets):
        # 更新管理组里所有的bullet对象的位置，并移除已经在屏幕外的bullet实例
        self.bullets.update()
        for bullet in bullets:
            if bullet.rect.top <= 0:
                bullets.remove(bullet)
        # print('num of existing bullets is' + str(len(self.bullets)))
        self.check_aliens_and_bullets()

    def check_aliens_and_bullets(self):
        pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if not self.aliens:
            # the statements inside if block execute only if the value(boolean) is False or if the value(collection)
            # is not empty.
            self.bullets.empty()
            self.create_fleet_aliens()

    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.biteme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 刷新屏幕
        pygame.display.flip()

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        # spare_space = self.screen.get_width() - 2 * alien_width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet_aliens(self):
        alien = Alien(self)
        # alien_width = alien.rect.width
        # alien_height = alien.rect.height
        # alien.rect.size返回一个Tuple元祖
        # 定义一个x, y = 1, 2
        # 则x=1, y=2且元组的元素值不可再更改
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        # 可用垂直空间
        available_vertical_space = self.setting.screen_height - (3 * alien_height) - ship_height
        rows_of_aliens = available_vertical_space // (2 * alien_height)
        spare_space = self.screen.get_width() - 2 * alien_width
        num_of_aliens = spare_space // (2 * alien_width)

        for y in range(rows_of_aliens):
            for i in range(num_of_aliens):
                self.create_alien(i, y)
        # print('num of existing aliens is' + str(len(self.aliens)))

    def check_fleet_edges(self):
        for alien in self.aliens:
            if alien.check_edge():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            y = float(alien.rect.y)
            y += self.setting.drop_down_speed
            alien.rect.move(alien.rect.x, y)
            # alien.rect.y = y
            # print(alien.rect.y)
        self.setting.move_direction *= -1

    def run_game(self):
        #  Make the most recently drawn screen visible
        while True:
            if self.stats.game_active:
                self.listen_to_keyboard()
                self.ship.update_position()
                self.bullets.update()
                self.move_aliens()
                self.remove_unnecessary_bullet(self.bullets)
                self.update_screen()
            else:
                print("game over!!!")
                sys.exit()


if __name__ == '__main__':
    ai_game = AlienInvasion()
    ai_game.run_game()

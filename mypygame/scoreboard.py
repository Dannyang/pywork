import pygame


class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.setting
        self.stats = ai_game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.rect = self.score_image.get_rect()
        self.rect.right = self.screen_rect.right - 20
        self.rect.top = 20

    def draw_score(self):
        self.screen.blit(self.score_image, self.rect)

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.setting
        self.reset_stats()
        # Start Alien Invasion in an active state.
        self.game_active = False
        self.score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit

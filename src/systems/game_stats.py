# src/systems/game_stats.py

class GameStats:
    def __init__(self, game, settings):
        self.game = game
        self.settings = settings
        self.player = None


    def on_death(self, player):
        self.player = player
        self.game.game_stats = self
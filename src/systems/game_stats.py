# src/systems/game_stats.py

class GameStats:
    def __init__(self, game, settings):
        self.game = game
        self.settings = settings
        self.stats = None

    def update(self, player, weapon)->dict:
        """met a jours les stats du joueur et les retourne"""
        self.stats = {**player.get_stats(), **weapon.get_stats()}
        return self.stats

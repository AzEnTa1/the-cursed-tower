# src/systems/game_stats.py

class GameStats:
    def __init__(self, game, settings):
        self.game = game
        self.settings = settings
        self.stats = None

    def update(self, player, weapon)->dict:
        """
        Mise à jour des Statistiques et les retournents
        Utilisée pour le menu Pause
        """
        self.stats = {**player.get_stats(), **weapon.get_stats()}
        return self.stats

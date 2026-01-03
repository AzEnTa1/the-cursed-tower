# src/scenes/sub_scenes/base_sub_scene.py

class BaseSubScene:
    """Classe de base pour toutes les sub-scènes du jeu""" 
    
    def __init__(self, game, game_scene, settings):
        self.game_scene = game_scene
        self.game = game
        self.settings = settings
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        self.game_scene.player.reset_player_movements()
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        pass
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""

    def resize(sel):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        pass
        
# src/scene/base_scene.py

class BaseScene:
    """Classe de base pour toutes les scènes du jeu""" # Game et Menu
    
    def __init__(self, game, settings):
        self.game = game
        self.settings = settings
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        pass
    
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
        
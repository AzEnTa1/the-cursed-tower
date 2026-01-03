# src/scenes/sub_scenes/base_sub_scene.py

class BaseSubScene:
    """Classe de base pour toutes les sub-scènes du jeu""" # Perks et Pause
    
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
        """appelé lorsque la fenêtre change de taille"""
        #height et width sont les vraie dimension de la fenetre
        #!= self.settings.screen_height/width qui sont les dimension de la fenetre interne 4:3
        #permet de diminué les calcules fait en permanance pour dessiner les élements
        #|-> surement inutils
        pass
        
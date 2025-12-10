import pygame
from .base_sub_scene import BaseSubScene
from src.ui.pause_ui import PauseUI

class PauseSubScene(BaseSubScene):
    """gere le menu pause""" # Perks et Pause
    
    def __init__(self, game, game_scene, settings):
        super().__init__(game, game_scene, settings)
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        self.ui = PauseUI(self.settings)
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
                #if self.play_button.collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)
                
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen)

    def resize(self, height, width):
        """appelé lorsque la fenêtre change de taille"""
        #height et width sont les vraie dimension de la fenetre
        #!= self.settings.screen_height/width qui sont les dimension de la fenetre interne 4:3
        #permet de diminué les calcules fait en permanance pour dessiner les élements
        #|-> surement inutils
        pass
        
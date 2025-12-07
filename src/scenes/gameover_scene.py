import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)

class GameOver_Scene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.font = None
        self.small_font = None
        self.play_button = None
        
    def on_enter(self):
        """Initialisation du Game Over"""
        print("Game Over Scene")
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        pass
    
    def menu_back(self):
        """Retourne au menu"""
        self.game.change_scene(self.settings.SCENE_MENU)
    
    def update(self):
        """"""
    
    def draw(self, screen):
        """Dessine le menu Game Over"""
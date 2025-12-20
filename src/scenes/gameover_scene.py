# src/scenes/gameover_scene.py 
import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)
from src.ui.game_over_ui import GameOverUI

class GameOverScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.ui = None
        self.quit_button = None
        
    def on_enter(self, game_stats):
        """Initialisation du Game Over"""
        self.ui = GameOverUI(self.settings, game_stats)
        
        self.quit_text = self.settings.font["h3"].render("retourner au menu", True, (0, 0, 0))
        
        self.quit_button = pygame.Rect(self.settings.screen_width*0.4, self.settings.screen_height*0.8, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)

        print("Game Over Scene")
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                 self.game.change_scene(self.settings.SCENE_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)

    
    def update(self):
        """Pas de logique à mettre à jour pour l'instant"""
        pass
    
    def draw(self, screen):
        """Dessine le menu Game Over"""
        self.ui.draw(screen, self.quit_button, self.quit_rect, self.quit_text)
        

    def resize(self):
        self.quit_button = pygame.Rect(self.settings.screen_width*0.4, self.settings.screen_height*0.8, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)
        self.ui.resize()


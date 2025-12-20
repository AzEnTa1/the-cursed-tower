# src/scenes/sub_scenes/pause_sub_scene.py
import pygame
from .base_sub_scene import BaseSubScene
from src.ui.pause_ui import PauseUI

class PauseSubScene(BaseSubScene):
    """Gère le Menu Pause""" # Perks et Pause
    
    def __init__(self, game, game_scene, settings):
        super().__init__(game, game_scene, settings)
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        self.ui = PauseUI(self.settings)
        
        self.exit_rect = None
        self.back_to_menu_rect = None
        self.resize()
        
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene.game_paused = False
            elif self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)
                
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.exit_rect, self.back_to_menu_rect)

    def resize(self):
        """appelé lorsque la fenêtre change de taille"""
        
        self.exit_rect = pygame.Rect(self.settings.screen_width*0.85 , self.settings.screen_width*0.05, self.settings.screen_width*0.1, self.settings.screen_width*0.1)
        self.back_to_menu_rect = pygame.Rect(self.settings.screen_width*0.4 , self.settings.screen_height*0.8, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        self.ui.resize()
        
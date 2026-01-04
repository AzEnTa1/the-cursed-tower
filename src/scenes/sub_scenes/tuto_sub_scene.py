# src/scenes/sub_scenes/tuto_sub_scene.py

import pygame
from .base_sub_scene import BaseSubScene

class TutoSubScene(BaseSubScene):
    """Gère le Menu Pause"""
    
    def __init__(self, game, game_scene, settings):
        super().__init__(game, game_scene, settings)
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        super().on_enter()
        
        self.bg_img = pygame.image.load(r"assets/images/tuto.png")
        self.bg_img = pygame.transform.scale(self.rect, (self.settings.screen_width, self.settings.screen_height))

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
        #met l'imade du tuto
        screen.blit(self.bg_img, (0, 0))

    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.bg_img = pygame.transform.scale(self.rect, (self.settings.screen_width, self.settings.screen_height))
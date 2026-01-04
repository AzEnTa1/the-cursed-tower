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
        self.rect = pygame.Rect(self.settings.screen_width//4, self.settings.screen_height//4,
                                self.settings.screen_width//2, self.settings.screen_height//2
                                )

    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene.game_paused = False


    def update(self):
        """Met à jour la logique de la scène"""
        pass

    def draw(self, screen):
        """Dessine la scène"""
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        pass
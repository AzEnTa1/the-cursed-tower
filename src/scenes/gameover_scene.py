import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)

class GameOverScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.font = None
        self.small_font = None
        self.play_button = None
        self.quit_button = None
        
    def on_enter(self):
        """Initialisation du Game Over"""
        self.quit_button = pygame.Rect(self.settings.screen_width*0.4, self.settings.screen_height*0.8, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        print("Game Over Scene")
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                 self.game.change_scene(self.settings.SCENE_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.collidepoint(event.pos):
                    self.game.change_scene(self.settings.SCENE_MENU)

    
    def update(self):
        """"""
    
    def draw(self, screen):
        """Dessine le menu Game Over"""
        screen.fill((100, 100, 100))
        pygame.draw.rect(screen, (255, 0, 0), self.quit_button)

    def resize(self, width, height):
        self.quit_button = pygame.Rect(self.settings.screen_width*0.4, self.settings.screen_height*0.8, self.settings.screen_width*0.2, self.settings.screen_height*0.1)

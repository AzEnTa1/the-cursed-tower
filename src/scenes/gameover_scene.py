# src/scenes/gameover_scene.py 
import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)
from src.ui.game_over_ui import GameOverUI

class GameOverScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.ui = None
        self.quit_button = None
        
    def on_enter(self, player_data, game_stats):
        """Initialisation du Game Over"""
        # Transforme le score en coins
        player_data["coins"] += game_stats["score"]
        player_data["all_time_coins"] += game_stats["score"]
        self.game.save()
        
        self.ui = GameOverUI(self.settings, game_stats)
        self.quit_text = self.settings.font["h3"].render("Revenir au Menu", True, (255, 0, 0))
        self.quit_button = pygame.image.load(r"assets/images/cadre.png")
        self.quit_button = pygame.transform.scale(self.quit_button, (200, 50))
        self.quit_button = self.quit_button.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2))
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)

    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                 self.game.change_scene(self.settings.SCENE_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)
    
    def update(self):
        """"""
        if self.quit_button.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.quit_text = self.settings.font["h3"].render("Revenir au Menu", True, (255, 255, 255))
            if not hasattr(self, 'exit_hovered') or not self.exit_hovered:
                self.exit_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.quit_text = self.settings.font["h3"].render("Revenir au Menu", True, (255, 0, 0))
            self.exit_hovered = False
    
    def draw(self, screen):
        """Dessine le menu Game Over"""        
        self.ui.draw(screen, self.quit_button, self.quit_rect, self.quit_text)
    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.quit_button.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2, 200, 50)
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)
        self.ui.resize()


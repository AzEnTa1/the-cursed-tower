# src/scenes/gameover_scene.py 
import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)

class GameOverScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.font = None
        self.small_font = None
        self.quit_button = None
        
    def on_enter(self, game_stats):
        """Initialisation du Game Over"""
        self.font = pygame.font.Font(None, 48) # Police par défaut, taille 48
        self.small_font = pygame.font.Font(None, 24) # ---, taille 24

        self.quit_button = pygame.Rect(self.settings.screen_width*0.4 + self.settings.x0, self.settings.screen_height*0.8 + self.settings.y0, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        self.stats_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.1 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.8)
        self.game_stats = game_stats
        self.quit_text = self.small_font.render("retourner au menu", True, (0, 0, 0))
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)
        self.stats_text = self.font.render(f"Score :{self.game_stats.player.score}", True, (0, 0, 0))
        self.stats_text_rect = self.stats_text.get_rect(center=(self.quit_button.center[0], self.settings.y0 + self.settings.screen_height*0.15))
        print("Game Over Scene")
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                 self.game.change_scene(self.settings.SCENE_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)

    
    def update(self):
        """Pas de logique à mettre à jour pour l'instant"""
        pass
    
    def draw(self, screen):
        """Dessine le menu Game Over"""
        screen.fill((100, 100, 100))

        pygame.draw.rect(screen, (255, 0, 255), self.stats_rect)
        screen.blit(self.stats_text, self.stats_text_rect)

        pygame.draw.rect(screen, (255, 0, 0), self.quit_button)
        screen.blit(self.quit_text, self.quit_rect)

    def resize(self, width, height):
        self.quit_button = pygame.Rect(self.settings.screen_width*0.4 + self.settings.x0, self.settings.screen_height*0.8 + self.settings.y0, self.settings.screen_width*0.2, self.settings.screen_height*0.1)
        self.quit_rect = self.quit_text.get_rect(center=self.quit_button.center)
        self.stats_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.1 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.8)
        self.stats_text_rect = self.quit_text.get_rect(center=(self.quit_button.center[0], self.settings.y0 + self.settings.screen_height*0.15))


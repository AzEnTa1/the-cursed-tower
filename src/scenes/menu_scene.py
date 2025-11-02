import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, SCENE_GAME
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)

class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = None
        self.small_font = None
        self.play_button = None
        
    def on_enter(self):
        """Initialisation du menu"""
        self.font = pygame.font.Font(None, 48) # Police par défaut, taille 48
        self.small_font = pygame.font.Font(None, 24) # ---, taille 24
        # Rectangle pour le bouton Jouer (x, y, width, height)
        self.play_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        print("Menu Scene")
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                self.start_game()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Touche ENTER
                self.start_game()
    
    def start_game(self):
        """Démarre le jeu"""
        self.game.change_scene(SCENE_GAME)
    
    def update(self):
        """Pas de logique particulière pour le menu simple"""
        pass
    
    def draw(self, screen):
        """Dessine le menu"""
        # Fond noir
        screen.fill((0, 0, 0))
        
        # Titre
        title_text = self.font.render("TOUR MAUDITE", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        screen.blit(title_text, title_rect)
        
        # Bouton Jouer
        pygame.draw.rect(screen, GREEN, self.play_button)
        play_text = self.small_font.render("JOUER (ou ENTER)", True, WHITE)
        play_rect = play_text.get_rect(center=self.play_button.center)
        screen.blit(play_text, play_rect)
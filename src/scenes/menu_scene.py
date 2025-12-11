import pygame
from .base_scene import BaseScene # Importation de la classe de base des scènes (jsp si on a le droit car on a théoriquement pas vu en cour)

class MenuScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.font = None
        self.small_font = None
        self.play_button = None
        self.bg_title_rect = None
        
    def on_enter(self):
        """Initialisation du menu"""
        self.font = pygame.font.Font(None, 48) # Police par défaut, taille 48
        self.small_font = pygame.font.Font(None, 24) # ---, taille 24
        # Rectangle pour le bouton Jouer (x, y, width, height)
        self.play_button = pygame.Rect(self.settings.x0 + self.settings.screen_width//2 - 100, self.settings.y0 + self.settings.screen_height//2, 200, 50)
        self.bg_title_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.2 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.2)
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
        self.game.change_scene(self.settings.SCENE_GAME)
    
    def update(self):
        """Pas de logique particulière pour le menu simple (pr l'instant)"""
        pass
    
    def draw(self, screen):
        """Dessine le menu"""
        # Fond noir
        screen.fill((0, 0, 0))

        
        # Titre
        pygame.draw.rect(screen, (255, 255, 0), self.bg_title_rect)
        title_text = self.font.render("Tour Maudite", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=self.bg_title_rect.center)
        screen.blit(title_text, title_rect)

        # Bouton Jouer
        pygame.draw.rect(screen, (0, 255, 0), self.play_button)
        play_text = self.small_font.render("JOUER (ou ENTER)", True, (0, 0, 0))
        play_rect = play_text.get_rect(center=self.play_button.center)
        screen.blit(play_text, play_rect)

    def resize(self, height, width):
        """appelé lorsque la fenêtre change de taille"""
        self.play_button = pygame.Rect(self.settings.x0 + self.settings.screen_width//2 - 100, self.settings.y0 + self.settings.screen_height//2, 200, 50)
        self.bg_title_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.2 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.2)
        
        
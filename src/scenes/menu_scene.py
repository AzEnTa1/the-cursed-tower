# src/scenes/menu_scene.py
import pygame
from .base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        
    def on_enter(self):
        """Initialisation du menu"""
        # Rectangle pour le bouton Jouer (x, y, width, height)
        self.play_button = pygame.Rect(self.settings.screen_width//2 - 100, self.settings.screen_height//2, 200, 50)
        self.bg_title_rect = pygame.Rect(self.settings.screen_width*0.1, self.settings.screen_height*0.2, self.settings.screen_width*0.8, self.settings.screen_height*0.2)
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
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
        # Charger l'image de fond
        try:
            bg_image = pygame.image.load("assets/images/Menu.png")
            bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
            screen.blit(bg_image, (0, 0))
        except FileNotFoundError:
            # Fallback si l'image n'existe pas
            screen.fill((50, 50, 100))
        
        # Bouton Jouer avec effet hover
        font = pygame.font.SysFont(None, 60)
        
        text_normal = font.render("JOUER(entrée)", True, (255, 255, 255))
        text_hover = font.render("JOUER(entrée)", True, (255, 200, 0))
        
        button_rect = text_normal.get_rect(center=self.play_button.center)
        mouse_pos = pygame.mouse.get_pos()
        
        # Afficher le bouton avec effet hover
        if button_rect.collidepoint(mouse_pos):
            screen.blit(text_hover, button_rect)
        else:
            screen.blit(text_normal, button_rect)
    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.play_button = pygame.Rect(self.settings.screen_width//2 - 100, self.settings.screen_height//2, 200, 50)
        self.bg_title_rect = pygame.Rect(self.settings.screen_width*0.1, self.settings.screen_height*0.2, self.settings.screen_width*0.8, self.settings.screen_height*0.2)
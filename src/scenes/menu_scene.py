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
        
        # Charger l'image de fond
        try:
            self.bg_image = pygame.image.load("assets/images/Menu.png")
            self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
            
        except FileNotFoundError:
            # Fallback si l'image n'existe pas
            self.bg_image = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            self.bg_image.fill((50, 50, 100))
        
        self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 200, 0))
        self.button_rect = self.text.get_rect(center=self.play_button.center)
    
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
        
        if self.button_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 200, 0))
        else:
            self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 255, 255))
    
    def draw(self, screen):
        """Dessine le menu"""
        
        # Image de fond
        screen.blit(self.bg_image, (0, 0))

        # Bouton Jouer avec effet hover
        
        screen.blit(self.text, self.button_rect)
    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.play_button.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2, 200, 50)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.button_rect = self.text.get_rect(center=self.play_button.center)
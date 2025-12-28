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
        self.exit_text = self.settings.font["h3"].render("Continuer (echap)", True, (255, 0, 0))
        self.exit_rect = pygame.image.load(r"assets/images/Fd_perks.png")
        self.exit_rect = pygame.transform.scale(self.exit_rect, (200, 50))
        self.exit_rect = self.exit_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 - 75))
        self.exit_text_rect = self.exit_text.get_rect(center=self.exit_rect.center)
        
        #fait un bouton transparant derrière le texte


        self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
        self.back_to_menu_rect = pygame.image.load(r"assets/images/Fd_perks.png")
        self.back_to_menu_rect = pygame.transform.scale(self.back_to_menu_rect, (200, 50))
        self.back_to_menu_rect = self.back_to_menu_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 + 37.5))
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
        

    
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
            else:
                None
                
    
    def update(self):
        """Met à jour la logique de la scène"""
        if self.exit_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.exit_text = self.settings.font["h3"].render("Continuer (echap)", True, (255, 255, 255))
        else:
            self.exit_text = self.settings.font["h3"].render("Continuer (echap)", True, (255, 0, 0))

        if self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 255, 255))
        else:
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))

    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.exit_rect, self.exit_text_rect, self.exit_text, self.back_to_menu_rect, self.back_to_menu_text_rect, self.back_to_menu_text)

    def resize(self):
        """appelé lorsque la fenêtre change de taille"""
        # Met à jour les positions des éléments UI en fonction de la nouvelle taille de l'écran
        self.exit_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 - 75, 200, 50)
        self.exit_text_rect = self.exit_text.get_rect(center=self.exit_rect.center)
        self.back_to_menu_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 37.5, 200, 50)
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
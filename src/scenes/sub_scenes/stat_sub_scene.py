# src/scenes/sub_scenes/pause_sub_scene.py
import pygame
from .base_sub_scene import BaseSubScene
from src.ui.stat_ui import StatUI

class StatSubScene(BaseSubScene):
    """Gère le Menu Pause""" # Perks et Pause
    
    def __init__(self, game, game_scene, settings):
        super().__init__(game, game_scene, settings)
        
    
    def on_enter(self, game_stats:dict):
        """Appelée quand la scène devient active"""

        self.ui = StatUI(game_stats, self.settings)

        #met un fond d'écran au stat

        self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
        self.back_to_menu_rect = pygame.image.load(r"assets/images/cadre.png")
        self.back_to_menu_rect = pygame.transform.scale(self.back_to_menu_rect, (200, 50))
        self.back_to_menu_rect = self.back_to_menu_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 +200))
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
        
    
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene.current_sub_scene = self.game_scene.pause_sub_scene
                self.game_scene.current_sub_scene.on_enter(self.game_scene.game_stats.update(self.game_scene.player, self.game_scene.weapon))              
    
    def update(self):
        """Met à jour la logique de la scène"""
        if self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 255, 255))
            if not hasattr(self, 'exit_hovered1') or not self.exit_hovered1:
                self.exit_hovered1 = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
            self.exit_hovered1 = False

    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.back_to_menu_rect, self.back_to_menu_text_rect, self.back_to_menu_text)


    def resize(self):
        """appelé lorsque la fenêtre change de taille"""
        # Met à jour les positions des éléments UI en fonction de la nouvelle taille de l'écran
        self.back_to_menu_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 200, 200, 50)
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
        self.ui.resize()
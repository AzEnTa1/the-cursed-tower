# src/scenes/sub_scenes/pause_sub_scene.py
import pygame
from .base_sub_scene import BaseSubScene
from src.ui.pause_ui import PauseUI

class PauseSubScene(BaseSubScene):
    """Gère le Menu Pause"""
    
    def __init__(self, game, game_scene, settings):
        super().__init__(game, game_scene, settings)
    
    def on_enter(self, game_stats:dict):
        """Appelée quand la scène devient active"""
        super().on_enter()
        self.ui = PauseUI(game_stats, self.settings)
        self.exit_text = self.settings.font["h3"].render("Continuer", True, (255, 0, 0))
        self.exit_rect = pygame.image.load(r"assets/images/cadre.png")
        self.exit_rect = pygame.transform.scale(self.exit_rect, (200, 50))
        self.exit_rect = self.exit_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 - 75))
        self.exit_text_rect = self.exit_text.get_rect(center=self.exit_rect.center)
        
        # Bouton Quitter au menu principal
        self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
        self.back_to_menu_rect = pygame.image.load(r"assets/images/cadre.png")
        self.back_to_menu_rect = pygame.transform.scale(self.back_to_menu_rect, (200, 50))
        self.back_to_menu_rect = self.back_to_menu_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 + 37.5))
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
        
        # Bouton Stats
        self.stat_text = self.settings.font["h3"].render("Statistiques", True, (255, 0, 0))
        self.stat_rect = pygame.image.load(r"assets/images/cadre.png")
        self.stat_rect = pygame.transform.scale(self.stat_rect, (200, 50))
        self.stat_rect = self.stat_rect.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 + 75*2))
        self.stat_text_rect = self.stat_text.get_rect(center=self.stat_rect.center)

    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene.game_paused = False
            elif self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene._handle_player_death()
            elif self.stat_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game_scene.current_sub_scene = self.game_scene.stat_sub_scene
                self.game_scene.current_sub_scene.on_enter(self.game_scene.game_stats.update(self.game_scene.player, self.game_scene.weapon))

    def update(self):
        """Met à jour la logique de la scène"""
        if self.exit_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.exit_text = self.settings.font["h3"].render("Continuer", True, (255, 255, 255))
            # Met un son uniquement la premiere fois que le curseur passe dessus
            if not hasattr(self, 'exit_hovered') or not self.exit_hovered:
                self.exit_hovered = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.exit_text = self.settings.font["h3"].render("Continuer", True, (255, 0, 0))
            self.exit_hovered = False

        if self.back_to_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 255, 255))
            # Pareille ici
            if not hasattr(self, 'exit_hovered1') or not self.exit_hovered1:
                self.exit_hovered1 = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.back_to_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
            self.exit_hovered1 = False

        if self.stat_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.stat_text = self.settings.font["h3"].render("Statistiques", True, (255, 255, 255))
            # Et ici aussi
            if not hasattr(self, 'stat_hovered') or not self.stat_hovered:
                self.stat_hovered = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.stat_text = self.settings.font["h3"].render("Statistiques", True, (255, 0, 0))
            self.stat_hovered = False

    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.exit_rect, self.exit_text_rect, self.exit_text, self.back_to_menu_rect, self.back_to_menu_text_rect, self.back_to_menu_text, self.stat_rect, self.stat_text_rect, self.stat_text)

    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        # Met à jour les positions des éléments UI en fonction de la nouvelle taille de l'écran
        self.exit_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 - 75, 200, 50)
        self.exit_text_rect = self.exit_text.get_rect(center=self.exit_rect.center)
        self.back_to_menu_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 37.5, 200, 50)
        self.back_to_menu_text_rect = self.back_to_menu_text.get_rect(center=self.back_to_menu_rect.center)
        self.stat_rect.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 75*2, 200, 50)
        self.stat_text_rect = self.stat_text.get_rect(center=self.stat_rect.center)
        self.ui.resize()
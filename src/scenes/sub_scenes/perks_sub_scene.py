# src/scenes/sub_scenes/perks_sub_scene.py
import pygame
from .base_sub_scene import BaseSubScene
from src.perks.perks_manager import PerksManager
from src.ui.perks_ui import PerksUI


class PerksSubScene(BaseSubScene):
    """Gère le menu de sélection d'améliorations"""
    
    def __init__(self, game, game_scene, settings, player, weapon):
        super().__init__(game, game_scene, settings)
        self.player = player
        self.weapon = weapon
        self.perks_manager = None
        self.perks_list = []
        self.ui = None
        self.perks_rect = []

    def on_enter(self):
        """Appelée quand la scène devient active"""
        super().on_enter()
        self.ui = PerksUI(self.settings)
        self.perks_manager = PerksManager(self.settings, self.player, self.weapon)
        self.perks_list = self.perks_manager.get_perks()
        
        # Calculer les rectangles une seule fois ici
        self._calculate_rectangles()
        
        # Debug
        print(f"[PERKS] Menu ouvert avec {len(self.perks_list)} perks")
        for i, perk in enumerate(self.perks_list):
            print(f"[PERKS] Option {i+1}: {perk}")
    
    def _calculate_rectangles(self):
        """Calcule les rectangles des boutons perks"""
        # Rect des 3 cases de perks
        images_rect = (
            pygame.Rect(
                int(self.settings.screen_width * 0.15),
                int(self.settings.screen_height * 0.3),
                int(self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2)
            ),
            pygame.Rect(
                int(self.settings.screen_width * 0.4),
                int(self.settings.screen_height * 0.3),
                int(self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2)
            ),
            pygame.Rect(
                int(self.settings.screen_width * 0.65),
                int(self.settings.screen_height * 0.3),
                int(self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2)
            )
        )
        
        text_rect = (
            pygame.Rect(
                int(self.settings.screen_width * 0.15),
                int(self.settings.screen_height * 0.3 + self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2),
                50
            ),
            pygame.Rect(
                int(self.settings.screen_width * 0.4),
                int(self.settings.screen_height * 0.3 + self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2),
                50
            ),
            pygame.Rect(
                int(self.settings.screen_width * 0.65),
                int(self.settings.screen_height * 0.3 + self.settings.screen_width * 0.2),
                int(self.settings.screen_width * 0.2),
                50
            )
        )
        
        # ((Rect de l'image, Rect du texte, union des 2), ...)
        self.perks_rect = (
            (
                images_rect[0],
                text_rect[0],
                pygame.Rect.union(images_rect[0], text_rect[0])
            ),
            (
                images_rect[1],
                text_rect[1],
                pygame.Rect.union(images_rect[1], text_rect[1])
            ),
            (
                images_rect[2],
                text_rect[2],
                pygame.Rect.union(images_rect[2], text_rect[2])
            )
        )
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        self.game_scene.game_paused = False
        self.game_scene.current_sub_scene = None
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche seulement
            # Convertir les coordonnées de la souris en coordonnées de la surface de jeu
            mouse_x = event.pos[0] - self.settings.x0
            mouse_y = event.pos[1] - self.settings.y0
            
            print(f"[PERKS] Clic à: {mouse_x}, {mouse_y}")
            
            # Vérifier chaque bouton
            for i, (_, _, union_rect) in enumerate(self.perks_rect):
                if union_rect.collidepoint(mouse_x, mouse_y):
                    print(f"[PERKS] Bouton {i+1} cliqué: {self.perks_list[i]}")
                    self.perks_manager.choose_perk(self.perks_list[i])
                    self.on_exit()
                    return  # Sortir après avoir traité le clic
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.perks_rect, self.perks_list)
    
    def resize(self):
        """Appelé lorsque la fenêtre change de taille"""
        self._calculate_rectangles()
        if self.ui:
            self.ui.resize()
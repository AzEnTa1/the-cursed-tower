import pygame
from .base_sub_scene import BaseSubScene
from src.perks.perks_manager import PerksManager
from src.ui.perks_ui import PerksUI


class PerksSubScene(BaseSubScene):
    """gere le menu de selection d'améliorations""" # Perks et Pause
    
    def __init__(self, game, game_scene, settings, player, weapon):
        super().__init__(game, game_scene, settings)
        self.player = player
        self.weapon = weapon

    def on_enter(self):
        """Appelée quand la scène devient active"""
        self.ui = PerksUI(self.settings)
        self.perks_manager = PerksManager(self.settings, self.player, self.weapon)
        self.perks_list = self.perks_manager.get_perks()
        self.perks_rect = ()
        self.resize()
        
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        self.game_scene.game_paused = False
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.perks_rect[0][2].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[0])
                self.on_exit()
            elif self.perks_rect[1][2].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[1])
                self.on_exit()
            elif self.perks_rect[2][2].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[2])
                self.on_exit()
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen, self.perks_rect, self.perks_list)

    def resize(self):
        """appelé lorsque la fenêtre change de taille"""
        #height et width sont les vraie dimension de la fenetre
        #!= self.settings.screen_height/width qui sont les dimension de la fenetre interne 4:3
        #permet de diminué les calcules fait en permanance pour dessiner les élements
        #|-> surement inutils
        
        # Rect des 3 cases de perks
        images_rect = (
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.15, self.settings.y0 + self.settings.screen_height*0.3, self.settings.screen_width*0.2, self.settings.screen_width*0.2),
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.4, self.settings.y0 + self.settings.screen_height*0.3, self.settings.screen_width*0.2, self.settings.screen_width*0.2),
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.65, self.settings.y0 + self.settings.screen_height*0.3, self.settings.screen_width*0.2, self.settings.screen_width*0.2)
            )
        text_rect = (
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.15, self.settings.y0 + self.settings.screen_height*0.3 + self.settings.screen_width*0.2, self.settings.screen_width*0.2, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.4, self.settings.y0 + self.settings.screen_height*0.3 + self.settings.screen_width*0.2, self.settings.screen_width*0.2, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width*0.65, self.settings.y0 + self.settings.screen_height*0.3 + self.settings.screen_width*0.2, self.settings.screen_width*0.2, 50)
        )
        #((Rect de l'image, Rect du texte, union des 2), ...)

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
        self.ui.resize()
        
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
        self.perks_rect = (
            pygame.Rect(self.settings.x0, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width//3, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width//3*2, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50)
        )
        self.perks_list = self.perks_manager.get_perks()

    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        self.game_scene.game_paused = False
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.perks_rect[0].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[0])
                self.on_exit()
            elif self.perks_rect[1].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[1])
                self.on_exit()
            elif self.perks_rect[2].collidepoint(event.pos):
                self.perks_manager.choose_perk(self.perks_list[2])
                self.on_exit()
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        self.ui.draw(screen)
        
        for rect, perk in zip(self.perks_rect, self.perks_list):
            txt = pygame.font.Font(None, 24).render(perk, True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255, 0), rect.inflate(-5, -5))
            screen.blit(txt, txt.get_rect(center=rect.center))


    def resize(self, height, width):
        """appelé lorsque la fenêtre change de taille"""
        #height et width sont les vraie dimension de la fenetre
        #!= self.settings.screen_height/width qui sont les dimension de la fenetre interne 4:3
        #permet de diminué les calcules fait en permanance pour dessiner les élements
        #|-> surement inutils
        self.perks_rect = (
            pygame.Rect(self.settings.x0, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width//3, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50),
            pygame.Rect(self.settings.x0 + self.settings.screen_width//3*2, self.settings.y0 + self.settings.screen_height//2 - 25, self.settings.screen_width//3, 50)
        )
        
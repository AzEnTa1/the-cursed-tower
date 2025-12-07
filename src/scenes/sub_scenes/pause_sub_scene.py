import pygame
from .base_sub_scene import BaseSubScene

class PauseSubScene(BaseSubScene):
    """gere le menu pause""" # Perks et Pause
    
    def __init__(self, game, settings):
        super().__init__(game, settings)
    
    def on_enter(self):
        """Appelée quand la scène devient active"""
        pass
    
    def on_exit(self):
        """Appelée quand la scène n'est plus active"""
        pass
    
    def handle_event(self, event):
        """Gère les événements pygame"""
        if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.change_scene(self.settings.SCENE_MENU)
                #if self.play_button.collidepoint(event.pos):
    
    def update(self):
        """Met à jour la logique de la scène"""
        pass
    
    def draw(self, screen):
        """Dessine la scène"""
        menu_rect = pygame.Rect(self.settings.x0 + 100, self.settings.y0 + 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
        pygame.draw.rect(screen, (255, 255, 0, 0), menu_rect)
        txt = pygame.font.Font(None, 24).render("cliquer pour quiter echap pour retourner au jeu", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=menu_rect.center)
        screen.blit(txt, rnd_rect)

    def resize(self, height, width):
        """appelé lorsque la fenêtre change de taille"""
        #height et width sont les vraie dimension de la fenetre
        #!= self.settings.screen_height/width qui sont les dimension de la fenetre interne 4:3
        #permet de diminué les calcules fait en permanance pour dessiner les élements
        #|-> surement inutils
        pass
        
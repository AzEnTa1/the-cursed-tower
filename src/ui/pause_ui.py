# src/ui/pause_ui
import pygame

class PauseUI:
    def __init__(self, settings):
        self.settings = settings
        self.menu_rect = pygame.Rect(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)


    def draw(self, screen, exit_rect, back_to_menu_rect):
        """dessine l'interface complète"""
        #créer une surface qui accepte de modifier le alpha
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        pygame.draw.rect(overlay, (100, 100, 100, 240), self.menu_rect)
        screen.blit(overlay, (0, 0))

        txt = self.settings.font["h3"].render("Cliquer pour quitter, ECHAP pour retourner au jeu", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=self.menu_rect.center)
        screen.blit(txt, rnd_rect)

        pygame.draw.rect(screen, (255, 0, 0), back_to_menu_rect)
        pygame.draw.rect(screen, (250, 110, 20), exit_rect)


    def resize(self):
        self.menu_rect.update(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
        
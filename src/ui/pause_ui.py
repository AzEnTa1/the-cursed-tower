import pygame

class PauseUI:
    def __init__(self, settings):
        self.settings = settings
        self.menu_rect = None

    def draw(self, screen, exit_rect, back_to_menu_rect):
        """dessine l'interface complète"""
        
        pygame.draw.rect(screen, (100, 100, 100, 0), self.menu_rect)
        txt = pygame.font.Font(None, 24).render("Cliquer pour quitter, ECHAP pour retourner au jeu", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=self.menu_rect.center)
        screen.blit(txt, rnd_rect)

        pygame.draw.rect(screen, (255, 0, 0), back_to_menu_rect)
        pygame.draw.rect(screen, (250, 110, 20), exit_rect)


    def resize(self):
        self.menu_rect = pygame.Rect(self.settings.x0 + 100, self.settings.y0 + 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
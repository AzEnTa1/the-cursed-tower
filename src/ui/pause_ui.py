import pygame

class PauseUI:
    def __init__(self, settings):

        self.settings = settings

    def draw(self, screen):
        """dessine l'interface complète"""
        menu_rect = pygame.Rect(self.settings.x0 + 100, self.settings.y0 + 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
        pygame.draw.rect(screen, (100, 100, 100, 0), menu_rect)
        txt = pygame.font.Font(None, 24).render("Cliquer pour quitter, ECHAP pour retourner au jeu", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=menu_rect.center)
        screen.blit(txt, rnd_rect)
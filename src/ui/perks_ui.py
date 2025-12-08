import pygame

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        self.menu_rect = pygame.Rect(self.settings.x0 + 100, self.settings.y0 + 50, self.settings.screen_width - 200, self.settings.screen_height - 100)


    def draw(self, screen):
        """dessine l'interface complète"""
        self._draw_background(screen)

    def _draw_background(self, screen):
        """dessine le background"""
        pygame.draw.rect(screen, (255, 255, 0, 0), self.menu_rect)
        txt = pygame.font.Font(None, 24).render("affichage perks", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=self.menu_rect.center)
        screen.blit(txt, rnd_rect)

    def resize(self, width, height):
        """redéfini la taille de chaque éléments"""
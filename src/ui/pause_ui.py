# src/ui/pause_ui
import pygame

class PauseUI:
    def __init__(self, settings):
        self.settings = settings
        self.menu_rect = pygame.Rect(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)


    def draw(self, screen, exit_rect, exit_text_rect, exit_text, back_to_menu_rect, back_to_menu_text_rect, back_to_menu_text):
        """dessine l'interface complète"""
        #créer une surface qui accepte de modifier le alpha
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        pygame.draw.rect(overlay, (100, 100, 100, 240), self.menu_rect)
        screen.blit(overlay, (0, 0))

        #met une image de fond
        bg_image = pygame.image.load(r"assets/images/Menu_pause.png")
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))

        #met le bouton quitter
        bg_image = pygame.image.load(r"assets/images/Fd_perks.png")
        bg_image = pygame.transform.scale(bg_image, (exit_rect.width, exit_rect.height))
        screen.blit(bg_image, exit_rect)
        screen.blit(exit_text, exit_text_rect)
        #met le bouton menu
        bg_image = pygame.image.load(r"assets/images/Fd_perks.png")
        bg_image = pygame.transform.scale(bg_image, (back_to_menu_rect.width, back_to_menu_rect.height))
        screen.blit(bg_image, back_to_menu_rect)
        screen.blit(back_to_menu_text, back_to_menu_text_rect)

    def resize(self):

        self.menu_rect.update(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
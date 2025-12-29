# src/ui/game_over_ui
import pygame

class GameOverUI:
    def __init__(self, settings, game_stats):
        self.settings = settings
        self.game_stats = game_stats
        
        self.stats_rect = pygame.Rect(self.settings.screen_width*0.1, self.settings.screen_height*0.1, self.settings.screen_width*0.8, self.settings.screen_height*0.8)

        self.stats_text = self.settings.font["h1"].render(f"Score :{self.game_stats["score"]}", True, (250, 0, 0))
        self.stats_text_rect = self.stats_text.get_rect(center=(self.stats_rect.center[0], self.settings.screen_height*0.15))

    def draw(self, screen, quit_button, quit_rect, quit_text):
        """dessine l'interface complète"""
        #met une image de fond
        bg_image = pygame.image.load(r"assets/images/Death_menu.png")        
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))
        screen.blit(self.stats_text, self.stats_text_rect)
        #dessine le bouton quitter
        bg_image2 = pygame.image.load(r"assets/images/Fd_perks.png")
        bg_image2 = pygame.transform.scale(bg_image2, (quit_button.width, quit_button.height))
        screen.blit(bg_image2, quit_button)
        screen.blit(quit_text, quit_rect)
        

    def resize(self):
        self.stats_rect.update(self.settings.screen_width*0.1, self.settings.screen_height*0.1, self.settings.screen_width*0.8, self.settings.screen_height*0.8)
        self.stats_text_rect = self.stats_text.get_rect(center=(self.stats_rect.center[0], self.settings.screen_height*0.15))
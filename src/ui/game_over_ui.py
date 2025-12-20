import pygame

class GameOverUI:
    def __init__(self, settings, game_stats):
        self.settings = settings
        self.game_stats = game_stats
        

        
        self.stats_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.1 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.8)

        self.stats_text = self.settings.font.render(f"Score :{self.game_stats.player.score}", True, (0, 0, 0))
        self.stats_text_rect = self.stats_text.get_rect(center=(self.stats_rect.center[0], self.settings.y0 + self.settings.screen_height*0.15))

    def draw(self, screen, quit_button, quit_rect, quit_text):
        """dessine l'interface complète"""
        screen.fill((100, 100, 100))

        pygame.draw.rect(screen, (255, 0, 255), self.stats_rect)
        screen.blit(self.stats_text, self.stats_text_rect)

        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        screen.blit(quit_text, quit_rect)
        


    def resize(self):
        self.stats_rect = pygame.Rect(self.settings.screen_width*0.1 + self.settings.x0, self.settings.screen_height*0.1 + self.settings.y0, self.settings.screen_width*0.8, self.settings.screen_height*0.8)
        self.stats_text_rect = self.stats_text.get_rect(center=(self.stats_rect.center[0], self.settings.y0 + self.settings.screen_height*0.15))
# src/ui/pause_ui
import pygame

class PauseUI:
    def __init__(self, game_stats:dict, settings):
        self.settings = settings
        self.game_stats = game_stats
        
        # Rect des stats et surface qui accepte de modifier l'alpha
        self.stats_rect = pygame.Rect(50, 20, self.settings.screen_width//2 - 50, self.settings.screen_height - 40)


    def draw(self, screen, exit_rect, exit_text_rect, exit_text, back_to_menu_rect, back_to_menu_text_rect, back_to_menu_text, stat_rect, stat_text_rect, stat_text):
        """dessine l'interface complète 
        importer les rect utils dans la logique de pause_sub_scene et draw ici
        """        

        # Met une image de fond
        bg_image = pygame.image.load(r"assets/images/background/pause_scene.png")
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))

        

        # Met le bouton quitter
        bg_image = pygame.image.load(r"assets/images/cadre.png")
        bg_image = pygame.transform.scale(bg_image, (exit_rect.width, exit_rect.height))
        screen.blit(bg_image, exit_rect)
        screen.blit(exit_text, exit_text_rect)

        # Met le bouton menu
        bg_image = pygame.image.load(r"assets/images/cadre.png")
        bg_image = pygame.transform.scale(bg_image, (back_to_menu_rect.width, back_to_menu_rect.height))
        screen.blit(bg_image, back_to_menu_rect)
        screen.blit(back_to_menu_text, back_to_menu_text_rect)   

        # Met les stats #
        bg_image = pygame.image.load(r"assets/images/cadre.png")
        bg_image = pygame.transform.scale(bg_image, (stat_rect.width, stat_rect.height))
        screen.blit(bg_image, stat_rect)
        screen.blit(stat_text, stat_text_rect)     


    def resize(self):
        self.stats_rect.update(50, 20, self.settings.screen_width//2 - 50, self.settings.screen_height - 40)
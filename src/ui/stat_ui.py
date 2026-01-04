# src/ui/pause_ui
import pygame

class StatUI:
    def __init__(self, game_stats:dict, settings):
        self.settings = settings
        self.game_stats = game_stats
        # Rect des stats et surface qui accepte de modifier l'alpha
        self.stats_rect = pygame.Rect(50, 20, self.settings.screen_width//2-60, self.settings.screen_height-300)
        self.bg_image1 = pygame.image.load(r"assets/images/cadre.png")
        self.bg_image1 = pygame.transform.scale(self.bg_image1, (self.stats_rect.width, self.stats_rect.height))
        

    def draw(self, screen, exit_rect, exit_text_rect, exit_text):
        """dessine l'interface complète 
        importer les rect utils dans la logique de pause_sub_scene et draw ici
        """        
        # Met une image de fond
        bg_image = pygame.image.load(r"assets/images/background/stat_scene.png")
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))

        # Crée le cadre des stats
        self.bg_image1.set_alpha()
        self.bg_image1.get_rect(center = (self.settings.screen_width//2, self.settings.screen_height//2))
        self.stats_rect.y = self.settings.screen_height//2 - self.stats_rect.height//2
        self.stats_rect.x = self.settings.screen_width//2 - self.stats_rect.width//2
        screen.blit(self.bg_image1, self.stats_rect)
        
        i = 0
        for key in self.game_stats.keys():
            i += 1
            txt = self.settings.font["h4"].render(f"{self.settings.data_translation_map.get(key, str(key))}: {self.game_stats[key]}", True, (255, 255, 255))
            rect = txt.get_rect(topleft = (self.stats_rect[0] + 5, self.stats_rect[1] + 20*i + 5))
            rect.center = (self.settings.screen_width//2, self.settings.screen_height//1.5 - 20*i)
            screen.blit(txt, rect)

        bg_image = pygame.image.load(r"assets/images/cadre.png")
        bg_image = pygame.transform.scale(bg_image, (exit_rect.width, exit_rect.height))
        screen.blit(bg_image, exit_rect)
        screen.blit(exit_text, exit_text_rect)

    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.stats_rect.update(50, 20, self.settings.screen_width//2 - 60, self.settings.screen_height -300)
        self.bg_image1 = pygame.transform.scale(self.bg_image1, (self.stats_rect.width, self.stats_rect.height))

        

        
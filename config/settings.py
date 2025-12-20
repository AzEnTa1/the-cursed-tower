# config/settings.py
import pygame

class Settings:
    def __init__(self):
        # CONFIGURATION GÉNÉRALE
        self.screen_width = 800
        self.screen_height = 600
        self.x0 = 0
        self.y0 = 0
        self.fps = 60
        self.title = "Tour Maudite"

        # COULEURS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE =  (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # JOUEUR
        self.player_speed = 5
        self.player_size = 20

        # SCÈNES
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"
        self.SCENE_GAME_OVER = "game_over"

        # FONTS
        self.font = {
            "h1":pygame.font.Font(None, 48),
            "h2":pygame.font.Font(None, 36),
            "h3":pygame.font.Font(None, 24),
            "h4":pygame.font.Font(None, 18)
        }

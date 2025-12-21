import pygame

class Settings:
    def __init__(self):
        # Configurations générales
        self.screen_width = 800
        self.screen_height = 600
        self.x0 = 0
        self.y0 = 0
        self.fps = 60
        self.title = "Tour Maudite"

        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE =  (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # Joueur
        self.player_speed = 5
        self.player_size = 20

        # Scènes
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"
        self.SCENE_GAME_OVER = "game_over"

        # Fonts
        self.font = None

        self.BORDER_COLOR = (50, 50, 50)  # Couleur de la bordure
        self.ASPECT_RATIO = (4, 3)        # Ratio largeur:hauteur
        self.BORDER_WIDTH = 2             # Largeur de la bordure
    
    def initialize_fonts(self):
        """Initialise les fonts"""
        self.font = {
            "h1": pygame.font.Font(None, 48),
            "h2": pygame.font.Font(None, 36),
            "h3": pygame.font.Font(None, 24),
            "h4": pygame.font.Font(None, 18)
        }


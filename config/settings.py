# config/settings.py
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
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # Joueur
        self.player_speed = 5
        self.player_size = 20
        self.player_health = 100

        # Scènes
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"
        self.SCENE_GAME_OVER = "game_over"

        # Armes
        self.WEAPON_DAMAGE = 30
        self.WEAPON_FIRE_RATE = 2  # tirs par seconde
        self.WEAPON_PROJECTILE_SPEED = 10
        self.WEAPON_DAMAGE_VARIANCE = 5  # ± pour les dégâts aléatoires
        
        # Multishot
        self.WEAPON_SHOT_INTERVAL = 100  # ms entre chaque projectile du multishot
        self.WEAPON_STATIONARY_THRESHOLD = 25  # frames d'immobilité avant tir
        self.WEAPON_TARGETING_RANGE = 500  # distance maximale pour cibler un ennemi
        self.WEAPON_ARC_ANGLE = 15  # degrés pour le tir en arc
        
        # Couleurs pour les multishots
        self.WEAPON_MULTISHOT_COLORS = [
            (255, 100, 100),  # Rouge
            (100, 255, 100),  # Vert
            (100, 100, 255),  # Bleu
            (255, 255, 100),  # Jaune
            (255, 100, 255),  # Magenta
            (100, 255, 255)   # Cyan
        ]
        
        # Couleurs pour les tirs en arc
        self.WEAPON_ARC_COLORS = [
            (255, 255, 0),    # Jaune pour le centre
            (255, 150, 0),    # Orange pour la gauche
            (255, 200, 0)     # Jaune-orange pour la droite
        ]

        # Fonts
        self.font = None

        # Bordures et ratio
        self.BORDER_COLOR = (50, 50, 50)  # Couleur de la bordure
        self.ASPECT_RATIO = (4, 3)        # Ratio largeur:hauteur
        self.BORDER_WIDTH = 2             # Largeur de la bordure
    
    def initialize_fonts(self):
        """Initialise les fonts"""
        self.font = {
            "h1": pygame.font.Font(None, 48),
            "h2": pygame.font.Font(None, 36),
            "h3": pygame.font.Font(None, 24),
            "h4": pygame.font.Font(None, 18),
            "main_menu": pygame.font.SysFont(None, 60)
        }
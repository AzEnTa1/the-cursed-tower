import pygame
import json
import os

class Settings:
    def __init__(self, player_data):
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

        self.ICON_PATH = "assets/images/icon.png"
        self.PLAYER_DATA_PATH = "data/player_data.json"
        self.SOUND_START_PATH = "assets/sounds/game_start.mp3"

        # Joueur
        self.player_speed = player_data.get("speed", 5)
        self.player_size = player_data.get("size", 20)
        self.player_health = player_data.get("max_health", 100)
        
        # Scènes
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"
        self.SCENE_GAME_OVER = "game_over"
        self.SCENE_TALENTS = "talents"

        # Armes
        self.WEAPON_DAMAGE = player_data.get("base_damages", 30)
        self.WEAPON_FIRE_RATE = player_data.get("fire_rate", 2)
        self.WEAPON_PROJECTILE_SPEED = player_data.get("projectile_speed", 10)
        self.WEAPON_DAMAGE_VARIANCE = player_data.get("damage_variance", 5)
        
        # Multishot
        self.WEAPON_SHOT_INTERVAL = 100
        self.WEAPON_STATIONARY_THRESHOLD = player_data.get("stationary_threshold", 25)
        self.WEAPON_TARGETING_RANGE = 500
        self.WEAPON_ARC_ANGLE = 15
        
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
        self.BORDER_COLOR = (50, 50, 50)
        self.ASPECT_RATIO = (4, 3)
        self.BORDER_WIDTH = 2
    
    def initialize_fonts(self):
        """Initialise les fonts"""
        self.font = {
            "h1": pygame.font.Font(None, 48),
            "h2": pygame.font.Font(None, 36),
            "h3": pygame.font.Font(None, 24),
            "h4": pygame.font.Font(None, 18),
            "main_menu": pygame.font.SysFont(None, 60),
            
        }
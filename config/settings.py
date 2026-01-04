# config/settings.py
import pygame

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

        # Joueur
        self.player_speed = player_data.get("player_speed", 5)
        self.player_size = player_data.get("player_size", 20)
        self.player_health = player_data.get("max_health", 100)
        self.player_regen_power = player_data.get("regen_power", 0.1)
        self.player_data = player_data
        
        # Scènes
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"
        self.SCENE_GAME_OVER = "game_over"
        self.SCENE_TALENTS = "talents"

        # Armes
        self.WEAPON_DAMAGE = player_data.get("attack_damages", 30)
        self.WEAPON_FIRE_RATE = player_data.get("attack_speed", 2)
        self.WEAPON_PROJECTILE_SPEED = player_data.get("projectile_speed", 10)
        self.WEAPON_DAMAGE_VARIANCE = 5
        
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

        self.master_volume = player_data["master_volume"]
        # Si certains sons on un volume différent des autres en permanance 
        # val entre 0.0 et 1.0 au dixième
        self.sounds_volume_map = {
            "boom":0.3,
            "spawn":0.5,
            "Tire_1":0.3,
            "Tire_2":0.3,
            "Tire_3":0.3,
            "Tire_4":0.3
        }
    
    def _init_fonts(self):
        """Initialise les fonts"""
        self.font = {
            "h1": pygame.font.Font(None, 48),
            "h2": pygame.font.Font(None, 36),
            "h3": pygame.font.Font(None, 24),
            "h4": pygame.font.Font(None, 18),
            "main_menu": pygame.font.SysFont(None, 60),
        }

    def _init_sounds(self):
        """Initialise les sons"""
        self.sounds = {
            "boom":pygame.mixer.Sound("assets/sounds/boom.mp3"),
            "coins":pygame.mixer.Sound("assets/sounds/coins.mp3"),
            "degat_1":pygame.mixer.Sound("assets/sounds/degat_1.mp3"),
            "game_over":pygame.mixer.Sound("assets/sounds/game_over.mp3"),
            "game_start":pygame.mixer.Sound("assets/sounds/game_start.mp3"),
            "souris_on_button":pygame.mixer.Sound("assets/sounds/souris_on_button.mp3"),
            "spawn":pygame.mixer.Sound("assets/sounds/spawn.mp3"),
            "Tire_1":pygame.mixer.Sound("assets/sounds/Tire_1.mp3"),
            "Tire_2":pygame.mixer.Sound("assets/sounds/Tire_2.mp3"),
            "Tire_3":pygame.mixer.Sound("assets/sounds/Tire_3.mp3"),
            "Tire_4":pygame.mixer.Sound("assets/sounds/Tire_4.mp3"),
            "mort_enemy":pygame.mixer.Sound("assets/sounds/mort_enemy.mp3")
        }

    def update_master_volume(self, val=0):
        self.master_volume += val
        self.master_volume = round(max(0, min(1, self.master_volume)), 2)
        self.player_data["master_volume"] = self.master_volume

        pygame.mixer.music.set_volume(self.master_volume)
        for key in self.sounds.keys():
            self.sounds[key].set_volume(self.master_volume * self.sounds_volume_map.get(key, 1))

    def update_player_data(self, player_data):
        # Joueur
        self.player_speed = player_data.get("player_speed", 5)
        self.player_size = player_data.get("player_size", 20)
        self.player_health = player_data.get("max_health", 100)
        self.player_data = player_data
        
        # Armes
        self.WEAPON_DAMAGE = player_data.get("attack_damages", 30)
        self.WEAPON_FIRE_RATE = player_data.get("attack_speed", 2)
        self.WEAPON_PROJECTILE_SPEED = player_data.get("projectile_speed", 10)
        self.WEAPON_STATIONARY_THRESHOLD = player_data.get("stationary_threshold", 25)

        # Volume
        self.master_volume = player_data["master_volume"]

    def cleanup(self):
        """Nettoie les ressources audio"""
        # Arrêter tous les sons
        if hasattr(self, 'sounds'):
            for sound_name, sound in self.sounds.items():
                sound.stop()
        
        # Arrêter la musique de fond (si il y en a)
        pygame.mixer.music.stop()
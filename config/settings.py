# config/settings.py
class Settings:
    def __init__(self):
        # CONFIGURATION GÉNÉRALE
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.title = "Tour Maudite"

        # COULEURS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE =  (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        # JOUEUR
        self.player_speed = 5
        self.player_size = 20

        # SCÈNES
        self.SCENE_MENU = "menu"
        self.SCENE_GAME = "game"

# CONFIGURATION GÉNÉRALE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Tour Maudite"

# COULEURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE =  (255, 0, 0)
YELLOW = (255, 255, 0)

# JOUEUR
PLAYER_SPEED = 20
PLAYER_SIZE = 20

# SCÈNES
SCENE_MENU = "menu"
SCENE_GAME = "game"
test = "exemple"
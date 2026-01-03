import math
from .enemy import Enemy
from config.settings import Settings

class Basic(Enemy):
    """
    Ennemi basique - suit simplement le joueur
    """
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "basic"
        self.speed = 2
        self.health = 30
        self.max_health = 30
        self.damage = 10
        self.color = self.settings.RED
        self.radius = 20
           
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        # Calcul direction vers le joueur
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Déplacement
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Garder l'ennemi dans les limites de l'écran
        self.x = max(self.radius, min(self.x, self.settings.screen_width - self.radius))
        self.y = max(self.radius, min(self.y, self.settings.screen_height - self.radius))
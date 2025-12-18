# src/entities/enemies/charger.py 
import math
from .enemy import Enemy

class Basic(Enemy):
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "basic"
        # Stats de base selon le type
        # enemy basic
        self.speed = 2
        self.health = 30
        self.max_health = 30
        self.damage = 10
        self.color = (255, 0, 0)  # Rouge
        self.radius = 20
        self.attack_range = 0
           
    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed
  
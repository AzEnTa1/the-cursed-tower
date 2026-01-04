# src/entities/enemies/suicide.py 
import pygame
import math
from .enemy import Enemy

class Suicide(Enemy):
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "suicide"
        # Explose au contact
        self.speed = 4
        self.health = 15
        self.max_health = 15
        self.damage = 30  # Dégâts élevés à l'explosion
        self.color = (255, 0, 255)  # Magenta
        self.radius = 16
        self.attack_range = 0
        self.explosion_radius = 60
        self.is_exploding = False
        self.explosion_timer = 0
    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        if self.is_exploding:
            self.explosion_timer -= 1
            return
        
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Se déplace vers le joueur
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Vérifie s'il est assez proche pour exploser
        if distance < 50:
            self.is_exploding = True
            self.explosion_timer = 15
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        super().draw(screen)

        # Effet d'explosion pour les suicides
        if self.is_exploding:
            explosion_size = self.radius + (15 - self.explosion_timer) * 6
            pygame.draw.circle(screen, (255, 150, 0), (int(self.x), int(self.y)), explosion_size, 3)
        
        # met un son une seul fois quand il explose
        if self.is_exploding and self.explosion_timer == 15:
            self.settings.sounds["boom"].play()

        # Indicateur de type (cercle intérieur ou motif)
        
        pygame.draw.circle(screen, (200, 0, 200), (int(self.x), int(self.y)), self.radius - 6)
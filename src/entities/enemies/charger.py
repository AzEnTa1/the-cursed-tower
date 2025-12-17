# src/entities/enemies/charger.py 
import pygame
import math
from .enemy import Enemy

class Charger(Enemy):
    def __init__(self, x, y, settings):
        super().__init__(self, x, y, settings)
        
        # Stats de base selon le type

        # Cours rapidement vers le joueur
        self.speed = 3
        self.health = 40
        self.max_health = 40
        self.damage = 15
        self.color = (255, 255, 0)  # Jaune
        self.radius = 22
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
    

    
    def draw(self, screen): #global pour enemies
        """Dessine l'ennemi avec sa barre de vie"""
        super().draw(self, screen)

        # Indicateur de type (cercle intérieur ou motif)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius - 8)       
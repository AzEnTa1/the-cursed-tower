# src/entities/enemys/shooter.py 
import pygame
import math
from .enemy import Enemy
from ..projectiles import Projectile

class Shooter(Enemy):
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "shooter"
        # Stats de base selon le type

        # Tire des projectiles
        self.speed = 1.5
        self.health = 25
        self.max_health = 25
        self.damage = 8
        self.color = (100, 100, 255)  # Bleu
        self.radius = 18
        self.attack_range = 300  
        self.shoot_cooldown = 0
        self.shoot_rate = 60 
        
    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        if distance > self.attack_range:
            # Trop loin, avance vers le joueur
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        elif distance < self.attack_range - 100:
            # Trop proche, recule
            self.x -= (dx / distance) * self.speed
            self.y -= (dy / distance) * self.speed
        
        # Condition de tir
        can_shoot = (distance <= self.attack_range and 
                    distance >= self.attack_range - 150)
        
        if self.shoot_cooldown <= 0 and can_shoot:
            self.shoot(dx, dy, projectiles)
            self.shoot_cooldown = self.shoot_rate
        elif self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    
    def shoot(self, dx, dy, projectiles):
        """Tire un projectile vers le joueur (pour shooter)"""
        if projectiles is None:
            return
            
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        projectiles.append(Projectile(
            self.x, self.y,
            dx * 7,
            dy * 7,
            self.damage,
            self.settings,
            color=(100, 200, 255)
        ))
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        super().draw(screen)
        
        pygame.draw.circle(screen, (50, 50, 255), (int(self.x), int(self.y)), self.radius - 8)
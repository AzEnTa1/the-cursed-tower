# src/entities/enemies/destructeur.py 
import pygame
import math
from .enemy import Enemy
from ..projectiles import Projectile

class Destructeur(Enemy):
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "destructeur"
        # Mini-boss : Tire une salve circulaire
        self.speed = 1.2  
        self.health = 150
        self.max_health = 150
        self.damage = 15
        self.color = (255, 100, 100)  # Rouge clair
        self.radius = 35  # Plus gros que les autres
        self.attack_range = 400  # Portée augmentée
        
        # Système de tir circulaire
        self.shoot_cooldown = 0
        self.shoot_rate = 120  # 2 secondes entre les tirs
        self.projectile_speed = 5
        self.projectile_count = 12  # Nombre de projectiles dans le cercle
        self.last_shot_time = 0

    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        if projectiles is None:
            return
            
        # 1. DÉPLACEMENT vers le joueur
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Se déplace vers le joueur s'il est trop loin
        if distance > self.attack_range * 0.125:
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            self.x += norm_dx * self.speed
            self.y += norm_dy * self.speed
        
        # 2. GESTION DES TIRS
        # Cooldown entre les tirs
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Tire un cercle de projectiles quand le joueur est à portée
        if (distance <= self.attack_range and 
            self.shoot_cooldown <= 0):
            
            self.shoot_circle(projectiles)
            self.shoot_cooldown = self.shoot_rate
    
    def shoot_circle(self, projectiles):
        """Mini-boss : Tire un cercle complet de projectiles dans toutes les directions"""
        angle_step = 2 * math.pi / self.projectile_count
        
        for i in range(self.projectile_count):
            angle = i * angle_step
            dx = math.cos(angle) * self.projectile_speed
            dy = math.sin(angle) * self.projectile_speed
            
            # Couleur qui varie selon la direction
            color_ratio = i / self.projectile_count
            r = int(200 + 55 * math.sin(color_ratio * 2 * math.pi))
            g = int(100 + 55 * math.cos(color_ratio * 2 * math.pi))
            b = int(100 + 55 * math.sin(color_ratio * 3 * math.pi))
            
            projectiles.append(Projectile(
                self.x, self.y,
                dx,
                dy,
                self.damage,
                self.settings,
                color=(r, g, b, 220),  # Légèrement transparent
                radius=7  # Projectile légèrement plus gros
            ))
    

    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        super().draw(screen)
        
        # Mini-boss 
        points = []
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            inner_radius = self.radius - 10
            if i % 2 == 0:
                inner_radius = self.radius - 5
            points.append((
                int(self.x + inner_radius * math.cos(angle)),
                int(self.y + inner_radius * math.sin(angle))
            ))
        pygame.draw.polygon(screen, (255, 200, 200), points)
        
    
    def _draw_health_bar(self, screen):
        """Dessine la barre de vie de l'ennemi"""
        super()._draw_health_bar(screen, 50, 8, -15)

        if self.type == "destructeur":
            # Pulsation rouge quand en basse vie
            if self.health < self.max_health * 0.5:
                pulse = int(20 * (1 + math.sin(pygame.time.get_ticks() * 0.008)))
                pygame.draw.circle(screen, (255, 50, 50, 150), 
                                 (int(self.x), int(self.y)), 
                                 self.radius + pulse, 3)
            
            # Aura permanente pour montrer que c'est un mini-boss
            aura_size = self.radius + 5
            pygame.draw.circle(screen, (255, 100, 100, 100), 
                             (int(self.x), int(self.y)), 
                             aura_size, 2)
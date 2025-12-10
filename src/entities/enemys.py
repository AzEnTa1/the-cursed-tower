# src/entities/enemys.py 
import pygame
import math
from .projectiles import Projectile

class Enemy:
    def __init__(self, x, y, settings, enemy_type="basic"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.settings = settings
        
        # Stats de base selon le type
        if enemy_type == "charger":
            # Cours rapidement vers le joueur
            self.speed = 3
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.color = (255, 255, 0)  # Jaune
            self.radius = 22
            self.attack_range = 0
            
        elif enemy_type == "shooter":
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
            
        elif enemy_type == "suicide":
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
            
        elif enemy_type == "destructeur":
            # Mini-boss : Tire une salve circulaire
            self.speed = 1.2  
            self.health = 200
            self.max_health = 200
            self.damage = 15
            self.color = (255, 100, 100)  # Rouge clair
            self.radius = 35  # Plus gros que les autres
            self.attack_range = 400  # Portée augmentée
            
            # Système de tir circulaire # avec la méthode shooot_circle
            self.shoot_cooldown = 0
            self.shoot_rate = 180  # 3 secondes entre les tirs
            self.projectile_speed = 5
            self.projectile_count = 12  # Nombre de projectiles dans le cercle
            self.last_shot_time = 0
            
        else:  # Type basique (par défaut)
            self.speed = 2
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.color = (255, 0, 0)  # Rouge
            self.radius = 20
            self.attack_range = 0
    
    def update(self, player, projectiles=None):
        """Met à jour l'ennemi selon son type"""
        if self.type == "charger":
            self._update_charger(player) 
        elif self.type == "shooter":
            self._update_shooter(player, projectiles)
        elif self.type == "suicide":
            self._update_suicide(player)
        elif self.type == "destructeur": 
            self._update_destructeur(player, projectiles)
        else:  # basic
            self._update_basic(player)
    
    def _update_suicide(self, player):
        """Comportement du suicide - court vers le joueur pour exploser"""
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
    
    def _update_basic(self, player):
        """Comportement de base - poursuite simple"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def _update_charger(self, player):
        """Charge rapidement vers le joueur"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def _update_shooter(self, player, projectiles):
        """Se déplace et tire des projectiles"""
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
    
    def _update_destructeur(self, player, projectiles):
        """Mini-boss : Se déplace lentement et tire un cercle de projectiles"""
        # déplacement vers le joueur (comme pour les autres)
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Se déplace vers le joueur s'il est trop loin (théorique vu que j'ai mis 0.0125)
        if distance > self.attack_range * 0.125:
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            self.x += norm_dx * self.speed
            self.y += norm_dy * self.speed
        
        # Tir de projectiles
        if projectiles is None:
            return
        
        # Cooldown entre les tirs
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Tire un cercle de projectiles quand le joueur est à portée
        if (distance <= self.attack_range and 
            self.shoot_cooldown <= 0):
            
            self.shoot_circle(projectiles)
            self.shoot_cooldown = self.shoot_rate
    
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
    
    def take_damage(self, amount):
        """Inflige des dégâts à l'ennemi"""
        self.health -= amount
        return self.health <= 0
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        # Effet d'explosion pour les suicides
        if self.type == "suicide" and self.is_exploding:
            explosion_size = self.radius + (15 - self.explosion_timer) * 6
            pygame.draw.circle(screen, (255, 150, 0), (int(self.x), int(self.y)), explosion_size, 3)
        
        # Corps de l'ennemi
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Indicateur de type (cercle intérieur ou motif)
        if self.type == "charger":
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius - 8)
        elif self.type == "shooter":
            pygame.draw.circle(screen, (50, 50, 255), (int(self.x), int(self.y)), self.radius - 8)
        elif self.type == "suicide":
            pygame.draw.circle(screen, (200, 0, 200), (int(self.x), int(self.y)), self.radius - 6)
        elif self.type == "destructeur":
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
        
        # Barre de vie (plus grande pour le mini-boss)
        bar_width = 50 if self.type == "destructeur" else 40
        bar_height = 8 if self.type == "destructeur" else 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 15 if self.type == "destructeur" else self.y - self.radius - 10
        
        # Fond de la barre
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Vie actuelle
        health_width = (self.health / self.max_health) * bar_width
        if self.health > self.max_health * 0.6:
            health_color = (0, 255, 0)
        elif self.health > self.max_health * 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
            
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Effet spécial pour le destructeur (mini-boss)
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
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
        if enemy_type == "charger":  # Cours sur le joueur
            self.speed = 3
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.color = (255, 255, 255)  # jaune pas clair ni foncé
            self.radius = 22
            self.attack_range = 0
            
        elif enemy_type == "shooter":  # Tire des projectiles
            self.speed = 1.5
            self.health = 25
            self.max_health = 25
            self.damage = 8
            self.color = (100, 100, 255)  # Bleu
            self.radius = 18
            self.attack_range = 300  
            self.shoot_cooldown = 0
            self.shoot_rate = 60 
            
        elif enemy_type == "suicide":  # Nouveau type - explose au contact
            self.speed = 4
            self.health = 15
            self.max_health = 15
            self.damage = 30  # Dégâts élevés à l'explosion
            self.color = (255, 0, 255)  # Magenta
            self.radius = 16
            self.attack_range = 0
            self.explosion_radius = 60  # Zone d'effet de l'explosion
            self.is_exploding = False
            self.explosion_timer = 0
        
        elif enemy_type == "destructeur":
            self.speed = 0.5
            self.health = 200
            self.max_health = 200
            self.damage = 15
            self.color = (255, 255, 255)  # blanc
            self.radius = 30
            self.attack_range = 250
            self.shoot_cooldown = 0
            self.shoot_rate = 120  # 2 secondes entre les tirs
            self.projectile_speed = 5
            self.projectile_count = 5  # Nombre de projectiles par tir
            self.spread_angle = 45  # Angle total de dispersion en degrés
            
        else:  # Type basique (par défaut) # faudrait changer mais trkl
            self.speed = 2
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.color = (255, 0, 0) # Rouge ? je crois
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
        else:
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
        if distance < 50:  # DISTANCE RÉDUITE pour l'explosion
            self.is_exploding = True
            self.explosion_timer = 10
    
    def _update_basic(self, player):
        """Comportement de base - poursuite simple""" # en soit faudrait changer la logique de charger parce que trop similaire a basic
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
        """ Se déplace et tire des projectiles"""
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
        
        # condition de tir
        can_shoot = (distance <= self.attack_range and 
                    distance >= self.attack_range - 150)
        
        if self.shoot_cooldown <= 0 and can_shoot:
            self.shoot(dx, dy, projectiles)
            self.shoot_cooldown = self.shoot_rate
        elif self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def _update_destructeur(self, player, projectiles):
        """Lent mais résistant, tire des gerbes de projectiles"""
        if projectiles is None:  # CORRIGÉ : vérifie seulement si None
            print("DEBUG: destructeur n'a pas de liste de projectiles!")
            return
            
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        print(f"DEBUG: destructeur distance={distance:.1f}, attack_range={self.attack_range}, cooldown={self.shoot_cooldown}")
        
        if self.shoot_cooldown <= 0 and distance <= self.attack_range:
            print("DEBUG: destructeur tire!")
            self.shoot_destructeur(dx, dy, projectiles)
            self.shoot_cooldown = self.shoot_rate
        elif self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self, dx, dy, projectiles):
        """Tire un projectile vers le joueur"""
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
        
    def shoot_destructeur(self, dx, dy, projectiles):
        """Tire une gerbe de projectiles en éventail"""
        if not projectiles:
            return
        
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Angle de base vers le joueur
        base_angle = math.atan2(dy, dx)
        
        # Calcul de l'angle entre chaque projectile
        angle_step = math.radians(self.spread_angle) / (self.projectile_count - 1)
        start_angle = base_angle - math.radians(self.spread_angle) / 2
        
        # Crée chaque projectile
        for i in range(self.projectile_count):
            angle = start_angle + (angle_step * i)
            
            # Calcul de la direction
            proj_dx = math.cos(angle) * self.projectile_speed
            proj_dy = math.sin(angle) * self.projectile_speed
            
            projectiles.append(Projectile(
                self.x, self.y,
                proj_dx,
                proj_dy,
                self.damage,  # Dégâts individuels
                self.settings,
                color=(255, 150, 150),  # Rose clair
                radius=7
            ))
    
    def take_damage(self, amount):
        """Inflige des dégâts à l'ennemi"""
        self.health -= amount
        return self.health <= 0
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        # Effet d'explosion pour les suicides
        if self.type == "suicide" and self.is_exploding:
            # Cercle d'explosion qui grandit
            explosion_size = self.radius + (10 - self.explosion_timer) * 5
            pygame.draw.circle(screen, (255, 150, 0), (int(self.x), int(self.y)), explosion_size, 3)
        
        # Corps de l'ennemi
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Indicateur de type (cercle intérieur)
        if self.type == "charger":
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius - 8)
        elif self.type == "shooter":
            pygame.draw.circle(screen, (50, 50, 255), (int(self.x), int(self.y)), self.radius - 8)
        elif self.type == "suicide":
            pygame.draw.circle(screen, (200, 0, 200), (int(self.x), int(self.y)), self.radius - 6)
        
        # Barre de vie
        bar_width = 40
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 10
        
        # Fond de la barre
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Vie actuelle
        health_width = (self.health / self.max_health) * bar_width
        health_color = (0, 255, 0) if self.health > self.max_health * 0.3 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
import pygame
import math
import random
from config.settings import *
from .projectiles import Projectile

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.type = enemy_type
        
        # Stats de base selon le type
        if enemy_type == "charger":  # Cours sur le joueur
            self.speed = 3.5
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.color = (255, 100, 100)  # Rouge clair
            self.radius = 22
            self.attack_range = 0
            
        elif enemy_type == "shooter":  # Tire des projectiles
            self.speed = 1.5
            self.health = 25
            self.max_health = 25
            self.damage = 8
            self.color = (100, 100, 255)  # Bleu
            self.radius = 18
            self.attack_range = 200  
            self.shoot_cooldown = 0
            self.shoot_rate = 60 
            
        elif enemy_type == "suicide":  # Nouveau type - explose au contact
            self.speed = 2.8
            self.health = 15
            self.max_health = 15
            self.damage = 30  # Dégâts élevés à l'explosion
            self.color = (255, 0, 255)  # Magenta
            self.radius = 16
            self.attack_range = 0
            self.explosion_radius = 60  # Zone d'effet de l'explosion
            self.is_exploding = False
            self.explosion_timer = 0
            
        else:  # Type basique (par défaut)
            self.speed = 2
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.color = RED
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
        if distance < 50:  # pour l'explosion
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
    
    def shoot(self, dx, dy, projectiles):
        """Tire un projectile vers le joueur"""
        if projectiles is None:
            return
            
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Vérification que projectiles est une liste modifiable
        projectiles.append(Projectile(
                self.x, self.y,
                dx * 7,
                dy * 7,
                self.damage,
                color=(100, 200, 255)
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
            pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.radius - 8)
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
        health_color = GREEN if self.health > self.max_health * 0.3 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
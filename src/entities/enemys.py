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
            self.attack_range = 1000  # Contact direct
            
        elif enemy_type == "shooter":  # Tire des projectiles
            self.speed = 1.5
            self.health = 25
            self.max_health = 25
            self.damage = 8
            self.color = (100, 100, 255)  # Bleu
            self.radius = 18
            self.attack_range = 300  # Portée de tir
            self.shoot_cooldown = 0
            self.shoot_rate = 1  # Toutes les 1.5 secondes (à 60 FPS)

        elif enemy_type == "suicide":  # Explose à proximité
            self.speed = 4.5
            self.health = 15
            self.max_health = 15
            self.damage = 30
            self.color = (255, 150, 0)  # Orange
            self.radius = 16
            self.attack_range = 50  # Portée d'explosion
        

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
        
        # Charge plus vite que les autres
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def _update_suicide(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Charge plus vite que les autres
        self.x += dx * self.speed
        self.y += dy * self.speed

    def _update_shooter(self, player, projectiles):
        """Se déplace et tire des projectiles"""
        # Calcul de la distance au joueur
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Se déplace pour maintenir la distance
        if distance < self.attack_range - 50:
            # Trop proche, recule
            self.x -= (dx / distance) * self.speed
            self.y -= (dy / distance) * self.speed
        elif distance > self.attack_range + 50:
            # Trop loin, avance
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        
        # Gestion du tir, 
        # comment coder un tir une balle par une balle avec 1 seconde d'ecart
    
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1   
        else:
            # Tire un projectile vers le joueur
            self.shoot(dx, dy, projectiles)
            self.shoot_cooldown = int(self.shoot_rate * 60)  # Convertit en frames (à 60 FPS)
        
    
    def shoot(self, dx, dy, projectiles):
        """Tire un projectile vers le joueur"""
        if projectiles is None:
            return
            
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        projectiles.append(Projectile(
            self.x, self.y,
            dx * 7,  # Vitesse du projectile
            dy * 7,
            self.damage,
            color=(100, 200, 255)  # Bleu clair pour les projectiles ennemis
        ))
    
    def take_damage(self, amount):
        """Inflige des dégâts à l'ennemi"""
        self.health -= amount
        return self.health <= 0
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        # Corps de l'ennemi
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Indicateur de type (cercle intérieur)
        if self.type == "charger":
            pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.radius - 8)
        elif self.type == "shooter":
            pygame.draw.circle(screen, (50, 50, 255), (int(self.x), int(self.y)), self.radius - 8)
        
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
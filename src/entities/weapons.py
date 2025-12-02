import pygame
import math
from .projectiles import Projectile

class Weapon:
    def __init__(self, settings, fire_rate=0.5, damage=100000, projectile_speed=20):
        self.fire_rate = fire_rate  # tirs par seconde
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.last_shot_time = 0
        self.last_direction = (1, 0)  # direction par défaut (droite)
        self.stationary_time = 0
        self.stationary_threshold = 25  # 0.5 secondes à 60 FPS
        self.settings = settings
    
    def update(self, player, current_time, projectiles, enemies):
        """Gère le tir automatique uniquement quand immobile"""
       # Détection d'immobilité basée sur last_dx et last_dy
        is_stationary = (player.last_dx == 0 and player.last_dy == 0)
        
        if is_stationary:
            self.stationary_time += 1
        else:
            self.stationary_time = 0
        
        # DEBUG: Afficher l'état de la visée (à enlever après test)
        print(f"Stationary: {is_stationary}, Time: {self.stationary_time}/{self.stationary_threshold}")
        
        # Tire seulement si immobile depuis assez longtemps
        if (self.stationary_time >= self.stationary_threshold and 
            current_time - self.last_shot_time > 1000 / self.fire_rate):
            
            target_enemy = self.find_closest_enemy(player, enemies)
            if target_enemy:
                self.shoot_at_target(player, target_enemy, projectiles)
            else:
                # Si pas d'ennemi, tire dans la dernière direction
                self.shoot(player, projectiles)
            
            self.last_shot_time = current_time
    
    def find_closest_enemy(self, player, enemies):
        """Trouve l'ennemi le plus proche du joueur"""
        if not enemies:
            return None
            
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        return closest_enemy if min_distance < 500 else None  # Portée max de visée
    
    def shoot_at_target(self, player, target, projectiles):
        """Tire vers l'ennemi ciblé"""
        dx = target.x - player.x
        dy = target.y - player.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Met à jour la dernière direction
        self.last_direction = (dx, dy)
        
        # Crée le projectile
        projectiles.append(Projectile(
            player.x, player.y,
            dx * self.projectile_speed,
            dy * self.projectile_speed,
            self.damage,
            self.settings
        ))
    
    def shoot(self, player, projectiles):
        """Crée un projectile dans la dernière direction """
        projectiles.append(Projectile(
            player.x, player.y,
            self.last_direction[0] * self.projectile_speed,
            self.last_direction[1] * self.projectile_speed,
            self.damage,
            self.settings
        ))
    
    def update_direction(self, dx, dy):
        """Met à jour la direction de tir basée sur le mouvement"""
        if dx != 0 or dy != 0:
            self.last_direction = (dx, dy)

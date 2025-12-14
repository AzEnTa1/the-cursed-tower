import pygame
import math
import random
from .projectiles import Projectile

class Weapon:
    def __init__(self, settings, damage, fire_rate=0.5, projectile_speed=20):
        self.fire_rate = fire_rate  # tirs par seconde
        self.damage = random.randint(damage - 5, damage + 5)
        self.projectile_speed = projectile_speed
        self.last_shot_time = 0
        self.last_direction = (1, 0)  # direction par défaut (droite)
        self.stationary_time = 0
        self.stationary_threshold = 25
        
        # Multishot system
        self.multishot_count = 0  # Nombre de projectiles supplémentaires
        self.shot_interval = 100  # ms entre chaque projectile du multishot
        self.multishot_timer = 0
        self.multishot_queue = []  # Queue pour les tirs multishot
        self.is_shooting_multishot = False
        
        self.settings = settings
        print(f"Weapon created: {self.damage} damage")
    
    def update(self, player, current_time, projectiles, enemies, dt):
        """Gère le tir automatique et le multishot"""
        
        # Gestion du multishot en cours
        if self.is_shooting_multishot and self.multishot_queue:
            self.multishot_timer += dt 
            
            while (self.multishot_queue and 
                   self.multishot_timer >= self.shot_interval):
                # Tire le prochain projectile de la queue
                projectile_data = self.multishot_queue.pop(0)
                self._create_projectile(projectile_data, projectiles)
                self.multishot_timer = 0
            
            if not self.multishot_queue:
                self.is_shooting_multishot = False
        
        # Détection d'immobilité pour le tir normal
        is_stationary = (player.last_dx == 0 and player.last_dy == 0)
        
        if is_stationary:
            self.stationary_time += 1
        else:
            self.stationary_time = 0
        
        # 3. Tir normal (si pas déjà en train de tirer un multishot)
        if (not self.is_shooting_multishot and
            self.stationary_time >= self.stationary_threshold and 
            current_time - self.last_shot_time > 1000 / self.fire_rate):
            
            target_enemy = self.find_closest_enemy(player, enemies)
            
            if target_enemy:
                self._shoot_at_target(player, target_enemy, projectiles)
            else:
                self._shoot_in_direction(player, projectiles)
            
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
        
        return closest_enemy if min_distance < 500 else None
    
    def _shoot_at_target(self, player, target, projectiles):
        """Tire vers l'ennemi ciblé"""
        dx = target.x - player.x
        dy = target.y - player.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Met à jour la dernière direction
        self.last_direction = (dx, dy)
        
        # Déclenche le tir (normal ou multishot)
        self._trigger_shot(player.x, player.y, dx, dy, projectiles)
    
    def _shoot_in_direction(self, player, projectiles):
        """Tire dans la dernière direction"""
        dx, dy = self.last_direction
        self._trigger_shot(player.x, player.y, dx, dy, projectiles)
    
    def _trigger_shot(self, x, y, dx, dy, projectiles):
        """Déclenche un tir (normal ou multishot)"""
        if self.multishot_count > 0:
            # Prépare le multishot
            self._prepare_multishot(x, y, dx, dy, projectiles)
        else:
            # Tir normal
            self._create_projectile({
                'x': x, 'y': y,
                'dx': dx * self.projectile_speed,
                'dy': dy * self.projectile_speed,
                'damage': self.damage
            }, projectiles)
    
    def _prepare_multishot(self, x, y, dx, dy, projectiles):
        """Prépare les projectiles pour le multishot"""
        total_shots = self.multishot_count + 1  # +1 pour le tir principal
        
        # Effet sonore spécial pour multishot
        print(f"debug multishot (et aussi d'autre truc futurement) nombre de tir : {total_shots} ")
        
        # Crée la queue de tirs et tire immédiatement le premier
        self.multishot_queue = []
        for i in range(total_shots):
            self.multishot_queue.append({
                'x': x, 'y': y,
                'dx': dx * self.projectile_speed,
                'dy': dy * self.projectile_speed,
                'damage': self.damage,
                'index': i
            })
        
        # Démarre le multishot et tire immédiatement le premier projectile
        self.is_shooting_multishot = True
        self.multishot_timer = 0
        
        # Tire le premier projectile immédiatement
        if self.multishot_queue:
            projectile_data = self.multishot_queue.pop(0)
            self._create_projectile(projectile_data, projectiles)
    
    def _create_projectile(self, data, projectiles):
        """Crée un projectile avec des effets spéciaux pour multishot"""
        # Effets visuels spéciaux pour les projectiles multishots
        if 'index' in data:
            # Couleurs différentes selon l'index
            colors = [
                (255, 100, 100),  # Rouge
                (100, 255, 100),  # Vert
                (100, 100, 255),  # Bleu
                (255, 255, 100),  # Jaune
                (255, 100, 255),  # Magenta
                (100, 255, 255)   # Cyan
            ]
            color_idx = data['index'] % len(colors)
            color = colors[color_idx]
            
            # Taille légèrement réduite pour les projectiles supplémentaires
            radius = 4 if data['index'] == 0 else 3
            
            # Effet de traînée spécial 
            trail_color = (color[0], color[1], color[2], 150)
        else:
            color = (255, 255, 0)  # Jaune pour les tirs normaux
            radius = 5
            trail_color = (255, 255, 0, 150)
        
        projectiles.append(Projectile(
            data['x'], data['y'],
            data['dx'], data['dy'],
            data['damage'],
            self.settings,
            color=color,
            radius=radius,
            is_multishot=('index' in data)
        ))
    
    def update_direction(self, dx, dy):
        """Met à jour la direction de tir basée sur le mouvement"""
        if dx != 0 or dy != 0:
            self.last_direction = (dx, dy)
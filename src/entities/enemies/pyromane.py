# src/entities/enemies/pyromane.py 
import pygame
import math
import random
from .enemy import Enemy
from ..projectiles import FireZone

class Pyromane(Enemy):
    """
    Ennemi pyromane - pose des zones de feu avec prévisualisation
    Se déplace en cercle autour du joueur
    """
    def __init__(self, x, y, settings):
        super().__init__(x, y, settings)
        self.type = "pyromane"       
        self.speed = 1.2
        self.health = 35
        self.max_health = 35
        self.color = (255, 100, 0)
        self.radius = 20
        self.attack_range = 250
        
        self.fire_zone_cooldown = 0
        self.fire_zone_rate = 210  # 3.5 secondes entre les attaques
        self.fire_zones_placed = 0
        self.max_fire_zones = random.randint(1, 2)  # Entre 1 et 2 flaques par attaque
        
        # Mouvement circulaire
        self.circle_angle = random.random() * 2 * math.pi
        self.circle_radius = 180
        self.circle_speed = 0.015
        
        # Gestion des flaques en attente
        self.pending_fire_zones = []  
        
        # Prévisualisation
        self.preview_cooldown = 0
        self.preview_duration = 45  # 0.75s à 60 FPS (45 frames)
        self.active_previews = []  # Prévisualisations actives [(x, y, timer)]


    def update(self, player, fire_zones=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance_to_player = math.sqrt(dx*dx + dy*dy)
        
        if distance_to_player > self.circle_radius:
            # Se rapprocher du cercle
            norm_dx = dx / max(distance_to_player, 0.1)
            norm_dy = dy / max(distance_to_player, 0.1)
            self.x += norm_dx * self.speed
            self.y += norm_dy * self.speed
        else:
            # Se déplacer en cercle AUTOUR du joueur
            self.circle_angle += self.circle_speed
            target_x = player.x + math.cos(self.circle_angle) * self.circle_radius
            target_y = player.y + math.sin(self.circle_angle) * self.circle_radius
            
            move_x = target_x - self.x
            move_y = target_y - self.y
            move_dist = math.sqrt(move_x*move_x + move_y*move_y)
            
            if move_dist > 0:
                move_x = move_x / move_dist * self.speed
                move_y = move_y / move_dist * self.speed
                self.x += move_x
                self.y += move_y
        
        # 2. GESTION DES PRÉVISUALISATIONS ACTIVES
        for preview in self.active_previews[:]:
            preview[2] -= 1  # Décrémente le timer
            if preview[2] <= 0:
                # Timer terminé -> créer la flaque de feu
                if fire_zones is not None:
                    fire_zones.append(FireZone(preview[0], preview[1], self.settings))
                self.active_previews.remove(preview)
        
        # 3. DÉCLENCHEMENT D'UNE NOUVELLE ATTAQUE (2 flaques)
        if (self.fire_zone_cooldown <= 0 and 
            fire_zones is not None and
            pending_zones is not None):
            
            # Calculer DEUX positions différentes pour les flaques
            flame_positions = []
            for i in range(2):
                # Position autour du joueur (éviter les positions trop proches)
                angle = random.random() * 2 * math.pi
                min_dist = 60  # Distance minimale entre les deux flaques
                max_dist = 120
                flame_distance = random.randint(min_dist, max_dist)
                
                flame_x = player.x + math.cos(angle) * flame_distance
                flame_y = player.y + math.sin(angle) * flame_distance
                
                # Garder dans l'écran
                flame_x = max(50, 
                            min(flame_x, self.settings.screen_width - 50))
                flame_y = max(50, 
                            min(flame_y, self.settings.screen_height - 50))
                
                flame_positions.append((flame_x, flame_y))
            
            # Ajouter les flaques au système de pending (pour prévisualisation globale)
            for i, (fx, fy) in enumerate(flame_positions):
                pending_zones.append({
                    'x': fx,
                    'y': fy,
                    'timer': self.preview_duration + (i * self.preview_duration),  # Décalage de 0.75s
                    'source': self  # Référence au Pyromante
                })
            
            self.fire_zone_cooldown = self.fire_zone_rate
        
        elif self.fire_zone_cooldown > 0:
            self.fire_zone_cooldown -= 1
        
        # Garde le Pyromante dans l'écran
        self.x = max(self.radius, 
                    min(self.x, self.settings.screen_width - self.radius))
        self.y = max(self.radius, 
                    min(self.y, self.settings.screen_height - self.radius))
    
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        super().draw(screen)
    
        # Flamme intérieure qui pulse
        flame_size = self.radius - 5 + int(3 * math.sin(pygame.time.get_ticks() * 0.01))
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), flame_size)
        
        # Indicateur de zone de feu (cercle extérieur) - pulse quand prêt à attaquer
        if self.fire_zone_cooldown <= 30:  # Prêt à attaquer
            zone_indicator = int(8 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
            pygame.draw.circle(screen, (255, 50, 0, 150), 
                            (int(self.x), int(self.y)), 
                            self.radius + zone_indicator, 3)
        
        # Indicateur du nombre de flaques disponibles
        if self.fire_zone_cooldown <= 0:
            for i in range(2):
                angle = i * (math.pi / 4) + pygame.time.get_ticks() * 0.001
                indicator_x = self.x + math.cos(angle) * (self.radius + 15)
                indicator_y = self.y + math.sin(angle) * (self.radius + 15)
                pygame.draw.circle(screen, (255, 100, 0), 
                                (int(indicator_x), int(indicator_y)), 4)

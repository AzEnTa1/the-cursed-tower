# src/entities/enemys.py 
import pygame
import math
from .projectiles import Projectile
import random
from .projectiles import FireZone

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
        
        elif enemy_type == "pyromante":
            # Support/Zone : Pose des zones de feu AVEC PRÉVISUALISATION
            self.speed = 1.2
            self.health = 35
            self.max_health = 35
            self.damage = 0
            self.color = (255, 100, 0)
            self.radius = 20
            self.attack_range = 250
            
            # Système de zones de feu amélioré
            self.fire_zone_cooldown = 0
            self.fire_zone_rate = 210  # 3.5 secondes entre les attaques
            self.fire_zones_placed = 0
            self.max_fire_zones = 2  # 2 flaques par attaque
            
            # Mouvement circulaire
            self.circle_angle = random.random() * 2 * math.pi
            self.circle_radius = 180
            self.circle_speed = 0.015
            
            # Gestion des flaques en attente
            self.pending_fire_zones = []  # Liste des flaques à créer avec leur timing
            
            # Prévisualisation
            self.preview_cooldown = 0
            self.preview_duration = 45  # 0.75s à 60 FPS (45 frames)
            self.active_previews = []  # Prévisualisations actives [(x, y, timer)]
            
        else:  # Type basique (par défaut)
            self.speed = 2
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.color = (255, 0, 0)  # Rouge
            self.radius = 20
            self.attack_range = 0
    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        if self.type == "charger":
            self._update_charger(player) 
        elif self.type == "shooter":
            self._update_shooter(player, projectiles)
        elif self.type == "suicide":
            self._update_suicide(player)
        elif self.type == "destructeur": 
            self._update_destructeur(player, projectiles)
        elif self.type == "pyromante":
            self._update_pyromante(player, projectiles, pending_zones)
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
    
    def _update_pyromante(self, player, fire_zones, pending_zones):
        """Pyromante : Se déplace en cercle et pose DEUX zones de feu avec prévisualisation"""
        # 1. MOUVEMENT CIRCULAIRE
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
                flame_x = max(self.settings.x0 + 50, 
                            min(flame_x, self.settings.x0 + self.settings.screen_width - 50))
                flame_y = max(self.settings.y0 + 50, 
                            min(flame_y, self.settings.y0 + self.settings.screen_height - 50))
                
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
        self.x = max(self.settings.x0 + self.radius, 
                    min(self.x, self.settings.x0 + self.settings.screen_width - self.radius))
        self.y = max(self.settings.y0 + self.radius, 
                    min(self.y, self.settings.y0 + self.settings.screen_height - self.radius))
    
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
        elif self.type == "pyromante":
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
        
        # BARRE DE VIE - AJOUT CRITIQUE !
        self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen):
        """Dessine la barre de vie de l'ennemi"""
        # Taille de la barre selon le type
        if self.type == "destructeur":
            bar_width = 50
            bar_height = 8
            bar_y_offset = -15  # Plus haut pour le mini-boss
        else:
            bar_width = 40
            bar_height = 6
            bar_y_offset = -10
        
        # Position de la barre (au-dessus de l'ennemi)
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius + bar_y_offset
        
        # Fond de la barre (gris foncé)
        pygame.draw.rect(screen, (50, 50, 50), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Calcul de la largeur de vie
        health_percent = max(0, self.health / self.max_health)
        health_width = int(bar_width * health_percent)
        
        # Couleur de la barre de vie (vert → jaune → rouge)
        if health_percent > 0.6:
            bar_color = (0, 255, 0)  # Vert
        elif health_percent > 0.3:
            bar_color = (255, 255, 0)  # Jaune
        else:
            bar_color = (255, 0, 0)  # Rouge
        
        # Barre de vie remplie
        if health_width > 0:
            pygame.draw.rect(screen, bar_color, 
                           (bar_x, bar_y, health_width, bar_height))
        
        # Bordure de la barre
        pygame.draw.rect(screen, (200, 200, 200), 
                        (bar_x, bar_y, bar_width, bar_height), 1)
        
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
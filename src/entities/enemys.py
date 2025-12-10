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
        
        if enemy_type == "destructeur":
            self.speed = 1.2  
            self.health = 200
            self.max_health = 200
            self.damage = 15
            self.color = (255, 200, 200)  # Rose clair
            self.radius = 30
            self.attack_range = 300  
            
            # Système de salves
            self.shoot_cooldown = 0
            self.shoot_rate = 180  # 3 secondes entre les salves
            self.projectile_speed = 6  # Un peu plus rapide
            self.salve_count = 0  # Nombre de tirs dans la salve actuelle
            self.max_salve_shots = 9  # 3x3 = 9 projectiles
            self.salve_delay = 5  # Frames entre chaque tir dans une salve
            self.salve_timer = 0
            self.is_in_salve = False  # Est en train de tirer une salve
            
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
        #print(self.type)
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
        
        # condition de tir
        can_shoot = (distance <= self.attack_range and 
                    distance >= self.attack_range - 150)
        
        if self.shoot_cooldown <= 0 and can_shoot:
            self.shoot(dx, dy, projectiles)
            self.shoot_cooldown = self.shoot_rate
        elif self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def _update_destructeur(self, player, projectiles):
        """Destructeur : se déplace et tire des salves de 3x3 projectiles"""
        # 1. DÉPLACEMENT vers le joueur
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Se déplace vers le joueur s'il est trop loin
        if distance > self.attack_range * 0.7:
            # Normalise la direction
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            # Déplacement
            self.x += norm_dx * self.speed
            self.y += norm_dy * self.speed
        
        # 2. GESTION DES TIRS EN SALVE
        if projectiles is None:
            return
        
        # Cooldown entre les salves
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Début d'une nouvelle salve si le joueur est en range et pas déjà en salve
        if (distance <= self.attack_range and 
            self.shoot_cooldown <= 0 and 
            not self.is_in_salve and 
            self.salve_count == 0):
            
            self.is_in_salve = True
            self.salve_count = 0
            self.salve_timer = 0
            #print("DEBUG: Destructeur commence une salve!")
        
        # Si en train de tirer une salve
        if self.is_in_salve:
            self.salve_timer += 1
            
            # Temps de tirer un nouveau projectile dans la salve
            if self.salve_timer >= self.salve_delay and self.salve_count < self.max_salve_shots:
                self.shoot_destructeur_salve(dx, dy, projectiles)
                self.salve_count += 1
                self.salve_timer = 0
                #print(f"DEBUG: Destructeur tire projectile {self.salve_count}/{self.max_salve_shots}")
            
            # Fin de la salve
            if self.salve_count >= self.max_salve_shots:
                self.is_in_salve = False
                self.shoot_cooldown = self.shoot_rate
                #print("DEBUG: Destructeur fin de salve, rechargement...")
    
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
        
    def shoot_destructeur_salve(self, dx, dy, projectiles):
        """Tire une salve de projectiles en grille 3x3"""
        if projectiles is None:
            return
        
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        dx /= distance
        dy /= distance
        
        # Calcul de l'angle vers le joueur
        base_angle = math.atan2(dy, dx)
        
        # Configuration de la grille 3x3
        rows = 3
        cols = 3
        row_spread = math.radians(30)  # Écart vertical
        col_spread = math.radians(40)  # Écart horizontal
        
        # Calcul de la position dans la salve (0 à 8)
        salve_index = self.salve_count
        
        # Convertir en coordonnées de grille
        row = salve_index // cols  # 0, 1, 2
        col = salve_index % cols   # 0, 1, 2
        
        # Calcul des décalages
        row_offset = (row - 1) * row_spread  # -1, 0, 1
        col_offset = (col - 1) * col_spread  # -1, 0, 1
        
        # Calcul de l'angle final
        angle = base_angle + col_offset
        
        # Calcul de la direction du projectile
        proj_dx = math.cos(angle) * self.projectile_speed
        proj_dy = math.sin(angle) * self.projectile_speed
        
        # Appliquer un léger décalage vertical
        proj_dy += row_offset * 2
        
        # Création du projectile
        projectiles.append(Projectile(
            self.x + col * 5,  # Léger décalage horizontal pour l'effet
            self.y + row * 5,  # Léger décalage vertical
            proj_dx,
            proj_dy,
            self.damage,
            self.settings,
            color=(255, 150, 150, 180),  # Rose semi-transparent
            radius=6  # Un peu plus gros
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
        
        # Indicateur spécial pour les destructeurs
        if self.type == "destructeur":
            # Effet de pulsation pour les destructeurs
            pulse = int(5 * (1 + math.sin(pygame.time.get_ticks() * 0.005)))
            pygame.draw.circle(screen, (255, 100, 100), 
                             (int(self.x), int(self.y)), 
                             self.radius + pulse, 2)
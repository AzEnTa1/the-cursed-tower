# src/entities/player.py
import pygame
import math
import random

class Player:
    """
    Classe du joueur
    Gère le déplacement, la vie, le score et les interactions
    """
    def __init__(self, x, y, settings, player_data):
        self.settings = settings
        self.x = x
        self.y = y
        self.speed = player_data["speed"]
        self.size = player_data["size"]
        self.color = self.settings.GREEN
        self.infinite_life = False

        # Points de vie
        self.health = player_data["max_health"]
        self.max_health = player_data["max_health"]
        
        # Score
        self.score = 0
        self.xp = 0

        # États des touches
        self.keys_pressed = {
            'left': False,
            'right': False, 
            'up': False,
            'down': False
        }

        # Dernière touche pressée pour chaque axe
        self.last_horizontal_key = None
        self.last_vertical_key = None
        
        # Direction du mouvement pour les tirs
        self.last_dx = 0
        self.last_dy = 0
        
        # Système de Dash
        self.dash_cooldown = 0
        self.dash_cooldown_max = 120  # 2 secondes à 60 FPS
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 15  # 0.25s à 60 FPS
        self.dash_speed_multiplier = 5
        self.dash_trail_particles = []
        self.dash_afterimages = []
        self.dash_afterimage_timer = 0
        self.dash_color = (100, 200, 255)  # Bleu clair pour le dash
        
        # Effets visuels
        self.damage_flash_timer = 0
        self.damage_flash_duration = 10
    
    def handle_event(self, event):
        """Gère les événements de pression et relâchement des touches"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_LEFT):
                self.keys_pressed['left'] = True
                self.last_horizontal_key = 'left'
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.keys_pressed['right'] = True
                self.last_horizontal_key = 'right'
            elif event.key in (pygame.K_z, pygame.K_UP):
                self.keys_pressed['up'] = True
                self.last_vertical_key = 'up'
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.keys_pressed['down'] = True
                self.last_vertical_key = 'down'
            # Dash 
            elif event.key == pygame.K_x and self.dash_cooldown <= 0:
                self.activate_dash()
                
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_q, pygame.K_LEFT):
                self.keys_pressed['left'] = False
                if self.last_horizontal_key == 'left':
                    self.last_horizontal_key = 'right' if self.keys_pressed['right'] else None
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.keys_pressed['right'] = False
                if self.last_horizontal_key == 'right':
                    self.last_horizontal_key = 'left' if self.keys_pressed['left'] else None
            elif event.key in (pygame.K_z, pygame.K_UP):
                self.keys_pressed['up'] = False
                if self.last_vertical_key == 'up':
                    self.last_vertical_key = 'down' if self.keys_pressed['down'] else None
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.keys_pressed['down'] = False
                if self.last_vertical_key == 'down':
                    self.last_vertical_key = 'up' if self.keys_pressed['up'] else None
    

    def reset_player_movements(self):
        self.keys_pressed['left'] = False
        self.keys_pressed['right'] = False
        self.keys_pressed['up'] = False
        self.keys_pressed['down'] = False
        self.last_horizontal_key = None
        self.last_vertical_key = None

    def update(self):
        """Met à jour la position du joueur avec priorité à la dernière touche"""
        if self.infinite_life:
            self.health = self.max_health

        # Gestion du dash
        if self.is_dashing:
            self.update_dash()
        else:
            self.update_normal_movement()
        
        # Update cooldowns et effets
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1
        
        # Update particules de traînée
        self.update_trail_particles()
    
    def update_normal_movement(self):
        """Mouvement normal du joueur"""
        # Mouvement horizontal - dernière touche prime
        dx = 0
        if self.last_horizontal_key == 'left':
            dx = -self.speed
        elif self.last_horizontal_key == 'right':
            dx = self.speed
        
        # Mouvement vertical - dernière touche prime
        dy = 0
        if self.last_vertical_key == 'up':
            dy = -self.speed
        elif self.last_vertical_key == 'down':
            dy = self.speed
        
        # toujours mettre à jour last_dx et last_dy
        self.last_dx = dx
        self.last_dy = dy
        
        # Applique le mouvement
        self.x += dx
        self.y += dy
        
        # Garde le joueur dans l'écran
        self.x = max(self.size, min(self.x, self.settings.screen_width - self.size))
        self.y = max(self.size, min(self.y, self.settings.screen_height - self.size))
    
    def activate_dash(self):
        """Active le dash"""
        if self.dash_cooldown > 0 or self.is_dashing:
            return
        
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_max
        
        # Créer un effet de particules initial
        self.create_dash_blast()
    
    def update_dash(self):
        """Met à jour le dash en cours"""
        self.dash_timer -= 1
        
        # Calcul de la direction du dash
        dx, dy = self.get_movement_vector()
        
        # Multiplicateur de vitesse pendant le dash
        dash_speed = self.speed * self.dash_speed_multiplier
        self.x += dx * dash_speed
        self.y += dy * dash_speed
        
        # Créer des afterimages
        self.dash_afterimage_timer += 1
        if self.dash_afterimage_timer >= 2:
            self.dash_afterimages.append({
                'x': self.x,
                'y': self.y,
                'timer': 15,
                'size': self.size,
                'color': self.dash_color
            })
            self.dash_afterimage_timer = 0
        
        # Créer des particules de traînée
        self.create_trail_particles()
        
        # Fin du dash
        if self.dash_timer <= 0:
            self.is_dashing = False
            self.create_dash_end_effect()
    
    def get_movement_vector(self):
        """Retourne le vecteur de mouvement normalisé"""
        dx, dy = 0, 0
        
        if self.last_horizontal_key == 'left':
            dx = -1
        elif self.last_horizontal_key == 'right':
            dx = 1
        
        if self.last_vertical_key == 'up':
            dy = -1
        elif self.last_vertical_key == 'down':
            dy = 1
        
        # Normaliser pour les diagonales
        if dx != 0 and dy != 0:
            length = math.sqrt(dx*dx + dy*dy)
            dx /= length
            dy /= length
        
        return dx, dy
    
    def create_dash_blast(self):
        """Crée l'effet visuel de départ du dash"""
        for i in range(20):
            angle = random.random() * math.pi * 2
            speed = random.uniform(3, 8)
            self.dash_trail_particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(15, 30),
                'color': self.dash_color,
                'size': random.uniform(2, 5)
            })
    
    def create_trail_particles(self):
        """Crée des particules pendant le dash"""
        for i in range(3):
            angle = random.random() * math.pi * 2
            offset_x = random.uniform(-self.size/2, self.size/2)
            offset_y = random.uniform(-self.size/2, self.size/2)
            
            self.dash_trail_particles.append({
                'x': self.x + offset_x,
                'y': self.y + offset_y,
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.5, 0.5),
                'life': random.randint(20, 40),
                'color': self.dash_color,
                'size': random.uniform(2, 4)
            })
    
    def create_dash_end_effect(self):
        """Crée l'effet visuel de fin du dash"""
        for i in range(15):
            angle = random.random() * math.pi * 2
            speed = random.uniform(1, 4)
            self.dash_trail_particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(20, 35),
                'color': (200, 230, 255),  # Bleu plus clair
                'size': random.uniform(3, 6)
            })
    
    def update_trail_particles(self):
        """Met à jour les particules de traînée"""
        for particle in self.dash_trail_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            # Légère gravité
            particle['dy'] += 0.1
            
            if particle['life'] <= 0:
                self.dash_trail_particles.remove(particle)
        
        # Mettre à jour les afterimages
        for afterimage in self.dash_afterimages[:]:
            afterimage['timer'] -= 1
            afterimage['size'] *= 0.95  # Rétrécit progressivement
            
            if afterimage['timer'] <= 0:
                self.dash_afterimages.remove(afterimage)
    
    def take_damage(self, amount):
        """Inflige des dégâts au joueur"""
        if self.is_dashing:
            return False  # Invulnérable pendant le dash

        self.settings.sounds["degat_1"].play()
        self.health -= amount
        self.damage_flash_timer = self.damage_flash_duration
        return self.health <= 0
    
    def add_score(self, points):
        """Ajoute des points au score"""
        self.score += points
        self.xp += points
    
    def draw(self, screen):
        """Dessine le joueur avec effets visuels"""
        # Dessiner les afterimages du dash (en premier)
        for afterimage in self.dash_afterimages:
            try:
                # Calcul de l'alpha
                alpha = int(255 * (afterimage['timer'] / 15.0))
                alpha = max(0, min(255, alpha))
                
                # Récupérer la couleur de base
                base_color = afterimage['color']
                # Si la couleur a 4 éléments, on ne prend que les 3 premiers
                if len(base_color) >= 3:
                    r, g, b = base_color[:3]
                else:
                    r, g, b = 100, 200, 255  # couleur par défaut
                
                color_with_alpha = (r, g, b, alpha)
                
                afterimage_size = int(afterimage['size'])
                if afterimage_size <= 0:
                    continue
                    
                surf = pygame.Surface((afterimage_size*2, afterimage_size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color_with_alpha, 
                                 (afterimage_size, afterimage_size), 
                                 afterimage_size)
                screen.blit(surf, (int(afterimage['x'] - afterimage_size), 
                                 int(afterimage['y'] - afterimage_size)))
            except Exception as e:
                print(f"Erreur lors du dessin d'une afterimage: {e}")
                print(f"Données de l'afterimage: {afterimage}")
                continue
        
        # Dessiner les particules de traînée
        for particle in self.dash_trail_particles:
            try:
                alpha = int(255 * (particle['life'] / 30.0))
                alpha = max(0, min(255, alpha))
                
                base_color = particle['color']
                if len(base_color) >= 3:
                    r, g, b = base_color[:3]
                else:
                    r, g, b = 100, 200, 255
                
                color_with_alpha = (r, g, b, alpha)
                
                particle_size = int(particle['size'])
                if particle_size <= 0:
                    continue
                    
                surf = pygame.Surface((particle_size*2, particle_size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color_with_alpha, 
                                 (particle_size, particle_size), 
                                 particle_size)
                screen.blit(surf, (int(particle['x'] - particle_size), 
                                 int(particle['y'] - particle_size)))
            except Exception as e:
                print(f"Erreur particule: {e}")
                continue
        
        # Déterminer la couleur du joueur (RGB seulement - pas d'alpha)
        if self.is_dashing:
            current_color = self.dash_color  # RGB
        elif self.damage_flash_timer > 0:
            # Flash rouge quand touché
            flash_intensity = (self.damage_flash_timer / self.damage_flash_duration)
            current_color = (
                min(255, int(self.color[0] + (255 - self.color[0]) * flash_intensity)),
                int(self.color[1] * (1 - flash_intensity * 0.5)),
                int(self.color[2] * (1 - flash_intensity * 0.5))
            )
        else:
            current_color = self.color  # RGB
        
        # Corps du joueur avec effet de glow pendant le dash
        if self.is_dashing:
            # Effet de glow extérieur - utiliser des surfaces avec transparence
            for i in range(3, 0, -1):
                glow_size = self.size + i * 2
                glow_alpha = 100 - i * 30
                
                # Créer surface pour le glow
                glow_surf = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
                glow_color = (
                    self.dash_color[0],
                    self.dash_color[1],
                    self.dash_color[2],
                    glow_alpha
                )
                pygame.draw.circle(glow_surf, glow_color, 
                                 (int(glow_size), int(glow_size)), 
                                 int(glow_size))
                screen.blit(glow_surf, (int(self.x - glow_size), 
                                      int(self.y - glow_size)))
        
        # Dessiner le joueur
        pygame.draw.circle(screen, current_color, 
                          (int(self.x), int(self.y)), 
                          self.size)
        
        # Contour pendant le dash
        if self.is_dashing:
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(self.x), int(self.y)), 
                             self.size, 2)
    
    def get_dash_cooldown_percent(self):
        """Retourne le pourcentage de recharge du dash (0-1)"""
        if self.dash_cooldown <= 0:
            return 1.0
        return 1.0 - (self.dash_cooldown / self.dash_cooldown_max)
    
    def get_stats(self)->dict:
        """sert a obtenir les stats du joueur"""
        return {
            "speed":self.speed,
            "size":self.size,
            "current_health":self.health,
            "max_health":self.max_health,
            "score":self.score,
            "xp":self.xp
        }
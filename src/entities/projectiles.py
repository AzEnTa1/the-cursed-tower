import pygame
import random
import math

class Projectile:
    def __init__(self, x, y, dx, dy, damage, settings, color=(255, 255, 0), radius=5, is_multishot=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.radius = radius
        self.color = color
        self.lifetime = 60  # frames avant disparition
        self.settings = settings
        self.is_multishot = is_multishot
        
        # Effet visuel spécial pour le multishot
        self.trail_particles = []
        self.trail_timer = 0
        self.sparkle_timer = 0
    
    def update(self):
        """Met à jour la position du projectile"""
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        
        # Effets de particules différents selon le type
        self.trail_timer += 1
        if self.trail_timer >= (2 if self.is_multishot else 3):
            particle_color = self.color if self.is_multishot else (255, 255, 0)
            alpha = 180 if self.is_multishot else 150
            self.trail_particles.append({
                'x': self.x,
                'y': self.y,
                'life': 20 if self.is_multishot else 15,
                'color': particle_color,
                'alpha': alpha
            })
            self.trail_timer = 0
        
        # Effet "d'étincelles" pour multishot
        if self.is_multishot:
            self.sparkle_timer += 1
            if self.sparkle_timer >= 5:
                self.trail_particles.append({
                    'x': self.x + random.randint(-3, 3),
                    'y': self.y + random.randint(-3, 3),
                    'life': 10,
                    'color': (255, 255, 200),
                    'alpha': 200
                })
                self.sparkle_timer = 0
        
        # Met à jour les particules
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
        
        # Vérifie les bords de l'écran
        if (self.x < 0 or self.x > self.settings.screen_width + self.settings.x0 or 
            self.y < 0 or self.y > self.settings.screen_height + self.settings.y0):
            self.lifetime = 0
    
    def draw(self, screen):
        """Dessine le projectile et sa traînée"""
        # Dessine la traînée
        for particle in self.trail_particles:
            alpha = int(particle['alpha'] * (particle['life'] / 20))
            size = max(1, self.radius // 2)
            pygame.draw.circle(screen, 
                             (particle['color'][0], particle['color'][1], particle['color'][2], alpha),
                             (int(particle['x']), int(particle['y'])), 
                             size)
        
        # Dessine le projectile principal
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def is_alive(self):
        return self.lifetime > 0


class FireZone:
    """Zone de feu posée par le Pyromante - Version améliorée visuellement"""
    def __init__(self, x, y, settings):
        self.x = x
        self.y = y
        self.base_radius = 50
        self.radius = self.base_radius
        self.duration = 300  # 5 secondes à 60 FPS
        self.damage_per_tick = 3
        self.lifetime = self.duration
        self.settings = settings
        self.last_damage_time = 0
        self.spawn_time = pygame.time.get_ticks()
        
        # Animations avancées
        self.pulse_timer = 0
        self.wave_timer = 0
        self.heat_distortion_timer = 0
        
        # Particules de flamme (système avancé)
        self.flame_particles = []
        self.spark_particles = []
        self.smoke_particles = []
        
        # Effet de pulsation multiple
        self.pulse_layers = [
            {'radius': 25, 'speed': 0.08, 'offset': random.random() * math.pi * 2},
            {'radius': 35, 'speed': 0.12, 'offset': random.random() * math.pi * 2},
            {'radius': 45, 'speed': 0.15, 'offset': random.random() * math.pi * 2}
        ]
        
        # Gradients de couleur pour les flammes
        self.fire_gradient = [
            (255, 255, 200, 255),  # Centre blanc-jaune
            (255, 200, 100, 220),  # Jaune vif
            (255, 150, 50, 200),   # Orange
            (255, 100, 0, 180),    # Orange foncé
            (200, 50, 0, 150),     # Rouge-orange
            (150, 30, 0, 120)      # Rouge sombre
        ]
        
        # Initialiser les particules
        self._initialize_particles()
    
    def _initialize_particles(self):
        """Initialise les particules de flamme, d'étincelles et de fumée"""
        # Particules de flamme principale
        for _ in range(40):
            angle = random.random() * 2 * math.pi
            dist = random.uniform(10, 40)
            speed = random.uniform(0.8, 2.5)
            size = random.uniform(4, 10)
            
            self.flame_particles.append({
                'x': self.x + math.cos(angle) * dist,
                'y': self.y + math.sin(angle) * dist,
                'base_x': self.x + math.cos(angle) * dist,
                'base_y': self.y + math.sin(angle) * dist,
                'size': size,
                'max_size': size,
                'life': random.randint(40, 100),
                'max_life': 100,
                'speed': speed,
                'speed_variation': random.uniform(0.95, 1.05),
                'angle': angle,
                'wiggle_speed': random.uniform(0.05, 0.15),
                'wiggle_amount': random.uniform(0.5, 2.0),
                'rise_speed': random.uniform(0.3, 1.0),
                'color_index': random.randint(0, len(self.fire_gradient)-1)
            })
        
        # Particules d'étincelles
        for _ in range(20):
            angle = random.random() * 2 * math.pi
            speed = random.uniform(2.0, 5.0)
            
            self.spark_particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed * 0.5 - random.uniform(1.0, 2.0),
                'size': random.uniform(1.5, 3.5),
                'life': random.randint(20, 50),
                'color': (255, 255, 200, 255),
                'trail': []
            })
        
        # Particules de fumée
        for _ in range(15):
            angle = random.random() * 2 * math.pi
            dist = random.uniform(20, 45)
            
            self.smoke_particles.append({
                'x': self.x + math.cos(angle) * dist,
                'y': self.y + math.sin(angle) * dist,
                'dx': random.uniform(-0.3, 0.3),
                'dy': random.uniform(-0.8, -0.3),
                'size': random.uniform(8, 15),
                'life': random.randint(80, 150),
                'max_life': 150,
                'color': (80, 80, 80, 180),
                'fade_start': random.randint(50, 100)
            })
    
    def update(self):
        """Met à jour la zone de feu avec toutes ses animations"""
        self.lifetime -= 1
        self.pulse_timer += 0.05
        self.wave_timer += 0.03
        self.heat_distortion_timer += 0.02
        
        # Animation de pulsation globale
        pulse = math.sin(self.pulse_timer) * 8
        self.radius = self.base_radius + pulse
        
        # Mettre à jour les couches de pulsation
        for layer in self.pulse_layers:
            layer['offset'] += layer['speed'] * 0.05
        
        # Mettre à jour les particules de flamme
        for particle in self.flame_particles[:]:
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                # Réinitialiser la particule
                angle = random.random() * 2 * math.pi
                dist = random.uniform(10, 40)
                particle['x'] = self.x + math.cos(angle) * dist
                particle['y'] = self.y + math.sin(angle) * dist
                particle['base_x'] = particle['x']
                particle['base_y'] = particle['y']
                particle['life'] = random.randint(40, 100)
                particle['size'] = random.uniform(4, 10)
                particle['max_size'] = particle['size']
                particle['color_index'] = random.randint(0, len(self.fire_gradient)-1)
            else:
                # Animation de la particule
                wiggle = math.sin(particle['life'] * particle['wiggle_speed']) * particle['wiggle_amount']
                particle['x'] = particle['base_x'] + wiggle
                particle['y'] = particle['base_y'] - (100 - particle['life']) * particle['rise_speed'] * 0.1
                
                # Taille qui pulse avec la vie
                life_ratio = particle['life'] / particle['max_life']
                particle['size'] = particle['max_size'] * (0.3 + 0.7 * life_ratio)
        
        # Mettre à jour les étincelles
        for spark in self.spark_particles[:]:
            spark['life'] -= 1
            
            if spark['life'] <= 0:
                self.spark_particles.remove(spark)
            else:
                spark['x'] += spark['dx']
                spark['y'] += spark['dy']
                spark['dy'] += 0.05  # Gravité légère
                
                # Ajouter à la traînée
                spark['trail'].append((spark['x'], spark['y']))
                if len(spark['trail']) > 5:
                    spark['trail'].pop(0)
        
        # Ajouter de nouvelles étincelles occasionnellement
        if random.random() < 0.1 and len(self.spark_particles) < 30:
            angle = random.random() * 2 * math.pi
            speed = random.uniform(2.0, 5.0)
            
            self.spark_particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed * 0.5 - random.uniform(1.0, 2.0),
                'size': random.uniform(1.5, 3.5),
                'life': random.randint(20, 50),
                'color': (255, 255, 200, 255),
                'trail': []
            })
        
        # Mettre à jour la fumée
        for smoke in self.smoke_particles[:]:
            smoke['life'] -= 1
            
            if smoke['life'] <= 0:
                self.smoke_particles.remove(smoke)
            else:
                smoke['x'] += smoke['dx']
                smoke['y'] += smoke['dy']
                smoke['dx'] += random.uniform(-0.02, 0.02)
                smoke['dy'] += random.uniform(-0.01, 0.01)
                
                # La fumée grossit et s'estompe
                if smoke['life'] < smoke['fade_start']:
                    smoke['size'] *= 1.02
        
        return self.lifetime > 0
    
    def check_damage(self, player):
        """Vérifie si le joueur est dans la zone et inflige des dégâts"""
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        current_time = pygame.time.get_ticks()
        
        if distance < self.radius:
            if current_time - self.last_damage_time >= 100:
                player.take_damage(self.damage_per_tick)
                self.last_damage_time = current_time
                
                # Créer des étincelles supplémentaires quand le joueur prend des dégâts
                for _ in range(3):
                    angle = random.random() * 2 * math.pi
                    self.spark_particles.append({
                        'x': player.x,
                        'y': player.y,
                        'dx': math.cos(angle) * random.uniform(2.0, 4.0),
                        'dy': math.sin(angle) * random.uniform(2.0, 4.0),
                        'size': random.uniform(2.0, 4.0),
                        'life': random.randint(15, 35),
                        'color': (255, 255, 200, 255),
                        'trail': []
                    })
                
                return True
        return False
    
    def draw(self, screen):
        """Dessine la zone de feu avec des effets visuels avancés"""
        # 1. DESSINER LA FUMÉE (en premier, au fond)
        for smoke in self.smoke_particles:
            if smoke['life'] > 0:
                alpha = int(180 * (smoke['life'] / smoke['max_life']))
                if smoke['life'] < smoke['fade_start']:
                    alpha = int(180 * (smoke['life'] / smoke['fade_start']))
                
                color = (smoke['color'][0], smoke['color'][1], smoke['color'][2], alpha)
                pygame.draw.circle(screen, color,
                                 (int(smoke['x']), int(smoke['y'])),
                                 int(smoke['size']))
        
        # 2. DESSINER LES COUCHES DE FLAMME PRINCIPALES
        for i, layer in enumerate(self.pulse_layers):
            layer_pulse = math.sin(self.pulse_timer * layer['speed'] + layer['offset']) * 5
            
            for r in range(int(layer['radius'] + layer_pulse), 0, -2):
                ratio = r / (layer['radius'] + layer_pulse)
                color_index = min(int(ratio * len(self.fire_gradient)), len(self.fire_gradient)-1)
                color = self.fire_gradient[color_index]
                
                alpha = int(color[3] * (0.3 + 0.7 * (1 - ratio)))
                adjusted_color = (color[0], color[1], color[2], alpha)
                
                temp_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, adjusted_color, (r, r), r)
                screen.blit(temp_surface, (int(self.x - r), int(self.y - r)))
        
        # 3. DESSINER LES PARTICULES DE FLAMME INDIVIDUELLES
        for particle in self.flame_particles:
            if particle['life'] > 0:
                life_ratio = particle['life'] / particle['max_life']
                color = self.fire_gradient[particle['color_index']]
                
                brightness = 0.5 + 0.5 * life_ratio
                adjusted_color = (
                    min(255, int(color[0] * brightness)),
                    min(255, int(color[1] * brightness)),
                    min(255, int(color[2] * brightness)),
                    int(color[3] * life_ratio * 0.7)
                )
                
                # Effet glow
                for glow in range(3, 0, -1):
                    glow_size = particle['size'] + glow
                    glow_alpha = int(adjusted_color[3] * 0.3 / glow)
                    glow_color = (adjusted_color[0], adjusted_color[1], adjusted_color[2], glow_alpha)
                    
                    temp_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
                    pygame.draw.circle(temp_surface, glow_color, 
                                     (int(glow_size), int(glow_size)), 
                                     int(glow_size))
                    screen.blit(temp_surface, 
                              (int(particle['x'] - glow_size), 
                               int(particle['y'] - glow_size)))
                
                # Particule principale
                pygame.draw.circle(screen, adjusted_color,
                                 (int(particle['x']), int(particle['y'])),
                                 int(particle['size']))
        
        # 4. DESSINER LES ÉTINCELLES
        for spark in self.spark_particles:
            if spark['life'] > 0:
                # Dessiner la traînée
                for i, (trail_x, trail_y) in enumerate(spark['trail']):
                    trail_alpha = int(255 * (i / len(spark['trail'])))
                    trail_size = spark['size'] * (0.3 + 0.7 * (i / len(spark['trail'])))
                    
                    trail_color = (spark['color'][0], spark['color'][1], spark['color'][2], trail_alpha)
                    pygame.draw.circle(screen, trail_color,
                                     (int(trail_x), int(trail_y)),
                                     int(trail_size))
                
                # Étincelle principale
                spark_alpha = int(255 * (spark['life'] / 50))
                spark_color = (spark['color'][0], spark['color'][1], spark['color'][2], spark_alpha)
                pygame.draw.circle(screen, spark_color,
                                 (int(spark['x']), int(spark['y'])),
                                 int(spark['size']))
        
        # 5. EFFET DE DISTORSION DE CHALEUR
        heat_wave = math.sin(self.heat_distortion_timer) * 3
        for i in range(8):
            angle = i * (math.pi / 4) + self.wave_timer
            wave_x = self.x + math.cos(angle) * (self.radius + heat_wave)
            wave_y = self.y + math.sin(angle) * (self.radius + heat_wave)
            
            for j in range(3):
                offset = j * 0.3
                end_x = wave_x + math.cos(angle + offset) * 10
                end_y = wave_y + math.sin(angle + offset) * 10
                
                pygame.draw.line(screen, (255, 200, 100, 80),
                               (int(wave_x), int(wave_y)),
                               (int(end_x), int(end_y)), 2)
        
        # 6. CONTOUR LUMINEUX
        for i in range(2, 0, -1):
            glow_radius = self.radius + i * 4
            glow_alpha = 30 - i * 10
            glow_color = (255, 150, 50, glow_alpha)
            
            temp_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, glow_color, 
                             (glow_radius, glow_radius), 
                             glow_radius, 3)
            screen.blit(temp_surface, 
                      (int(self.x - glow_radius), 
                       int(self.y - glow_radius)))
import pygame
import random

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
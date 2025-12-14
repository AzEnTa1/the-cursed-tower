import pygame

class Projectile:
    def __init__(self, x, y, dx, dy, damage, settings, color=(255, 255, 0), radius=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.radius = radius if radius is not None else 5
        self.color = color
        self.lifetime = 60  # frames avant disparition
        self.settings = settings
        
        # Effet visuel spécial pour le triple shot
        self.trail_particles = []
        self.trail_timer = 0
    
    def update(self):
        """Met à jour la position du projectile"""
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        
        # Ajoute des particules de traînée
        self.trail_timer += 1
        if self.trail_timer >= 3:  # Une particule toutes les 3 frames
            self.trail_particles.append({
                'x': self.x,
                'y': self.y,
                'life': 15
            })
            self.trail_timer = 0
        
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
            alpha = int(255 * (particle['life'] / 15))
            pygame.draw.circle(screen, 
                             (self.color[0], self.color[1], self.color[2], alpha),
                             (int(particle['x']), int(particle['y'])), 
                             max(1, self.radius // 2))
        
        # Dessine le projectile
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    
    def is_alive(self):
        return self.lifetime > 0
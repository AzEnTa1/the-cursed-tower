import pygame

class Projectile:
    def __init__(self, x, y, dx, dy, damage, settings, color=(255, 255, 0), radius=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.radius = 5
        self.color = color
        self.lifetime = 60  # frames avant disparition
        self.settings = settings
    
    def update(self):
        """Met à jour la position du projectile"""
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        
        # Vérifie les bords de l'écran
        if (self.x < 0 or self.x > self.settings.screen_width + self.settings.x0 or 
            self.y < 0 or self.y > self.settings.screen_height + self.settings.y0):
            self.lifetime = 0
    
    def draw(self, screen):
        """Dessine le projectile"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def is_alive(self):
        return self.lifetime > 0
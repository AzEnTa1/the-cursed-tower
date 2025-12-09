import pygame
#from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class TransitionEffect:
    def __init__(self, settings):
        self.alpha = 0
        self.duration = 1000  # 1 seconde
        self.current_time = 0
        self.active = False
        self.callback = None
        self.settings = settings
        
    def start(self, callback=None):
        """Démarre l'effet de transition"""
        self.alpha = 0
        self.current_time = 0
        self.active = True
        self.callback = callback
        
    def update(self, dt):
        """Met à jour l'effet de transition"""
        if not self.active:
            return
            
        self.current_time += dt
        progress = min(self.current_time / self.duration, 1.0)
        
        # Fondu au noir puis retour a la normale
        if progress < 0.5:
            self.alpha = int(255 * (progress * 2))
        else:
            self.alpha = int(255 * ((1 - progress) * 2))
            
        # Fin de la transition
        if progress >= 1.0:
            self.active = False
            if self.callback:
                self.callback()
                
    def draw(self, screen):
        """Dessine l'effet de superposition"""
        if self.active and self.alpha > 0:
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.alpha))
            screen.blit(overlay, (self.settings.x0, self.settings.y0))
            
    def is_active(self):
        return self.active
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class TransitionEffect:
    def __init__(self):
        self.alpha = 0
        self.fade_speed = 5
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill(BLACK)
        self.fade_surface.set_alpha(self.alpha)
        self.state = "none"  # "fade_out", "fade_in", "none"
    
    def start_fade_out(self):
        """Commence un fondu vers le noir"""
        self.state = "fade_out"
        self.alpha = 0
    
    def start_fade_in(self):
        """Commence un fondu depuis le noir"""
        self.state = "fade_in" 
        self.alpha = 255
    
    def update(self):
        """Met à jour l'effet de transition"""
        if self.state == "fade_out":
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.state = "complete"
                
        elif self.state == "fade_in":
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.alpha = 0
                self.state = "none"
        
        self.fade_surface.set_alpha(self.alpha)
    
    def draw(self, screen):
        """Dessine l'effet de fondu"""
        if self.alpha > 0:
            screen.blit(self.fade_surface, (0, 0))
    
    def is_complete(self):
        """Vérifie si la transition est terminée"""
        return self.state == "complete" or self.state == "none"
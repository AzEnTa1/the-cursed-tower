# src/entities/spawn_effect.py
import pygame
import math

class SpawnEffect:
    """Effet visuel pour l'apparition d'un ennemi"""
    def __init__(self, x, y, settings, enemy_type="basic"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.settings = settings
        self.timer = 0
        self.duration = 1000  # 1 seconde
        self.is_active = True
        
        # Animation du cercle
        self.max_radius = 45
        self.current_radius = 0
        self.circle_color = (255, 255, 0)  # Jaune
        self.pulse_speed = 4
        self.pulse_phase = 0
        self.warning_color = (255, 100, 0)  # Orange pour avertissement
        
        # Son d'apparition
        self.settings.sounds["spawn"].play()

    def update(self, dt):
        """Met à jour l'animation"""
        self.timer += dt
        self.pulse_phase += 0.05 * self.pulse_speed
        
        # Rayon qui grandit puis rétrécit à la fin
        if self.timer < self.duration * 0.8:
            self.current_radius = (self.max_radius * self.timer / (self.duration * 0.8)) # grandit
        else:
            # Rétrécit à la fin
            remaining = self.duration - self.timer
            self.current_radius = self.max_radius * (remaining / (self.duration * 0.2))
        
        # Effet de pulsation, comme ds enemy "destructeur"
        pulse = math.sin(self.pulse_phase) * 3
        self.current_radius = max(5, self.current_radius + pulse)
        
        if self.timer >= self.duration:
            self.is_active = False
    
    def draw(self, screen):
        """Dessine l'effet d'apparition"""
        if not self.is_active:
            return
        
        # Intensité basée sur le temps restant
        alpha = int(255 * (1 - self.timer / self.duration))
        
        # Cercle extérieur (avertissement)
        pygame.draw.circle(screen, self.warning_color, 
                          (int(self.x), int(self.y)), 
                          int(self.current_radius * 1.2), 2)
        
        # Cercle principal pulsant
        pulse_width = int(2 + math.sin(self.pulse_phase * 2) * 1.5)
        pygame.draw.circle(screen, self.circle_color, 
                          (int(self.x), int(self.y)), 
                          int(self.current_radius), pulse_width)
        
        # Cercle intérieur
        inner_radius = self.current_radius * 0.6
        pygame.draw.circle(screen, (255, 200, 0), 
                          (int(self.x), int(self.y)), 
                          int(inner_radius), 1)
        
        # Indicateur de type d'ennemi
        font = pygame.font.Font(None, 28)
        
        # Code couleur selon le type
        if self.enemy_type == "charger":
            color = (255, 255, 0)  # Jaune
        elif self.enemy_type == "shooter":
            color = (100, 150, 255)  # Bleu
        elif self.enemy_type == "suicide":
            color = (255, 0, 255)  # Magenta
        elif self.enemy_type == "destructeur":
            color = (255, 200, 200)  # Rose
        else:
            color = (255, 100, 100)  # Rouge
        
        # Texte avec ombre pour meilleure lisibilité
        text_surface = font.render("", True, color)
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        
        # Ombre du texte
        shadow_surface = font.render("", True, (0, 0, 0))
        screen.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        screen.blit(text_surface, text_rect)
    
    def get_position(self):
        """Retourne la position de spawn"""
        return self.x, self.y
    
    def is_complete(self):
        """Vérifie si l'effet est terminé"""
        return not self.is_active
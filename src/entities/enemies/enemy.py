# src/entities/enemies/charger.py 
import pygame

class Enemy:
    def __init__(self, x, y, settings):
        self.x = x
        self.y = y
        self.settings = settings
        # enemy basic
        self.speed = 2
        self.health = 30
        self.max_health = 30
        self.damage = 10
        self.color = (255, 0, 0)  # Rouge
        self.radius = 20
        self.attack_range = 0
    
    def update(self, player, projectiles=None, pending_zones=None):
        """Met à jour l'ennemi selon son type"""
        pass
    
    
    def take_damage(self, amount): #global pour enemies
        """Inflige des dégâts à l'ennemi"""
        self.health -= amount
        return self.health <= 0
    
    def draw(self, screen):
        """Dessine l'ennemi avec sa barre de vie"""
        
        # Corps de l'ennemi
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # BARRE DE VIE - AJOUT CRITIQUE !
        self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen, bar_width = 40, bar_height = 6, bar_y_offset = -10): #pour tous sauf destructeur
        """Dessine la barre de vie de l'ennemi""" 
        
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
        
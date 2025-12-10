# src/entities/player.py
import pygame
#from config.settings import PLAYER_SPEED, PLAYER_SIZE, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, RED

class Player:
    def __init__(self, x, y, settings):
        self.settings = settings
        self.x = x
        self.y = y
        self.speed = settings.player_speed
        self.size = settings.player_size
        self.color = (0, 255, 0)
        
        # Points de vie
        self.health = 100
        self.max_health = 100
        
        # Score
        self.score = 0
        
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
    
    def update(self):
        """Met à jour la position du joueur avec priorité à la dernière touche"""
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
        self.x = max(self.settings.x0 + self.size, min(self.x, self.settings.x0 + self.settings.screen_width - self.size))
        self.y = max(self.settings.y0 + self.size, min(self.y, self.settings.y0 + self.settings.screen_height - self.size))
    
    def take_damage(self, amount):
        """Inflige des dégâts au joueur"""
        self.health -= amount
        return self.health <= 0
    
    def add_score(self, points):
        """Ajoute des points au score"""
        self.score += points
    
    def draw(self, screen):
        """Dessine le joueur avec sa barre de vie"""
        # Corps du joueur
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
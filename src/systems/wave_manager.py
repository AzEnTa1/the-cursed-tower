import pygame
from src.utils.queue import WaveQueue
import random

class WaveManager:
    """Gère le déroulement des vagues d'ennemis avec système de file personnalisé"""
    
    def __init__(self, settings):
        self.wave_queue = WaveQueue(settings)
        self.current_wave_enemies = []  # Gardé : ennemis actifs de la vague
        self.wave_number = 0
        self.floor_number = 1
        self.enemies_remaining = 0
        self.state = "between_waves"  # between_waves, in_wave, all_cleared
        self.settings = settings
        
        # Timing des vagues
        self.wave_start_time = 0
        self.time_between_waves = 2000  # 2 secondes entre les vagues
    
    def setup_floor(self, floor_number):
        """Configure les vagues pour un nouvel étage"""
        self.floor_number = floor_number
        self.wave_number = 0
        self.wave_queue.setup_waves_for_floor(floor_number)
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
        self.current_wave_enemies.clear()
        self.enemies_remaining = 0
    
    def update(self, current_time):
        """Met à jour l'état du gestionnaire de vagues"""
        if self.state == "between_waves" and self.wave_queue.has_more_waves():
            if current_time - self.wave_start_time >= self.time_between_waves:
                return True # Indique qu'une nouvelle vague doit commencer
        return False
    
    def start_next_wave(self):
        """Démarre la vague suivante"""
        if not self.wave_queue.has_more_waves():
            return []
        
        wave_data = self.wave_queue.get_next_wave()
        if not wave_data:
            return []
        
        self.wave_number += 1
        self.enemies_remaining = len(wave_data)
        self.state = "in_wave"
        
        spawn_positions = []
        for enemy_type in wave_data:
            x, y = self.generate_spawn_position()
            spawn_positions.append((x, y, enemy_type))
        
        print(f"Vague {self.wave_number} - {len(spawn_positions)} ennemis")
        return spawn_positions
    
    def generate_spawn_position(self):
        """Génère une position de spawn à l'intérieur de l'écran"""
        margin = 100
        center_margin = 200
        
        left = self.settings.x0 + margin
        right = self.settings.x0 + self.settings.screen_width - margin
        top = self.settings.y0 + margin
        bottom = self.settings.y0 + self.settings.screen_height - margin
        
        center_x = self.settings.x0 + self.settings.screen_width // 2
        center_y = self.settings.y0 + self.settings.screen_height // 2
        
        max_attempts = 10
        for _ in range(max_attempts):
            side = random.randint(0, 3)
            
            if side == 0:  # Haut
                x = random.randint(left, right)
                y = top
            elif side == 1:  # Droite
                x = right
                y = random.randint(top, bottom)
            elif side == 2:  # Bas
                x = random.randint(left, right)
                y = bottom
            else:  # Gauche
                x = left
                y = random.randint(top, bottom)
            
            distance_to_center = ((x - center_x)**2 + (y - center_y)**2)**0.5
            if distance_to_center > center_margin:
                return x, y
            
        x = random.randint(left, right)
        y = random.randint(top, bottom)
        return x, y
    
    def on_enemy_died(self, enemy):
        """Appelé quand un ennemi meurt"""
        if enemy in self.current_wave_enemies:
            self.current_wave_enemies.remove(enemy)
            self.enemies_remaining -= 1
            
            if self.enemies_remaining <= 0:
                self.on_wave_cleared()
    
    def on_wave_cleared(self):
        """Appelé quand une vague est terminée"""
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
        
        if not self.wave_queue.has_more_waves():
            self.state = "all_cleared"
            print("Toutes les vagues terminées")
    
    def is_between_waves(self):
        return self.state == "between_waves"
    
    def are_all_waves_cleared(self):
        return self.state == "all_cleared"
    
    def get_wave_info(self):
        """Retourne les informations sur la vague actuelle"""
        return {
            'floor': self.floor_number,
            'current_wave': self.wave_number,
            'enemies_remaining': self.enemies_remaining,
            'state': self.state
        }
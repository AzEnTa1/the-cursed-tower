# src/systems/wave_manager.py
import pygame
from src.utils.queue import WaveQueue
from src.entities.enemys import Enemy

class WaveManager:
    """Gère le déroulement des vagues d'ennemis avec système de file personnalisé"""
    
    def __init__(self, settings):
        self.wave_queue = WaveQueue()
        self.current_wave_enemies = []
        self.wave_number = 0
        self.floor_number = 1
        self.enemies_remaining = 0
        self.state = "between_waves"  # between_waves, in_wave, all_cleared
        self.settings = settings
        
        # Timing des vagues
        self.wave_start_time = 0
        self.time_between_waves = 3000  # 3 secondes entre les vagues
    
    def setup_floor(self, floor_number):
        """Configure les vagues pour un nouvel étage"""
        self.floor_number = floor_number
        self.wave_number = 0
        self.wave_queue.setup_waves_for_floor(floor_number)
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
    
    def update(self, current_time):
        """Met à jour l'état du gestionnaire de vagues"""
        if self.state == "between_waves" and self.wave_queue.has_more_waves():
            # Vérifie si c'est le moment de lancer la prochaine vague
            if current_time - self.wave_start_time >= self.time_between_waves:
                self.start_next_wave()
    
    def start_next_wave(self):
        """Démarre la vague suivante"""
        if not self.wave_queue.has_more_waves():
            return []
        
        wave_data = self.wave_queue.get_next_wave()
        if not wave_data:
            return []
        
        self.wave_number += 1
        self.current_wave_enemies = []
        self.enemies_remaining = len(wave_data)
        self.state = "in_wave"
        
        # Crée les instances d'ennemis
        enemies = []
        for enemy_type in wave_data:
            enemy = self.create_enemy(enemy_type)
            enemies.append(enemy)
            self.current_wave_enemies.append(enemy)
        
        print(f"Vague {self.wave_number} lancée avec {len(enemies)} ennemis")
        return enemies
    
    def create_enemy(self, enemy_type):
        """Crée un ennemi avec une position de spawn aléatoire sur les bords"""
        import random
        
        side = random.randint(0, 3)
        if side == 0:  # Haut
            x = random.randint(50, round(self.settings.x0 + self.settings.screen_width - 50))
            y = -30 + self.settings.y0
        elif side == 1:  # Droite
            x = self.settings.screen_width + 30 + self.settings.x0
            y = random.randint(50, round(self.settings.y0 + self.settings.screen_height - 50))
        elif side == 2:  # Bas
            x = random.randint(50, round(self.settings.x0 + self.settings.screen_width - 50))
            y = self.settings.screen_height + 30 + self.settings.y0
        else:  # Gauche
            x = -30 + self.settings.x0
            y = random.randint(50, round(self.settings.y0 + self.settings.screen_height - 50))
        
        return Enemy(x, y, self.settings, enemy_type)
    
    def on_enemy_died(self, enemy):
        """Appelé quand un ennemi meurt"""
        if enemy in self.current_wave_enemies:
            self.current_wave_enemies.remove(enemy)
            self.enemies_remaining -= 1
            
            # Vérifie si la vague est terminée
            if self.enemies_remaining <= 0:
                self.on_wave_cleared()
    
    def on_wave_cleared(self):
        """Appelé quand une vague est terminée"""
        print(f"Vague {self.wave_number} terminée!")
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
        
        if not self.wave_queue.has_more_waves():
            self.state = "all_cleared"
            print("les vague sont terminées")
    
    def is_wave_in_progress(self):
        """Vérifie si une vague est en cours"""
        return self.state == "in_wave"
    
    def is_between_waves(self):
        """Vérifie si on est entre deux vagues"""
        return self.state == "between_waves"
    
    def are_all_waves_cleared(self):
        """Vérifie si toutes les vagues sont terminées"""
        return self.state == "all_cleared"
    
    def get_wave_info(self):
        """Retourne les informations sur la vague actuelle"""
        return {
            'floor': self.floor_number,
            'current_wave': self.wave_number,
            'total_waves': self.wave_queue.wave_count,
            'enemies_remaining': self.enemies_remaining,
            'state': self.state
        }
# src/systems/wave_manager.py
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
        self.is_boss_floor = False
        
        # Timing des vagues
        self.wave_start_time = 0
        self.time_between_waves = 2000  # 2 secondes entre les vagues
    
    def setup_floor(self, floor_number):
        """Configure les vagues pour un nouvel étage"""
        self.floor_number = floor_number
        self.wave_number = 0
        
        # Boss tous les 3 étages (étages 3, 6, 9, etc.)
        self.is_boss_floor = (floor_number > 1 and floor_number % 3 == 0)
        
        if self.is_boss_floor:
            # Pour un étage de boss
            self.wave_queue.setup_boss_floor(floor_number)
        else:
            # Étage normal
            self.wave_queue.setup_waves_for_floor(floor_number)
        
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
        self.current_wave_enemies.clear()
        self.enemies_remaining = 0
    
    def update(self, current_time):
        """Met à jour l'état du gestionnaire de vagues"""
        if self.state == "between_waves" and self.wave_queue.has_more_waves():
            if current_time - self.wave_start_time >= self.time_between_waves:
                return True  # Indique qu'une nouvelle vague doit commencer
        return False
    
    def start_next_wave(self):
        """Démarre la vague suivante"""
        if not self.wave_queue.has_more_waves():
            return []
        
        wave_data = self.wave_queue.get_next_wave()
        if not wave_data:
            return []
        
        self.wave_number += 1
        self.state = "in_wave"
        
        spawn_positions = []
        
        # Traiter chaque élément de la vague
        for enemy_info in wave_data:
            x, y = self.generate_spawn_position()
            
            # Déterminer le type d'ennemi
            if isinstance(enemy_info, tuple) and enemy_info[0] == "boss":
                # C'est un boss : ("boss", seed)
                _, boss_seed = enemy_info
                spawn_positions.append((x, y, "boss", boss_seed))
                self.enemies_remaining = 1
                print(f"[WAVE] Boss généré avec seed {boss_seed}")
            else:
                # C'est un ennemi normal : juste le nom du type
                enemy_type = enemy_info
                spawn_positions.append((x, y, enemy_type))
                self.enemies_remaining = len(wave_data)
                print(f"[WAVE] {enemy_type} généré")
        
        return spawn_positions
    
    def generate_spawn_position(self):
        """Génère une position de spawn à l'intérieur de l'écran"""
        margin = 100
        center_margin = 200
        
        left = round(margin)
        right = round(self.settings.screen_width - margin)
        top = round(margin)
        bottom = round(self.settings.screen_height - margin)
        
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2
        
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
        
        # Fallback
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
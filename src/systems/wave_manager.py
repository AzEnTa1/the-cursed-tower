# src/systems/wave_manager.py
import pygame
from src.utils.queue import WaveQueue
import random

class WaveManager:
    """Gère le déroulement des vagues d'ennemis avec système de file personnalisé"""
    
    def __init__(self, settings):
        self.settings = settings
        self.wave_queue = WaveQueue(settings)
        self.current_wave_enemies = []
        self.wave_number = 0
        self.floor_number = 1
        self.enemies_remaining = 0
        self.state = "between_waves"  # between_waves, in_wave, boss_wave, all_cleared
        self.boss_spawned = False
        
        # Timing des vagues
        self.wave_start_time = 0
        self.time_between_waves = 2000  # 2 secondes entre les vagues
        
        # Initialisation
        self.reset_to_floor(1)
    
    def reset_to_floor(self, floor_number):
        """Réinitialise le manager pour un nouvel étage"""
        self.floor_number = floor_number
        self.wave_number = 0
        self.enemies_remaining = 0
        self.state = "between_waves"
        self.boss_spawned = False
        
        # Configurer les vagues pour cet étage (3 vagues normales)
        self.wave_queue.setup_waves_for_floor(floor_number)
        
        self.wave_start_time = pygame.time.get_ticks()
        self.current_wave_enemies.clear()
    
    def update(self, current_time):
        """Met à jour l'état du gestionnaire de vagues"""
        if self.state == "between_waves" and (self.wave_queue.has_more_waves() or (self.wave_number >= 3 and not self.boss_spawned)):
            if current_time - self.wave_start_time >= self.time_between_waves:
                return True  # Indique qu'une nouvelle vague doit commencer
        return False
    
    def start_next_wave(self):
        """Démarre la vague suivante ou le boss"""
        # Si on a fini les 3 vagues normales et le boss n'a pas encore spawn
        if self.wave_number >= 3 and not self.boss_spawned:
            # C'est l'heure du boss !
            return self.start_boss_wave()
        
        # Sinon, c'est une vague normale
        if not self.wave_queue.has_more_waves():
            return []
        
        wave_data = self.wave_queue.get_next_wave()
        if not wave_data:
            return []
        
        self.wave_number += 1
        self.state = "in_wave"
        spawn_positions = []
        
        # Traiter chaque ennemi de la vague
        for enemy_type in wave_data:
            x, y = self.generate_spawn_position()
            spawn_positions.append((x, y, enemy_type))
        
        self.enemies_remaining = len(wave_data)
        return spawn_positions
    
    def start_boss_wave(self):
        """Démarre la vague de boss"""
        boss_seed = hash((self.floor_number, pygame.time.get_ticks())) % (2**32)
        x, y = self.generate_boss_spawn_position()
        
        self.state = "boss_wave"
        self.boss_spawned = True
        self.enemies_remaining = 1
        
        return [(x, y, "boss", boss_seed)]
    
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
    
    def generate_boss_spawn_position(self):
        """Génère une position de spawn spéciale pour le boss"""
        # Le boss apparaît au centre de l'écran
        x = self.settings.screen_width // 2
        y = self.settings.screen_height // 2
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
        
        # Si c'était le boss, l'étage est terminé
        if self.boss_spawned and self.enemies_remaining == 0:
            self.state = "all_cleared"
    
    def is_between_waves(self):
        return self.state == "between_waves"
    
    def are_all_waves_cleared(self):
        return self.state == "all_cleared"
    
    def get_wave_info(self):
        """Retourne les informations sur la vague actuelle"""
        # Pour l'affichage, on montre seulement les vagues normales (1 à 3)
        # Le boss est traité séparément
        
        return {
            'floor': self.floor_number,
            'current_wave': self.wave_number if self.state != "boss_wave" else 3,  # Quand boss, on reste à 3/3
            'total_waves': 3,  # Toujours 3 vagues normales
            'enemies_remaining': self.enemies_remaining,
            'state': self.state,
            'is_boss_wave': self.state == "boss_wave"
        }
    
    def get_remaining_waves_count(self):
        """Retourne le nombre de vagues normales restantes"""
        if self.state == "all_cleared" or self.boss_spawned:
            return 0
        elif self.state == "in_wave":
            return max(0, 3 - self.wave_number + 1)
        else:
            return max(0, 3 - self.wave_number)

    def on_enemy_divided(self, original_enemy, new_enemies):
        """
        Appelé quand un boss se divise
        """
        # Retirer le boss original des listes
        if original_enemy in self.current_wave_enemies:
            self.current_wave_enemies.remove(original_enemy)
        
        # Ajouter les nouveaux bosses aux listes
        for new_enemy in new_enemies:
            self.current_wave_enemies.append(new_enemy)
        
        # Mettre à jour le compteur d'ennemis restants
        self.enemies_remaining = len(self.current_wave_enemies)
    
    def is_boss_wave_current(self):
        """Retourne True si c'est le moment du boss"""
        return self.state == "boss_wave"
    
    def reset(self):
        """Réinitialise complètement le wave manager"""
        self.wave_queue = WaveQueue(self.settings)
        self.reset_to_floor(1)
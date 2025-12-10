import pygame
from src.utils.queue import WaveQueue
from src.entities.enemys import Enemy
from src.entities.spawn_effect import SpawnEffect  # NOUVEAU IMPORT
import random

class WaveManager:
    """Gère le déroulement des vagues d'ennemis avec système de file personnalisé"""
    
    def __init__(self, settings):
        self.wave_queue = WaveQueue(settings)
        self.current_wave_enemies = []
        self.spawn_effects = []  # Liste des effets d'apparition actifs
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
        self.spawn_effects.clear()
        self.current_wave_enemies.clear()
        self.enemies_remaining = 0
    
    def update(self, current_time):
        """Met à jour l'état du gestionnaire de vagues"""
        if self.state == "between_waves" and self.wave_queue.has_more_waves():
            # Vérifie si c'est le moment de lancer la prochaine vague
            if current_time - self.wave_start_time >= self.time_between_waves:
                self.start_next_wave()
    
    def start_next_wave(self):
        """Démarre la vague suivante avec effets d'apparition"""
        if not self.wave_queue.has_more_waves():
            return []
        
        wave_data = self.wave_queue.get_next_wave()
        if not wave_data:
            return []
        
        self.wave_number += 1
        self.current_wave_enemies = []
        self.spawn_effects.clear()
        self.enemies_remaining = len(wave_data)
        self.state = "in_wave"
        
        # Crée les effets d'apparition pour tous les ennemis
        spawn_positions = []
        for enemy_type in wave_data:
            x, y = self.generate_spawn_position()
            effect = SpawnEffect(x, y, self.settings, enemy_type)
            self.spawn_effects.append(effect)
            spawn_positions.append((x, y, enemy_type))
        
        print(f"Vague {self.wave_number} lancée - {len(self.spawn_effects)} ennemis en approche...")
        return spawn_positions
    
    def generate_spawn_position(self):
        """Génère une position de spawn À L'INTÉRIEUR de l'écran"""
        
        # Définir une zone de spawn qui évite le centre (où est le joueur)
        margin = 100  # Marge par rapport aux bords
        center_margin = 200  # Zone centrale à éviter
        
        # Calculer la zone de spawn
        left_bound = self.settings.x0 + margin
        right_bound = self.settings.x0 + self.settings.screen_width - margin
        top_bound = self.settings.y0 + margin
        bottom_bound = self.settings.y0 + self.settings.screen_height - margin
        
        # Centre de l'écran (là où le joueur commence)
        center_x = self.settings.x0 + self.settings.screen_width // 2
        center_y = self.settings.y0 + self.settings.screen_height // 2
        
        # Générer des positions jusqu'à en trouver une qui n'est pas trop proche du centre
        max_attempts = 10
        for _ in range(max_attempts):
            # Choisir un côté aléatoire (0-3)
            side = random.randint(0, 3)
            
            if side == 0:  # Haut
                x = random.randint(left_bound, right_bound)
                y = top_bound
            elif side == 1:  # Droite
                x = right_bound
                y = random.randint(top_bound, bottom_bound)
            elif side == 2:  # Bas
                x = random.randint(left_bound, right_bound)
                y = bottom_bound
            else:  # Gauche
                x = left_bound
                y = random.randint(top_bound, bottom_bound)
            
            # Vérifier la distance par rapport au centre
            distance_to_center = ((x - center_x)**2 + (y - center_y)**2)**0.5
            
            if distance_to_center > center_margin:
                return x, y
        
        # Si on n'a pas trouvé, retourner une position aléatoire
        x = random.randint(left_bound, right_bound)
        y = random.randint(top_bound, bottom_bound)
        return x, y
    
    def update_spawn_effects(self, dt):
        """Met à jour tous les effets d'apparition"""
        completed_effects = []
        
        for effect in self.spawn_effects:
            effect.update(dt)
            if effect.is_complete():
                completed_effects.append(effect)
        
        # Retire les effets terminés
        for effect in completed_effects:
            if effect in self.spawn_effects:
                self.spawn_effects.remove(effect)
        
        return len(completed_effects) > 0
    
    def create_enemy_from_effect(self, effect):
        """Crée un ennemi après la fin de l'effet"""
        x, y = effect.get_position()
        enemy = Enemy(x, y, self.settings, effect.enemy_type)
        self.current_wave_enemies.append(enemy)
        return enemy
    
    def on_enemy_died(self, enemy):
        """Appelé quand un ennemi meurt"""
        if enemy in self.current_wave_enemies:
            self.current_wave_enemies.remove(enemy)
            self.enemies_remaining -= 1
            
            # Vérifie si la vague est terminée
            if self.enemies_remaining <= 0: #and len(self.spawn_effects) == 0:
                self.on_wave_cleared()
    
    def on_wave_cleared(self):
        """Appelé quand une vague est terminée"""
        print(f"Vague {self.wave_number} terminée!")
        self.state = "between_waves"
        self.wave_start_time = pygame.time.get_ticks()
        
        if not self.wave_queue.has_more_waves():
            self.state = "all_cleared"
            print("Toutes les vagues sont terminées pour cet étage!")
    
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
            'enemies_remaining': self.enemies_remaining,
            'state': self.state,
            'spawns_pending': len(self.spawn_effects)
        }
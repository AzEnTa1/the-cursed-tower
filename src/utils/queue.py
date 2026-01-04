# src/utils/queue.py
from random import choices

class Queue:
    """
    Implémentation d'une file (First-In, First-Out) avec liste Python
    
    Utilisée par WaveManager pour gérer la séquence des vagues d'ennemis
    """
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Ajoute un élément à la file"""
        self.items.append(item)
    
    def dequeue(self):
        """Retire et retourne le premier élément de la file"""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self):
        """Vérifie si la file est vide"""
        return len(self.items) == 0
    
    def size(self):
        """Retourne la taille de la file"""
        return len(self.items)
    
    def peek(self):
        """Regarde le premier élément sans le retirer"""
        if self.is_empty():
            return None
        return self.items[0]

class WaveQueue:
    """Génère uniquement les vagues normales (3 par étage)"""
    
    ENEMY_TYPES = ['basic', 'charger', 'shooter', 'destructeur', 'suicide', 'pyromane']
    
    WAVE_CONFIGS = [
        [35, 15, 15, 5, 10, 20],     # Vague 1 (la plus facile)
        [25, 20, 15, 10, 10, 20],    # Vague 2
        [15, 20, 20, 15, 10, 20],    # Vague 3
    ]
    
    def __init__(self, settings=None):
        self.waves = Queue()
        self.settings = settings
    
    def generate_normal_wave(self, floor_number, wave_number):
        """Génère une vague d'ennemis normaux basée sur l'étage et le numéro de vague"""
        # S'assurer qu'on ne dépasse pas le nombre de configurations
        wave_config_index = min(wave_number - 1, len(self.WAVE_CONFIGS) - 1)
        weights = self.WAVE_CONFIGS[wave_config_index]
        
        # Augmente le nombre d'ennemis avec les étages et les vagues
        base_enemies = 5
        floor_bonus = (floor_number - 1) * 2
        wave_bonus = (wave_number - 1) * 2
        
        enemy_count = base_enemies + floor_bonus + wave_bonus
        enemy_count = min(enemy_count, 15)  # Limiter à 15 ennemis max
        
        enemies = []
        for _ in range(enemy_count):
            enemy_type_index = choices(
                population=range(len(self.ENEMY_TYPES)), 
                weights=weights,
                k=1
            )[0]
            enemies.append(self.ENEMY_TYPES[enemy_type_index])
        
        return enemies
    
    def setup_waves_for_floor(self, floor_number):
        """Configure uniquement les 3 vagues normales"""
        self.waves = Queue()
        
        # Vagues normales : toujours 3
        for wave_num in range(1, 4):  # wave_num de 1 à 3
            wave_enemies = self.generate_normal_wave(floor_number, wave_num)
            self.waves.enqueue(wave_enemies)
    
    def get_next_wave(self):
        """Récupère la prochaine vague d'ennemis normaux"""
        if self.waves.is_empty():
            return None
        
        wave = self.waves.dequeue()
        return wave
    
    def has_more_waves(self):
        """Vérifie s'il reste des vagues normales"""
        return not self.waves.is_empty()
    
    def get_remaining_waves_count(self):
        """Retourne le nombre de vagues normales restantes"""
        return self.waves.size()
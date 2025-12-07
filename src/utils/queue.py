from random import choices

class Queue:
    """Implémentation personnalisée d'une file (FIFO) pour gérer les vagues d'ennemis"""
    
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
    """Génère des vagues d'ennemis de plus en plus difficiles"""
    
    # Configuration des vagues : [basic, charger, shooter, suicide]
    WAVE_CONFIGS = [
        [70, 20, 10, 0],    # Vague 1 : 70% basic, 20% charger, 10% shooter, 0% suicide
        [50, 30, 15, 5],    # Vague 2
        [40, 25, 20, 15],   # Vague 3
        [30, 25, 25, 20],   # Vague 4
        [20, 25, 30, 25],   # Vague 5
    ]
    
    ENEMY_TYPES = ['basic', 'charger', 'shooter', 'suicide']
    
    def __init__(self):
        self.waves = Queue()
        self.wave_count = 0
        self.enemies_per_wave = 8  # Commence avec 8 ennemis par vague
    
    def generate_wave(self, floor_number):
        """Génère une vague d'ennemis basée sur l'étage actuel"""
        wave_config_index = min(floor_number - 1, len(self.WAVE_CONFIGS) - 1)
        weights = self.WAVE_CONFIGS[wave_config_index]
        
        # Augmente le nombre d'ennemis avec les étages
        enemy_count = self.enemies_per_wave + (floor_number - 1) * 2
        
        enemies = []
        for _ in range(enemy_count):
            enemy_type_index = choices(
                population=[0, 1, 2, 3],
                weights=weights,
                k=1
            )[0]
            enemies.append(self.ENEMY_TYPES[enemy_type_index])
        
        return enemies
    
    def setup_waves_for_floor(self, floor_number, waves_count=3):
        """Configure les vagues pour un étage donné"""
        self.waves = Queue()
        
        for wave_num in range(waves_count):
            # Chaque vague successive dans le même étage a une difficulté légèrement accrue
            effective_floor = floor_number + (wave_num * 0.3)
            wave_enemies = self.generate_wave(int(effective_floor))
            self.waves.enqueue(wave_enemies)
        
        self.wave_count = waves_count
    
    def get_next_wave(self):
        """Récupère la prochaine vague d'ennemis"""
        if self.waves.is_empty():
            return None
        return self.waves.dequeue()
    
    def has_more_waves(self):
        """Vérifie s'il reste des vagues"""
        return not self.waves.is_empty()
    
    def get_remaining_waves_count(self):
        """Retourne le nombre de vagues restantes"""
        return self.waves.size()
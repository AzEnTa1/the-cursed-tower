# src/systems/wave_manager.pyw
import pygame
from src import Queue # importer ce que vs avez besoin

class WaveManager:
    def __init__(self):
        self.waves_queue = Queue()
        self.current_wave = None
        self.wave_number = 0
        self.enemies_remaining = 0
    
    def setup_waves(self, floor_number):
        # Configurer 3 vagues d'ennemis selon l'étage
        pass
    
    def start_next_wave(self):
        # Commencer la vague suivante
        pass
    
    def is_wave_cleared(self):
        # Vérifier si la vague est terminée
        pass
    
    def are_all_waves_cleared(self):
        # Vérifier si toutes les vagues sont terminées
        pass
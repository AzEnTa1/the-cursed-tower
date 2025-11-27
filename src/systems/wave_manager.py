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
        if floor_number == 1:
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
        elif floor_number == 2:
            Queue.conteur_wave = 4
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)

    def start_next_wave(self):
        # Commencer la vague suivante
        if not self.waves_queue.is_empty():
            self.current_wave = self.waves_queue.dequeue()
            self.enemies_remaining = len(self.current_wave)
            self.wave_number += 1
    
    def is_wave_cleared(self):
        # Vérifier si la vague est terminée
        return self.enemies_remaining == 0
    
    def are_all_waves_cleared(self):
        # Vérifier si toutes les vagues sont terminées
        return self.waves_queue.is_empty()

class WaweManager:
    def __init__(self):
        self.active_waves = []
    
    def enqueue(self, wave):
        self.active_waves.append(wave)

    def dequeue(self):
        if not self.is_empty():
            return self.active_waves.pop(0)
        return None

    def is_empty(self):
        return len(self.active_waves) == 0
    
    def size(self):
        return len(self.active_waves)
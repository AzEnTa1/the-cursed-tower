# src/systems/wave_manager.pyw
import pygame
from src.utils import Queue # importer ce que vs avez besoin
from src.entities.enemys import Enemy

class WaveManager:
    def __init__(self, enemies):
        self.waves_queue = Queue()
        self.current_wave = None
        self.wave_number = 0
        self.enemies_remaining = enemies

        self.lst = []# A SUPRIME !

    def setup_waves(self, floor_number):
        # Configurer 3 vagues d'ennemis selon l'étage
        
        # ici faudrait ajouter a la queue(file) 3 vagues aléatoires
        """if floor_number == 1:
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
        elif floor_number == 2:
            Queue.conteur_wave = 4
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)
            Queue.create_wave(self.waves_queue)"""
        #merde temporaire pk flem 
        for i in range(3):
            self.lst.append("vague 1")

    def start_next_wave(self)->list:
        # Commencer la vague suivante
        """if not self.waves_queue.is_empty():
            self.current_wave = self.waves_queue.dequeue()
            self.enemies_remaining = len(self.current_wave)
            self.wave_number += 1"""
        #merde temporaire pk flem II
        if len(self.lst) == 0:
            self.setup_waves(1)
        liste_enemies_ajoutes = []
        if self.lst.pop() == "vague 1":
            for i in range(10):
                liste_enemies_ajoutes.append(Enemy(10*i, 10*i))
        else:
            for i in range(10):
                liste_enemies_ajoutes.append(Enemy(10*i, 10*i, "charger"))
        return liste_enemies_ajoutes

    
    def is_wave_cleared(self):
        # Vérifier si la vague est terminée
        #return self.enemies_remaining == 0
        return True
    
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
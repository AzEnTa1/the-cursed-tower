
from random import *


class Queue:
    """ cree des wague de 10 ennemis de plus en plus fort a chaque vague, les normaux on un score de dureter de 1, les charger 2, les shooter 3 et les suicide 4"""

    def __init__(self):
        self.waves = []
        self.conteur_wave = 0
        self.enemies = []

    def create_wave(self):
        for i in range(10):
            if self.conteur_wave == 0:
                random = random.choices(population=[1, 2, 3, 4],weights=[50, 25, 35, 10],k=1)[0]
                if random == 1:
                    self.enemies.append('basic')
                if random == 2:
                    self.enemies.append('charger')
                if random == 3:
                    self.enemies.append('shooter')
                if random == 4:
                    self.enemies.append('suicide')
            if self.conteur_wave == 1:
                random = random.choices(population=[1, 2, 3, 4],weights=[50, 50, 35, 10],k=1)[0]
                if random == 1:
                    self.enemies.append('basic')
                if random == 2:
                    self.enemies.append('charger')
                if random == 3:
                    self.enemies.append('shooter')
                if random == 4:
                    self.enemies.append('suicide')
            if self.conteur_wave == 2:
                random = random.choices(population=[1, 2, 3, 4],weights=[50, 50, 50, 30],k=1)[0]
                if random == 1:
                    self.enemies.append('basic')
                if random == 2:
                    self.enemies.append('charger')
                if random == 3:
                    self.enemies.append('shooter')
                if random == 4:
                    self.enemies.append('suicide')
            if self.conteur_wave == 3:
                random = random.choices(population=[1, 2, 3, 4],weights=[50, 50, 50, 50],k=1)[0]
                if random == 1:
                    self.enemies.append('basic')
                if random == 2:
                    self.enemies.append('charger')
                if random == 3:
                    self.enemies.append('shooter')
                if random == 4:
                    self.enemies.append('suicide')
            if self.conteur_wave == 4:
                random = random.choices(population=[1, 2, 3, 4],weights=[50, 50, 50, 50],k=1)[0]
                if random == 1:
                    self.enemies.append('basic')
                if random == 2:
                    self.enemies.append('charger')
                if random == 3:
                    self.enemies.append('shooter')
                if random == 4:
                    self.enemies.append('suicide')
        
        self.waves.append(self.enemies)
        self.enemies = []
        self.conteur_wave += 1

import pygame
from src import test # importer ce que vs avez besoin

# src/utils/queue.py
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        # Ajouter un élément
        pass
    
    def dequeue(self):
        # Retirer le premier élément
        pass
    
    def is_empty(self):
        pass
    
    def size(self):
        pass


# jsp qui fera ca mais fait comme tu en as envie, tu peux reprendre le cours faut juste une file


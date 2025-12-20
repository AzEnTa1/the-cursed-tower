# src/levels/room_manager.py
import pygame
from src import test # importer ce que vs avez besoin

# Gestion de la génération des salles

# Transition entre salles

# État des portes (ouvertes/fermées)

# src/levels/room_manager.py
class RoomManager:
    def __init__(self):
        self.current_room = None
        self.current_floor = 1
        self.generate_new_room()
    
    def generate_new_room(self):
        # Créer une nouvelle salle pour l'étage actuel
        pass
    
    def next_floor(self):
        # Passer à l'étage suivant
        self.current_floor += 1
        self.generate_new_room()
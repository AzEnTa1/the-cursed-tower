# src/levels/room.py
import pygame
from src import test # importer ce que vs avez besoin

class Room:
    def __init__(self, room_type="normal"):
        self.room_type = room_type
        self.walls = []  # Liste des rectangles pour les murs
        self.doors = []  # Liste des portes (position et état (ouvert, fermé))
        self.is_cleared = False
        self.generate_room()
    
    def generate_room(self):
        # Générer les murs selon le type de salle
        # Positionner les portes
        pass
    
    def open_doors(self):
        # Ouvrir les portes quand la salle est fin
        pass
    
    def draw(self, screen):
        # Dessiner murs + portes
        pass


# Créer src/levels/room.py

# Classe Room avec dimensions, murs et portes

# Méthodes pour dessiner la salle

# Gestion des collisions avec les murs
import pygame
from src import test # importer ce que vs avez besoin

# src/ui/hud.py
class HUD:
    def __init__(self, player, wave_manager, room_manager):
        self.player = player
        self.wave_manager = wave_manager
        self.room_manager = room_manager
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, screen):
        # Afficher toutes les informations
        self.draw_health(screen)
        self.draw_wave_info(screen)
        self.draw_floor_info(screen)
        self.draw_score(screen)
# src/perks/perks_manager.py
import random
from .perks import Perks

class PerksManager:
    def __init__(self, settings, player, weapon):
        self.settings = settings
        self.perks = Perks(settings, player, weapon)
        
        self.perks_dict = {
            "player_speed": self.perks.player_speed,
            "player_attack_speed": self.perks.player_attack_speed,
            "player_attack_damage": self.perks.player_attack_damage,
            "player_max_health": self.perks.player_max_health,
            "player_size_up": self.perks.player_size_up,
            "player_size_down": self.perks.player_size_down,
            "player_regen": self.perks.player_regen,
            "projectil_speed": self.perks.projectile_speed,
            "multishot": self.perks.multishot,
            "infinite life": self.perks.infinite_life
        }

    def get_perks(self) -> list:
        # Ajouter des poids pour
        variable_debug = 1000 # si vs voulez tester l'apparition de certaines perks 
        weights = {
            "player_speed": 10, # COmmun
            "player_attack_speed": 10,
            "player_attack_damage": 10,
            "player_max_health": 10,
            "player_size_up": 5,
            "player_size_down": 2,
            "player_regen": 8,
            "projectil_speed": 10,
            "multishot": variable_debug,  # (Plus rare)
            "infinite life": variable_debug  # (Très rare)
        }
        
        perks_list = list(self.perks_dict.keys())
        weighted_list = []
        for perk in perks_list:
            weighted_list.extend([perk] * weights.get(perk, 5))
        
        selected = []
        while len(selected) < 3:
            choice = random.choice(weighted_list)
            if choice not in selected:
                selected.append(choice)
        
        return selected
    
    def choose_perk(self, perk):
        self.perks_dict[perk]()

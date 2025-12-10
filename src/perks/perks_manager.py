# src/perks/perks_manager.py
import random
from .perks import Perks

class PerksManager:
    def __init__(self, settings, player, weapon):
        self.settings = settings
        self.perks = Perks(settings, player, weapon)
        
        self.perks_dict = {"player_speed":self.perks.player_speed,
                           "player_attack_speed":self.perks.player_attack_speed,
                           "player_attack_damage":self.perks.player_attack_damage,
                           "player_max_health":self.perks.player_max_health,
                           "player_size_up":self.perks.player_size_up,
                           "player_size_down":self.perks.player_size_down,
                           "player_regen":self.perks.player_regen,
                           "projectil_speed":self.perks.projectile_speed
                           }

    def get_perks(self)->list:
        #utiliser des poids plus tard
        perks = []
        for _ in range(3):
            perks.append(random.choice(list(self.perks_dict.keys())))
        return perks
    
    def choose_perk(self, perk):
        self.perks_dict[perk]()

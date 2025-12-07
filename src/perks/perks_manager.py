import random
from .perks import Perks

class PerksManager:
    def __init__(self, settings):
        self.settings = settings
        self.perks = Perks(settings)
        
        self.perks_dict = {"player_speed":self.perks.player_speed,
                           "player_attack_speed":self.perks.player_attack_speed,
                           "player_attack_damage":self.perks.player_attack_damage,
                           "player_health":self.perks.player_health
                           }

    def choose_perks(self)->list:
        #utiliser des poids plus tard
        perks = []
        for _ in range(3):
            perks.append(random.choice(self.perks_dict.keys()))
        return perks

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
            "projectile_speed": self.perks.projectile_speed,
            "multishot": self.perks.multishot,
            "arc_shot": self.perks.arc_shot
        }

    def get_perks(self) -> list:
        # d'ailleurs 
        # 10 => commun
        # 8 => rare
        # 6 => Epique
        # 4 => mythic
        # 2 => Legendaire
        # Ajouter des poids pour
        variable_debug = 1000  # si vous voulez tester l'apparition de certaines perks 
        weights = {
            "player_speed": 10,  # Commun
            "player_attack_speed": 10,
            "player_attack_damage": 10,
            "player_max_health": 10,
            "player_size_up": 10,
            "player_size_down": 9,
            "player_regen": 8,
            "projectile_speed": 8,
            "multishot": 6,  
            "arc_shot": 4   
            # shot_rebounce
            # wall_rebounce
            # zone de dégat autour peri-
            # life steal
            # poison projectile
            # chain lightnig
            # explosive arrow
            # piercing shot
            # homing shot
            # shotgun
            # laser beam
            # area heal
            # shield
            # reflect projectile
            # time slow
            # invincibility
            # double damage 
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
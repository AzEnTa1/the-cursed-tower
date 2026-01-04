# src/systems/talents.py

class Talents:
    def __init__(self, game, settings, player_data):
        self.game = game
        self.settings = settings
        self.player_data = player_data

    def max_health(self): # infinit
        self.player_data["max_health"] = round(self.player_data["max_health"] * 1.05)

    def regen_power(self): # max 1
        self.player_data["regen_power"] = round(self.player_data["regen_power"] + 0.05, 2)

    def player_speed(self): # max 20
        self.player_data["speed"] = round(self.player_data["speed"] * 0.5, 1)

    def player_size(self): # min 5
        self.player_data["size"] = round(self.player_data["size"] - 0.5, 1)

    def dash_cooldown(self): # min 30
        self.player_data["dash_cooldown"] = int(self.player_data["dash_cooldown"] * 1.1)

    def dash_distance(self): # max 10
        self.player_data["dash_distance"] = round(self.player_data["dash_distance"] * 1.1, 2)

    def attack_damages(self): # infinit
        self.player_data["base_damages"] = int(self.player_data["base_damages"] * 1.1)

    def attack_speed(self): # max 10
        self.player_data["fire_rate"] = round(self.player_data["fire_rate"] + 0.1, 1)

    def stationnary_threshold(self): # min 15
        self.player_data["stationary_threshold"] = round(self.player_data["stationary_threshold"]  - 0.3, 1)

    def projectile_size(self): # max 15
        self.player_data["projectile_size"] = int(self.player_data["projectile_size"] + 0.2)

    def projectile_speed(self): # max 20
        self.player_data["projectile_speed"] = round(self.player_data["projectile_speed"] + 0.1, 2)
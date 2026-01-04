# src/systems/talents.py

class Talents:
    def __init__(self, game, settings, player_data):
        self.game = game
        self.settings = settings
        self.player_data = player_data

    def max_health(self):
        self.player_data["max_health"] = round(self.player_data["max_health"] * 1.1)

    def regen_power(self): # NYI
        self.player_data["regen_power"] = round(self.player_data["regen_power"] * 1.1, 2)

    def player_speed(self):
        self.player_data["speed"] = round(self.player_data["speed"] * 1.1, 2)

    def player_size(self):
        self.player_data["size"] = round(self.player_data["size"] / 1.1)

    def dash_cooldown(self): # NYI
        self.player_data["dash_cooldown"] = round(self.player_data["dash_cooldown"] * 1.1)

    def dash_distance(self): # NYI
        self.player_data["dash_distance"] = round(self.player_data["dash_distance"] * 1.1, 2)

    def attack_damages(self):
        self.player_data["base_damages"] = round(self.player_data["base_damages"] * 1.1)

    def attack_speed(self):
        self.player_data["fire_rate"] = round(self.player_data["fire_rate"] * 1.1, 2)

    def stationnary_threshold(self):
        self.player_data["stationary_threshold"] = round(self.player_data["stationary_threshold"] / 1.1)

    def projectile_size(self): # NYI
        self.player_data["projectile_size"] = round(self.player_data["projectile_size"] * 1.1)

    def projectile_speed(self):
        self.player_data["projectile_speed"] = round(self.player_data["projectile_speed"] * 1.1, 2)
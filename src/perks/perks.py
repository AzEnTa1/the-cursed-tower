# src/perks/perks.py
import math 

class Perks:
    def __init__(self, settings, player, weapon):
        self.settings = settings
        self.player = player
        self.weapon = weapon

    def player_speed(self):
        self.player.speed = round(self.player.speed * 1.2)
    
    def player_attack_speed(self):
        self.weapon.fire_rate = round(self.weapon.fire_rate * 1.2)

    def player_attack_damage(self):
        self.weapon.damage = round(self.weapon.damage + 30)

    def player_max_health(self):
        self.player.max_health = round(self.player.max_health + 20)

    def player_size_up(self):
        self.player.size = round(self.player.size * 1.1)

    def player_size_down(self):
        self.player.size = round(self.player.size * 0.9)

    def player_regen(self):
        self.player.health = round(self.player.health + (self.player.max_health * 0.2))
        if self.player.health > self.player.max_health:
            self.player.health = self.player.max_health

    def projectile_speed(self):
        self.weapon.projectile_speed = round(self.weapon.projectile_speed * 1.1)

    def multishot(self):
        """Ajoute un projectile supplémentaire avec intervalle"""
        if hasattr(self.weapon, 'multishot_count'):
            self.weapon.multishot_count += 1
        else:
            self.weapon.multishot_count = 1
            self.weapon.shot_interval = 50  # ms entre chaque projectile
            self.weapon.multishot_timer = 0
            self.weapon.multishot_queue = []

    def infinite_life(self):
        self.player.infinite_life = True

    def arc_shot(self):
        """Active le tir en arc (3 projectiles en éventail)"""
        self.weapon.arc_shot = True
        self.weapon.arc_angle = math.radians(15)  # Angle de 15 degrés entre les projectiles

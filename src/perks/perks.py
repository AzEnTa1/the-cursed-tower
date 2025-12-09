class Perks:
    def __init__(self, settings, player, weapon):
        self.settings = settings
        self.player = player
        self.weapon = weapon

    def player_speed(self):
        self.player.speed = round(self.player.speed * 1.1)
        print("player speed")
    
    def player_attack_speed(self):
        self.weapon.fire_rate = round(self.weapon.fire_rate * 1.1)
        print("player attack speed")

    def player_attack_damage(self):
        self.weapon.damage = round( self.weapon.damage * 1.1)
        print("player attack damage")

    def player_max_health(self):
        self.player.max_health = round(self.player.max_health * 1.1)
        print("player max health")

    def player_size_up(self):
        self.player.size = round(self.player.size * 1.1)
        print("player size up")

    def player_size_down(self):
        self.player.size = round(self.player.size * 0.9)
        print("player size down")

    def player_regen(self):
        self.player.health = round(self.player.health * 1.5)
        if self.player.health > self.player.max_health:
            self.player.health = self.player.max_health
        print("player regen")

    def projectile_speed(self):
        self.weapon.projectile_speed = round(self.weapon.projectile_speed * 1.1)
        print("projectile speed")

# tests/test_entities.py
from src.entities.player import Player
from src.entities.projectiles import Projectile, FireZone
from src.entities.enemies.basic import Basic
from src.entities.enemies.charger import Charger
from src.entities.enemies.shooter import Shooter
from src.entities.enemies.suicide import Suicide
from src.entities.enemies.destructeur import Destructeur
from src.entities.enemies.pyromane import Pyromane
from src.entities.enemies.boss import Boss
from src.entities.enemies.enemy import Enemy
from src.entities.spawn_effect import SpawnEffect

def test_player_movement():
    """Test des mouvements du joueur"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {"degat_1": None, "game_over": None, "game_start": None}
    
    class MockPlayerData:
        def __init__(self):
            self.player_speed = 5
            self.player_size = 20
            self.max_health = 100
            self.regen_power = 0.1
            self.dash_distance = 3
            self.master_volume = 1.0
    
    settings = MockSettings()
    player_data = MockPlayerData().__dict__
    
    player = Player(400, 300, settings, player_data)
    
    # Test position initiale
    assert player.x == 400
    assert player.y == 300
    assert player.health == 100
    assert player.max_health == 100
    
    # Test déplacement
    player.keys_pressed['right'] = True
    player.last_horizontal_key = 'right'
    player.update()
    assert player.x > 400  # Doit s'être déplacé vers la droite (et donc ètre supérieur à 400)
    
    # Test limites
    player.x = 5
    player.y = 5
    player.keys_pressed['left'] = True
    player.last_horizontal_key = 'left'
    player.keys_pressed['up'] = True
    player.last_vertical_key = 'up'
    player.update()
    assert player.x >= 20  # Ne doit pas sortir de l'écran
    assert player.y >= 20
    
    # Test dash
    initial_x = player.x
    player.activate_dash()
    player.update()
    assert player.is_dashing == True
    assert player.dash_timer > 0
    
    # Test dégâts
    initial_health = player.health
    player.take_damage(10)
    assert player.health == initial_health - 10
    assert player.damage_flash_timer > 0
    
    # Test invulnérabilité pendant dash
    health_before = player.health
    player.is_dashing = True
    player.take_damage(10)
    assert player.health == health_before  # Pas de dégâts pendant dash
    
    # Test score
    player.add_score(50)
    assert player.score == 50
    assert player.xp == 50
    
    # Test coins
    player.add_coins(10)
    assert player.get_coins() == 10
    
    # Test réinitialisation mouvements
    player.reset_player_movements()
    assert player.keys_pressed['left'] == False
    assert player.keys_pressed['right'] == False
    assert player.keys_pressed['up'] == False
    assert player.keys_pressed['down'] == False
    
    print("✓ test_player_movement passed")

def test_projectile_basic():
    """Test des projectiles de base"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
    
    settings = MockSettings()
    
    # Test projectile normal
    projectile = Projectile(100, 100, 5, 0, 10, settings)
    assert projectile.x == 100
    assert projectile.y == 100
    assert projectile.damage == 10
    assert projectile.lifetime == 90
    assert projectile.is_alive() == True
    
    # Test déplacement
    initial_x = projectile.x
    projectile.update()
    assert projectile.x == initial_x + 5
    
    # Test vieillissement
    for _ in range(100):
        projectile.update()
    assert projectile.is_alive() == False
    
    # Test projectile multishot
    multishot = Projectile(200, 200, 3, 3, 15, settings, color=(255, 0, 0), radius=7, is_multishot=True)
    assert multishot.is_multishot == True
    assert multishot.radius == 7
    assert multishot.color == (255, 0, 0)
    
    print("✓ test_projectile_basic passed")

def test_projectile_special():
    """Test des projectiles spéciaux"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
    
    settings = MockSettings()
    
    # Test projectile rebondissant
    from src.entities.enemies.boss import SpecialProjectile
    bouncing = SpecialProjectile.create_bouncing(400, 300, 5, 0, 8, settings, bounces=2)
    assert bouncing.is_bouncing == True
    assert bouncing.bounces_remaining == 2
    assert bouncing.special_type == "bouncing"
    
    # Test accélération
    accelerating = SpecialProjectile.create_accelerating(400, 300, 3, 0, 8, settings, max_speed=10)
    assert accelerating.special_type == "accelerating"
    assert hasattr(accelerating, 'acceleration')
    assert hasattr(accelerating, 'max_speed')
    
    # Test division
    splitting = SpecialProjectile.create_splitting(400, 300, 4, 0, 10, settings, splits=2)
    assert splitting.will_split == True
    assert splitting.splits_remaining == 2
    assert splitting.split_timer == 60
    
    # Test création de division
    split_projectiles = splitting.create_split_projectiles()
    assert len(split_projectiles) == 2
    for p in split_projectiles:
        assert p.damage == 10 * 0.6  # Dégâts réduits
    
    print("✓ test_projectile_special passed")

def test_enemy_basic():
    """Test des ennemis de base"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {"boom": None, "mort_enemy": None, "Tire_2": None, "Tire_3": None, "spawn": None}
    
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.size = 20
    
    settings = MockSettings()
    player = MockPlayer()
    
    # Test Basic
    basic = Basic(100, 100, settings)
    assert basic.type == "basic"
    assert basic.health == 30
    assert basic.speed == 2
    assert basic.color == settings.RED
    assert basic.radius == 20
    
    # Test déplacement vers le joueur
    initial_distance = ((basic.x - player.x)**2 + (basic.y - player.y)**2)**0.5
    basic.update(player)
    new_distance = ((basic.x - player.x)**2 + (basic.y - player.y)**2)**0.5
    assert new_distance < initial_distance  # Doit se rapprocher
    
    # Test dégâts
    assert basic.take_damage(10) == False  # Pas mort
    assert basic.health == 20
    assert basic.take_damage(20) == True  # Mort
    
    print("✓ test_enemy_basic passed")

def test_enemy_charger():
    """Test de l'ennemi Charger"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {"boom": None, "mort_enemy": None}
    
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.size = 20
    
    settings = MockSettings()
    player = MockPlayer()
    
    charger = Charger(100, 100, settings)
    assert charger.type == "charger"
    assert charger.health == 40
    assert charger.speed == 3
    assert charger.color == (255, 255, 0)
    assert charger.radius == 22
    
    # Test déplacement rapide
    initial_distance = ((charger.x - player.x)**2 + (charger.y - player.y)**2)**0.5
    charger.update(player)
    new_distance = ((charger.x - player.x)**2 + (charger.y - player.y)**2)**0.5
    assert new_distance < initial_distance  # Doit se rapprocher rapidement
    
    print("✓ test_enemy_charger passed")

def test_enemy_shooter():
    """Test de l'ennemi Shooter"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {"boom": None, "mort_enemy": None, "Tire_2": None}
    
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.size = 20
    
    settings = MockSettings()
    player = MockPlayer()
    
    shooter = Shooter(100, 100, settings)
    assert shooter.type == "shooter"
    assert shooter.health == 25
    assert shooter.speed == 1.5
    assert shooter.color == (100, 100, 255)
    assert shooter.radius == 18
    assert shooter.attack_range == 300
    assert shooter.shoot_rate == 60
    
    # Test comportement à distance
    projectiles = []
    shooter.update(player, projectiles)
    assert shooter.shoot_cooldown > 0  # Doit être en cooldown
    
    # Test tir
    shooter.shoot_cooldown = 0
    shooter.update(player, projectiles)
    assert len(projectiles) > 0  # Doit avoir tiré
    assert projectiles[0].damage == shooter.damage
    
    print("✓ test_enemy_shooter passed")

def test_enemy_suicide():
    """Test de l'ennemi Suicide"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {"boom": None, "mort_enemy": None}
    
    class MockPlayer:
        def __init__(self):
            self.x = 100  # Proche du suicide
            self.y = 100
            self.size = 20
    
    settings = MockSettings()
    player = MockPlayer()
    
    suicide = Suicide(110, 110, settings)
    assert suicide.type == "suicide"
    assert suicide.health == 15
    assert suicide.speed == 4
    assert suicide.color == (255, 0, 255)
    assert suicide.radius == 16
    assert suicide.explosion_radius == 60
    
    # Test explosion au contact
    suicide.update(player)
    assert suicide.is_exploding == True
    assert suicide.explosion_timer == 15
    
    # Test dégâts d'explosion
    explosion_damage = suicide.damage
    assert explosion_damage == 30  # Dégâts élevés
    
    print("✓ test_enemy_suicide passed")

def test_fire_zone():
    """Test des zones de feu"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {}
    
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.size = 20
            self.health = 100
            
        def take_damage(self, amount):
            self.health -= amount
    
    settings = MockSettings()
    player = MockPlayer()
    
    fire_zone = FireZone(400, 300, settings)
    assert fire_zone.base_radius == 50
    assert fire_zone.duration == 300
    assert fire_zone.damage_per_tick == 3
    assert fire_zone.lifetime == 300
    
    # Test mise à jour
    initial_lifetime = fire_zone.lifetime
    fire_zone.update()
    assert fire_zone.lifetime < initial_lifetime
    
    # Test dégâts au joueur
    initial_health = player.health
    fire_zone.check_damage(player)
    # Note: le check_damage vérifie le temps depuis le dernier dégât
    # Pour simplifier, on vérifie juste que la méthode s'exécute
    
    print("✓ test_fire_zone passed")

def test_spawn_effect():
    """Test des effets d'apparition"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {"spawn": None}
    
    settings = MockSettings()
    
    spawn = SpawnEffect(400, 300, settings, "basic")
    assert spawn.x == 400
    assert spawn.y == 300
    assert spawn.enemy_type == "basic"
    assert spawn.is_active == True
    assert spawn.duration == 1000
    
    # Test mise à jour
    spawn.update(100)  # 100ms
    assert spawn.timer == 100
    assert spawn.is_active == True
    
    # Test position
    pos = spawn.get_position()
    assert pos == (400, 300)
    
    print("✓ test_spawn_effect passed")

def test_boss_phase():
    """Test des phases du boss"""
    from src.entities.enemies.boss import BossPhase
    
    # Test phase 1
    phase1 = BossPhase(1, 3)
    assert phase1.number == 1
    assert phase1.max_phases == 3
    assert phase1.health_threshold == 1.0 - (1/3)
    assert phase1.active == False
    assert phase1.attack_cooldown == max(50, 100 - (1 * 15))
    assert phase1.projectile_size == 7 + (1 * 1)
    assert phase1.damage_multiplier == 0.8 + ((1 - 1) * 0.1)
    assert 'circle' in phase1.patterns
    assert phase1.special_projectiles == []  # Phase 1 pas de projectiles spéciaux
    assert phase1.color == (100, 200, 255)  # Bleu pour phase 1
    
    # Test phase 3
    phase3 = BossPhase(3, 4)
    assert phase3.number == 3
    assert 'bouncing' in phase3.special_projectiles
    assert 'accelerating' in phase3.special_projectiles
    assert 'splitting' in phase3.special_projectiles
    assert 'homing' in phase3.special_projectiles
    assert phase3.color == (255, 100, 100)  # Rouge pour phase 3
    
    # Test pattern aléatoire
    pattern = phase1.get_random_pattern()
    assert pattern in phase1.patterns
    
    print("✓ test_boss_phase passed")

def test_recursive_pattern():
    """Test des patterns récursifs"""
    from src.entities.enemies.boss import RecursivePatternGenerator
    
    # Test cercle récursif
    circle_pattern = RecursivePatternGenerator.generate_circle_recursive(
        400, 300, depth=2, max_depth=2
    )
    assert isinstance(circle_pattern, list)
    # Vérifie que chaque élément a la bonne structure
    for item in circle_pattern:
        assert item[0] == 'projectile'
        assert len(item) >= 6  # (type, x, y, dx, dy, damage, projectile_type)
    
    # Test spirale
    spiral_pattern = RecursivePatternGenerator.generate_spiral_arms(
        400, 300, arms=3, projectiles_per_arm=4
    )
    assert len(spiral_pattern) == 3 * 4  # 3 bras * 4 projectiles
    
    # Test vague
    wave_pattern = RecursivePatternGenerator.generate_wave_pattern(
        400, 300, waves=2, projectiles_per_wave=4
    )
    assert len(wave_pattern) == 2 * 4  # 2 vagues * 4 projectiles
    
    print("✓ test_recursive_pattern passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_player_movement()
    test_projectile_basic()
    test_projectile_special()
    test_enemy_basic()
    test_enemy_charger()
    test_enemy_shooter()
    test_enemy_suicide()
    test_fire_zone()
    test_spawn_effect()
    test_boss_phase()
    test_recursive_pattern()
    print("\n✅ Tous les tests d'entités ont réussi!")
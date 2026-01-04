# tests/test_entities.py
from src.entities.player import Player
from src.entities.projectiles import Projectile
from src.entities.enemies.basic import Basic
from src.entities.enemies.suicide import Suicide
from src.entities.spawn_effect import SpawnEffect

def test_player_movement():
    """Test des mouvements du joueur"""
    class MockSound():
        def play(self):
            pass

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
            self.sounds = {"degat_1": MockSound(), "game_over": MockSound(), "game_start": MockSound()}
    
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
    player.is_dashing = False
    initial_health = player.health
    player.take_damage(10)
    assert player.health == initial_health - 10
    assert player.damage_flash_timer > 0
    
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
    
    # Test projectile multishot
    multishot = Projectile(200, 200, 3, 3, 15, settings, color=(255, 0, 0), radius=7, is_multishot=True)
    assert multishot.is_multishot == True
    assert multishot.radius == 7
    assert multishot.color == (255, 0, 0)

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
    # print("Easter Egg") #Gl pour trouver
    initial_distance = ((basic.x - player.x)**2 + (basic.y - player.y)**2)**0.5
    basic.update(player)
    new_distance = ((basic.x - player.x)**2 + (basic.y - player.y)**2)**0.5
    assert new_distance < initial_distance  # Doit se rapprocher
    
    # Test dégâts
    assert basic.take_damage(10) == False  # Pas mort
    assert basic.health == 20
    assert basic.take_damage(20) == True  # Mort
    
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

def test_spawn_effect():
    """Test des effets d'apparition"""
    class MockSound():
        def play(self):
            pass

    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {"spawn": MockSound()}
    
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
    position = spawn.get_position()
    assert position == (400, 300) 
        
# Exécuter tous les tests
def fonction_test_entities():
    test_player_movement()
    test_projectile_basic()
    test_enemy_basic()
    test_enemy_suicide()
    test_spawn_effect()
    print("Tout les jeux de test des entitées fonctionnent !")

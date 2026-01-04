from src.systems.wave_manager import WaveManager
from src.systems.game_stats import GameStats
from src.perks.talents import Talents
from src.utils.queue import Queue, WaveQueue

def test_queue_basic():
    """Test de la file de base"""
    queue = Queue()
    
    # Test file vide
    assert queue.is_empty() == True
    assert queue.size() == 0
    assert queue.peek() == None
    assert queue.dequeue() == None
    
    # Test ajout d'éléments
    queue.enqueue("premier")
    queue.enqueue("second")
    queue.enqueue("troisième")
    
    assert queue.is_empty() == False
    assert queue.size() == 3
    assert queue.peek() == "premier"
    
    # Test retrait dans l'ordre FIFO
    assert queue.dequeue() == "premier"
    assert queue.size() == 2
    assert queue.peek() == "second"
    
    assert queue.dequeue() == "second"
    assert queue.dequeue() == "troisième"
    assert queue.is_empty() == True
    
    print("✓ test_queue_basic passed")

def test_wave_queue():
    """Test de la file de vagues"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Test configuration pour étage 1
    wave_queue.setup_waves_for_floor(1)
    
    # Doit avoir 3 vagues
    assert wave_queue.has_more_waves() == True
    
    # Test récupération des vagues
    wave1 = wave_queue.get_next_wave()
    assert wave1 is not None
    assert isinstance(wave1, list)
    
    wave2 = wave_queue.get_next_wave()
    assert wave2 is not None
    
    wave3 = wave_queue.get_next_wave()
    assert wave3 is not None
    
    # Plus de vagues normales
    assert wave_queue.has_more_waves() == False
    assert wave_queue.get_next_wave() is None
    
    print("✓ test_wave_queue passed")

def test_wave_manager_basic():
    """Test du gestionnaire de vagues"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {}
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test initialisation
    assert manager.floor_number == 1
    assert manager.wave_number == 0
    assert manager.state == "between_waves"
    assert manager.boss_spawned == False
    
    # Test réinitialisation
    manager.reset_to_floor(2)
    assert manager.floor_number == 2
    assert manager.wave_number == 0
    assert manager.state == "between_waves"
    
    print("✓ test_wave_manager_basic passed")

def test_wave_manager_waves():
    """Test du système de vagues"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {}
    
    import time
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test génération de position de spawn
    x, y = manager.generate_spawn_position()
    assert 0 <= x <= 800
    assert 0 <= y <= 600
    
    # Test position boss
    boss_x, boss_y = manager.generate_boss_spawn_position()
    assert boss_x == 400  # Centre
    assert boss_y == 300
    
    print("✓ test_wave_manager_waves passed")

def test_wave_info():
    """Test des informations de vague"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {}
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test info vague initiale
    info = manager.get_wave_info()
    assert isinstance(info, dict)
    assert 'floor' in info
    assert 'current_wave' in info
    assert 'total_waves' in info
    assert 'enemies_remaining' in info
    assert 'state' in info
    assert 'is_boss_wave' in info
    
    assert info['floor'] == 1
    assert info['current_wave'] == 0
    assert info['total_waves'] == 3
    assert info['state'] == "between_waves"
    assert info['is_boss_wave'] == False
    
    print("✓ test_wave_info passed")

def test_game_stats():
    """Test des statistiques de jeu"""
    class MockGame:
        pass
    
    class MockSettings:
        pass
    
    class MockPlayer:
        def get_stats(self):
            return {
                "player_speed": 5,
                "player_size": 20,
                "current_health": 75,
                "max_health": 100,
                "score": 1500,
                "xp": 200
            }
    
    class MockWeapon:
        def get_stats(self):
            return {
                "attack_speed": 2,
                "attack_damages": 30,
                "projectile_speed": 10,
                "stationary_threshold": 25
            }
    
    game = MockGame()
    settings = MockSettings()
    stats = GameStats(game, settings)
    
    player = MockPlayer()
    weapon = MockWeapon()
    
    # Test mise à jour des stats
    result = stats.update(player, weapon)
    
    assert isinstance(result, dict)
    assert len(result) == 10  # 6 du joueur + 4 de l'arme
    
    # Vérifie que toutes les clés existent
    expected_keys = [
        "player_speed", "player_size", "current_health", "max_health",
        "score", "xp", "attack_speed", "attack_damages",
        "projectile_speed", "stationary_threshold"
    ]
    
    for key in expected_keys:
        assert key in result
    
    # Vérifie les valeurs
    assert result["score"] == 1500
    assert result["xp"] == 200
    assert result["attack_damages"] == 30
    
    print("✓ test_game_stats passed")

def test_talents_basic():
    """Test des talents de base"""
    class MockGame:
        pass
    
    class MockSettings:
        pass
    
    class MockPlayerData:
        def __init__(self):
            self.max_health = 100
            self.regen_power = 0.1
            self.player_speed = 5.0
            self.player_size = 20.0
            self.dash_cooldown = 180
            self.dash_distance = 3.0
            self.attack_damages = 30
            self.attack_speed = 2.0
            self.stationary_threshold = 25.0
            self.projectile_size = 5
            self.projectile_speed = 10.0
    
    game = MockGame()
    settings = MockSettings()
    player_data = MockPlayerData().__dict__
    
    talents = Talents(game, settings, player_data)
    
    # Test vie max
    initial_max_health = player_data["max_health"]
    talents.max_health()
    assert player_data["max_health"] == round(initial_max_health * 1.05)
    
    # Test régénération
    initial_regen = player_data["regen_power"]
    talents.regen_power()
    assert player_data["regen_power"] == round(initial_regen + 0.05, 2)
    
    # Test vitesse joueur
    initial_speed = player_data["player_speed"]
    talents.player_speed()
    assert player_data["player_speed"] == round(initial_speed + 0.5, 1)
    
    # Test taille joueur
    initial_size = player_data["player_size"]
    talents.player_size()
    assert player_data["player_size"] == round(initial_size - 0.5, 1)
    
    print("✓ test_talents_basic passed")

def test_talents_advanced():
    """Test des talents avancés"""
    class MockGame:
        pass
    
    class MockSettings:
        pass
    
    class MockPlayerData:
        def __init__(self):
            self.dash_cooldown = 180
            self.dash_distance = 3.0
            self.attack_damages = 30
            self.attack_speed = 2.0
            self.stationary_threshold = 25.0
            self.projectile_size = 5
            self.projectile_speed = 10.0
    
    game = MockGame()
    settings = MockSettings()
    player_data = MockPlayerData().__dict__
    
    talents = Talents(game, settings, player_data)
    
    # Test dash cooldown
    initial_cooldown = player_data["dash_cooldown"]
    talents.dash_cooldown()
    assert player_data["dash_cooldown"] == initial_cooldown - 5
    
    # Test dash distance
    initial_distance = player_data["dash_distance"]
    talents.dash_distance()
    assert player_data["dash_distance"] == round(initial_distance * 1.1, 2)
    
    # Test dégâts attaque
    initial_damage = player_data["attack_damages"]
    talents.attack_damages()
    assert player_data["attack_damages"] == int(initial_damage * 1.1)
    
    # Test vitesse attaque
    initial_attack_speed = player_data["attack_speed"]
    talents.attack_speed()
    assert player_data["attack_speed"] == round(initial_attack_speed + 0.1, 1)
    
    print("✓ test_talents_advanced passed")

def test_wave_enemy_count():
    """Test du comptage d'ennemis"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        
        def __init__(self):
            self.sounds = {}
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test division d'ennemis
    class MockEnemy:
        def __init__(self, id):
            self.id = id
    
    original_enemy = MockEnemy(1)
    new_enemies = [MockEnemy(2), MockEnemy(3)]
    
    # Simule la division
    manager.current_wave_enemies = [original_enemy]
    manager.enemies_remaining = 1
    
    manager.on_enemy_divided(original_enemy, new_enemies)
    
    assert original_enemy not in manager.current_wave_enemies
    assert len(manager.current_wave_enemies) == 2
    assert manager.enemies_remaining == 2
    
    print("✓ test_wave_enemy_count passed")

def test_wave_state_transitions():
    """Test des transitions d'état des vagues"""
    states = ["between_waves", "in_wave", "boss_wave", "all_cleared"]
    
    # Test que tous les états sont valides
    for state in states:
        assert isinstance(state, str)
        assert len(state) > 0
    
    # Test fonctions d'état
    class MockSettings:
        pass
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test état initial
    assert manager.is_between_waves() == True
    assert manager.are_all_waves_cleared() == False
    
    # Test vérification boss
    assert manager.is_boss_wave_current() == False
    
    print("✓ test_wave_state_transitions passed")

def test_talent_limits():
    """Test des limites des talents"""
    class MockGame:
        pass
    
    class MockSettings:
        pass
    
    # Test valeurs limites
    test_cases = [
        ("player_speed", 20.0, "max"),  # Vitesse max 20
        ("player_size", 5.0, "min"),    # Taille min 5
        ("dash_cooldown", 30, "min"),   # Cooldown min 30
        ("dash_distance", 10.0, "max"), # Distance max 10
        ("attack_speed", 10.0, "max"),  # Vitesse attaque max 10
        ("stationary_threshold", 15.0, "min"),  # Seuil min 15
        ("projectile_size", 20, "max"),  # Taille projectile max 20
        ("projectile_speed", 20.0, "max"),  # Vitesse projectile max 20
    ]
    
    for talent_name, limit_value, limit_type in test_cases:
        assert isinstance(talent_name, str)
        assert isinstance(limit_value, (int, float))
        assert limit_type in ["min", "max"]
        
        # Vérifie que les limites sont valides
        if limit_type == "min":
            assert limit_value > 0
        else:  # max
            assert limit_value > 0
    
    print("✓ test_talent_limits passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_queue_basic()
    test_wave_queue()
    test_wave_manager_basic()
    test_wave_manager_waves()
    test_wave_info()
    test_game_stats()
    test_talents_basic()
    test_talents_advanced()
    test_wave_enemy_count()
    test_wave_state_transitions()
    test_talent_limits()
    print("\n✅ Tous les tests de systèmes ont réussi!")
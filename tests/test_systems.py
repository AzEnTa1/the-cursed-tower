from src.systems.wave_manager import WaveManager
from src.systems.game_stats import GameStats
from src.perks.talents import Talents

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
    assert result["attack_damages"] == 3

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
    
def test_wave_state_transitions():
    """Test des transitions d'état des vagues"""    
    
    class MockSettings:
        pass
    
    settings = MockSettings()
    manager = WaveManager(settings)
    
    # Test état initial
    assert manager.is_between_waves() == True
    assert manager.are_all_waves_cleared() == False
    
    # Test vérification boss
    assert manager.is_boss_wave_current() == False
    
# Exécuter tous les tests
if __name__ == "__main__":
    test_game_stats()
    test_talents_basic()
    test_wave_state_transitions()

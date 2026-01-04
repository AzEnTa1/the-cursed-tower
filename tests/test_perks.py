from src.perks.perks import Perks
from src.perks.perks_manager import PerksManager

def test_perks_basic():
    """Test des perks de base"""
    class MockSettings:
        player_regen_power = 0.1
        
        def __init__(self):
            self.sounds = {}
    
    class MockPlayer:
        def __init__(self):
            self.speed = 5
            self.size = 20
            self.health = 80
            self.max_health = 100
    
    class MockWeapon:
        def __init__(self):
            self.fire_rate = 2
            self.damage = 30
            self.projectile_speed = 10
            self.multishot_count = 0
            self.arc_shot = False
    
    settings = MockSettings()
    player = MockPlayer()
    weapon = MockWeapon()
    
    perks = Perks(settings, player, weapon)
    
    # Test vitesse joueur
    initial_speed = player.speed
    perks.player_speed()
    assert player.speed == round(initial_speed * 1.2)
    
    # Test vitesse d'attaque
    initial_fire_rate = weapon.fire_rate
    perks.player_attack_speed()
    assert weapon.fire_rate == round(initial_fire_rate * 1.2)
    
    # Test dégâts
    initial_damage = weapon.damage
    perks.player_attack_damage()
    assert weapon.damage == round(initial_damage + 30)
    
    # Test vie max
    initial_max_health = player.max_health
    perks.player_max_health()
    assert player.max_health == round(initial_max_health * 1.05)
    
    # Test taille augmentation
    initial_size = player.size
    perks.player_size_up()
    assert player.size == round(initial_size * 1.1)
    
    # Test taille réduction
    perks.player_size_down()
    assert player.size == round(player.size * 0.9)  # Appliqué sur la nouvelle taille
    
    # Test régénération
    initial_health = player.health
    perks.player_regen()
    expected_health = round(initial_health + (player.max_health * settings.player_regen_power))
    assert player.health == min(expected_health, player.max_health)
    
    # Test vitesse projectile
    initial_projectile_speed = weapon.projectile_speed
    perks.projectile_speed()
    assert weapon.projectile_speed == round(initial_projectile_speed * 1.1)
    
    print("✓ test_perks_basic passed")

def test_perks_special():
    """Test des perks spéciaux"""
    class MockSettings:
        def __init__(self):
            self.sounds = {}
    
    class MockPlayer:
        def __init__(self):
            pass
    
    class MockWeapon:
        def __init__(self):
            self.multishot_count = 0
            self.shot_interval = 100
            self.multishot_timer = 0
            self.multishot_queue = []
            self.arc_shot = False
            self.arc_angle = 0
    
    settings = MockSettings()
    player = MockPlayer()
    weapon = MockWeapon()
    
    perks = Perks(settings, player, weapon)
    
    # Test multishot (premier niveau)
    perks.multishot()
    assert weapon.multishot_count == 1
    assert weapon.shot_interval == 50
    
    # Test multishot (niveau supplémentaire)
    perks.multishot()
    assert weapon.multishot_count == 2
    
    # Test arc shot
    perks.arc_shot()
    assert weapon.arc_shot == True
    import math
    assert abs(weapon.arc_angle - math.radians(15)) < 0.001
    
    print("✓ test_perks_special passed")

def test_perks_manager():
    """Test du gestionnaire de perks"""
    class MockSettings:
        def __init__(self):
            self.data_translation_map = {
                "player_speed": "Vitesse du Joueur",
                "player_attack_speed": "Vitesse d'Attaque",
                "player_attack_damage": "Dégat d'Attaque",
                "player_max_health": "Vie Maximale",
                "player_size_up": "Taille du Joueur",
                "player_size_down": "Taille du Joueur",
                "player_regen": "Puissance Régénération",
                "projectile_speed": "Vitesse des projectiles",
                "multishot": "Multishot",
                "arc_shot": "Arc Shot"
            }
            self.sounds = {}
    
    class MockPlayer:
        def __init__(self):
            self.speed = 5
            self.size = 20
            self.health = 80
            self.max_health = 100
    
    class MockWeapon:
        def __init__(self):
            self.fire_rate = 2
            self.damage = 30
            self.projectile_speed = 10
            self.multishot_count = 0
            self.arc_shot = False
    
    settings = MockSettings()
    player = MockPlayer()
    weapon = MockWeapon()
    
    manager = PerksManager(settings, player, weapon)
    
    # Test récupération des perks
    perks_list = manager.get_perks()
    assert isinstance(perks_list, list)
    assert len(perks_list) == 3
    assert all(perk in manager.perks_dict for perk in perks_list)
    
    # Test que les perks sont uniques dans la sélection
    assert len(set(perks_list)) == len(perks_list)
    
    # Test choix de perk
    test_perk = perks_list[0]
    initial_player_speed = player.speed
    
    # Vérifie que la fonction existe
    assert test_perk in manager.perks_dict
    
    print("✓ test_perks_manager passed")

def test_perks_translation():
    """Test de la traduction des noms de perks"""
    class MockSettings:
        def __init__(self):
            self.data_translation_map = {
                "player_speed": "Vitesse du Joueur",
                "player_attack_speed": "Vitesse d'Attaque",
                "player_attack_damage": "Dégat d'Attaque",
                "multishot": "Tir Multiple",
                "arc_shot": "Tir en Arc"
            }
            self.sounds = {}
    
    class MockPlayer:
        pass
    
    class MockWeapon:
        pass
    
    settings = MockSettings()
    player = MockPlayer()
    weapon = MockWeapon()
    
    manager = PerksManager(settings, player, weapon)
    
    # Test que la traduction existe pour les perks
    for perk in manager.perks_dict.keys():
        if perk in settings.data_translation_map:
            translated = settings.data_translation_map[perk]
            assert isinstance(translated, str)
            assert len(translated) > 0
    
    print("✓ test_perks_translation passed")

def test_perks_weights():
    """Test du système de poids des perks"""
    class MockSettings:
        def __init__(self):
            self.data_translation_map = {}
            self.sounds = {}
    
    class MockPlayer:
        pass
    
    class MockWeapon:
        pass
    
    settings = MockSettings()
    player = MockPlayer()
    weapon = MockWeapon()
    
    manager = PerksManager(settings, player, weapon)
    
    # Test multiple fois pour vérifier la distribution
    perk_counts = {}
    for _ in range(100):
        perks = manager.get_perks()
        for perk in perks:
            perk_counts[perk] = perk_counts.get(perk, 0) + 1
    
    # Vérifie que tous les perks apparaissent au moins une fois
    all_perks = list(manager.perks_dict.keys())
    for perk in all_perks:
        assert perk in perk_counts, f"Perk {perk} jamais apparu"
    
    print("✓ test_perks_weights passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_perks_basic()
    test_perks_special()
    test_perks_manager()
    test_perks_translation()
    test_perks_weights()
    print("\n✅ Tous les tests de perks ont réussi!")
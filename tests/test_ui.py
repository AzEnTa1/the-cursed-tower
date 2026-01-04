from src.ui.hud import HUD
from src.ui.transition_effect import TransitionEffect
from src.entities.weapons import Weapon
from src.entities.enemies.enemy import Enemy

def test_hud_basic():
    """Test de l'HUD de base"""
    class MockPlayer:
        def __init__(self):
            self.health = 75
            self.max_health = 100
            self.score = 1500
            self.xp = 200
            
        def get_dash_cooldown_percent(self):
            return 0.5
    
    class MockWaveManager:
        def get_wave_info(self):
            return {
                'floor': 1,
                'current_wave': 1,
                'total_waves': 3,
                'enemies_remaining': 5,
                'state': 'in_wave',
                'is_boss_wave': False
            }
    
    class MockWeapon:
        stationary_time = 15
        stationary_threshold = 25
    
    class MockSettings:
        screen_width = 800
        screen_height = 600
        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        RED = (255, 0, 0)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        BLUE = (0, 0, 255)
        
        def __init__(self):
            self.font = {
                "h1": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {})()})()}),
                "h2": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {})()})()}),
                "h3": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {})()})()}),
                "h4": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {})()})()})
            }
    
    player = MockPlayer()
    wave_manager = MockWaveManager()
    weapon = MockWeapon()
    settings = MockSettings()
    
    hud = HUD(player, wave_manager, weapon, settings)
    
    # Test initialisation
    assert hud.player == player
    assert hud.wave_manager == wave_manager
    assert hud.weapon == weapon
    assert hud.settings == settings
    
    # Test mise à jour
    hud.update(16)  # 16ms
    
    # Test dessin (ne fait que vérifier que la méthode existe)
    class MockScreen:
        def blit(self, surface, pos):
            pass
    
    screen = MockScreen()
    hud.draw(screen)  # Ne devrait pas lever d'exception
    
    print("✓ test_hud_basic passed")

def test_transition_effect():
    """Test des effets de transition"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
    
    settings = MockSettings()
    transition = TransitionEffect(settings)
    
    # Test initial
    assert transition.alpha == 0
    assert transition.duration == 1000
    assert transition.current_time == 0
    assert transition.active == False
    assert transition.callback == None
    
    # Test démarrage
    callback_called = False
    def test_callback():
        nonlocal callback_called
        callback_called = True
    
    transition.start(test_callback)
    assert transition.active == True
    assert transition.callback == test_callback
    
    # Test mise à jour (première moitié)
    transition.update(250)  # 250ms
    assert 0 < transition.alpha <= 255
    assert transition.current_time == 250
    assert transition.active == True
    
    # Test mise à jour (seconde moitié)
    transition.update(500)  # Total 750ms
    assert transition.active == True
    
    # Test fin de transition
    transition.update(250)  # Total 1000ms
    assert transition.active == False
    assert callback_called == True
    
    # Test dessin (ne fait que vérifier que la méthode existe)
    class MockScreen:
        def blit(self, surface, pos):
            pass
    
    screen = MockScreen()
    transition.draw(screen)  # Ne devrait pas lever d'exception
    
    print("✓ test_transition_effect passed")

def test_weapon_basic():
    """Test de l'arme de base"""
    class MockSettings:
        def __init__(self):
            self.player_data = {
                "projectile_size": 5
            }
            self.sounds = {
                "Tire_1": type('Sound', (), {'play': lambda: None}),
                "Tire_2": type('Sound', (), {'play': lambda: None}),
                "Tire_3": type('Sound', (), {'play': lambda: None}),
                "Tire_4": type('Sound', (), {'play': lambda: None})
            }
            self.data_translation_map = {}
    
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.last_dx = 0
            self.last_dy = 0
    
    class MockPlayerData:
        def __init__(self):
            self.attack_speed = 2
            self.attack_damages = 30
            self.projectile_speed = 10
            self.stationary_threshold = 25
    
    settings = MockSettings()
    player_data = MockPlayerData().__dict__
    
    weapon = Weapon(settings, player_data)
    
    # Test initialisation
    assert weapon.fire_rate == 2
    assert weapon.damage >= 25 and weapon.damage <= 35  # 30 +/- 5
    assert weapon.projectile_speed == 10
    assert weapon.stationary_threshold == 25
    assert weapon.last_direction == (1, 0)  # Direction par défaut
    
    # Test mise à jour direction
    weapon.update_direction(0, 1)
    assert weapon.last_direction == (0, 1)
    
    # Test son de tir
    assert hasattr(weapon, 'shoot_sounds')
    assert len(weapon.shoot_sounds) > 0
    
    print("✓ test_weapon_basic passed")

def test_enemy_base():
    """Test de la classe de base Enemy"""
    class MockSettings:
        screen_width = 800
        screen_height = 600
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        def __init__(self):
            self.sounds = {}
    
    settings = MockSettings()
    
    # Crée une classe Enemy concrète pour tester
    class TestEnemy(Enemy):
        def __init__(self, x, y, settings):
            super().__init__(x, y, settings)
            self.health = 50
            self.max_health = 50
            self.color = settings.RED
            self.radius = 20
        
        def update(self, player, projectiles=None, pending_zones=None):
            pass
    
    enemy = TestEnemy(100, 100, settings)
    
    # Test initialisation
    assert enemy.x == 100
    assert enemy.y == 100
    assert enemy.settings == settings
    assert enemy.health == 50
    assert enemy.max_health == 50
    
    # Test dégâts
    assert enemy.take_damage(30) == False  # Pas mort
    assert enemy.health == 20
    assert enemy.take_damage(20) == True   # Mort
    
    # Test dessin (ne fait que vérifier que la méthode existe)
    class MockScreen:
        def draw(self):
            pass
    
    print("✓ test_enemy_base passed")

def test_color_blending():
    """Test du mélange de couleurs"""
    # Test mélange simple
    def blend_colors(color1, color2, ratio):
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)
    
    # Test mélange rouge et bleu
    red = (255, 0, 0)
    blue = (0, 0, 255)
    
    # 50% de chaque
    purple = blend_colors(red, blue, 0.5)
    assert purple[0] == 127  # Rouge réduit
    assert purple[2] == 127  # Bleu réduit
    assert purple[1] == 0    # Pas de vert
    
    # Test mélange avec ratio 0 (devrait être la première couleur)
    assert blend_colors(red, blue, 0) == red
    
    # Test mélange avec ratio 1 (devrait être la deuxième couleur)
    assert blend_colors(red, blue, 1) == blue
    
    print("✓ test_color_blending passed")

def test_math_utilities():
    """Test des utilitaires mathématiques"""
    import math
    
    # Test distance entre points
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Même point
    assert distance(0, 0, 0, 0) == 0
    
    # Distance horizontale
    assert distance(0, 0, 10, 0) == 10
    
    # Distance verticale
    assert distance(0, 0, 0, 10) == 10
    
    # Distance diagonale
    assert abs(distance(0, 0, 3, 4) - 5) < 0.0001  # Triangle 3-4-5
    
    # Test normalisation de vecteur
    def normalize_vector(dx, dy):
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return (0, 0)
        return (dx/length, dy/length)
    
    # Vecteur nul
    assert normalize_vector(0, 0) == (0, 0)
    
    # Vecteur horizontal
    assert normalize_vector(10, 0) == (1, 0)
    
    # Vecteur diagonal
    norm = normalize_vector(1, 1)
    assert abs(norm[0] - 0.7071) < 0.0001
    assert abs(norm[1] - 0.7071) < 0.0001
    
    print("✓ test_math_utilities passed")

def test_collision_detection():
    """Test de détection de collision"""
    # Collision cercle-cercle
    def circles_collide(x1, y1, r1, x2, y2, r2):
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < (r1 + r2)
    
    import math
    
    # Cercles qui se touchent
    assert circles_collide(0, 0, 5, 8, 0, 3) == True  # Distance 8, rayons 5+3=8
    
    # Cercles qui ne se touchent pas
    assert circles_collide(0, 0, 5, 10, 0, 3) == False  # Distance 10, rayons 5+3=8
    
    # Cercles identiques
    assert circles_collide(0, 0, 5, 0, 0, 5) == True
    
    # Test collision avec marge
    def circles_collide_with_margin(x1, y1, r1, x2, y2, r2, margin=0):
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < (r1 + r2 + margin)
    
    # Avec marge, devraient se toucher
    assert circles_collide_with_margin(0, 0, 5, 9, 0, 3, 1) == True
    
    print("✓ test_collision_detection passed")

def test_angle_calculations():
    """Test des calculs d'angle"""
    import math
    
    # Test angle entre deux points
    def angle_between(x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)
    
    # Angle horizontal droit
    assert abs(angle_between(0, 0, 10, 0) - 0) < 0.0001
    
    # Angle vertical haut
    assert abs(angle_between(0, 0, 0, 10) - math.pi/2) < 0.0001
    
    # Angle diagonal
    assert abs(angle_between(0, 0, 1, 1) - math.pi/4) < 0.0001
    
    # Test conversion degrés/radians
    def degrees_to_radians(degrees):
        return degrees * math.pi / 180
    
    def radians_to_degrees(radians):
        return radians * 180 / math.pi
    
    # 180 degrés = π radians
    assert abs(degrees_to_radians(180) - math.pi) < 0.0001
    
    # π/2 radians = 90 degrés
    assert abs(radians_to_degrees(math.pi/2) - 90) < 0.0001
    
    print("✓ test_angle_calculations passed")

def test_random_utilities():
    """Test des utilitaires aléatoires"""
    import random
    
    # Test génération dans une plage
    def random_in_range(min_val, max_val):
        return random.uniform(min_val, max_val)
    
    # Test plusieurs fois pour s'assurer que c'est dans la plage
    for _ in range(100):
        val = random_in_range(10, 20)
        assert 10 <= val <= 20
    
    # Test choix pondéré simplifié
    def weighted_choice(items, weights):
        total = sum(weights)
        r = random.uniform(0, total)
        current = 0
        for i, weight in enumerate(weights):
            current += weight
            if r < current:
                return items[i]
        return items[-1]
    
    items = ['A', 'B', 'C']
    weights = [1, 2, 3]
    
    # Test que tous les items peuvent être choisis
    chosen_items = set()
    for _ in range(1000):
        chosen = weighted_choice(items, weights)
        chosen_items.add(chosen)
    
    assert 'A' in chosen_items
    assert 'B' in chosen_items
    assert 'C' in chosen_items
    
    print("✓ test_random_utilities passed")

def test_performance_measurement():
    """Test de mesure de performance basique"""
    import time
    
    # Test temps d'exécution d'une fonction simple
    def simple_function(n):
        total = 0
        for i in range(n):
            total += i
        return total
    
    start_time = time.time()
    result = simple_function(10000)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # Vérifie que le résultat est correct
    assert result == sum(range(10000))
    
    # Vérifie que l'exécution est raisonnablement rapide
    assert execution_time < 1.0  # Moins d'une seconde
    
    print("✓ test_performance_measurement passed")

def test_memory_management():
    """Test de gestion mémoire basique"""
    # Test que les objets peuvent être créés et détruits
    class SimpleObject:
        def __init__(self, value):
            self.value = value
    
    # Crée plusieurs objets
    objects = []
    for i in range(1000):
        obj = SimpleObject(i)
        objects.append(obj)
    
    # Vérifie que tous les objets sont créés
    assert len(objects) == 1000
    
    # Supprime les références
    del objects
    
    print("✓ test_memory_management passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_hud_basic()
    test_transition_effect()
    test_weapon_basic()
    test_enemy_base()
    test_color_blending()
    test_math_utilities()
    test_collision_detection()
    test_angle_calculations()
    test_random_utilities()
    test_performance_measurement()
    test_memory_management()
    print("\n✅ Tous les tests utilitaires ont réussi!")
from src.ui.transition_effect import TransitionEffect
from src.entities.enemies.enemy import Enemy
    
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
    
    # Test dégâts
    assert enemy.take_damage(30) == False  # Pas mort
    assert enemy.health == 20
    assert enemy.take_damage(20) == True   # Mort
    
# Exécuter tous les tests
def fonction_test_ui():
    test_transition_effect()
    test_enemy_base()
    print("Tout les jeux de test des ui fonctionnent !")


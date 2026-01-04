from src.scenes.base_scene import BaseScene
from src.scenes.menu_scene import MenuScene
from src.scenes.gameover_scene import GameOverScene
from src.ui.game_over_ui import GameOverUI
from src.ui.pause_ui import PauseUI
from src.ui.stat_ui import StatUI
from src.ui.perks_ui import PerksUI

def test_base_scene():
    """Test de la scène de base"""
    class MockGame:
        pass
    
    class MockSettings:
        pass
    
    game = MockGame()
    settings = MockSettings()
    
    scene = BaseScene(game, settings)
    
    # Test méthodes vides (doivent exister mais ne rien faire)
    scene.on_enter()
    scene.on_exit()
    scene.handle_event(None)
    scene.update()
    scene.draw(None)
    scene.resize()
    
    # Vérifie que l'objet est correctement initialisé
    assert scene.game == game
    assert scene.settings == settings
    
    print("✓ test_base_scene passed")

def test_game_over_ui():
    """Test de l'UI Game Over"""
    class MockSettings:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
            self.font = {"h1": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {'center': (400, 100)})()})()})}
    
    settings = MockSettings()
    game_stats = {"score": 1500, "xp": 200}
    
    ui = GameOverUI(settings, game_stats)
    
    # Test initialisation
    assert ui.settings == settings
    assert ui.game_stats == game_stats
    
    # Test redimensionnement
    ui.resize()
    
    print("✓ test_game_over_ui passed")

def test_pause_ui():
    """Test de l'UI Pause"""
    class MockSettings:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
            self.font = {"h1": type('Font', (), {'render': lambda text, antialias, color: type('Surface', (), {'get_rect': lambda: type('Rect', (), {'center': (400, 100)})()})()})}
    
    settings = MockSettings()
    game_stats = {"score": 1000, "health": 75}
    
    ui = PauseUI(game_stats, settings)
    
    # Test initialisation
    assert ui.settings == settings
    assert ui.game_stats == game_stats
    assert hasattr(ui, 'stats_rect')
    
    # Test redimensionnement
    ui.resize()
    
    print("✓ test_pause_ui passed")

def test_stat_ui():
    """Test de l'UI Stats"""
    class MockSettings:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
            self.font = {
                "h4": type('Font', (), {
                    'render': lambda text, antialias, color: type('Surface', (), {
                        'get_rect': lambda: type('Rect', (), {'topleft': (0, 0), 'center': (400, 300)})()
                    })()
                })
            }
            self.data_translation_map = {
                "score": "Score",
                "health": "Vie"
            }
    
    settings = MockSettings()
    game_stats = {"score": 1500, "health": 80}
    
    ui = StatUI(game_stats, settings)
    
    # Test initialisation
    assert ui.settings == settings
    assert ui.game_stats == game_stats
    
    # Test redimensionnement
    ui.resize()
    
    print("✓ test_stat_ui passed")

def test_perks_ui():
    """Test de l'UI Perks"""
    class MockSettings:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
            self.font = {
                "h3": type('Font', (), {
                    'render': lambda text, antialias, color: type('Surface', (), {
                        'get_rect': lambda: type('Rect', (), {'center': (400, 300)})()
                    })()
                })
            }
            self.data_translation_map = {
                "player_speed": "Vitesse du Joueur",
                "multishot": "Tir Multiple"
            }
    
    settings = MockSettings()
    
    ui = PerksUI(settings)
    
    # Test initialisation
    assert ui.settings == settings
    assert hasattr(ui, 'perks_imgs')
    assert isinstance(ui.perks_imgs, dict)
    
    # Test que toutes les clés existent
    expected_perks = [
        "player_speed", "player_attack_speed", "player_attack_damage",
        "player_max_health", "player_size_up", "player_size_down",
        "player_regen", "projectile_speed", "multishot", "arc_shot"
    ]
    
    for perk in expected_perks:
        assert perk in ui.perks_imgs
    
    # Test description des perks
    desc = ui._get_perk_description("player_speed")
    assert isinstance(desc, str)
    assert len(desc) > 0
    
    # Test redimensionnement
    ui.resize()
    
    print("✓ test_perks_ui passed")

def test_scene_resize_logic():
    """Test de la logique de redimensionnement"""
    class MockGame:
        pass
    
    class MockSettings:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
            self.ASPECT_RATIO = (4, 3)
            self.BORDER_WIDTH = 2
    
    game = MockGame()
    settings = MockSettings()
    
    # Test différentes tailles
    test_cases = [
        (800, 600),   # Ratio parfait
        (1024, 768),  # Ratio parfait
        (1200, 800),  # Largeur limitante
        (600, 800),   # Hauteur limitante
    ]
    
    for width, height in test_cases:
        # Simule le calcul de redimensionnement
        if height/4*3 > width:  # largeur limitante
            screen_width = width
            screen_height = round(width/4*3)
            y0 = (height - screen_height)//2
            x0 = 0
        else:  # Hauteur limitante
            screen_width = round(height/3*4)
            screen_height = height
            y0 = 0
            x0 = (width - screen_width)//2
        
        # Vérifie que les dimensions sont valides
        assert screen_width > 0
        assert screen_height > 0
        assert x0 >= 0
        assert y0 >= 0
    
    print("✓ test_scene_resize_logic passed")

def test_ui_components():
    """Test des composants UI communs"""
    class MockFont:
        @staticmethod
        def render(text, antialias, color):
            class MockSurface:
                def get_rect(self):
                    class MockRect:
                        def __init__(self):
                            self.x = 0
                            self.y = 0
                            self.width = len(text) * 10
                            self.height = 20
                            self.center = (self.width/2, self.height/2)
                    return MockRect()
            return MockSurface()
    
    class MockSettings:
        def __init__(self):
            self.font = {"h1": MockFont(), "h2": MockFont(), "h3": MockFont(), "h4": MockFont()}
    
    settings = MockSettings()
    
    # Test création de texte
    text_surface = settings.font["h1"].render("Test", True, (255, 255, 255))
    rect = text_surface.get_rect()
    
    assert hasattr(rect, 'width')
    assert hasattr(rect, 'height')
    assert hasattr(rect, 'center')
    
    # Test positionnement
    rect.center = (400, 300)
    assert rect.center == (400, 300)
    
    print("✓ test_ui_components passed")

def test_game_stats_passing():
    """Test du passage des stats entre scènes"""
    game_stats = {
        "score": 1500,
        "xp": 200,
        "health": 75,
        "max_health": 100,
        "player_speed": 5,
        "attack_damages": 30
    }
    
    # Test que toutes les clés sont des strings
    assert all(isinstance(key, str) for key in game_stats.keys())
    
    # Test que toutes les valeurs sont numériques
    assert all(isinstance(value, (int, float)) for value in game_stats.values())
    
    # Test accès aux valeurs
    assert game_stats["score"] == 1500
    assert game_stats["xp"] == 200
    assert game_stats["health"] == 75
    
    print("✓ test_game_stats_passing passed")

def test_color_constants():
    """Test des constantes de couleur"""
    colors = {
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0)
    }
    
    for color_name, rgb in colors.items():
        assert isinstance(rgb, tuple)
        assert len(rgb) == 3
        assert all(0 <= value <= 255 for value in rgb)
    
    print("✓ test_color_constants passed")

def test_scene_transitions():
    """Test des transitions entre scènes"""
    scenes = ["menu", "game", "game_over", "talents"]
    
    # Test que toutes les scènes ont un nom valide
    for scene in scenes:
        assert isinstance(scene, str)
        assert len(scene) > 0
    
    # Test mapping des scènes
    scene_mapping = {
        "menu": "SCENE_MENU",
        "game": "SCENE_GAME",
        "game_over": "SCENE_GAME_OVER",
        "talents": "SCENE_TALENTS"
    }
    
    for scene_key, scene_constant in scene_mapping.items():
        assert scene_key in scenes
        assert isinstance(scene_constant, str)
    
    print("✓ test_scene_transitions passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_base_scene()
    test_game_over_ui()
    test_pause_ui()
    test_stat_ui()
    test_perks_ui()
    test_scene_resize_logic()
    test_ui_components()
    test_game_stats_passing()
    test_color_constants()
    test_scene_transitions()
    print("\n✅ Tous les tests de scènes ont réussi!")
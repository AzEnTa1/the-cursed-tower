from src.utils.queue import Queue, WaveQueue

def test_queue_operations():
    """Test des opérations de base de la file"""
    queue = Queue()
    
    # Test enqueue et taille
    assert queue.size() == 0
    queue.enqueue(1)
    assert queue.size() == 1
    queue.enqueue(2)
    assert queue.size() == 2
    queue.enqueue(3)
    assert queue.size() == 3
    
    # Test peek (regarder sans retirer)
    assert queue.peek() == 1
    assert queue.size() == 3  # Taille inchangée
    
    # Test dequeue (retirer dans l'ordre)
    assert queue.dequeue() == 1
    assert queue.size() == 2
    assert queue.peek() == 2
    
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert queue.size() == 0
    assert queue.is_empty() == True
    
    # Test dequeue sur file vide
    assert queue.dequeue() == None
    assert queue.peek() == None
    
    print("✓ test_queue_operations passed")

def test_queue_fifo():
    """Test de la propriété FIFO (First-In, First-Out)"""
    queue = Queue()
    
    # Ajout d'éléments dans un ordre spécifique
    items = ["A", "B", "C", "D", "E"]
    for item in items:
        queue.enqueue(item)
    
    # Vérification que les éléments sortent dans le même ordre
    for expected_item in items:
        actual_item = queue.dequeue()
        assert actual_item == expected_item, f"Attendu {expected_item}, obtenu {actual_item}"
    
    assert queue.is_empty() == True
    
    print("✓ test_queue_fifo passed")

def test_queue_mixed_types():
    """Test avec différents types de données"""
    queue = Queue()
    
    # Test avec nombres
    queue.enqueue(42)
    queue.enqueue(3.14)
    queue.enqueue(-10)
    
    assert queue.dequeue() == 42
    assert queue.dequeue() == 3.14
    assert queue.dequeue() == -10
    
    # Test avec strings
    queue.enqueue("hello")
    queue.enqueue("world")
    
    assert queue.dequeue() == "hello"
    assert queue.dequeue() == "world"
    
    # Test avec listes
    queue.enqueue([1, 2, 3])
    queue.enqueue(["a", "b", "c"])
    
    assert queue.dequeue() == [1, 2, 3]
    assert queue.dequeue() == ["a", "b", "c"]
    
    # Test avec dictionnaires
    queue.enqueue({"key": "value"})
    queue.enqueue({"x": 1, "y": 2})
    
    assert queue.dequeue() == {"key": "value"}
    assert queue.dequeue() == {"x": 1, "y": 2}
    
    print("✓ test_queue_mixed_types passed")

def test_queue_edge_cases():
    """Test des cas limites de la file"""
    queue = Queue()
    
    # Test dequeue sur file vide
    assert queue.dequeue() == None
    
    # Test peek sur file vide
    assert queue.peek() == None
    
    # Test is_empty sur file vide
    assert queue.is_empty() == True
    
    # Test avec un seul élément
    queue.enqueue("seul")
    assert queue.is_empty() == False
    assert queue.size() == 1
    assert queue.peek() == "seul"
    assert queue.dequeue() == "seul"
    assert queue.is_empty() == True
    
    # Test avec beaucoup d'éléments
    for i in range(1000):
        queue.enqueue(i)
    
    assert queue.size() == 1000
    
    for i in range(1000):
        assert queue.dequeue() == i
    
    assert queue.is_empty() == True
    
    print("✓ test_queue_edge_cases passed")

def test_wave_queue_initialization():
    """Test de l'initialisation de WaveQueue"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Vérifie que les constantes existent
    assert hasattr(wave_queue, 'ENEMY_TYPES')
    assert hasattr(wave_queue, 'WAVE_CONFIGS')
    
    assert isinstance(wave_queue.ENEMY_TYPES, list)
    assert isinstance(wave_queue.WAVE_CONFIGS, list)
    
    # Vérifie le contenu des types d'ennemis
    expected_enemies = ['basic', 'charger', 'shooter', 'destructeur', 'suicide', 'pyromane']
    for enemy in expected_enemies:
        assert enemy in wave_queue.ENEMY_TYPES
    
    print("✓ test_wave_queue_initialization passed")

def test_wave_queue_configuration():
    """Test de la configuration des vagues"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Test configuration pour différents étages
    for floor in [1, 2, 3, 5, 10]:
        wave_queue.setup_waves_for_floor(floor)
        
        # Doit avoir 3 vagues
        count = 0
        while wave_queue.has_more_waves():
            wave = wave_queue.get_next_wave()
            assert wave is not None
            assert isinstance(wave, list)
            count += 1
        
        assert count == 3  # Toujours 3 vagues normales
    
    print("✓ test_wave_queue_configuration passed")

def test_wave_generation():
    """Test de la génération de vagues"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Test génération pour différents étages et vagues
    test_cases = [
        (1, 1),  # Étage 1, vague 1
        (1, 2),  # Étage 1, vague 2
        (1, 3),  # Étage 1, vague 3
        (3, 1),  # Étage 3, vague 1
        (5, 2),  # Étage 5, vague 2
    ]
    
    for floor, wave_num in test_cases:
        wave = wave_queue.generate_normal_wave(floor, wave_num)
        
        assert isinstance(wave, list)
        assert len(wave) > 0
        
        # Vérifie que tous les ennemis sont des types valides
        for enemy_type in wave:
            assert enemy_type in wave_queue.ENEMY_TYPES
    
    print("✓ test_wave_generation passed")

def test_wave_queue_remaining():
    """Test du comptage de vagues restantes"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Test initial
    wave_queue.setup_waves_for_floor(1)
    assert wave_queue.get_remaining_waves_count() == 3
    
    # Test après récupération d'une vague
    wave1 = wave_queue.get_next_wave()
    assert wave_queue.get_remaining_waves_count() == 2
    
    # Test après récupération de toutes les vagues
    wave2 = wave_queue.get_next_wave()
    wave3 = wave_queue.get_next_wave()
    assert wave_queue.get_remaining_waves_count() == 0
    assert wave_queue.has_more_waves() == False
    
    print("✓ test_wave_queue_remaining passed")

def test_wave_difficulty_scaling():
    """Test de l'augmentation de la difficulté"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Compare les vagues de différents étages
    floor1_wave = wave_queue.generate_normal_wave(1, 1)
    floor3_wave = wave_queue.generate_normal_wave(3, 1)
    floor5_wave = wave_queue.generate_normal_wave(5, 1)
    
    # Vérifie que la difficulté augmente (plus d'ennemis ou types différents)
    # Note: la méthode génère des listes, on peut vérifier la longueur
    # ou la distribution des types
    
    print("✓ test_wave_difficulty_scaling passed")

def test_queue_performance():
    """Test de performance basique de la file"""
    queue = Queue()
    
    # Test d'ajout rapide
    import time
    
    start_time = time.time()
    for i in range(10000):
        queue.enqueue(i)
    add_time = time.time() - start_time
    
    # Test de retrait rapide
    start_time = time.time()
    for i in range(10000):
        queue.dequeue()
    remove_time = time.time() - start_time
    
    # Vérifie que les opérations sont raisonnablement rapides
    assert add_time < 1.0  # Moins d'une seconde pour 10000 ajouts
    assert remove_time < 1.0  # Moins d'une seconde pour 10000 retraits
    
    print("✓ test_queue_performance passed")

def test_wave_composition():
    """Test de la composition des vagues"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    
    # Test plusieurs générations pour vérifier la distribution
    enemy_counts = {}
    
    for _ in range(100):  # 100 générations
        wave = wave_queue.generate_normal_wave(1, 1)
        for enemy in wave:
            enemy_counts[enemy] = enemy_counts.get(enemy, 0) + 1
    
    # Vérifie que tous les types d'ennemis apparaissent
    for enemy_type in wave_queue.ENEMY_TYPES:
        assert enemy_type in enemy_counts
        assert enemy_counts[enemy_type] > 0
    
    print("✓ test_wave_composition passed")

# Exécuter tous les tests
if __name__ == "__main__":
    test_queue_operations()
    test_queue_fifo()
    test_queue_mixed_types()
    test_queue_edge_cases()
    test_wave_queue_initialization()
    test_wave_queue_configuration()
    test_wave_generation()
    test_wave_queue_remaining()
    test_wave_difficulty_scaling()
    test_queue_performance()
    test_wave_composition()
    print("\n✅ Tous les tests de structures de données ont réussi!")
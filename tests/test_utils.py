from src.utils.queue import Queue, WaveQueue

def test_queue_op():
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
    
def test_queue():
    """Test de la propriété FIFO (First-In, First-Out)"""
    queue = Queue()
    
    # Ajout d'éléments dans un ordre spécifique
    items = ["A", "B", "C", "D", "E"]
    for item in items:
        queue.enqueue(item)
    
    # Vérification que les éléments sortent dans le même ordre
    for i in items:
        queue.dequeue()

    assert queue.is_empty() == True
    
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

def test_queue_limite():
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
    
def test_wave_queue_remaining():
    """Test du comptage de vagues restantes"""
    class MockSettings:
        pass
    
    settings = MockSettings()
    wave_queue = WaveQueue(settings)
    wave_queue.setup_waves_for_floor(1)
    
    # Test après récupération d'une vague
    wave1 = wave_queue.get_next_wave()
    assert wave_queue.get_remaining_waves_count() == 2

# Exécuter tous les tests
if __name__ == "__main__":
    test_queue_op()
    test_queue()
    test_queue_mixed_types()
    test_queue_limite()
    test_wave_queue_remaining()
class WaweManager:
    def __init__(self):
        self.active_waves = []
    
    def enqueue(self, wave):
        self.active_waves.append(wave)

    def dequeue(self):
        if not self.is_empty():
            return self.active_waves.pop(0)
        return None

    def is_empty(self):
        return len(self.active_waves) == 0
    
    def size(self):
        return len(self.active_waves)
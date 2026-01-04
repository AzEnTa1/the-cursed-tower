# Main.py
import pygame
from src import Game

def main():
    pygame.init() # initialise tous les modules internes de Pygame
    game = Game()
    game.run()
    

# Lorsque que Python exécute un fichier, il définit une variable spéciale __name__ égale à "__main__"
# donc on peut l'utiliser pour exécuter du code uniquement si le fichier est exécuté directement.
if __name__ == "__main__":
    main()
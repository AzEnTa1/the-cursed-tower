import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, SCENE_MENU, SCENE_GAME
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Horloge pour les FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.current_scene = None
        
        # Initialisation des scènes
        self.scenes = {
            SCENE_MENU: MenuScene(self),
            SCENE_GAME: GameScene(self)
        }
        
        # Commencer par le menu
        self.change_scene(SCENE_MENU)
    
    def change_scene(self, scene_name):
        """Change la scène actuelle"""
        if scene_name in self.scenes:
            # Appel on_exit sur l'ancienne scène
            if self.current_scene: # Au cas ou c'est None
                self.current_scene.on_exit()
            
            # Change de scène
            self.current_scene = self.scenes[scene_name]
            
            # Appel on_enter sur la nouvelle scène
            self.current_scene.on_enter()
    
    def handle_events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            # Événement de fermeture
            if event.type == pygame.QUIT:
                self.running = False
            
            # Passe les événements à la scène actuelle
            if self.current_scene:
                self.current_scene.handle_event(event)
    
    def update(self):
        """Mise à jour de la logique du jeu"""
        if self.current_scene:
            self.current_scene.update()
    
    def draw(self):
        """Rendu graphique"""
        # Efface l'écran
        self.screen.fill((0, 0, 0))
        
        # Dessine la scène actuelle
        if self.current_scene:
            self.current_scene.draw(self.screen)
        
        # Met à jour l'affichage
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            # Gestion des événements
            self.handle_events()
            
            # Mise à jour de la logique
            self.update()
            
            # Rendu
            self.draw()
            
            # Contrôle des FPS
            self.clock.tick(FPS)
        
        # Nettoyage
        pygame.quit()
        sys.exit()
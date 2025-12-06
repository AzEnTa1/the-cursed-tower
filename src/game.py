import pygame
import sys
from config.settings import Settings
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        #Initialisation des Paramettres
        self.settings = Settings() 

        # Initialisation de Pygame
        pygame.init()
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(self.settings.title)
        
        # Horloge pour les FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.current_scene = None
        
        # Initialisation des scènes
        self.scenes = {
            self.settings.SCENE_MENU: MenuScene(self, self.settings),
            self.settings.SCENE_GAME: GameScene(self, self.settings)
        }
        
        # Commencer par le menu
        self.change_scene(self.settings.SCENE_MENU)
    
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
            
            elif event.type == pygame.VIDEORESIZE:
                if event.dict["h"]/3*4 > event.dict["w"] : #si plus haut que large(format 4:3)
                    self.settings.screen_width, self.settings.screen_height = event.dict["w"], event.dict["w"]/4*3
                    self.settings.y0 = (event.dict["h"] - self.settings.screen_height)//2
                    self.settings.x0 = 0
                    
                    print(1)
                else:
                    self.settings.screen_width, self.settings.screen_height = event.dict["h"]/3*4, event.dict["h"]
                    self.settings.y0 = 0
                    self.settings.x0 = (event.dict["w"] - self.settings.screen_width)//2
                    
                    print(2)
                self.current_scene.resize(event.dict["w"], event.dict["h"])
                print(self.settings.screen_width, self.settings.screen_height)

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
        
        
        #dessine la bordure pour vérifier le format plein écran
        border_size = self.settings.screen_height*0.01
        pygame.draw.rect(self.screen, (240, 230, 180), (0, 0, self.settings.x0, self.settings.screen_height))
        pygame.draw.rect(self.screen, (240, 230, 180), (0, 0, self.settings.screen_width, self.settings.y0))
        pygame.draw.rect(self.screen, (240, 230, 180), (self.settings.x0 + self.settings.screen_width, 0, self.settings.x0, self.settings.screen_height))
        pygame.draw.rect(self.screen, (240, 230, 180), (0, self.settings.y0 + self.settings.screen_height, self.settings.screen_width, self.settings.y0))

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
            self.clock.tick(self.settings.fps)
        
        # Nettoyage
        pygame.quit()
        sys.exit()
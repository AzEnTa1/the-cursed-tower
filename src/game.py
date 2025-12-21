# src/game.py 
import pygame
import sys
from config.settings import Settings
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene
from src.scenes.gameover_scene import GameOverScene

class Game:
    """
    Classe principale du jeu
    Gère l'initialisation, la boucle principale, les scènes, et les événements
    """
    def __init__(self):
        # Initialisation des paramètres 
        self.settings = Settings() 

        # Initialisation de Pygame
        pygame.init()
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)
        self.full_screen = False
        pygame.display.set_caption(self.settings.title)

        # Initialiser les fonts
        self.settings.initialize_fonts()
        
        # Surface de la fenetre utilisé
        self.used_screen = pygame.Surface((self.settings.screen_width, self.settings.screen_height))

        # Horloge pour les FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.current_scene = None
        
        # Initialisation des scènes
        self.scenes = {
            self.settings.SCENE_MENU: MenuScene(self, self.settings),
            self.settings.SCENE_GAME: GameScene(self, self.settings),
            self.settings.SCENE_GAME_OVER: GameOverScene(self, self.settings)
        }
        # Statistiques du jeu à passer à l'écran de fin
        self.game_stats = None

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
            if scene_name == self.settings.SCENE_GAME_OVER:
                self.current_scene.on_enter(self.game_stats)
            else:
                self.current_scene.on_enter()
            
    
    def handle_events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            # Événement de fermeture
            if event.type == pygame.QUIT:
                self.running = False
            
            # Événement de redimensionnement
            elif event.type == pygame.VIDEORESIZE:
                if event.dict["h"]/self.settings.ASPECT_RATIO[1]*self.settings.ASPECT_RATIO[0] > event.dict["w"] : # largeur limitante 
                    self.settings.screen_width, self.settings.screen_height = event.dict["w"], round(event.dict["w"]/self.settings.ASPECT_RATIO[0]*self.settings.ASPECT_RATIO[1])
                    self.settings.y0 = (event.dict["h"] - self.settings.screen_height)//self.settings.BORDER_WIDTH
                    self.settings.x0 = 0
                else: # Hauteur limitante
                    self.settings.screen_width, self.settings.screen_height = round(event.dict["h"]/self.settings.ASPECT_RATIO[1]*self.settings.ASPECT_RATIO[0]), event.dict["h"]
                    self.settings.y0 = 0
                    self.settings.x0 = (event.dict["w"] - self.settings.screen_width)//self.settings.BORDER_WIDTH
                self.used_screen = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
                self.current_scene.resize()
                print(self.settings.screen_width, self.settings.screen_height)


            # Événement de bascule plein écran
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not self.full_screen:
                        self.full_screen = True
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
                    else:
                        self.full_screen = False
                        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
                    self.current_scene.resize()

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
            self.current_scene.draw(self.used_screen)
    
        # Dessiner les bordures
        pygame.draw.rect(self.screen, self.settings.BORDER_COLOR, (0, 0, self.settings.x0, self.settings.screen_height))
        pygame.draw.rect(self.screen, self.settings.BORDER_COLOR, (0, 0, self.settings.screen_width, self.settings.y0))
        pygame.draw.rect(self.screen, self.settings.BORDER_COLOR, (self.settings.x0 + self.settings.screen_width, 0, self.settings.x0, self.settings.screen_height))
        pygame.draw.rect(self.screen, self.settings.BORDER_COLOR, (0, self.settings.y0 + self.settings.screen_height, self.settings.screen_width, self.settings.y0))

        # Met à jour l'affichage
        self.screen.blit(self.used_screen, (self.settings.x0, self.settings.y0))
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
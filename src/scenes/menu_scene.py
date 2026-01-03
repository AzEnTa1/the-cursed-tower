# src/scenes/menu_scene.py
import pygame
from .base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        
    def on_enter(self, player_data):
        """Initialisation du menu"""
        # Rectangle pour les boutons (x, y, width, height)
        self.play_button = pygame.Rect(self.settings.screen_width//2 - 100, self.settings.screen_height//2-50, 200, 50)
        self.talents_button = pygame.Rect(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 20, 200, 50)

        #augmenter la taille de la police pour le menu principal
        



        # Charger l'image de fond
        try:
            self.bg_image = pygame.image.load("assets/images/background/menu_scene.png")
            self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
            
        except FileNotFoundError:
            # Fallback si l'image n'existe pas
            self.bg_image = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            self.bg_image.fill((50, 50, 100))
        
        self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 200, 0))
        self.button_rect = self.text.get_rect(center=self.play_button.center)



        self.text_talents = self.settings.font["main_menu"].render("Talents", True, (255, 200, 0))
        self.talents_button = self.text_talents.get_rect(center=self.talents_button.center)

        

    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                pygame.mixer.Sound("assets/sounds/game_start.mp3").play()
                self.start_game()
            elif self.talents_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                        self.game.change_scene(self.settings.SCENE_TALENTS)

        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Touche ENTER
                pygame.mixer.Sound("assets/sounds/game_start.mp3").play()
                self.start_game()
    
    def start_game(self):
        """Démarre le jeu"""
        self.game.change_scene(self.settings.SCENE_GAME)
    
    def update(self):
        """Pas de logique particulière pour le menu simple (pr l'instant)"""
        
        if self.button_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 200, 0))
            if not hasattr(self, 'exit_hovered') or not self.exit_hovered:
                self.exit_hovered = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.text = self.settings.font["main_menu"].render("JOUER(entrée)", True, (255, 255, 255))
            self.exit_hovered = False

        if self.talents_button.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text_talents = self.settings.font["main_menu"].render("Talents", True, (255, 200, 0))
            if not hasattr(self, 'talents_hovered') or not self.talents_hovered:
                self.talents_hovered = True
                pygame.mixer.Sound("assets/sounds/souris_on_bouton.mp3").play()
        else:
            self.text_talents = self.settings.font["main_menu"].render("Talents", True, (255, 255, 255))
            self.talents_hovered = False
    
    def draw(self, screen):
        """Dessine le menu"""
        
        # Image de fond
        screen.blit(self.bg_image, (0, 0))

        # Bouton Jouer avec effet hover
        
        screen.blit(self.text, self.button_rect)

        # Bouton Talents avec effet hover
        screen.blit(self.text_talents, self.talents_button)

    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.play_button.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 -50, 200, 50)
        self.talents_button.update(self.settings.screen_width//2 - 100, self.settings.screen_height//2 + 20, 200, 50)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.button_rect = self.text.get_rect(center=self.play_button.center)
        self.talents_button = self.text_talents.get_rect(center=self.talents_button.center)

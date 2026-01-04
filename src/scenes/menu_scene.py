# src/scenes/menu_scene.py
import pygame
from .base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        
    def on_enter(self, player_data):
        """Initialisation du menu"""
        self.player_data = player_data

        self.shift_pressed = False

        # Rectangle pour les boutons (x, y, width, height)
        self.play_button = pygame.Rect(self.settings.screen_width//2-100, self.settings.screen_height//2-20, 200, 50)
        self.talents_button = pygame.Rect(self.settings.screen_width-200, self.settings.screen_height - 50, 200, 50)
        self.reset_button = pygame.Rect(0, self.settings.screen_height - 50, 200, 50)

        self.volume_plus = pygame.Rect(self.settings.screen_width - 50, 0, 50, 50)
        self.plus_bouton = pygame.image.load("assets/images/son_plus.png").convert_alpha()
        self.plus_bouton = pygame.transform.scale(self.plus_bouton, (50, 50)) 
        self.volume_moins = pygame.Rect(self.settings.screen_width - 190, 0, 50, 50)
        self.moins_bouton = pygame.image.load("assets/images/son_moins.png").convert_alpha()
        self.moins_bouton = pygame.transform.scale(self.moins_bouton, (50, 50))
        self.val_volume = pygame.Rect(self.settings.screen_width - 120, 0, 50, 50)

        self.txt_val_volume = self.settings.font["h2"].render(str(int(self.settings.master_volume*100)), True, (0, 0, 0))
        self.txt_vel_volume_rect = self.txt_val_volume.get_rect(center=self.val_volume.center)

        # Charger l'image de fond

        self.bg_image = pygame.image.load("assets/images/background/menu_scene.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

        self.text = self.settings.font["main_menu"].render("JOUER", True, (255, 200, 0))
        self.button_rect = self.text.get_rect(center=self.play_button.center)

        self.text_talents = self.settings.font["h1"].render("Talents", True, (0, 0, 255))
        self.talents_button = self.text_talents.get_rect(center=self.talents_button.center)

        self.text_reset = self.settings.font["h2"].render("Réinitialisation", True, (111, 6, 6))
        self.reset_button = self.text_reset.get_rect(center=self.reset_button.center)

        
        

    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.start_game()

            elif self.talents_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_TALENTS)

            elif self.reset_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.player_data = self.game.reset_player_data()
                self.settings.sounds["game_over"].play()
                # Actualise le son car il est aussi reset
                self.txt_val_volume = self.settings.font["h2"].render(str(int(self.settings.master_volume*100)), True, (0, 0, 0))
                self.txt_vel_volume_rect = self.txt_val_volume.get_rect(center=self.val_volume.center)

            elif self.volume_plus.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.update_volume(1)
            elif self.volume_moins.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.update_volume(-1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Touche ENTER
                self.start_game()
            # Véeifie si shift et pressé pour faire + 10 au son au lieu de +1
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.shift_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.shift_pressed = False
    
    def start_game(self):
        """Démarre le jeu"""
        self.settings.sounds["game_start"].play()
        self.game.change_scene(self.settings.SCENE_GAME)
        # simule l'entré dans une sub scene depuis game_scene
        if self.player_data["game_played"] == 0:
            self.game.scenes[self.settings.SCENE_GAME].game_paused = True
            self.game.scenes[self.settings.SCENE_GAME].current_sub_scene = self.game.scenes[self.settings.SCENE_GAME].tuto_sub_scene
            self.game.scenes[self.settings.SCENE_GAME].current_sub_scene.on_enter()
        self.player_data["game_played"] += 1

    def update_volume(self, val):
        # volume compris entre 0 et 1
        if self.shift_pressed:
            self.settings.update_master_volume(val*0.1)
        else:
            self.settings.update_master_volume(val*0.01)

        # Update le text affiché
        self.txt_val_volume = self.settings.font["h2"].render(str(int(self.settings.master_volume*100)), True, (0, 0, 0))
        self.txt_vel_volume_rect = self.txt_val_volume.get_rect(center=self.val_volume.center)

    def update(self):
        """Pas de logique particulière pour le menu simple (pr l'instant)"""
        
        if self.button_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text = self.settings.font["main_menu"].render("JOUER", True, (255, 200, 0))
            if not hasattr(self, 'exit_hovered') or not self.exit_hovered: 
                self.exit_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.text = self.settings.font["main_menu"].render("JOUER", True, (255, 255, 255))
            self.exit_hovered = False

        if self.talents_button.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text_talents = self.settings.font["h1"].render("Talents", True, (0, 0, 255))
            if not hasattr(self, 'talents_hovered') or not self.talents_hovered:
                self.talents_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.text_talents = self.settings.font["h1"].render("Talents", True, (0, 0, 100))
            self.talents_hovered = False

        if self.reset_button.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.text_reset = self.settings.font["h2"].render("Réinitialisation", True, (198, 12, 12))
            if not hasattr(self, 'reset_hovered') or not self.reset_hovered:
                self.reset_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.text_reset = self.settings.font["h2"].render("Réinitialisation", True, (111, 6, 6))
            self.reset_hovered = False

        if self.volume_plus.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            #change la couleur du rectangle
            self.plus_bouton = pygame.image.load("assets/images/son_plus_hover.png").convert_alpha()
            self.plus_bouton = pygame.transform.scale(self.plus_bouton, (50, 50))
            if not hasattr(self, 'volume_hovered') or not self.volume_hovered:
                self.volume_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.volume_hovered = False
            self.plus_bouton = pygame.image.load("assets/images/son_plus.png").convert_alpha()
            self.plus_bouton = pygame.transform.scale(self.plus_bouton, (50, 50))
        
        if self.volume_moins.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            #change la couleur du rectangle
            self.moins_bouton = pygame.image.load("assets/images/son_moins_hover.png").convert_alpha()
            self.moins_bouton = pygame.transform.scale(self.moins_bouton, (50, 50))
            if not hasattr(self, 'volume_moins_hovered') or not self.volume_moins_hovered:
                self.volume_moins_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.volume_moins_hovered = False
            self.moins_bouton = pygame.image.load("assets/images/son_moins.png").convert_alpha()
            self.moins_bouton = pygame.transform.scale(self.moins_bouton, (50, 50))
        

    def draw(self, screen):
        """Dessine le menu"""
        
        # Image de fond
        screen.blit(self.bg_image, (0, 0))

        # Bouton Jouer avec effet hover
        screen.blit(self.text, self.button_rect)

        # Bouton Talents avec effet hover
        screen.blit(self.text_talents, self.talents_button)

        # Bouton reset avec effet hover
        screen.blit(self.text_reset, self.reset_button)

        # Boutons pour changer le volume
        
        pygame.draw.rect(screen, (255, 255, 255), self.volume_plus)
        screen.blit(self.plus_bouton, self.volume_plus)
        pygame.draw.rect(screen, (255, 255, 255), self.volume_moins)
        screen.blit(self.moins_bouton, self.volume_moins)
        pygame.draw.rect(screen, (255, 255, 255), self.val_volume)

        screen.blit(self.txt_val_volume, self.txt_vel_volume_rect)

    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.play_button.update(self.settings.screen_width//2-100, self.settings.screen_height//2-20, 200, 50)
        self.talents_button.update(self.settings.screen_width-200, self.settings.screen_height - 50, 200, 50)
        self.reset_button.update(0, self.settings.screen_height - 50, 200, 50)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.button_rect = self.text.get_rect(center=self.play_button.center)
        self.talents_button = self.text_talents.get_rect(center=self.talents_button.center)
        self.reset_button = self.text_reset.get_rect(center=self.reset_button.center)
        self.volume_plus.update(self.settings.screen_width - 50, 0, 50, 50)
        self.volume_moins.update(self.settings.screen_width - 190, 0, 50, 50)
        self.val_volume.update(self.settings.screen_width - 120, 0, 50, 50)
        self.txt_vel_volume_rect = self.txt_val_volume.get_rect(center=self.val_volume.center)

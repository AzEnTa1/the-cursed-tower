# src/scenes/talents_scene.py
import pygame
from .base_scene import BaseScene
from src.perks.talents import Talents


class TalentsScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        
    def on_enter(self, player_data):
        """Initialisation du menu"""
        self.player_data = player_data
        self.talents = Talents(self.game, self.settings, player_data)
        # Rect pour quiter le menu
        self.exit_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
        self.cadre = pygame.image.load(r"assets\images\cadre.png")
        self.exit_menu_rect = pygame.Rect(self.settings.screen_width - 210, 50, 200, 50)
        self.quit_button_img = pygame.transform.scale(self.cadre, (self.exit_menu_rect.width, self.exit_menu_rect.height))
        self.exit_menu_text_rect = self.exit_menu_text.get_rect(center=self.exit_menu_rect.center)
        
        self.talent_dict = {
            "max_health":{
                "img":pygame.image.load(r"assets\images\perks_icons\Heal_icon.png"),
                "val_min":100
                },
            "regen_power":{"img":pygame.image.load(r"assets\images\perks_icons\Regen_icon.png"),
                "val_min":0.1,
                "val_max":1.0
                },
            "player_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Speed_Icon.png"),
                "val_min":5,
                "val_max":20
                },
            "player_size":{"img":pygame.image.load(r"assets\images\perks_icons\Player_size_up_icon.png"),
                "val_min":5,
                "val_max":20
                },
            "dash_cooldown":{"img":pygame.image.load(r"assets\images\perks_icons\dash_cooldown_icon.png"),
                "val_min":30,
                "val_max":180
                },
            "dash_distance":{"img":pygame.image.load(r"assets\images\perks_icons\dash_distance_icon.png"),
                "val_min":4,
                "val_max":10
                },
            "attack_damages":{"img":pygame.image.load(r"assets\images\perks_icons\Attack_icon.png"),
                "val_min":20
                },
            "attack_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Attack_speed_icon.png"),
                "val_min":2,
                "val_max":10
                },
            "stationary_threshold":{"img":pygame.image.load(r"assets\images\perks_icons\stationnary_threshold_icon.png"),
                "val_min":15,
                "val_max":30
                },
            "projectile_size":{"img":pygame.image.load(r"assets\images\perks_icons\Projectile_size_up_icon.png"),
                "val_min":5,
                "val_max":20
                },
            "projectile_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Projectile_speed_icon.png"),
                "val_min":10,
                "val_max":20
                }
        }
        
        # Calcul des positions et tailles des éléments
        base_talent_rect = pygame.Rect(self.settings.screen_width//16, self.settings.screen_width//6, self.settings.screen_width//8, self.settings.screen_width//8)
        i = 0
        for key in list(self.talent_dict.keys()):
            self.talent_dict[key]["rect"] = base_talent_rect.move(self.settings.screen_width*5//32 * (i%4), self.settings.screen_width*3//16 * (i//4))
            self.talent_dict[key]["img"] = pygame.transform.scale(self.talent_dict[key]["img"], base_talent_rect.size)
            
            # définit le text
            self.talent_dict[key]["txt"] = []
            self.talent_dict[key]["txt_rect"] = []

            words = self.settings.data_translation_map.get(key, key).split(" ")
            print(words)
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if len(test_line) <= 12: # 12 chr / lignes
                    current_line = test_line
                else:
                    if current_line != " ":
                        self.talent_dict[key]["txt"].append(current_line)
                    current_line = word + " "
            self.talent_dict[key]["txt"].append(current_line)
            print(self.talent_dict[key]["txt"])
            self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"]
            self.talent_dict[key]["total_rect"].inflate_ip(5, 55)
            self.talent_cadre = pygame.transform.scale(self.cadre, self.talent_dict[key]["total_rect"].size)
            i += 1

        self.stats_rect = pygame.Rect(self.settings.screen_width*2//3, self.settings.screen_height//4, self.settings.screen_width//3, self.settings.screen_height//2+100)
        
        # Charger l'image de fond
        bg_img = pygame.image.load("assets/images/background/talents_scene.png")
        self.bg_image = pygame.transform.scale(bg_img, (self.settings.screen_width, self.settings.screen_height))

    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)
            else:
                for key in list(self.talent_dict.keys()):
                    if self.talent_dict[key]["rect"].move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                        # Vérifie qu'on a l'argent
                        if self.player_data["coins"] >= 100:
                            getattr(self.talents, key)()
                            # Vérifie que les valeurs ne sont pas trop élevé / basse
                            if self.talent_dict[key].get("val_min", 0) > self.player_data[key]:
                                self.player_data[key] = self.talent_dict[key]["val_min"]
                                self.settings.sounds["degat_1"].play()
                            elif self.talent_dict[key].get("val_max", 2147483647) < self.player_data[key]:
                                self.player_data[key] = self.talent_dict[key]["val_max"]
                                self.settings.sounds["degat_1"].play()
                            else:
                                self.player_data["coins"] -= 100
                                self.settings.sounds["coins"].play()
                        else:
                            self.settings.sounds["degat_1"].play()
                        break         
    
    def update(self):
        """met a jours les éléments et la logique de la scene"""
        if self.exit_menu_rect.move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
            self.exit_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 255, 255))
            if not hasattr(self, 'exit_hovered') or not self.exit_hovered:
                self.exit_hovered = True
                self.settings.sounds["souris_on_button"].play()
        else:
            self.exit_menu_text = self.settings.font["h3"].render("Quitter", True, (255, 0, 0))
            self.exit_hovered = False

    def draw(self, screen):
        """Dessine la scene"""

        # Image de fond
        screen.blit(self.bg_image, (0, 0))

        # Bouton quitter
        screen.blit(self.quit_button_img, self.exit_menu_rect)
        screen.blit(self.exit_menu_text, self.exit_menu_text_rect)

        # Affiche les talents
        for i, key in enumerate(self.talent_dict.keys()):
            screen.blit(self.talent_cadre, self.talent_dict[key]["total_rect"].topleft)

            screen.blit(self.talent_dict[key]["img"], self.talent_dict[key]["rect"].topleft)
            # Affiche le text
            for i, line in enumerate(self.talent_dict[key]["txt"]):
                text_surface = self.settings.font["h3"].render(line, True, (255, 255, 255))
                txt_rect = text_surface.get_rect(midtop=(self.talent_dict[key]["rect"].center[0], self.talent_dict[key]["rect"].center[1] + i * 25 + 25))
                
                screen.blit(text_surface, txt_rect)


        # Affiche les stats
        stats_img = pygame.transform.scale(self.cadre, (self.stats_rect.width, self.stats_rect.height))
        screen.blit(stats_img, self.stats_rect)

        for i, key in enumerate(self.player_data.keys()):
            txt = self.settings.font["h4"].render(f"{self.settings.data_translation_map.get(key, key)}: {self.player_data[key]}", True, (255, 255, 255))
            rect = txt.get_rect(midtop = (self.stats_rect.midtop)).move(0, 25 + 20*i)
            screen.blit(txt, rect)
    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions et la taille des éléments
        """
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.exit_menu_rect.update(self.settings.screen_width - 210, 50, 200, 50)
        self.quit_button_img = pygame.transform.scale(self.cadre, (self.exit_menu_rect.width, self.exit_menu_rect.height))
        self.exit_menu_text_rect.center = self.exit_menu_rect.center

        # On recalcule tout les talents
        i = 0
        for key in list(self.talent_dict.keys()):
            self.talent_dict[key]["rect"].update(
                self.settings.screen_width//16 + self.settings.screen_width*5//32 * (i%4),
                self.settings.screen_width//6 + self.settings.screen_width*3//16 * (i//4),
                self.settings.screen_width//8,
                self.settings.screen_width//8
                )
            # Redimensionne l'image
            self.talent_dict[key]["img"] = pygame.transform.scale(self.talent_dict[key]["img"], self.talent_dict[key]["rect"].size)
            # définit le text
            self.talent_dict[key]["txt"] = []
            self.talent_dict[key]["txt_rect"] = []

            words = self.settings.data_translation_map.get(key, key).split(" ")
            print(words)
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if len(test_line) <= 12: # 12 chr / lignes
                    current_line = test_line
                else:
                    if current_line != " ":
                        self.talent_dict[key]["txt"].append(current_line)
                    current_line = word + " "
            self.talent_dict[key]["txt"].append(current_line)
            print(self.talent_dict[key]["txt"])
            self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"]
            self.talent_dict[key]["total_rect"].inflate_ip(5, 55)
            # Redimensionne le cadre
            if i == 0:
                self.talent_cadre = pygame.transform.scale(self.cadre, self.talent_dict[key]["total_rect"].size)
            i += 1

        self.stats_rect.update(self.settings.screen_width*2//3, self.settings.screen_height//4, self.settings.screen_width//3, self.settings.screen_height//2+100)
        
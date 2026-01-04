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
                "val_min":1,
                "val_max":1
                },
            "regen_power":{"img":pygame.image.load(r"assets\images\perks_icons\Regen_icon.png"),
                "val_min":0,
                "val_max":1
                },
            "player_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Speed_Icon.png"),
                "val_min":1,
                "val_max":1
                },
            "player_size":{"img":pygame.image.load(r"assets\images\perks_icons\Player_size_up_icon.png"),
                "val_min":5,
                "val_max":20
                },
            "dash_cooldown":{"img":pygame.image.load(r"assets\images\perks_icons\dash_cooldown_icon.png"),
                "val_min":1,
                "val_max":1
                },
            "dash_distance":{"img":pygame.image.load(r"assets\images\perks_icons\dash_distance_icon.png"),
                "val_min":1,
                "val_max":1
                },
            "attack_damages":{"img":pygame.image.load(r"assets\images\perks_icons\Attack_icon.png"),
                "val_min":1
                },
            "attack_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Attack_speed_icon.png"),
                "val_min":1,
                "val_max":1
                },
            "stationnary_threshold":{"img":pygame.image.load(r"assets\images\perks_icons\stationnary_threshold_icon.png"),
                "val_min":1,
                "val_max":1
                },
            "projectile_size":{"img":pygame.image.load(r"assets\images\perks_icons\Projectile_size_up_icon.png"),
                "val_min":1,
                "val_max":1
                },
            "projectile_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Projectile_speed_icon.png"),
                "val_min":1,
                "val_max":1
                }
        }
        
        # Calcul des positions et tailles des éléments
        base_talent_rect = pygame.Rect(self.settings.screen_width//16, self.settings.screen_width//6, self.settings.screen_width//8, self.settings.screen_width//8)
        i = 0
        for key in list(self.talent_dict.keys()):
            self.talent_dict[key]["rect"] = base_talent_rect.move(self.settings.screen_width*5//32 * (i%4), self.settings.screen_width*3//16 * (i//4))
            self.talent_dict[key]["img"] = pygame.transform.scale(self.talent_dict[key]["img"], base_talent_rect.size)
            
            
            if len(key) < 12:
                self.talent_dict[key]["txt"] = [self.settings.font["h3"].render(key.replace("_", " "), True, (255, 255, 255))]
                self.talent_dict[key]["txt_rect"] = [self.talent_dict[key]["txt"][0].get_rect(midtop=self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8).midtop)]
            else:
                self.talent_dict[key]["txt"] = []
                self.talent_dict[key]["txt_rect"] = []
                mots = key.split("_")
                ligne = 0
                for mot in mots:
                    txt = self.settings.font["h3"].render(mot, True, (255, 255, 255))
                    txt_rect = txt.get_rect(midtop=self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8 + ligne).midtop)
                    self.talent_dict[key]["txt"].append(txt)
                    self.talent_dict[key]["txt_rect"].append(txt_rect)
                    ligne += 25 # font size + 1
            self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"]
            self.talent_dict[key]["total_rect"].union_ip(self.talent_dict[key]["txt_rect"][0].move(0, 25))
            self.talent_dict[key]["total_rect"].inflate_ip(5, 5)
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
                        if self.player_data["coins"] >= 100:
                            getattr(self.talents, key)()
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

        i = 0
        for key in list(self.talent_dict.keys()):
            screen.blit(self.talent_cadre, self.talent_dict[key]["total_rect"].topleft)

            screen.blit(self.talent_dict[key]["img"], self.talent_dict[key]["rect"].topleft)
            for txt, txt_rect in zip(self.talent_dict[key]["txt"], self.talent_dict[key]["txt_rect"]):
                screen.blit(txt, txt_rect)
            i += 1

        bg_image1 = pygame.transform.scale(self.cadre, (self.stats_rect.width, self.stats_rect.height))
        screen.blit(bg_image1, self.stats_rect)
        i = 0
        for key in self.player_data.keys():
            i += 1
            txt = self.settings.font["h4"].render(f"{key.replace("_", " ")}: {self.player_data[key]}", True, (255, 255, 255))
            rect = txt.get_rect(midtop = (self.stats_rect.midtop)).move(0, 20*i)
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
            ligne = 0
            for rect in self.talent_dict[key]["txt_rect"]:
                rect.midtop = self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8 + ligne).midtop
                ligne += 25 # font size + 1

            self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"].copy()
            self.talent_dict[key]["total_rect"].union_ip(self.talent_dict[key]["txt_rect"][0].move(0, 25))
            self.talent_dict[key]["total_rect"].inflate_ip(5, 5)
            # Redimensionne le cadre
            if i == 0:
                self.talent_cadre = pygame.transform.scale(self.cadre, self.talent_dict[key]["total_rect"].size)
            i += 1

        self.stats_rect.update(self.settings.screen_width*2//3, self.settings.screen_height//4, self.settings.screen_width//3, self.settings.screen_height//2+100)
        
# src/scenes/talents_scene.py
import pygame
from .base_scene import BaseScene
from src.systems.talents import Talents


class TalentsScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        
    def on_enter(self, player_data):
        """Initialisation du menu"""
        self.player_data = player_data
        # Rect pour quiter le menu
        self.exit_button = pygame.Rect(self.settings.screen_width - 60, 10, 50, 50)
        #si quelqu'un veut en rajouter in gam c possible
        self.talent_dict = {
            "max_health":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "regen_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "player_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "player_size":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "dash_cooldown":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "dash_distance":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "attack_damages":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "attack_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "stationnary_threshold":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "projectil_size":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
            "projectil_speed":{"img":pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")},
        }
        cadre = pygame.image.load(r"assets\images\cadre.png")
        # case en haut a gauche les autres sont généré a partir de ce Rect
        base_talent_rect = pygame.Rect(self.settings.screen_width//16, self.settings.screen_width//6, self.settings.screen_width//8, self.settings.screen_width//8)
        i = 0
        for key in list(self.talent_dict.keys()):
            self.talent_dict[key]["rect"] = base_talent_rect.move(self.settings.screen_width*5//32 * (i%4), self.settings.screen_width*3//16 * (i//4))
            self.talent_dict[key]["img"] = pygame.transform.scale(self.talent_dict[key]["img"], base_talent_rect.size)
            
            
            if len(key) < 12:
                self.talent_dict[key]["txt"] = [self.settings.font["h3"].render(key.replace("_", " "), True, (255, 255, 255))]
                self.talent_dict[key]["txt_rect"] = [self.talent_dict[key]["txt"][0].get_rect(midtop=self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8).midtop)]
                self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"].union(self.talent_dict[key]["txt_rect"][0])
            else:
                self.talent_dict[key]["txt"] = []
                self.talent_dict[key]["txt_rect"] = []
                self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"].copy()
                mots = key.split("_")
                ligne = 0
                for mot in mots:
                    txt = self.settings.font["h3"].render(mot, True, (255, 255, 255))
                    txt_rect = txt.get_rect(midtop=self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8 + ligne).midtop)
                    self.talent_dict[key]["txt"].append(txt)
                    self.talent_dict[key]["txt_rect"].append(txt_rect)
                    self.talent_dict[key]["total_rect"].union_ip(txt_rect)
                    ligne += 25 # font size + 1
            self.talent_dict[key]["cadre"] = pygame.transform.scale(cadre, self.talent_dict[key]["total_rect"].size)
            i += 1

        self.stats_rect = pygame.Rect(self.settings.screen_width*2//3, self.settings.screen_height//4, self.settings.screen_width//3, self.settings.screen_height//2)
        
        # Charger l'image de fond
        bg_img = pygame.image.load("assets/images/background/perks_scene.png")
        self.bg_image = pygame.transform.scale(bg_img, (self.settings.screen_width, self.settings.screen_height))

        
    
    def handle_event(self, event):
        """Gère les clics de souris et touches"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_button.move(self.settings.x0, self.settings.y0).collidepoint(event.pos):
                self.game.change_scene(self.settings.SCENE_MENU)
    
    
    
    def update(self):
        """met a jours les éléments et la logique de la scene"""
        pass
    
    def draw(self, screen):
        """Dessine la scene"""

        # Image de fond
        screen.blit(self.bg_image, (0, 0))

        pygame.draw.rect(screen, (255, 255, 0), self.exit_button)
        
        i = 0
        for key in list(self.talent_dict.keys()):
            screen.blit(self.talent_dict[key]["cadre"], self.talent_dict[key]["total_rect"].topleft)

            screen.blit(self.talent_dict[key]["img"], self.talent_dict[key]["rect"].topleft)
            for txt, txt_rect in zip(self.talent_dict[key]["txt"], self.talent_dict[key]["txt_rect"]):
                screen.blit(txt, txt_rect)
            i += 1

        pygame.draw.rect(screen, (100, 100, 100), self.stats_rect)
        i = 0
        for key in self.player_data.keys():
            i += 1
            txt = self.settings.font["h4"].render(f"{key}: {self.player_data[key]}", True, (0, 0, 0))
            rect = txt.get_rect(topleft = (self.stats_rect[0] + 5, self.stats_rect[1] + 20*i + 5))
            screen.blit(txt, rect)
    
    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions et la taille des éléments
        """
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.exit_button.update(self.settings.screen_width - 60, 10, 50, 50)

        i = 0
        for key in list(self.talent_dict.keys()):
            self.talent_dict[key]["rect"].update(
                self.settings.screen_width//16 + self.settings.screen_width*5//32 * (i%4),
                self.settings.screen_width//6 + self.settings.screen_width*3//16 * (i//4),
                self.settings.screen_width//8,
                self.settings.screen_width//8
                )
            # ça baisse la qualité des images quand on passe à une taille plus petite mais flem (image redéfini a partir des précedents)
            self.talent_dict[key]["img"] = pygame.transform.scale(self.talent_dict[key]["img"], self.talent_dict[key]["rect"].size)
            self.talent_dict[key]["total_rect"] = self.talent_dict[key]["rect"].copy()
            ligne = 0
            for rect in self.talent_dict[key]["txt_rect"]:
                rect.midtop = self.talent_dict[key]["rect"].move(0, self.settings.screen_width//8 + ligne).midtop
                self.talent_dict[key]["total_rect"].union_ip(rect)
                ligne += 25 # font size + 1
            i += 1
            
            self.talent_dict[key]["cadre"] = pygame.transform.scale(self.talent_dict[key]["cadre"], self.talent_dict[key]["total_rect"].size)

            self.stats_rect.update(self.settings.screen_width*2//3, self.settings.screen_height//4, self.settings.screen_width//3, self.settings.screen_height//2)
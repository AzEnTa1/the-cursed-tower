# src/ui/perks_ui.py
import pygame

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        
        self.perks_imgs = {
                           "player_speed":pygame.image.load(r"assets\images\perks_icons\Speed_Icon.png"),
                           "player_attack_speed":pygame.image.load(r"assets\images\perks_icons\Attack_speed_icon.png"),
                           "player_attack_damage":pygame.image.load(r"assets\images\perks_icons\Attack_icon.png"),
                           "player_max_health":pygame.image.load(r"assets\images\perks_icons\Heal_icon.png"),
                           "player_size_up":pygame.image.load(r"assets\images\perks_icons\Player_size_up_icon.png"),
                           "player_size_down":pygame.image.load(r"assets\images\perks_icons\Player_size_down_icon.png"),
                           "player_regen":pygame.image.load(r"assets\images\perks_icons\Regen_icon.png"),
                           "projectile_speed":pygame.image.load(r"assets\images\perks_icons\Projectile_speed_icon.png"), 
                           "multishot":pygame.image.load(r"assets\images\perks_icons\Multishot_icon.png"),
                           "infinite life":pygame.image.load(r"assets\images\perks_icons\Shield_icon.png"),
                           "arc_shot":pygame.image.load(r"assets\images\perks_icons\Arc_shoot_icon.png"),
        }

        # si une image n'est pas trouvée, on remplace par une image aléatoire parmi celle disponibles
        for perks in self.perks_imgs:
            if self.perks_imgs[perks] is None:
                self.perks_imgs[perks] = pygame.image.load(r"assets\images\perks_icons\Blank_Icon.png")

        self.menu_rect = pygame.Rect(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
        

    def draw(self, screen, perks_rect, perks_list):
        """dessine l'interface complète"""
        self._draw_background(screen)
        for rect, perk in zip(perks_rect, perks_list):
            txt = self.settings.font["h3"].render(perk, True, (0, 0, 0))
            fd_perks = pygame.image.load(r"assets/images/cadre.png")
            fd_perks = pygame.transform.scale(fd_perks, (rect[0][2], rect[0][3]))
            screen.blit(fd_perks, rect[0])
            fd_text = pygame.image.load(r"assets/images/cadre.png")
            fd_text = pygame.transform.scale(fd_text, (rect[1][2], rect[1][3]))
            screen.blit(fd_text, rect[1])
            txt = self.settings.font["h3"].render(perk, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=rect[1].center))
            #affichage image
            screen.blit(pygame.transform.smoothscale(self.perks_imgs[perk], (rect[0][2], rect[0][3])), rect[0])


    def _draw_background(self, screen):
        """dessine le background"""
        bg_image = pygame.image.load(r"assets/images/background/perks_scene.png")        
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))

    def resize(self):
        """redéfini la taille de chaque éléments"""
        self.menu_rect.update(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)

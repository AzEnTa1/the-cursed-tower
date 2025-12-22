# src/ui/perks_ui.py
import pygame

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        
        self.perks_imgs = {
                           "player_speed":pygame.image.load(r"assets\images\Speed_Icon.png"),
                           "player_attack_speed":pygame.image.load(r"assets\images\Attack_speed_icon.png"),
                           "player_attack_damage":pygame.image.load(r"assets\images\Attack_icon.png"),
                           "player_max_health":pygame.image.load(r"assets\images\Heal_icon.png"),
                           "player_size_up":pygame.image.load(r"assets\images\Player_size_up_icon.png"),
                           "player_size_down":pygame.image.load(r"assets\images\Player_size_down_icon.png"),
                           "player_regen":pygame.image.load(r"assets\images\Regen_icon.png"),
                           "projectil_speed":pygame.image.load(r"assets\images\Projectil_speed_icon.png"), 
                           "multishot":pygame.image.load(r"assets\images\Multishot_icon.png"),
                           "infinite life":pygame.image.load(r"assets\images\Shield_icon.png"),
                           "arc_shot":pygame.image.load(r"assets\images\Arc_shoot_icon.png"),
        }

        # si une image n'est pas trouvée, on remplace par une image aléatoire parmi celle disponibles
        for perks in self.perks_imgs:
            if self.perks_imgs[perks] is None:
                self.perks_imgs[perks] = pygame.image.load(r"assets\images\Blank_Icon.png")

        self.menu_rect = pygame.Rect(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)
        

    def draw(self, screen, perks_rect, perks_list):
        """dessine l'interface complète"""
        self._draw_background(screen)
        for rect, perk in zip(perks_rect, perks_list):
            txt = self.settings.font["h3"].render(perk, True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0, 0), rect[2])
            pygame.draw.rect(screen, (255, 255, 255, 0), rect[2].inflate(-5, -5))
            screen.blit(txt, txt.get_rect(center=rect[1].center))
            #affichage image
            screen.blit(pygame.transform.smoothscale(self.perks_imgs[perk], (rect[0][2], rect[0][3])), rect[0])


    def _draw_background(self, screen):
        """dessine le background"""
        pygame.draw.rect(screen, (255, 255, 0, 0), self.menu_rect)
        txt = self.settings.font["h3"].render("affichage perks", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=self.menu_rect.center)
        screen.blit(txt, rnd_rect)

    def resize(self):
        """redéfini la taille de chaque éléments"""
        self.menu_rect.update(100, 50, self.settings.screen_width - 200, self.settings.screen_height - 100)

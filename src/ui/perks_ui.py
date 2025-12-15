import pygame
import random

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        
        self.perks_imgs = {
                           "player_speed":pygame.image.load(r"assets\images\Speed_Icon.png"),
                           "player_attack_speed":None,
                           "player_attack_damage":None,
                           "player_max_health":pygame.image.load(r"assets\images\Heal_Icon.png"),
                           "player_size_up":None,
                           "player_size_down":None,
                           "player_regen":pygame.image.load(r"assets\images\Heal_Icon.png"),
                           "projectil_speed":None, 
                           "multishot":None,
                           "infinite life":None,
                           "arc_shot":None
        }

        # si une image n'est pas trouvée, on remplace par une image aléatoire parmi celle disponibles
        for perks in self.perks_imgs:
            if self.perks_imgs[perks] is None:
                self.perks_imgs[perks] = random.choice([img for img in self.perks_imgs.values() if img is not None])

    def draw(self, screen, perks_rect, perks_list):
        """dessine l'interface complète"""
        self._draw_background(screen)
        for rect, perk in zip(perks_rect, perks_list):
            txt = pygame.font.Font(None, 24).render(perk, True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0, 0), rect[2])
            pygame.draw.rect(screen, (255, 255, 255, 0), rect[2].inflate(-5, -5))
            screen.blit(txt, txt.get_rect(center=rect[1].center))
            #affichage image
            screen.blit(pygame.transform.smoothscale(self.perks_imgs[perk], (rect[0][2], rect[0][3])), rect[0])


    def _draw_background(self, screen):
        """dessine le background"""
        pygame.draw.rect(screen, (255, 255, 0, 0), self.menu_rect)
        txt = pygame.font.Font(None, 24).render("affichage perks", True, (0, 0, 0))
        rnd_rect = txt.get_rect(center=self.menu_rect.center)
        screen.blit(txt, rnd_rect)

    def resize(self):
        """redéfini la taille de chaque éléments"""
        self.menu_rect = pygame.Rect(self.settings.x0 + 100, self.settings.y0 + 50, self.settings.screen_width - 200, self.settings.screen_height - 100)

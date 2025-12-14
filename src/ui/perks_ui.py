import pygame

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        
        
        self.perks_imgs = {
                           "player_speed":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_attack_speed":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_attack_damage":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_max_health":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_size_up":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_size_down":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "player_regen":pygame.image.load(r"assets\images\Speed_icon.png"),
                           "projectil_speed":pygame.image.load(r"assets\images\Speed_icon.png"), 
                           "multishot":pygame.image.load(r"assets\images\Speed_icon.png")
        }

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

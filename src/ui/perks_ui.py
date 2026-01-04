# src/ui/perks_ui.py
import pygame

class PerksUI:
    def __init__(self, settings):
        self.settings = settings
        
        self.perks_imgs = {
            "player_speed": pygame.image.load(r"assets/images/perks_icons/Speed_icon.png").convert_alpha(),
            "player_attack_speed": pygame.image.load(r"assets/images/perks_icons/Attack_speed_icon.png").convert_alpha(),
            "player_attack_damage": pygame.image.load(r"assets/images/perks_icons/Attack_icon.png").convert_alpha(),
            "player_max_health": pygame.image.load(r"assets/images/perks_icons/Heal_icon.png").convert_alpha(),
            "player_size_up": pygame.image.load(r"assets/images/perks_icons/Player_size_up_icon.png").convert_alpha(),
            "player_size_down": pygame.image.load(r"assets/images/perks_icons/Player_size_down_icon.png").convert_alpha(),
            "player_regen": pygame.image.load(r"assets/images/perks_icons/Regen_icon.png").convert_alpha(),
            "projectile_speed": pygame.image.load(r"assets/images/perks_icons/Projectile_speed_icon.png").convert_alpha(),
            "multishot": pygame.image.load(r"assets/images/perks_icons/Multishot_icon.png").convert_alpha(),
            "infinite life": pygame.image.load(r"assets/images/perks_icons/Shield_icon.png").convert_alpha(),
            "arc_shot": pygame.image.load(r"assets/images/perks_icons/Arc_shoot_icon.png").convert_alpha(),
        }

        # Si une image n'est pas trouvée, on remplace par une image par défaut
        for perk_name in self.perks_imgs:
            if self.perks_imgs[perk_name] is None:
                self.perks_imgs[perk_name] = pygame.Surface((64, 64), pygame.SRCALPHA)
                self.perks_imgs[perk_name].fill((100, 100, 100, 200))
        
        self.cadre_img = pygame.image.load(r"assets/images/cadre.png").convert_alpha()
        self.background_img = pygame.image.load(r"assets/images/background/perks_scene.png").convert()
        
        self.title_font = pygame.font.Font(None, 48)
        self.perk_font = pygame.font.Font(None, 24)
        

    def draw(self, screen, perks_rect, perks_list):
        """Dessine l'interface complète"""
        
        self._draw_background(screen)
        # Titre
        title = self.title_font.render("CHOISISSEZ UNE CAPACITÉ", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, screen.get_height() - 130))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = self.perk_font.render("Cliquez sur une capacité pour l'équiper", 
                                           True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(self.settings.screen_width // 2, screen.get_height()  - 80))
        screen.blit(instructions, instructions_rect)
        # Affichage des perks
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
            screen.blit(pygame.transform.smoothscale(self.perks_imgs[perk], (rect[0][2], rect[0][3])), rect[0])
            
            if rect[2].move(self.settings.x0, self.settings.y0).collidepoint(pygame.mouse.get_pos()):
                hover_cadre = pygame.image.load(r"assets/images/cadre.png")
                hover_cadre = pygame.transform.scale(hover_cadre, (rect[0][2]+10, rect[0][3]+10))
                hover_rect = hover_cadre.get_rect(center=rect[0].center)
                screen.blit(hover_cadre, hover_rect)
                # Affiche l'icône agrandie
                screen.blit(pygame.transform.smoothscale(self.perks_imgs[perk], (rect[0][2]+10, rect[0][3]+10)), rect[0].move(-5, -5))
                # Affiche la description du perk
                desc = self._get_perk_description(perk)
                if desc:
                    desc_bg = pygame.image.load(r"assets/images/cadre.png")
                    desc_bg = pygame.transform.scale(desc_bg, (rect[1][2]+200, 40))
                    desc_bg_rect = desc_bg.get_rect(center=(rect[1].center[0], rect[1].center[1] + 40))
                    screen.blit(desc_bg, desc_bg_rect)
                    
                    desc_surface = self.perk_font.render(desc, True, (255, 255, 255))
                    desc_rect = desc_surface.get_rect(center=(rect[1].center[0], rect[1].center[1] + 40))
                    screen.blit(desc_surface, desc_rect)
            
    def _get_perk_description(self, perk_name):
        """Retourne la description d'un perk"""
        descriptions = {
            "player_speed": "+20% vitesse de déplacement",
            "player_attack_speed": "+20% vitesse d'attaque",
            "player_attack_damage": "+30 dégâts",
            "player_max_health": "+20 points de vie max",
            "player_size_up": "+10% taille (meilleure visibilité)",
            "player_size_down": "-10% taille (plus difficile à toucher)",
            "player_regen": "Soigne 20% de vos PV",
            "projectile_speed": "+10% vitesse des projectiles",
            "multishot": "Tire +1 projectile supplémentaire",
            "infinite life": "INVINCIBILITÉ (debug)",
            "arc_shot": "Tire 3 projectiles en éventail",
        }

        return descriptions.get(perk_name, "")
    
    def _draw_background(self, screen):
        """
        Dessine le fond de l'interface des perks
        """
        bg_image = pygame.image.load(r"assets/images/background/perks_scene.png")        
        bg_image = pygame.transform.scale(bg_image, (self.settings.screen_width, self.settings.screen_height))
        screen.blit(bg_image, (0, 0))

    def resize(self):
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        pass
    
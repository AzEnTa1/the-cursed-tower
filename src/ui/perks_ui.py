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
                print(f"[UI] Image manquante pour {perk_name}")
                self.perks_imgs[perk_name] = pygame.Surface((64, 64), pygame.SRCALPHA)
                self.perks_imgs[perk_name].fill((100, 100, 100, 200))
        
        self.cadre_img = pygame.image.load(r"assets/images/cadre.png").convert_alpha()
        self.background_img = pygame.image.load(r"assets/images/background/perks_scene.png").convert()
        
        self.title_font = pygame.font.Font(None, 48)
        self.perk_font = pygame.font.Font(None, 24)
        
        self.hovered_index = -1

    def draw(self, screen, perks_rect, perks_list):
        """Dessine l'interface complète"""
        # Vérifier la souris pour l'effet hover
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_index = -1
        
        for i, (_, _, union_rect) in enumerate(perks_rect):
            # Convertir les coordonnées pour la détection de souris
            rect_in_screen = union_rect.move(self.settings.x0, self.settings.y0)
            if rect_in_screen.collidepoint(mouse_pos):
                self.hovered_index = i
                break
        
        # Dessiner le fond
        scaled_bg = pygame.transform.scale(self.background_img, 
                                         (self.settings.screen_width, self.settings.screen_height))
        screen.blit(scaled_bg, (0, 0))
        
        # Titre
        title = self.title_font.render("CHOISISSEZ UNE AMÉLIORATION", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 80))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = self.perk_font.render("Cliquez sur une amélioration pour l'équiper", 
                                           True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(self.settings.screen_width // 2, 120))
        screen.blit(instructions, instructions_rect)
        
        # Dessiner les 3 perks
        for i, (image_rect, text_rect, union_rect) in enumerate(perks_rect):
            if i >= len(perks_list):
                continue
                
            perk_name = perks_list[i]
            
            # Effet de survol
            is_hovered = (i == self.hovered_index)
            
            # Dessiner le cadre
            cadre_scaled = pygame.transform.scale(self.cadre_img, 
                                                (union_rect.width + 20, union_rect.height + 20))
            cadre_pos = (union_rect.x - 10, union_rect.y - 10)
            
            # Changer la couleur du cadre si survolé
            if is_hovered:
                # Créer une surface colorée pour l'effet de survol
                overlay = pygame.Surface((union_rect.width + 20, union_rect.height + 20), pygame.SRCALPHA)
                overlay.fill((255, 255, 200, 50))  # Jaune semi-transparent
                screen.blit(cadre_scaled, cadre_pos)
                screen.blit(overlay, cadre_pos)
            else:
                screen.blit(cadre_scaled, cadre_pos)
            
            # Dessiner l'image du perk
            if perk_name in self.perks_imgs:
                img = self.perks_imgs[perk_name]
                img_scaled = pygame.transform.smoothscale(img, (image_rect.width, image_rect.height))
                screen.blit(img_scaled, image_rect)
            
            # Dessiner le texte du perk
            text_color = (255, 255, 200) if is_hovered else (255, 255, 255)
            perk_text = self.perk_font.render(perk_name.replace('_', ' ').title(), True, text_color)
            text_pos = text_rect.center
            
            # Ajuster la position du texte pour qu'il soit centré
            text_rect_obj = perk_text.get_rect(center=text_pos)
            screen.blit(perk_text, text_rect_obj)
            
            # Description supplémentaire pour certains perks
            if is_hovered:
                desc = self._get_perk_description(perk_name)
                if desc:
                    desc_surface = self.perk_font.render(desc, True, (200, 255, 200))
                    desc_rect = desc_surface.get_rect(center=(text_pos[0], text_pos[1] + 30))
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

    def resize(self):
        """Redimensionne les éléments UI"""
        pass  # Les rectangles sont recalculés dans la scène
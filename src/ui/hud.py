import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, BLUE, YELLOW

class HUD:
    def __init__(self, player, wave_manager, current_floor):
        self.player = player
        self.wave_manager = wave_manager
        self.current_floor = current_floor
        
        # Polices
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Positions des éléments HUD
        self.hud_margin = 10
        self.bar_width = 200
        self.bar_height = 20
    
    def update_floor(self, new_floor):
        """Met à jour l'étage affiché"""
        self.current_floor = new_floor
    
    def draw(self, screen):
        """Dessine tous les éléments du HUD"""
        self.draw_health_bar(screen)
        self.draw_wave_info(screen)
        self.draw_floor_info(screen)
        self.draw_score(screen)
        self.draw_weapon_info(screen)
        self.draw_aim_indicator(screen)
        self.draw_legend(screen)
    
    def draw_health_bar(self, screen):
        """Barre de vie du joueur"""
        bar_x = self.hud_margin
        bar_y = self.hud_margin
        
        # Fond de la barre
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, self.bar_width, self.bar_height))
        
        # Vie actuelle
        health_percent = self.player.health / self.player.max_health
        health_width = int(self.bar_width * health_percent)
        
        # Couleur qui change selon la vie
        if health_percent > 0.6:
            color = GREEN
        elif health_percent > 0.3:
            color = YELLOW
        else:
            color = RED
            
        pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, self.bar_height))
        
        # Texte
        health_text = self.font_medium.render(f"VIE: {self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (bar_x, bar_y + 25))
    
    def draw_wave_info(self, screen):
        """Informations sur la vague actuelle"""
        wave_info = self.wave_manager.get_wave_info()
        
        wave_text = self.font_medium.render(
            f"VAGUE: {wave_info['current_wave']}/3", 
            True, WHITE
        )
        screen.blit(wave_text, (self.hud_margin, 70))
        
        # Ennemis restants dans la vague
        enemies_text = self.font_small.render(
            f"Ennemis: {wave_info['enemies_remaining']}", 
            True, WHITE
        )
        screen.blit(enemies_text, (self.hud_margin, 95))
        
        # État de la vague
        state_text = ""
        state_color = WHITE
        if wave_info['state'] == "between_waves" and self.wave_manager.wave_queue.has_more_waves():
            state_text = "Prochaine vague..."
            state_color = (255, 255, 0)
        elif wave_info['state'] == "in_wave":
            state_text = "COMBAT!"
            state_color = (255, 100, 100)
        elif wave_info['state'] == "all_cleared":
            state_text = "Étage terminé!"
            state_color = (100, 255, 100)
        
        state_display = self.font_small.render(state_text, True, state_color)
        screen.blit(state_display, (self.hud_margin, 120))
    
    def draw_floor_info(self, screen):
        """Informations sur l'étage actuel"""
        floor_text = self.font_large.render(
            f"ÉTAGE {self.current_floor}", 
            True, WHITE
        )
        text_rect = floor_text.get_rect(center=(SCREEN_WIDTH // 2, 25))
        screen.blit(floor_text, text_rect)
    
    def draw_score(self, screen):
        """Score du joueur"""
        score_text = self.font_medium.render(
            f"SCORE: {self.player.score}", 
            True, WHITE
        )
        screen.blit(score_text, (SCREEN_WIDTH - 150, self.hud_margin))
    
    def draw_weapon_info(self, screen):
        """Informations sur l'arme"""
        if hasattr(self.player, 'weapon') and self.player.weapon:
            weapon_text = self.font_small.render(
                f"Arme: {self.player.weapon.fire_rate} tirs/sec", 
                True, WHITE
            )
            screen.blit(weapon_text, (SCREEN_WIDTH - 150, 30))
    
    def draw_aim_indicator(self, screen):
        """Indicateur de visée automatique"""
        if hasattr(self.player, 'weapon') and self.player.weapon:
            stationary_percent = min(self.player.weapon.stationary_time / self.player.weapon.stationary_threshold, 1.0)
            
            # Barre de progression de visée
            aim_bar_x = SCREEN_WIDTH - 150
            aim_bar_y = 60
            aim_bar_width = 120
            aim_bar_height = 8
            
            # Fond
            pygame.draw.rect(screen, (50, 50, 50), (aim_bar_x, aim_bar_y, aim_bar_width, aim_bar_height))
            
            # Progression
            aim_width = int(aim_bar_width * stationary_percent)
            pygame.draw.rect(screen, BLUE, (aim_bar_x, aim_bar_y, aim_width, aim_bar_height))
            
            # Texte
            aim_text = self.font_small.render("Visée", True, WHITE)
            screen.blit(aim_text, (aim_bar_x, aim_bar_y + 12))
            
            if stationary_percent >= 1.0:
                ready_text = self.font_small.render("PRÊT!", True, GREEN)
                screen.blit(ready_text, (aim_bar_x + 50, aim_bar_y + 12))
    
    def draw_legend(self, screen):
        """Légende des ennemis"""
        legend_y = SCREEN_HEIGHT - 100
        self.font_small.render("Légende:", True, WHITE)
        screen.blit(self.font_small.render("Légende:", True, WHITE), (10, legend_y))
        screen.blit(self.font_small.render("Rouge: Chargeur", True, (255, 100, 100)), (10, legend_y + 20))
        screen.blit(self.font_small.render("Bleu: Tireur", True, (100, 100, 255)), (10, legend_y + 40))
        screen.blit(self.font_small.render("Magenta: Suicide", True, (255, 0, 255)), (10, legend_y + 60))
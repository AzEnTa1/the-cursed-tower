import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, BLUE, YELLOW

class HUD:
    def __init__(self, player, wave_manager, weapon):
        self.player = player
        self.wave_manager = wave_manager
        self.weapon = weapon
        
        # Polices
        self.title_font = pygame.font.Font(None, 36)
        self.normal_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Positions
        self.margin = 10
        self.bar_height = 8
        self.bar_width = 150
        
    def draw(self, screen):
        """Dessine l'interface complète sans radar"""
        self.draw_health_bar(screen)
        self.draw_wave_info(screen)
        self.draw_aim_indicator(screen)
        self.draw_floor_info(screen)
        self.draw_quick_stats(screen)
        
    def draw_health_bar(self, screen):
        """Barre de vie avec pourcentage"""
        # Fond de la barre
        bar_x = self.margin
        bar_y = self.margin
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
        health_text = self.normal_font.render(
            f"VIE: {self.player.health}/{self.player.max_health}", 
            True, WHITE
        )
        screen.blit(health_text, (bar_x, bar_y + self.bar_height + 2))
        
    def draw_wave_info(self, screen):
        """Informations sur les vagues"""
        wave_info = self.wave_manager.get_wave_info()
        
        # Étage et vague
        floor_text = self.title_font.render(
            f"ÉTAGE {wave_info['floor']}", 
            True, WHITE
        )
        screen.blit(floor_text, (SCREEN_WIDTH - 150, self.margin))
        
        wave_text = self.normal_font.render(
            f"VAGUE {wave_info['current_wave']}/3", 
            True, WHITE
        )
        screen.blit(wave_text, (SCREEN_WIDTH - 150, self.margin + 35))
        
        # État de la vague avec couleur
        state_text = ""
        state_color = WHITE
        
        if wave_info['state'] == "between_waves" and self.wave_manager.wave_queue.has_more_waves():
            state_text = "PRÉPAREZ-VOUS"
            state_color = YELLOW
        elif wave_info['state'] == "in_wave":
            state_text = f"ENNEMIS: {wave_info['enemies_remaining']}"
            state_color = RED
        elif wave_info['state'] == "all_cleared":
            state_text = "ÉTAGE TERMINÉ!"
            state_color = GREEN
            
        state_display = self.normal_font.render(state_text, True, state_color)
        screen.blit(state_display, (SCREEN_WIDTH - 150, self.margin + 60))
        
    def draw_aim_indicator(self, screen):
        """Indicateur de visée avec barre de progression"""
        stationary_percent = min(self.weapon.stationary_time / self.weapon.stationary_threshold, 1.0)
        
        # Barre de progression de visée
        aim_x = self.margin
        aim_y = 80  # Sous la barre de vie
        
        # Fond
        pygame.draw.rect(screen, (50, 50, 50), (aim_x, aim_y, self.bar_width, self.bar_height))
        
        # Progression
        aim_width = int(self.bar_width * stationary_percent)
        pygame.draw.rect(screen, BLUE, (aim_x, aim_y, aim_width, self.bar_height))
        
        # Texte
        if stationary_percent >= 1.0:
            aim_text = self.normal_font.render("PRÊT À TIRER!", True, GREEN)
        else:
            aim_text = self.normal_font.render(f"VISÉE: {int(stationary_percent * 100)}%", True, WHITE)
            
        screen.blit(aim_text, (aim_x, aim_y + self.bar_height + 2))
        
    def draw_floor_info(self, screen):
        """Informations générales en bas"""
        info_y = SCREEN_HEIGHT - 40
        
        # Score
        score_text = self.small_font.render(f"Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (self.margin, info_y))
        
        # Instructions
        instructions = self.small_font.render("ZQSD: Déplacer • Stop: Viser automatique • ESC: Menu", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, info_y))
        
    def draw_quick_stats(self, screen):
        """Statistiques rapides en haut à droite"""
        stats_x = SCREEN_WIDTH - 200
        stats_y = 100
        
        # Score actuel
        score_text = self.normal_font.render(f"SCORE: {self.player.score}", True, YELLOW)
        screen.blit(score_text, (stats_x, stats_y))
        
        # Ennemis tués dans cette vague (approximatif)
        enemies_killed = max(0, self.wave_manager.enemies_remaining - len(self.wave_manager.current_wave_enemies))
        if self.wave_manager.wave_number > 0:
            kills_text = self.small_font.render(f"Tués cette vague: {enemies_killed}", True, WHITE)
            screen.blit(kills_text, (stats_x, stats_y + 30))
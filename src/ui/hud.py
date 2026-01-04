# src/ui/hud.py
import pygame
import math

class HUD:
    def __init__(self, player, wave_manager, weapon, settings):
        self.player = player
        self.wave_manager = wave_manager
        self.weapon = weapon
        self.settings = settings
        
        # Positions et dimensions
        self.margin = 15
        self.bar_height = 12
        self.small_bar_height = 8
        self.corner_radius = 4
        self.pulse_value = 0
        self.pulse_speed = 0.05
        
        # Police pour les petites infos
        self.small_font = pygame.font.Font(None, 20)
    
    def update(self, dt):
        """Met à jour les animations du HUD"""
        self.pulse_value = (self.pulse_value + self.pulse_speed) % (2 * math.pi)
    
    def draw(self, screen):
        """Dessine l'interface complète"""
        # Dessiner les éléments principaux
        self.draw_health_bar(screen)
        self.draw_dash_indicator(screen)
        self.draw_wave_info(screen)
        self.draw_aim_indicator(screen)
        self.draw_floor_overview(screen)
        
        # Infos rapides en bas
        self.draw_quick_info(screen)
    
    def draw_health_bar(self, screen):
        """Barre de vie épurée"""
        bar_x = self.margin
        bar_y = self.margin
        bar_width = 200
        
        # Calcul de la santé
        health_percent = self.player.health / self.player.max_health
        
        # Fond de la barre
        pygame.draw.rect(screen, (40, 40, 40), 
                        (bar_x, bar_y, bar_width, self.bar_height),
                        border_radius=self.corner_radius)
        
        # Barre de vie
        if health_percent > 0:
            health_width = int(bar_width * health_percent)
            
            # Déterminer la couleur
            if health_percent > 0.6:
                color = self.settings.GREEN
            elif health_percent > 0.3:
                color = self.settings.YELLOW
            else:
                color = self.settings.RED
                # Pulsation rouge pour basse vie
                pulse = math.sin(self.pulse_value * 3) * 2
                health_width = max(5, health_width + int(pulse))
            
            pygame.draw.rect(screen, color, 
                           (bar_x, bar_y, health_width, self.bar_height),
                           border_radius=self.corner_radius)
        
        # Bordure
        pygame.draw.rect(screen, (80, 80, 80), 
                        (bar_x, bar_y, bar_width, self.bar_height),
                        1, border_radius=self.corner_radius)
        
        # Texte santé
        health_text = self.settings.font["h3"].render(
            f"{int(self.player.health)}/{self.player.max_health}", 
            True, (255, 255, 255)
        )
        screen.blit(health_text, (bar_x + bar_width + 10, bar_y - 2))
    
    def draw_dash_indicator(self, screen):
        """Indicateur de dash simple"""
        dash_x = self.margin
        dash_y = self.margin + 30
        bar_width = 120
        
        # Calcul du cooldown
        dash_percent = self.player.get_dash_cooldown_percent()
        is_ready = dash_percent >= 1.0
        
        # Fond
        pygame.draw.rect(screen, (30, 30, 50), 
                        (dash_x, dash_y, bar_width, self.small_bar_height),
                        border_radius=self.corner_radius)
        
        # Barre de recharge
        if dash_percent > 0:
            dash_width = int(bar_width * dash_percent)
            dash_color = (100, 200, 255) if is_ready else (50, 100, 255)
            pygame.draw.rect(screen, dash_color, 
                           (dash_x, dash_y, dash_width, self.small_bar_height),
                           border_radius=self.corner_radius)
        
        # Bordure
        border_color = (100, 200, 255) if is_ready else (80, 80, 120)
        pygame.draw.rect(screen, border_color, 
                        (dash_x, dash_y, bar_width, self.small_bar_height),
                        1, border_radius=self.corner_radius)
        
        # Texte
        status = "PRÊT" if is_ready else f"{(self.player.dash_cooldown/60):.1f}s"
        dash_text = self.settings.font["h4"].render(
            f"DASH: {status}", 
            True, (200, 200, 255)
        )
        screen.blit(dash_text, (dash_x + bar_width + 10, dash_y - 3))
    
    def draw_wave_info(self, screen):
        """Informations sur la vague actuelle"""
        wave_info = self.wave_manager.get_wave_info()
        
        # Position en haut à droite
        info_x = self.settings.screen_width - 130
        info_y = self.margin
        
        # Étage
        floor_text = self.settings.font["h2"].render(
            f"Étage {wave_info['floor']}", 
            True, (255, 215, 0)
        )
        screen.blit(floor_text, (info_x, info_y))
        
        # Vague actuelle - CORRIGÉ POUR AFFICHER CORRECTEMENT
        if wave_info['is_boss']:
            wave_text = self.settings.font["h3"].render(
                "BOSS", 
                True, (255, 50, 50)
            )
        else:
            # Afficher "Vague X/3" où X est la vague en cours
            current_display_wave = wave_info['current_wave']
            if wave_info['state'] == "between_waves" and current_display_wave < wave_info['total_waves']:
                current_display_wave += 1  # Afficher la prochaine vague si on est entre les vagues
            
            wave_text = self.settings.font["h3"].render(
                f"Vague {current_display_wave}/{wave_info['total_waves']}", 
                True, (100, 150, 255)
            )
        
        screen.blit(wave_text, (info_x, info_y + 35))
        
        # État de la vague
        if wave_info['state'] == "between_waves" and self.wave_manager.wave_queue.has_more_waves():
            state_text = "Préparation"
            state_color = self.settings.YELLOW
        elif wave_info['state'] == "in_wave":
            state_text = f"Ennemis: {wave_info['enemies_remaining']}"
            state_color = self.settings.RED
        elif wave_info['state'] == "all_cleared":
            state_text = "Étage terminé"
            state_color = self.settings.GREEN
        else:
            state_text = wave_info['state']
            state_color = self.settings.WHITE
        
        state_display = self.settings.font["h3"].render(state_text, True, state_color)
        screen.blit(state_display, (info_x, info_y + 65))
    
    def draw_aim_indicator(self, screen):
        """Indicateur de visée simple"""
        stationary_percent = min(self.weapon.stationary_time / self.weapon.stationary_threshold, 1.0)
        
        aim_x = self.margin
        aim_y = self.margin + 60
        bar_width = 150
        
        # Fond
        pygame.draw.rect(screen, (40, 40, 40), 
                        (aim_x, aim_y, bar_width, self.small_bar_height),
                        border_radius=self.corner_radius)
        
        # Barre de progression
        if stationary_percent > 0:
            aim_width = int(bar_width * stationary_percent)
            aim_color = (100, 150, 255) if stationary_percent < 1.0 else (100, 255, 100)
            pygame.draw.rect(screen, aim_color, 
                           (aim_x, aim_y, aim_width, self.small_bar_height),
                           border_radius=self.corner_radius)
        
        # Bordure
        pygame.draw.rect(screen, (80, 120, 200), 
                        (aim_x, aim_y, bar_width, self.small_bar_height),
                        1, border_radius=self.corner_radius)
        
        # Texte
        status = "Prêt" if stationary_percent >= 1.0 else f"{int(stationary_percent * 100)}%"
        aim_text = self.settings.font["h4"].render(
            f"Visée: {status}", 
            True, (200, 220, 255)
        )
        screen.blit(aim_text, (aim_x + bar_width + 10, aim_y - 3))
    
    def draw_floor_overview(self, screen):
        """Vue d'ensemble de l'étage"""
        wave_info = self.wave_manager.get_wave_info()
        
        info_x = self.settings.screen_width - 130
        info_y = self.margin + 100
        
        # Indicateur de boss
        is_boss_floor = wave_info['is_boss']
        boss_text = "BOSS" if is_boss_floor else "Normal"
        boss_color = (255, 50, 50) if is_boss_floor else (100, 200, 100)
        
        boss_display = self.settings.font["h3"].render(boss_text, True, boss_color)
        screen.blit(boss_display, (info_x, info_y))
        
        # Vagues restantes
        if is_boss_floor:
            waves_text = "Vague unique"
        else:
            total_waves = wave_info['total_waves']
            current_wave = wave_info['current_wave']
            
            if wave_info['state'] == "in_wave":
                # Pendant une vague, on compte la vague actuelle comme "en cours"
                remaining = max(0, total_waves - current_wave + 1)
            elif wave_info['state'] == "between_waves" and current_wave < total_waves:
                # Entre les vagues, on affiche le nombre de vagues restantes
                remaining = max(0, total_waves - current_wave)
            else:
                remaining = 0
                
            waves_text = f"Vagues restantes: {remaining}"
        
        waves_display = self.settings.font["h4"].render(
            waves_text, 
            True, (200, 200, 200)
        )
        screen.blit(waves_display, (info_x, info_y + 30))
    
    def draw_quick_info(self, screen):
        """Informations rapides en bas de l'écran"""
        info_y = self.settings.screen_height - 40
        
        # Score
        score_text = self.settings.font["h4"].render(
            f"Score: {self.player.score}", 
            True, (255, 255, 255)
        )
        screen.blit(score_text, (self.margin, info_y))
        
        # XP
        xp_text = self.settings.font["h4"].render(
            f"XP: {self.player.xp}/200", 
            True, (200, 200, 255)
        )
        screen.blit(xp_text, (self.margin + 150, info_y))
        
        # Instructions 
        instructions = self.small_font.render(
            "ZQSD: Déplacer • Stop: Viser • X: Dash • ESC: Menu", 
            True, (150, 150, 150)
        )
        screen.blit(instructions, 
                   (self.settings.screen_width // 2 - instructions.get_width() // 2, info_y))
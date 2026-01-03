import pygame
import math
from enum import Enum

class HUDMode(Enum):
    """Modes d'affichage du HUD"""
    NORMAL = "normal"
    BOSS = "boss"
    LEVEL_UP = "level_up"
    PAUSED = "paused"

class HUD:
    def __init__(self, player, wave_manager, weapon, settings):
        self.player = player
        self.wave_manager = wave_manager
        self.weapon = weapon
        self.settings = settings
        
        # Configuration
        self.MARGIN = 15
        self.BAR_HEIGHT = 14
        self.BAR_WIDTH = 200
        self.CORNER_RADIUS = 6
        
        # Couleurs
        self.COLOR_BG = (20, 20, 30, 200)
        self.COLOR_BORDER = (60, 60, 80)
        self.COLOR_TEXT = (240, 240, 245)
        self.COLOR_ACCENT = (100, 200, 255)
        self.COLOR_WARNING = (255, 150, 50)
        self.COLOR_DANGER = (255, 80, 80)
        self.COLOR_SUCCESS = (100, 255, 150)
        
        # Surfaces semi-transparentes
        self.panel_bg = self._create_panel_surface()
        self.boss_panel = self._create_boss_panel()
        
        # État
        self.mode = HUDMode.NORMAL
        self.boss_health_last = 0
        self.damage_numbers = []
        self.combo_timer = 0
        self.combo_count = 0
        
        # Animations
        self.pulse_alpha = 0
        self.pulse_direction = 1
        
    def _create_panel_surface(self):
        """Crée un fond de panel semi-transparent"""
        surface = pygame.Surface((self.BAR_WIDTH + 30, 100), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.COLOR_BG, 
                        surface.get_rect(), border_radius=self.CORNER_RADIUS)
        pygame.draw.rect(surface, self.COLOR_BORDER, 
                        surface.get_rect(), 2, border_radius=self.CORNER_RADIUS)
        return surface
    
    def _create_boss_panel(self):
        """Crée un panel spécial pour les boss"""
        width = min(400, self.settings.screen_width - 100)
        surface = pygame.Surface((width, 80), pygame.SRCALPHA)
        pygame.draw.rect(surface, (40, 20, 40, 220), 
                        surface.get_rect(), border_radius=10)
        pygame.draw.rect(surface, (255, 100, 200, 255), 
                        surface.get_rect(), 3, border_radius=10)
        return surface
    
    def update(self, dt):
        """Met à jour les animations du HUD"""
        # Animation pulse
        self.pulse_alpha += 0.05 * self.pulse_direction * dt
        if self.pulse_alpha > 1:
            self.pulse_alpha = 1
            self.pulse_direction = -1
        elif self.pulse_alpha < 0:
            self.pulse_alpha = 0
            self.pulse_direction = 1
        
        # Mettre à jour les nombres de dégâts
        for dmg in self.damage_numbers[:]:
            dmg['timer'] -= dt
            dmg['y'] -= 0.5 * dt
            if dmg['timer'] <= 0:
                self.damage_numbers.remove(dmg)
        
        # Timer de combo
        if self.combo_timer > 0:
            self.combo_timer -= dt
    
    def draw(self, screen):
        """Dessine l'interface complète"""
        self._draw_top_bar(screen)
        self._draw_bottom_bar(screen)
        self._draw_right_panel(screen)
        self._draw_weapon_info(screen)
        self._draw_player_status(screen)
        
        # Mode spécial boss
        if self.mode == HUDMode.BOSS:
            self._draw_boss_info(screen)
        
        # Nombres de dégâts flottants
        self._draw_damage_numbers(screen)
        
        # Combo
        if self.combo_timer > 0:
            self._draw_combo(screen)
    
    def _draw_top_bar(self, screen):
        """Barre supérieure avec vie et dash"""
        # Panel de fond
        screen.blit(self.panel_bg, (self.MARGIN, self.MARGIN))
        
        # Vie
        health_pct = self.player.health / self.player.max_health
        self._draw_progress_bar(
            screen,
            self.MARGIN + 20,
            self.MARGIN + 20,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
            health_pct,
            self._get_health_color(health_pct),
            f"VIE: {int(self.player.health)}/{self.player.max_health}"
        )
        
        # Dash
        dash_pct = self.player.get_dash_cooldown_percent()
        dash_color = self.COLOR_ACCENT if dash_pct == 1.0 else (100, 100, 150)
        dash_text = "DASH PRÊT!" if dash_pct == 1.0 else f"DASH: {int(dash_pct*100)}%"
        
        self._draw_progress_bar(
            screen,
            self.MARGIN + 20,
            self.MARGIN + 50,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
            dash_pct,
            dash_color,
            dash_text
        )
    
    def _draw_bottom_bar(self, screen):
        """Barre inférieure avec score et XP"""
        y_pos = self.settings.screen_height - 80
        
        # Panel de fond
        bottom_panel = pygame.Surface((self.settings.screen_width - 2*self.MARGIN, 60), pygame.SRCALPHA)
        pygame.draw.rect(bottom_panel, self.COLOR_BG, 
                        bottom_panel.get_rect(), border_radius=self.CORNER_RADIUS)
        screen.blit(bottom_panel, (self.MARGIN, y_pos))
        
        # Score
        score_text = self.settings.font["h2"].render(f"SCORE: {self.player.score}", True, (255, 215, 0))
        screen.blit(score_text, (self.MARGIN + 20, y_pos + 10))
        
        # XP
        xp_pct = self.player.xp / 200
        xp_remaining = 200 - self.player.xp
        xp_color = (150, 50, 255) if xp_pct >= 1.0 else (100, 200, 255)
        
        self._draw_progress_bar(
            screen,
            self.settings.screen_width - self.BAR_WIDTH - self.MARGIN - 20,
            y_pos + 20,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
            min(xp_pct, 1.0),
            xp_color,
            f"XP: {self.player.xp}/200" if xp_pct < 1.0 else "NIVEAU! [P]"
        )
    
    def _draw_right_panel(self, screen):
        """Panel droit avec infos de vague"""
        wave_info = self.wave_manager.get_wave_info()
        panel_x = self.settings.screen_width - 220
        
        # Panel
        right_panel = pygame.Surface((200, 120), pygame.SRCALPHA)
        pygame.draw.rect(right_panel, self.COLOR_BG, 
                        right_panel.get_rect(), border_radius=self.CORNER_RADIUS)
        pygame.draw.rect(right_panel, self.COLOR_BORDER, 
                        right_panel.get_rect(), 2, border_radius=self.CORNER_RADIUS)
        screen.blit(right_panel, (panel_x, self.MARGIN))
        
        # Titre
        title_text = self.settings.font["h2"].render(f"ÉTAGE {wave_info['floor']}", True, (255, 200, 100))
        screen.blit(title_text, (panel_x + 20, self.MARGIN + 15))
        
        # Vague
        wave_status = ""
        status_color = self.COLOR_TEXT
        
        if wave_info['state'] == "between_waves":
            wave_status = f"VAGUE {wave_info['current_wave']+1}/3"
            status_color = self.COLOR_WARNING
        elif wave_info['state'] == "in_wave":
            wave_status = f"ENNEMIS: {wave_info['enemies_remaining']}"
            status_color = self.COLOR_DANGER
        else:
            wave_status = "ÉTAGE TERMINÉ!"
            status_color = self.COLOR_SUCCESS
        
        status_text = self.settings.font["h3"].render(wave_status, True, status_color)
        screen.blit(status_text, (panel_x + 20, self.MARGIN + 50))
        
        # Mini-indicateur de vagues
        wave_y = self.MARGIN + 85
        for i in range(3):
            color = self.COLOR_SUCCESS if i < wave_info['current_wave'] else (80, 80, 100)
            if i == wave_info['current_wave'] and wave_info['state'] == "in_wave":
                color = self.COLOR_WARNING
            pygame.draw.rect(screen, color, (panel_x + 20 + i*25, wave_y, 20, 8), border_radius=2)
    
    def _draw_weapon_info(self, screen):
        """Informations sur l'arme"""
        weapon_stats = self.weapon.get_stats()
        
        # Panel
        weapon_panel = pygame.Surface((180, 100), pygame.SRCALPHA)
        pygame.draw.rect(weapon_panel, (30, 30, 40, 180), 
                        weapon_panel.get_rect(), border_radius=self.CORNER_RADIUS)
        screen.blit(weapon_panel, (self.settings.screen_width//2 - 90, self.MARGIN))
        
        # Titre
        title = self.settings.font["h3"].render("ARME", True, (200, 200, 255))
        screen.blit(title, (self.settings.screen_width//2 - 25, self.MARGIN + 10))
        
        # Stats
        stats = [
            f"DGT: {weapon_stats['damage']}",
            f"VIT: {weapon_stats['fire_rate']}/s",
            f"PRÉC: {100 - self.weapon.stationary_threshold}%"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.settings.font["h4"].render(stat, True, self.COLOR_TEXT)
            screen.blit(stat_text, (self.settings.screen_width//2 - 80, self.MARGIN + 35 + i*20))
    
    def _draw_player_status(self, screen):
        """Status du joueur (buff/debuff)"""
        # Indicateur de visée
        aim_pct = min(self.weapon.stationary_time / self.weapon.stationary_threshold, 1.0)
        
        # Cercle de visée autour du joueur
        if aim_pct > 0:
            radius = 30 + 20 * aim_pct
            alpha = int(150 * aim_pct)
            
            # Créer surface pour le cercle
            aim_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            color = (100, 200, 255, alpha) if aim_pct < 1.0 else (255, 200, 100, 200)
            
            # Cercle extérieur
            pygame.draw.circle(aim_surface, color, (radius, radius), radius, 3)
            
            # Remplissage progressif
            if aim_pct < 1.0:
                angle = 2 * math.pi * aim_pct
                pygame.draw.arc(aim_surface, color, 
                               aim_surface.get_rect(), -math.pi/2, angle - math.pi/2, 3)
            else:
                # Plein cercle quand prêt
                pygame.draw.circle(aim_surface, (255, 200, 100, 100), 
                                 (radius, radius), radius)
            
            # Afficher autour du joueur
            screen.blit(aim_surface, (self.player.x - radius, self.player.y - radius))
    
    def _draw_boss_info(self, screen):
        """Panel spécial pour les boss"""
        if not hasattr(self, 'current_boss'):
            return
        
        boss = self.current_boss
        center_x = self.settings.screen_width // 2
        
        # Panel de boss
        screen.blit(self.boss_panel, (center_x - self.boss_panel.get_width()//2, 50))
        
        # Nom du boss
        boss_name = self.settings.font["h2"].render(f"BOSS - Niveau {boss.level}", True, (255, 150, 255))
        screen.blit(boss_name, (center_x - boss_name.get_width()//2, 60))
        
        # Barre de vie du boss (grande)
        boss_health_pct = boss.health / boss.max_health
        boss_bar_width = 350
        
        # Effet de dégâts (barre rouge qui suit)
        damage_diff = self.boss_health_last - boss_health_pct
        if damage_diff > 0:
            self.boss_health_last = boss_health_pct
        
        # Barre principale
        pygame.draw.rect(screen, (80, 20, 40), 
                        (center_x - boss_bar_width//2, 100, boss_bar_width, 25), 
                        border_radius=5)
        
        # Vie actuelle
        pygame.draw.rect(screen, (255, 50, 100), 
                        (center_x - boss_bar_width//2, 100, int(boss_bar_width * boss_health_pct), 25), 
                        border_radius=5)
        
        # Texte de vie
        health_text = self.settings.font["h3"].render(
            f"{int(boss.health)}/{boss.max_health}", True, (255, 255, 255)
        )
        screen.blit(health_text, (center_x - health_text.get_width()//2, 102))
    
    def _draw_damage_numbers(self, screen):
        """Affiche les nombres de dégâts flottants"""
        for dmg in self.damage_numbers:
            alpha = int(255 * (dmg['timer'] / 60))
            size_factor = 1.0 + (1.0 - dmg['timer'] / 60) * 0.5
            
            # Couleur basée sur le type de dégâts
            if dmg['type'] == 'critical':
                color = (255, 50, 50, alpha)
                size = int(24 * size_factor)
            elif dmg['type'] == 'multishot':
                color = (100, 200, 255, alpha)
                size = int(20 * size_factor)
            else:
                color = (255, 255, 200, alpha)
                size = int(18 * size_factor)
            
            # Créer la surface pour le texte
            font = pygame.font.Font(None, size)
            text = font.render(str(dmg['value']), True, color[:3])
            
            # Position avec effet de flottement
            x = dmg['x'] - text.get_width()//2
            y = dmg['y'] - text.get_height()//2
            
            screen.blit(text, (x, y))
    
    def _draw_combo(self, screen):
        """Affiche le compteur de combo"""
        combo_alpha = int(255 * (self.combo_timer / 180))
        scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1
        
        combo_text = f"{self.combo_count} COMBO!"
        font_size = int(36 * scale)
        
        font = pygame.font.Font(None, font_size)
        text = font.render(combo_text, True, (255, 200, 100, combo_alpha))
        
        x = self.settings.screen_width // 2 - text.get_width() // 2
        y = 150
        
        screen.blit(text, (x, y))
    
    def _draw_progress_bar(self, screen, x, y, width, height, progress, color, text):
        """Dessine une barre de progression stylisée"""
        # Fond
        pygame.draw.rect(screen, (40, 40, 50), (x, y, width, height), border_radius=3)
        
        # Barre de progression
        if progress > 0:
            bar_width = int(width * progress)
            pygame.draw.rect(screen, color, (x, y, bar_width, height), border_radius=3)
            
            # Effet de brillance
            if progress > 0.1:
                highlight = pygame.Surface((bar_width, height//3), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 50))
                screen.blit(highlight, (x, y))
        
        # Bordure
        pygame.draw.rect(screen, self.COLOR_BORDER, (x, y, width, height), 2, border_radius=3)
        
        # Texte
        if text:
            text_surface = self.settings.font["h3"].render(text, True, self.COLOR_TEXT)
            screen.blit(text_surface, (x + width//2 - text_surface.get_width()//2, y - 2))
    
    def _get_health_color(self, percent):
        """Retourne une couleur basée sur le pourcentage de vie"""
        if percent > 0.7:
            return self.COLOR_SUCCESS
        elif percent > 0.4:
            return self.COLOR_WARNING
        else:
            return self.COLOR_DANGER
    
    def add_damage_number(self, value, x, y, dmg_type='normal'):
        """Ajoute un nombre de dégâts flottant"""
        self.damage_numbers.append({
            'value': value,
            'x': x,
            'y': y,
            'timer': 60,  # 1 seconde à 60 FPS
            'type': dmg_type
        })
        
        # Gestion du combo
        self.combo_count += 1
        self.combo_timer = 180  # 3 secondes
    
    def set_boss(self, boss):
        """Définit le boss actuel pour le HUD spécial"""
        self.current_boss = boss
        self.boss_health_last = boss.health / boss.max_health
        self.mode = HUDMode.BOSS
    
    def set_mode(self, mode):
        """Change le mode d'affichage du HUD"""
        self.mode = mode
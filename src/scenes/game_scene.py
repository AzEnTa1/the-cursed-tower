import pygame
import random
import math
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, SCENE_MENU
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.entities.enemys import Enemy
from src.systems.wave_manager import WaveManager
from .base_scene import BaseScene

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.weapon = None
        self.font = None
        self.small_font = None
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.current_time = 0
        self.current_floor = 1
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = Weapon(fire_rate=2)
        self.wave_manager = WaveManager()
        self.wave_manager.setup_floor(self.current_floor)
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        
        print(f"Début de l'étage {self.current_floor}")

    def handle_event(self, event):
        """Gère les événements du jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_MENU)
        
        self.player.handle_event(event)
    
    def update(self):
        """Met à jour le jeu"""
        self.current_time = pygame.time.get_ticks()
        
        # Met à jour le joueur
        self.player.update()
        
        # Met à jour l'arme et les tirs
        self.weapon.update_direction(self.player.last_dx, self.player.last_dy)
        self.weapon.update(self.player, self.current_time, self.projectiles, self.enemies)
        
        # Met à jour les projectiles du joueur
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # Met à jour les projectiles ennemis
        for projectile in self.enemy_projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.enemy_projectiles.remove(projectile)
            
            # Collisions projectiles ennemis → joueur
            distance = ((projectile.x - self.player.x)**2 + (projectile.y - self.player.y)**2)**0.5
            if distance < self.player.size + projectile.radius:
                if self.player.take_damage(projectile.damage):
                    print("Game Over!")
                if projectile in self.enemy_projectiles:
                    self.enemy_projectiles.remove(projectile)

        # CORRECTION : Met à jour le wave manager AVANT de gérer les vagues
        self.wave_manager.update(self.current_time)
        
        # CORRECTION : Gestion simplifiée des nouvelles vagues
        if (self.wave_manager.is_between_waves() and 
            self.wave_manager.wave_queue.has_more_waves() and
            len(self.enemies) == 0):  # Attendre que tous les ennemis soient morts
            
            new_enemies = self.wave_manager.start_next_wave()
            if new_enemies:
                self.enemies.extend(new_enemies)
                print(f"Vague {self.wave_manager.wave_number} commencée avec {len(new_enemies)} ennemis!")

        # CORRECTION : Vérifie si l'étage est terminé
        if (self.wave_manager.are_all_waves_cleared() and 
            len(self.enemies) == 0 and 
            len(self.enemy_projectiles) == 0):
            
            print(f"Étage {self.current_floor} terminé! Passage à l'étage suivant...")
            self.next_floor()

        # CORRECTION AMÉLIORÉE : Met à jour les ennemis
        for enemy in self.enemies[:]:
            # CORRECTION : TOUJOURS passer enemy_projectiles aux shooters
            if enemy.type == "shooter":
                enemy.update(self.player, self.enemy_projectiles)
            else:
                enemy.update(self.player, None)  # Même si pas utilisé
            
            # Collisions projectiles joueur → ennemis
            for projectile in self.projectiles[:]:
                distance = ((enemy.x - projectile.x)**2 + (enemy.y - projectile.y)**2)**0.5
                if distance < enemy.radius + projectile.radius:
                    if enemy.take_damage(projectile.damage):
                        self.enemies.remove(enemy)
                        self.wave_manager.on_enemy_died(enemy)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # CORRECTION AMÉLIORÉE : Collisions ennemis mêlée → joueur
            if enemy.type != "shooter":  # Les tireurs ne font pas de dégâts de contact
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.radius + self.player.size:
                    if self.player.take_damage(enemy.damage):
                        print("Game Over!")
                    
                    # CORRECTION : Recul pour tous les ennemis de mêlée
                    dx = enemy.x - self.player.x
                    dy = enemy.y - self.player.y
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                    enemy.x += (dx / distance) * 15  # Augmenté le recul
                    enemy.y += (dy / distance) * 15

            # CORRECTION AMÉLIORÉE : Gestion des suicides
            if enemy.type == "suicide":
                distance_to_player = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                
                if enemy.is_exploding and enemy.explosion_timer <= 0:
                    # Explosion finale
                    if distance_to_player < enemy.explosion_radius:
                        if self.player.take_damage(enemy.damage):
                            print("Game Over! (Explosion suicide)")
                    self.enemies.remove(enemy)
                    self.wave_manager.on_enemy_died(enemy)
                elif distance_to_player < 50 and not enemy.is_exploding:  # Distance d'explosion
                    enemy.is_exploding = True
                    enemy.explosion_timer = 15  # Légèrement plus long pour l'animation
    
    def next_floor(self):
        """Passe à l'étage suivant"""
        self.current_floor += 1
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        
        # CORRECTION : Réinitialisation complète du wave manager
        self.wave_manager = WaveManager()
        self.wave_manager.setup_floor(self.current_floor)
        
        # Replace le joueur au centre
        self.player.x = SCREEN_WIDTH // 2
        self.player.y = SCREEN_HEIGHT // 2
        
        # Petit heal entre les étages (optionnel)
        self.player.health = min(self.player.health + 20, self.player.max_health)
        
        print(f"Nouvel étage: {self.current_floor}")
    
    def draw(self, screen):
        """Dessine le jeu"""
        # Fond noir
        screen.fill((0, 0, 0))
        
        # Dessine les projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        for projectile in self.enemy_projectiles:
            projectile.draw(screen)
        
        # Dessine les ennemis
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Dessine le joueur
        self.player.draw(screen)
        
        # Bordure
        border_size = SCREEN_HEIGHT * 0.01
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, SCREEN_WIDTH, border_size))
        pygame.draw.rect(screen, (255, 255, 0), (SCREEN_WIDTH - border_size, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, SCREEN_HEIGHT - border_size, SCREEN_WIDTH, border_size))

        # CORRECTION : Informations de vague plus claires
        wave_info = self.wave_manager.get_wave_info()
        
        # Progression
        floor_text = self.font.render(f"Étage: {self.current_floor}", True, WHITE)
        screen.blit(floor_text, (10, 10))
        
        wave_text = self.font.render(f"Vague: {wave_info['current_wave']}/3", True, WHITE)
        screen.blit(wave_text, (10, 50))
        
        enemies_text = self.font.render(f"Ennemis: {len(self.enemies)}", True, WHITE)
        screen.blit(enemies_text, (10, 90))
        
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
        
        state_display = self.small_font.render(state_text, True, state_color)
        screen.blit(state_display, (10, 130))
        
        # Interface joueur
        stationary_percent = min(self.weapon.stationary_time / self.weapon.stationary_threshold, 1.0)
        aim_text = self.small_font.render(f"Visée: {int(stationary_percent * 100)}%", True, WHITE)
        screen.blit(aim_text, (SCREEN_WIDTH - 200, 10))
        
        if self.weapon.stationary_time >= self.weapon.stationary_threshold:
            ready_text = self.small_font.render("PRÊT À TIRER!", True, GREEN)
            screen.blit(ready_text, (SCREEN_WIDTH - 200, 35))
        
        health_text = self.font.render(f"Vie: {self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (SCREEN_WIDTH - 200, 70))
        
        # Légende
        legend_y = SCREEN_HEIGHT - 120
        screen.blit(self.small_font.render("Légende:", True, WHITE), (10, legend_y))
        screen.blit(self.small_font.render("Rouge: Chargeur", True, (255, 100, 100)), (10, legend_y + 25))
        screen.blit(self.small_font.render("Bleu: Tireur", True, (100, 100, 255)), (10, legend_y + 45))
        screen.blit(self.small_font.render("Magenta: Suicide", True, (255, 0, 255)), (10, legend_y + 65))
        screen.blit(self.small_font.render("Rouge foncé: Basic", True, (200, 0, 0)), (10, legend_y + 85))
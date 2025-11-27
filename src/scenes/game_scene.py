import pygame
import random
import math
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, SCENE_MENU
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.entities.enemys import Enemy
from .base_scene import BaseScene  # Import relatif

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.weapon = None
        self.font = None
        self.small_font = None
        self.projectiles = []
        self.enemy_projectiles = []  # Projectiles des ennemis
        self.enemies = []
        self.spawn_timer = 0
        self.current_time = 0
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = Weapon(fire_rate=2)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.spawn_timer = 0
        print("Game scene entered - Stop moving to auto-aim and shoot")
    
    def handle_event(self, event):
        """Gère les événements du jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_MENU)
        
        # Passe les événements au joueur
        self.player.handle_event(event)
    
    def update(self):
        """Met à jour le jeu"""
        self.current_time = pygame.time.get_ticks()
        
        # Met à jour le joueur
        self.player.update()
        
        # Met à jour l'arme et les tirs (avec visée automatique)
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
            
            # Vérifie les collisions avec le joueur
            distance = ((projectile.x - self.player.x)**2 + (projectile.y - self.player.y)**2)**0.5
            if distance < self.player.size + projectile.radius:
                if self.player.take_damage(projectile.damage):
                    print("Game Over!")
                    # TODO: Implémenter l'écran Game Over
                if projectile in self.enemy_projectiles:
                    self.enemy_projectiles.remove(projectile)
        
        # Génération d'ennemis
        self.spawn_timer += 1
        if self.spawn_timer >= 120:  # Toutes les 2 secondes (à 60 FPS)
            self.spawn_enemy()
            self.spawn_timer = 0
        
        # Met à jour les ennemis
        for enemy in self.enemies[:]:
            if enemy.type == "shooter":
                enemy.update(self.player, self.enemy_projectiles)
            else:
                enemy.update(self.player)
            
            # Vérifie les collisions avec les projectiles du joueur
            for projectile in self.projectiles[:]:
                distance = ((enemy.x - projectile.x)**2 + (enemy.y - projectile.y)**2)**0.5
                if distance < enemy.radius + projectile.radius:
                    if enemy.take_damage(projectile.damage):
                        self.enemies.remove(enemy)

                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # Vérifie les collisions avec le joueur (pour les ennemis de mêlée)
            if enemy.type != "shooter":  # Les tireurs ne font pas de dégâts de contact
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.radius + self.player.size:
                    if self.player.take_damage(enemy.damage):
                        print("Game Over!")
                    # L'ennemi recule légèrement après avoir touché
                    dx = enemy.x - self.player.x
                    dy = enemy.y - self.player.y
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                    enemy.x += (dx / distance) * 10
                    enemy.y += (dy / distance) * 10

            if enemy.type == "suicide":
                # Vérifie si l'ennemi est à portée d'explosion
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.attack_range:
                    if self.player.take_damage(enemy.damage):
                        print("Game Over!")
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
    
    def spawn_enemy(self):
        """Fait apparaître un ennemi aléatoirement sur les bords de l'écran"""
        side = random.randint(0, 3)
        if side == 0:  # Haut
            x = random.randint(0, round(SCREEN_WIDTH*0.8))
            y = SCREEN_HEIGHT*0.1
        elif side == 1:  # Droite
            x = SCREEN_WIDTH*0.9
            y = random.randint(0, round(SCREEN_HEIGHT*0.8))
        elif side == 2:  # Bas
            x = random.randint(0, round(SCREEN_WIDTH*0.8))
            y = SCREEN_HEIGHT*0.9
        else:  # Gauche
            x = SCREEN_WIDTH*0.1
            y = random.randint(0, round(SCREEN_HEIGHT*0.8))
        
        # Choisit un type d'ennemi aléatoire
        enemy_type = random.choice(["charger", "shooter", "basic", "suicide"])
        self.enemies.append(Enemy(x, y, enemy_type))
    
    def draw(self, screen):
        """Dessine le jeu"""
        # Fond noir
        screen.fill((0, 0, 0))
        
        # Dessine les projectiles du joueur
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Dessine les projectiles ennemis
        for projectile in self.enemy_projectiles:
            projectile.draw(screen)
        
        # Dessine les ennemis
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Dessine le joueur
        self.player.draw(screen)
        
        #dessine la bordure
        border_size = SCREEN_HEIGHT*0.01
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, SCREEN_WIDTH, border_size))
        pygame.draw.rect(screen, (255, 255, 0), (SCREEN_WIDTH - border_size, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, SCREEN_HEIGHT - border_size, SCREEN_WIDTH, border_size))
        

        # Affiche les informations
        instr_text = self.font.render("ZQSD pour se déplacer", True, WHITE)
        screen.blit(instr_text, (10, 10))
        
        back_text = self.font.render("ESC pour menu", True, WHITE)
        screen.blit(back_text, (10, 50))
        
        # Instructions de tir
        stationary_percent = min(self.weapon.stationary_time / self.weapon.stationary_threshold, 1.0)
        aim_text = self.small_font.render(f"Visée: {int(stationary_percent * 100)}%", True, WHITE)
        screen.blit(aim_text, (10, 90))
        
        if self.weapon.stationary_time >= self.weapon.stationary_threshold:
            ready_text = self.small_font.render("PRÊT À TIRER!", True, GREEN)
            screen.blit(ready_text, (10, 115))
        
        # Statistiques
        stats_text = self.font.render(
            f"Ennemis: {len(self.enemies)}", 
            True, WHITE
        )
        screen.blit(stats_text, (SCREEN_WIDTH - 200, 10))
        
        # Vie du joueur
        health_text = self.font.render(f"Vie: {self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (SCREEN_WIDTH - 200, 50))
        
        # Légende des ennemis
        legend_y = SCREEN_HEIGHT - 100
        self.small_font.render("Légende:", True, WHITE)
        screen.blit(self.small_font.render("Légende:", True, WHITE), (10, legend_y))
        screen.blit(self.small_font.render("Rouge: Chargeur", True, (255, 100, 100)), (10, legend_y + 25))
        screen.blit(self.small_font.render("Bleu: Tireur", True, (100, 100, 255)), (10, legend_y + 45))
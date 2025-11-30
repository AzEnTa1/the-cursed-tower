import pygame
import random
import math
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, SCENE_MENU
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.entities.enemys import Enemy
from src.systems.wave_manager import WaveManager
from src.ui.hud import HUD  # AJOUT: Importer le HUD
from .base_scene import BaseScene

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.weapon = None
        self.hud = None  # AJOUT: Référence au HUD
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.current_time = 0
        self.current_floor = 1
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = Weapon(fire_rate=2)
        self.player.weapon = self.weapon  # AJOUT: Lier l'arme au joueur
        
        self.wave_manager = WaveManager()
        self.wave_manager.setup_floor(self.current_floor)
        
        # AJOUT: Initialiser le HUD
        self.hud = HUD(self.player, self.wave_manager, self.current_floor)
        
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

        # Met à jour le wave manager AVANT de gérer les vagues
        self.wave_manager.update(self.current_time)
        
        # Gestion des nouvelles vagues
        if (self.wave_manager.is_between_waves() and 
            self.wave_manager.wave_queue.has_more_waves() and
            len(self.enemies) == 0):
            
            new_enemies = self.wave_manager.start_next_wave()
            if new_enemies:
                self.enemies.extend(new_enemies)
                print(f"Vague {self.wave_manager.wave_number} commencée avec {len(new_enemies)} ennemis!")

        # Vérifie si l'étage est terminé
        if (self.wave_manager.are_all_waves_cleared() and 
            len(self.enemies) == 0 and 
            len(self.enemy_projectiles) == 0):
            
            print(f"Étage {self.current_floor} terminé! Passage à l'étage suivant...")
            self.next_floor()

        # Met à jour les ennemis
        for enemy in self.enemies[:]:
            if enemy.type == "shooter":
                enemy.update(self.player, self.enemy_projectiles)
            else:
                enemy.update(self.player, None)
            
            # Collisions projectiles joueur → ennemis
            for projectile in self.projectiles[:]:
                distance = ((enemy.x - projectile.x)**2 + (enemy.y - projectile.y)**2)**0.5
                if distance < enemy.radius + projectile.radius:
                    if enemy.take_damage(projectile.damage):
                        self.enemies.remove(enemy)
                        self.wave_manager.on_enemy_died(enemy)
                        # AJOUT: Ajouter des points au score
                        self.player.add_score(10)  # 10 points par ennemi
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # Collisions ennemis mêlée → joueur
            if enemy.type != "shooter":
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.radius + self.player.size:
                    if self.player.take_damage(enemy.damage):
                        print("Game Over!")
                    
                    # Recul pour tous les ennemis de mêlée
                    dx = enemy.x - self.player.x
                    dy = enemy.y - self.player.y
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                    enemy.x += (dx / distance) * 15
                    enemy.y += (dy / distance) * 15
    
    def next_floor(self):
        """Passe à l'étage suivant"""
        self.current_floor += 1
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        
        # Réinitialisation complète du wave manager
        self.wave_manager = WaveManager()
        self.wave_manager.setup_floor(self.current_floor)
        
        # AJOUT: Mettre à jour le HUD avec le nouvel étage
        self.hud.update_floor(self.current_floor)
        
        # Replace le joueur au centre
        self.player.x = SCREEN_WIDTH // 2
        self.player.y = SCREEN_HEIGHT // 2
        
        # Petit heal entre les étages
        self.player.health = min(self.player.health + 20, self.player.max_health)
        
        # AJOUT: Bonus de score pour avoir terminé l'étage
        self.player.add_score(50 * self.current_floor)  # 50 points par étage
        
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
        
        # SUPPRIMÉ: Ancienne interface remplacée par HUD
        # Dessine le HUD (doit être après tous les éléments de jeu)
        self.hud.draw(screen)
        
        # SUPPRIMÉ: Bordure jaune (optionnel - garde-la si tu préfères)
        border_size = SCREEN_HEIGHT * 0.01
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, SCREEN_WIDTH, border_size))
        pygame.draw.rect(screen, (255, 255, 0), (SCREEN_WIDTH - border_size, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, border_size, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (0, SCREEN_HEIGHT - border_size, SCREEN_WIDTH, border_size))
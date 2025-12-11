# src/scenes/game_scene.py
import pygame
import math
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.entities.enemys import Enemy
from src.entities.spawn_effect import SpawnEffect
from src.systems.wave_manager import WaveManager
from src.systems.game_stats import GameStats
from src.ui.hud import HUD
from src.ui.transition_effect import TransitionEffect
from .base_scene import BaseScene
from .sub_scenes.perks_sub_scene import PerksSubScene
from .sub_scenes.pause_sub_scene import PauseSubScene


class GameScene(BaseScene):
    def __init__(self, game, settings):
        super().__init__(game, settings)
        self.player = None
        self.weapon = None
        self.wave_manager = None
        self.game_stats = None
        self.hud = None
        self.transition = None
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.current_time = 0
        self.current_floor = 1
        self.spawn_effects = []
        
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(
            self.settings.x0 + self.settings.screen_width//2, 
            self.settings.y0 + self.settings.screen_height//2, 
            self.settings
        )
        self.weapon = Weapon(self.settings, damage=30, fire_rate=2, projectile_speed=20) 
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.setup_floor(self.current_floor)
        self.game_stats = GameStats(self.game, self.settings)
        
        # sous scènes
        self.perks_sub_scene = PerksSubScene(self.game, self, self.settings, self.player, self.weapon)
        self.pause_sub_scene = PauseSubScene(self.game, self, self.settings)
        self.game_paused = False
        self.current_sub_scene = None

        # HUD
        self.hud = HUD(self.player, self.wave_manager, self.weapon, self.settings)
        self.transition = TransitionEffect(self.settings)
        
        # Listes
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.spawn_effects = [] 
        
        print(f"Début de l'étage {self.current_floor}")

    def handle_event(self, event):
        """Gère les événements du jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Met le jeu en pause
                self.game_paused = not self.game_paused
                if self.game_paused:
                    self.current_sub_scene = self.pause_sub_scene
                    self.current_sub_scene.on_enter()
                else:
                    self.current_sub_scene = None
                
            elif event.key == pygame.K_p:
                # Affiche les perks (temporaire)
                self.game_paused = not self.game_paused
                if self.game_paused:
                    self.current_sub_scene = self.perks_sub_scene
                    self.current_sub_scene.on_enter()
                else:
                    self.current_sub_scene = None

        if self.game_paused:
            self.current_sub_scene.handle_event(event)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pass
            self.player.handle_event(event)
    
    def update(self):
        """Met à jour le jeu"""
        if self.game_paused:
            self.current_sub_scene.update()
            return
        
        self.current_time = pygame.time.get_ticks()
        dt = self.game.clock.get_time()
        
        # Met à jour l'effet de transition
        self.transition.update(dt)
        if self.transition.is_active():
            return
        
        # mahj des effets d'apparition
        for effect in self.spawn_effects[:]:
            effect.update(dt)
            if effect.is_complete():
                # Crée l'ennemi après l'effet
                enemy = self.create_enemy_from_effect(effect)
                self.enemies.append(enemy)
                self.wave_manager.current_wave_enemies.append(enemy) 
                self.spawn_effects.remove(effect)
        
        # si possible, démarrer une nouvelle vague
        if (self.wave_manager.is_between_waves() and 
            self.wave_manager.update(self.current_time) and 
            len(self.enemies) == 0 and 
            len(self.spawn_effects) == 0):
            
            spawn_positions = self.wave_manager.start_next_wave()
            if spawn_positions:
                for x, y, enemy_type in spawn_positions:
                    effect = SpawnEffect(x, y, self.settings, enemy_type)
                    self.spawn_effects.append(effect)

        # maj joueur
        self.player.update()
        
        # maj arme + tir
        self.weapon.update_direction(self.player.last_dx, self.player.last_dy)
        self.weapon.update(self.player, self.current_time, self.projectiles, self.enemies)
        
        # maj projectiles joueurs
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # maj des projectiles ennemis
        for projectile in self.enemy_projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.enemy_projectiles.remove(projectile)
            
            # Collisions projectiles ennemis → joueur
            distance = ((projectile.x - self.player.x)**2 + (projectile.y - self.player.y)**2)**0.5
            if distance < self.player.size + projectile.radius:
                if self.player.take_damage(projectile.damage):
                    self.game_stats.on_death(self.player)
                    self.game.change_scene(self.settings.SCENE_GAME_OVER)
                self.enemy_projectiles.remove(projectile)

        # maj des ennemis
        for enemy in self.enemies[:]:
            # Passe la bonne liste de projectiles selon le type
            if enemy.type in ["shooter", "destructeur"]:
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
                        # Score différent selon le type d'ennemi
                        if enemy.type == "destructeur":
                            self.player.add_score(50)
                        elif enemy.type == "suicide":
                            self.player.add_score(20)
                        else:
                            self.player.add_score(10)

                        # Affiche les perks si le score est divisible par 200
                        if self.player.score % 200 == 0:
                            self.game_paused = True
                            self.current_sub_scene = self.perks_sub_scene
                            self.current_sub_scene.on_enter()
                    
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # Collisions ennemis mêlée → joueur
            if enemy.type != "shooter" and enemy.type != "destructeur":
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.radius + self.player.size:
                    if self.player.take_damage(enemy.damage):
                        self.game_stats.on_death(self.player)
                        self.game.change_scene(self.settings.SCENE_GAME_OVER)
                
                    # Recul
                    dx = enemy.x - self.player.x
                    dy = enemy.y - self.player.y
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                    enemy.x += (dx / distance) * 15
                    enemy.y += (dy / distance) * 15

            # Gestion des suicides
            if enemy.type == "suicide":
                distance_to_player = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                
                if enemy.is_exploding and enemy.explosion_timer <= 0:
                    if distance_to_player < enemy.explosion_radius:
                        if self.player.take_damage(enemy.damage):
                            self.game_stats.on_death(self.player)
                            self.game.change_scene(self.settings.SCENE_GAME_OVER)
                    self.enemies.remove(enemy)
                    self.wave_manager.on_enemy_died(enemy)
                    self.player.add_score(15)

                    # Affiche les perks si le score est divisible par 200
                    if self.player.score % 200 == 0:
                        self.game_paused = True
                        self.current_sub_scene = self.perks_sub_scene
                        self.current_sub_scene.on_enter()
                elif distance_to_player < 50 and not enemy.is_exploding:
                    enemy.is_exploding = True
                    enemy.explosion_timer = 15
        
        # vérifier si l'étage est fini
        if (self.wave_manager.are_all_waves_cleared() and 
            len(self.enemies) == 0 and 
            len(self.enemy_projectiles) == 0 and
            len(self.spawn_effects) == 0):
            
            self.transition.start(self.next_floor)
    
    def create_enemy_from_effect(self, effect):
        """Crée un ennemi après la fin de l'effet"""
        return Enemy(effect.x, effect.y, self.settings, effect.enemy_type)
    
    def next_floor(self):
        """Passe à l'étage suivant (appelé après la transition)"""
        self.current_floor += 1
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        self.spawn_effects.clear()
        
        # Réinitialisation complète du wave manager
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.setup_floor(self.current_floor)
        
        # Replace le joueur au centre
        self.player.x = self.settings.x0 + self.settings.screen_width // 2
        self.player.y = self.settings.y0 + self.settings.screen_height // 2
        
        # Petit heal entre les étages
        self.player.health = min(self.player.health + 20, self.player.max_health)
        
        print(f"Nouvel étage: {self.current_floor}")
    
    def draw(self, screen):
        """Dessine le jeu"""
        # Fond noir
        screen.fill((0, 0, 0))
        
        # Dessine les effets d'apparition EN PREMIER (au fond)
        for effect in self.spawn_effects:
            effect.draw(screen)
        
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
        
        # Dessine le HUD
        self.hud.draw(screen)
        
        # Dessine l'effet de transition
        self.transition.draw(screen)
        
        # Dessine le menu de pause
        if self.game_paused:
            self.current_sub_scene.draw(screen)

    def resize(self, height, width):
        if self.game_paused:
            self.current_sub_scene.resize(height, width)
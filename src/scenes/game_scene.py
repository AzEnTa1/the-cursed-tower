# src/scenes/game_scene.py
import pygame
import math
import random
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.entities.enemies import *
from src.entities.spawn_effect import SpawnEffect
from src.systems.wave_manager import WaveManager
from src.systems.game_stats import GameStats
from src.ui.hud import HUD
from src.ui.transition_effect import TransitionEffect
from .base_scene import BaseScene
from .sub_scenes.perks_sub_scene import PerksSubScene
from .sub_scenes.pause_sub_scene import PauseSubScene
from src.entities.projectiles import FireZone


class GameScene(BaseScene):
    def __init__(self, game, settings):
        """
        Scène principale de jeu
        """
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
        self.fire_zones = []  # Zones de feu actives
        self.pending_fire_zones = []  # Zones en prévisualisation
        self.global_seed = random.randint(0, 2**32 - 1)  # Seed unique par partie
        random.seed(self.global_seed)
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(
            self.settings.screen_width//2, 
            self.settings.screen_height//2, 
            self.settings
        )
        self.weapon = Weapon(self.settings, damage=30, fire_rate=2, projectile_speed=10) 
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.setup_floor(self.current_floor)
        self.game_stats = GameStats(self.game, self.settings)
        
        # Sous-scènes
        self.perks_sub_scene = PerksSubScene(self.game, self, self.settings, self.player, self.weapon)
        self.pause_sub_scene = PauseSubScene(self.game, self, self.settings)
        self.game_paused = False
        self.current_sub_scene = None

        # HUD
        self.hud = HUD(self.player, self.wave_manager, self.weapon, self.settings)
        self.transition = TransitionEffect(self.settings)

        # Image de fond
        self.fond = pygame.image.load(r"assets/images/Sol-compressed.jpg")
        self.fond = pygame.transform.scale(self.fond, (self.settings.screen_width, self.settings.screen_height))
        
        # Listes
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.spawn_effects = [] 
        self.fire_zones = []
        self.pending_fire_zones = []

    def handle_event(self, event):
        """
        Gère les événements du jeu
        """
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
                    pass  # Touche P déjà gérée
            self.player.handle_event(event)
    
    def update(self):
        """Met à jour la logique du jeu"""
        if self.game_paused:
            self.current_sub_scene.update()
            return
        
        self.current_time = pygame.time.get_ticks()
        dt = self.game.clock.get_time()  # Delta time en millisecondes
        
        # Mise à jour de l'effet de transition
        self.transition.update(dt)
        if self.transition.is_active():
            return
        
        # Mise à jour des différentes composantes du jeu
        self._update_spawn_effects(dt)
        self._update_wave_manager()
        self._update_player_and_weapon(dt)
        self._update_projectiles()
        self._update_enemies(dt)
        self._update_fire_zones()
        
        self._check_floor_completion()
    
    def _update_spawn_effects(self, dt):
        """Met à jour les effets d'apparition des ennemis"""
        for effect in self.spawn_effects[:]:
            effect.update(dt)
            if effect.is_complete():
                # Crée l'ennemi après l'effet
                enemy = self.create_enemy_from_effect(effect)
                self.enemies.append(enemy)
                self.wave_manager.current_wave_enemies.append(enemy) 
                self.spawn_effects.remove(effect)
    
    def _update_wave_manager(self):
        """Met à jour le gestionnaire de vagues"""
        # Si possible, démarrer une nouvelle vague
        if (self.wave_manager.is_between_waves() and 
            self.wave_manager.update(self.current_time) and 
            len(self.enemies) == 0 and 
            len(self.spawn_effects) == 0):
            
            spawn_positions = self.wave_manager.start_next_wave()
            if spawn_positions:
                for x, y, enemy_type in spawn_positions:
                    effect = SpawnEffect(x, y, self.settings, enemy_type)
                    self.spawn_effects.append(effect)
    
    def _update_player_and_weapon(self, dt):
        """Met à jour le joueur et son arme"""
        # Mise à jour du joueur
        self.player.update()
        
        # Mise à jour de l'arme et tir de projectiles
        self.weapon.update_direction(self.player.last_dx, self.player.last_dy)
        self.weapon.update(self.player, self.current_time, self.projectiles, self.enemies, dt)
    
    def _update_projectiles(self):
        """Met à jour les projectiles du joueur et des ennemis"""
        # Mise à jour des projectiles joueurs
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # Mise à jour des projectiles ennemis
        for projectile in self.enemy_projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.enemy_projectiles.remove(projectile)
            
            # Collisions projectiles ennemis → joueur
            distance = ((projectile.x - self.player.x)**2 + (projectile.y - self.player.y)**2)**0.5
            if distance < self.player.size + projectile.radius:
                if self.player.take_damage(projectile.damage):
                    self._handle_player_death()
                if projectile in self.enemy_projectiles:
                    self.enemy_projectiles.remove(projectile)
    
    def _update_enemies(self, dt):
        """Met à jour tous les ennemis"""
        for enemy in self.enemies[:]:
            # Passe les zones de feu et pending_zones au pyromane
            if enemy.type == "pyromane":
                enemy.update(self.player, self.fire_zones, self.pending_fire_zones)
            # Passe les projectiles ennemis au shooter et destructeur
            elif enemy.type in ["shooter", "destructeur", "boss"]:
                enemy.update(self.player, self.enemy_projectiles)
            else:   
                enemy.update(self.player, None)
                        
            # Collisions projectiles joueur → ennemis
            self._check_player_projectile_collisions(enemy)
            
            # Collisions ennemis mêlée → joueur
            if enemy.type != "shooter" and enemy.type != "destructeur":
                self._check_melee_collision(enemy)
            
            # Gestion des suicides
            if enemy.type == "suicide":
                self._handle_suicide_enemy(enemy)
    
    def _check_player_projectile_collisions(self, enemy):
        """Vérifie les collisions entre projectiles joueur et ennemi"""
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
                    
                    self._check_for_level_up()

                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
                break
    
    def _check_melee_collision(self, enemy):
        """Vérifie les collisions en mêlée entre ennemi et joueur"""
        distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
        if distance < enemy.radius + self.player.size:
            if self.player.take_damage(enemy.damage):
                self._handle_player_death()
            
            # Recul
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
            enemy.x += (dx / distance) * 15
            enemy.y += (dy / distance) * 15
    
    def _handle_suicide_enemy(self, enemy):
        """Gère le comportement de l'ennemi suicide"""
        distance_to_player = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
        
        if enemy.is_exploding and enemy.explosion_timer <= 0:
            if distance_to_player < enemy.explosion_radius:
                if self.player.take_damage(enemy.damage):
                    self._handle_player_death()
            if enemy in self.enemies:
                self.enemies.remove(enemy)
            self.wave_manager.on_enemy_died(enemy)
            self.player.add_score(15)
            self._check_for_level_up()
        elif distance_to_player < 50 and not enemy.is_exploding:
            enemy.is_exploding = True
            enemy.explosion_timer = 15
    
    def _update_fire_zones(self):
        """Met à jour les zones de feu"""
        # Mettre à jour les prévisualisations de flammes
        for pending in self.pending_fire_zones[:]:
            pending['timer'] -= 1
            
            if pending['timer'] <= 0:
                # Créer la flaque de feu
                self.fire_zones.append(FireZone(pending['x'], pending['y'], self.settings))
                self.pending_fire_zones.remove(pending)
        
        # Mise à jour des zones de feu et dégâts au joueur
        for fire_zone in self.fire_zones[:]:
            if not fire_zone.update():
                self.fire_zones.remove(fire_zone)
            else:
                # Vérifie les dégâts au joueur
                fire_zone.check_damage(self.player)
    
    def _check_floor_completion(self):
        """Vérifie si l'étage est terminé"""
        if (self.wave_manager.are_all_waves_cleared() and 
            len(self.enemies) == 0 and 
            len(self.enemy_projectiles) == 0 and
            len(self.spawn_effects) == 0):

            # Démarre l'effet de transition
            self.transition.start(self.next_floor)
    
    def _handle_player_death(self):
        """Gère la mort du joueur"""
        self.game_stats.on_death(self.player)
        self.game.change_scene(self.settings.SCENE_GAME_OVER)
    
    def _check_for_level_up(self):
        """Vérifie si le joueur peut monter de niveau"""
        if self.player.xp >= 200:
            self.player.xp %= 200
            self.game_paused = True
            self.current_sub_scene = self.perks_sub_scene
            self.current_sub_scene.on_enter()
    
    def create_enemy_from_effect(self, effect):
        """
        Crée un ennemi après la fin de l'effet d'apparition
        """
        if effect.enemy_type == "charger":
            return Charger(effect.x, effect.y, self.settings)
        elif effect.enemy_type == "shooter":
            return Shooter(effect.x, effect.y, self.settings)
        elif effect.enemy_type == "suicide":
            return Suicide(effect.x, effect.y, self.settings)
        elif effect.enemy_type == "destructeur":
            return Destructeur(effect.x, effect.y, self.settings)
        elif effect.enemy_type == "pyromane":
            return Pyromane(effect.x, effect.y, self.settings)
        elif effect.enemy_type == "boss":
            return ProceduralBoss(
                effect.x, effect.y, 
                self.settings, 
                self.current_floor,
                self.game.global_seed  # Passer la seed globale
            )
        else:
            return Basic(effect.x, effect.y, self.settings)
    
    def next_floor(self):
        """
        Passe à l'étage suivant
        Appelé après la fin de l'effet de transition
        """
        self.current_floor += 1
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        self.spawn_effects.clear()
        self.fire_zones.clear()  # Vide les zones de feu
        self.pending_fire_zones.clear()  # Vide les prévisualisations
        
        # Réinitialisation complète du wave manager
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.setup_floor(self.current_floor)
        
        # Replace le joueur au centre
        self.player.x = self.settings.screen_width // 2
        self.player.y = self.settings.screen_height // 2
        
        # Petit heal entre les étages (20 PV)
        self.player.health = min(self.player.health + 20, self.player.max_health)
        
        # Log: Nouvel étage {self.current_floor}
    
    def draw(self, screen):
        """
        Dessine le jeu sur l'écran
        """
        # image de fond
        
        screen.blit(self.fond, (0, 0))
        
        
        # Dessine les effets d'apparition EN PREMIER (au fond)
        for effect in self.spawn_effects:
            effect.draw(screen)
        
        # Dessine les prévisualisations de flammes
        self._draw_fire_previews(screen)
        
        # Dessine les projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        for projectile in self.enemy_projectiles:
            projectile.draw(screen)

        # Dessine les zones de feu
        for fire_zone in self.fire_zones:
            fire_zone.draw(screen)
        
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
    
    def _draw_fire_previews(self, screen):
        """Dessine les prévisualisations des zones de feu"""
        for pending in self.pending_fire_zones:
            preview_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            preview_radius = 40
            
            # Cercle extérieur pulsant
            pulse = 5 * math.sin(pygame.time.get_ticks() * 0.005)
            outer_radius = preview_radius + pulse
            
            # Alpha basé sur le temps restant (max 45 frames)
            progress = min(pending['timer'], 45) / 45.0
            alpha = int(180 * progress)
            
            # Cercle extérieur (orange transparent)
            pygame.draw.circle(preview_surface, (255, 150, 0, alpha), 
                              (50, 50), outer_radius, 3)
            
            # Cercle intérieur (rouge plus transparent)
            inner_alpha = max(0, alpha - 60)
            pygame.draw.circle(preview_surface, (255, 50, 0, inner_alpha), 
                              (50, 50), preview_radius // 2)
            
            # Effet "onde concentrique"
            wave_progress = 1.0 - (min(pending['timer'], 45) / 45)
            wave_radius = int(preview_radius * wave_progress)
            pygame.draw.circle(preview_surface, (255, 200, 100, int(alpha * 0.3)), 
                              (50, 50), wave_radius, 2)
            
            # Appliquer la surface
            screen.blit(preview_surface, (pending['x'] - 50, pending['y'] - 50))
            
            # Texte de compte à rebours
            if pending['timer'] > 0:
                time_left = pending['timer'] / 60  # Convertir en secondes
                countdown_text = self.settings.font["h3"].render(f"{time_left:.1f}s", True, (255, 255, 255))
                screen.blit(countdown_text, (pending['x'] - 15, pending['y'] - 60))

    def resize(self):
        """Appelé lorsque la fenêtre change de taille"""
        self.fond = pygame.transform.scale(self.fond, (self.settings.screen_width, self.settings.screen_height))
        
        if self.game_paused:
            self.current_sub_scene.resize()

# src/scenes/game_scene.py 
import pygame
import math
from src.entities.player import Player
from src.entities.weapons import Weapon
from src.systems.wave_manager import WaveManager
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
        self.hud = None
        self.transition = None
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.current_time = 0
        self.current_floor = 1
        
    def on_enter(self):
        """Initialisation du jeu"""
        self.player = Player(self.settings.x0 + self.settings.screen_width//2, self.settings.y0 + self.settings.screen_height//2, self.settings)
        self.weapon = Weapon(self.settings, fire_rate=2)
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.setup_floor(self.current_floor)
        self.perks_sub_scene = PerksSubScene(self.game, self.settings)
        self.pause_sub_scene = PauseSubScene(self.game, self.settings)
        self.game_paused = False
        self.current_sub_scene = None

        # HUD sans radar
        self.hud = HUD(self.player, self.wave_manager, self.weapon, self.settings)
        self.transition = TransitionEffect(self.settings)
        
        self.projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        
        print(f"Début de l'étage {self.current_floor}")

    def handle_event(self, event):
        """Gère les événements du jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #met le jeu en pause
                self.game_paused = not self.game_paused
                self.current_sub_scene = self.pause_sub_scene
                self.current_sub_scene.on_enter()
                
            elif event.key == pygame.K_p:
                #temp affiche les perks a déplacer quand fuat mettre les perks
                self.current_sub_scene = self.perks_sub_scene
                self.game_paused = not self.game_paused
                self.current_sub_scene.on_enter()


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
            return#le jeu est en pause
        self.current_time = pygame.time.get_ticks()
        
        # Met à jour l'effet de transition
        dt = self.game.clock.get_time()
        self.transition.update(dt)
        if self.transition.is_active():
            return  # Pause le jeu pendant la transition
        
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

        # Met à jour le wave manager
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
            self.transition.start(self.next_floor)

        # Met à jour les ennemis
        # Met à jour les ennemis
        for enemy in self.enemies[:]:
            # DEBUG: affiche le type exact
            print(f"DEBUG GAME_SCENE: enemy.type = '{enemy.type}'")
            
            if enemy.type in ["shooter", "destructeur"]: 
                print(f"DEBUG GAME_SCENE: {enemy.type} reçoit projectiles")
                enemy.update(self.player, self.enemy_projectiles)
            else:
                print(f"DEBUG GAME_SCENE: {enemy.type} reçoit None")
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
                            self.player.add_score(50)  # Gros score pour destructeur
                        else:
                            self.player.add_score(10)  # Score normal
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # Collisions ennemis mêlée → joueur
            if enemy.type != "shooter":
                distance = ((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)**0.5
                if distance < enemy.radius + self.player.size:
                    if self.player.take_damage(enemy.damage):
                        print("Game Over!")
                    
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
                            print("Game Over! (Explosion suicide)")
                    self.enemies.remove(enemy)
                    self.wave_manager.on_enemy_died(enemy)
                    self.player.add_score(15)  # Score bonus pour suicide
                elif distance_to_player < 50 and not enemy.is_exploding:
                    enemy.is_exploding = True
                    enemy.explosion_timer = 15
    
    def next_floor(self):
        """Passe à l'étage suivant (appelé après la transition)"""
        self.current_floor += 1
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        
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
        
        # Dessine le HUD (sans radar)
        self.hud.draw(screen)
        
        # Dessine l'effet de transition
        self.transition.draw(screen)
        
        # Dessine le menu de pause
        if self.game_paused:
            self.current_sub_scene.draw(screen)
            
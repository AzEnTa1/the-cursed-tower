import pygame
import math
import random
from src.entities import *
from src.entities.enemies import *
from src.entities.spawn_effect import SpawnEffect
from src.systems.wave_manager import WaveManager
from src.systems.game_stats import GameStats
from src.ui.hud import HUD
from src.ui.transition_effect import TransitionEffect
from .base_scene import BaseScene
from .sub_scenes import *


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
        self.current_floor = 1

    def on_enter(self, player_data):
        """Initialisation du jeu"""
        self.current_floor = 1  # Réinitialiser l'étage
        self.player = Player(
            self.settings.screen_width//2, 
            self.settings.screen_height//2, 
            self.settings,
            player_data
        )
        self.weapon = Weapon(self.settings, player_data) 
        self.wave_manager = WaveManager(self.settings)
        self.wave_manager.reset_to_floor(self.current_floor)
        self.game_stats = GameStats(self.game, self.settings)
        
        # Sous-scènes
        self.stat_sub_scene = StatSubScene(self.game, self, self.settings)
        self.perks_sub_scene = PerksSubScene(self.game, self, self.settings, self.player, self.weapon)
        self.pause_sub_scene = PauseSubScene(self.game, self, self.settings)
        self.tuto_sub_scene = TutoSubScene(self.game, self, self.settings)
        self.game_paused = False
        self.current_sub_scene = None

        # HUD
        self.hud = HUD(self.player, self.wave_manager, self.weapon, self.settings)
        self.transition = TransitionEffect(self.settings)

        # Image de fond
        self.fond = pygame.image.load(r"assets/images/background/game_scene.png")
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
                    self.current_sub_scene.on_enter(self.game_stats.update(self.player, self.weapon))
                else:
                    self.current_sub_scene = None

            elif event.key == pygame.K_t:
                # Affiche le tuto
                if not self.game_paused:
                    self.game_paused = True
                    self.current_sub_scene = self.tuto_sub_scene
                    self.current_sub_scene.on_enter()
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
        self.hud.update(dt)

        
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
        if (self.wave_manager.is_between_waves() and 
            self.wave_manager.update(self.current_time) and 
            len(self.enemies) == 0 and 
            len(self.spawn_effects) == 0):
            
            spawn_positions = self.wave_manager.start_next_wave()
            if spawn_positions:
                for spawn_data in spawn_positions:
                    
                    # Vérifier si c'est un boss (tuple de 4 éléments)
                    if isinstance(spawn_data, tuple) and len(spawn_data) == 4 and spawn_data[2] == "boss":
                        # Boss : (x, y, "boss", seed)
                        x, y, enemy_type, boss_seed = spawn_data
                        effect = SpawnEffect(x, y, self.settings, "boss")
                        effect.boss_data = boss_seed
                        self.spawn_effects.append(effect)
                    elif isinstance(spawn_data, tuple) and len(spawn_data) == 3:
                        # Ennemi normal : (x, y, enemy_type)
                        x, y, enemy_type = spawn_data
                        effect = SpawnEffect(x, y, self.settings, enemy_type)
                        self.spawn_effects.append(effect)
                    else:
                        # Format inattendu (j'ai eu un problème ici une fois)
                        print(f"Format de spawn : {spawn_data}")

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
            
            # Gestion des projectiles qui se divisent
            if hasattr(projectile, 'will_split') and projectile.will_split and projectile.split_timer <= 0:
                split_projectiles = projectile.create_split_projectiles()
                self.projectiles.extend(split_projectiles)
                projectile.will_split = False
            
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # Mise à jour des projectiles ennemis
        for projectile in self.enemy_projectiles[:]:
            projectile.update()
            
            # Gestion des projectiles qui se divisent
            if hasattr(projectile, 'will_split') and projectile.will_split and projectile.split_timer <= 0:
                split_projectiles = projectile.create_split_projectiles()
                self.enemy_projectiles.extend(split_projectiles)
                projectile.will_split = False
            
            if not projectile.is_alive():
                self.enemy_projectiles.remove(projectile)
            else:
                # Collisions projectiles ennemis → joueur
                distance = ((projectile.x - self.player.x)**2 + (projectile.y - self.player.y)**2)**0.5
                if distance < self.player.size + projectile.radius:
                    if self.player.take_damage(projectile.damage):
                        self._handle_player_death()
                    if projectile in self.enemy_projectiles:
                        self.enemy_projectiles.remove(projectile)
    
    def _update_enemies(self, dt):
        """Met à jour tous les ennemis"""
        new_bosses_from_division = []
        
        for enemy in self.enemies[:]:
            # Passe les zones de feu et pending_zones au pyromane
            if enemy.type == "pyromane":
                enemy.update(self.player, self.fire_zones, self.pending_fire_zones)
            # Passe les projectiles ennemis au shooter et destructeur
            elif enemy.type in ["shooter", "destructeur"]:
                enemy.update(self.player, self.enemy_projectiles)
            elif enemy.type == "boss":
                # Le boss retourne maintenant (ennemis_créés, bosses_de_division)
                enemies_created, division_bosses = enemy.update(self.player, self.enemy_projectiles)
                if division_bosses:
                    new_bosses_from_division.extend(division_bosses)
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
        
        # Ajouter les nouveaux bosses de division
        for boss in new_bosses_from_division:
            if boss not in self.enemies:
                self.enemies.append(boss)
                self.wave_manager.current_wave_enemies.append(boss)
    
    def _check_player_projectile_collisions(self, enemy):
        """Vérifie les collisions entre projectiles joueur et ennemi"""
        for projectile in self.projectiles[:]:
            distance = ((enemy.x - projectile.x)**2 + (enemy.y - projectile.y)**2)**0.5
            if distance < enemy.radius + projectile.radius:
                if enemy.take_damage(projectile.damage):
                    self.enemies.remove(enemy)
                    self.wave_manager.on_enemy_died(enemy)
                    
                    # Score et pièces selon le type d'ennemi
                    if enemy.type == "boss":
                        score_amount = 200
                        coins_amount = 50
                    elif enemy.type == "destructeur":
                        score_amount = 50
                        coins_amount = 15
                    elif enemy.type == "suicide":
                        score_amount = 20
                        coins_amount = 5
                    else:
                        score_amount = 10
                        coins_amount = 2
                    
                    self.player.add_score(score_amount)
                    self.player.add_coins(coins_amount) 
                    self.settings.sounds["mort_enemy"].play()  
                    
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
    
    def _check_boss_projectile_collisions(self, enemy, projectile):
        """Vérifie les collisions entre un projectile et le boss arborescent"""
        # Vérifier collision avec le nœud racine
        distance_to_root = ((enemy.root.x - projectile.x)**2 + 
                        (enemy.root.y - projectile.y)**2)**0.5
        
        if distance_to_root < enemy.root.radius + projectile.radius:
            if enemy.root.take_damage(projectile.damage):
                # Si le cœur est détruit
                self.enemies.remove(enemy)
                self.wave_manager.on_enemy_died(enemy)
                self.player.add_score(200)  # Gros score pour le boss
                self._check_for_level_up()
            return True
        
        # Vérifier récursivement les collisions avec les nœuds enfants
        return self._check_boss_node_collisions(enemy.root, projectile)

    def _check_boss_node_collisions(self, node, projectile, nodes_to_remove=None):
        """Vérifie récursivement les collisions avec les nœuds de l'arbre"""
        if nodes_to_remove is None:
            nodes_to_remove = []
        
        if not node.active:
            return False
        
        # Vérifier collision avec ce nœud
        distance = ((node.x - projectile.x)**2 + (node.y - projectile.y)**2)**0.5
        if distance < node.radius + projectile.radius:
            if node.take_damage(projectile.damage):
                nodes_to_remove.append(node)
                self.player.add_score(10)  # Petit score pour un nœud
            return True
        
        # Vérifier récursivement avec les enfants
        for child in node.children:
            if self._check_boss_node_collisions(child, projectile, nodes_to_remove):
                return True
        
        return False
    
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
        # vérifie si le joueur est mort
        if self.player.health <= 0:
            self._handle_player_death()
    
    def _check_floor_completion(self):
        """Vérifie si l'étage est terminé"""
        if (self.wave_manager.are_all_waves_cleared() and 
            len(self.enemies) == 0 and 
            len(self.enemy_projectiles) == 0 and
            len(self.spawn_effects) == 0):

            self.transition.start(self.next_floor)
    
    def _handle_player_death(self):
        """Gère la mort du joueur"""
        self.game_stats.update(self.player, self.weapon)
        self.game.game_stats = self.game_stats.stats
        
        self.current_floor = 1
        
        self.game.change_scene(self.settings.SCENE_GAME_OVER)
        pygame.mixer.music.stop()
        self.settings.sounds["game_over"].play()

    def _handle_perks_menu_selection(self, perk_index):
        """Gère la sélection d'un perk dans le menu"""
        if perk_index < len(self.perks_sub_scene.perks_list):
            perk = self.perks_sub_scene.perks_list[perk_index]
            self.perks_sub_scene.perks_manager.choose_perk(perk)
        
        # Quitter le menu
        self.game_paused = False
        self.current_sub_scene = None
    
    def _check_for_level_up(self):
        """Vérifie si le joueur peut monter de niveau"""
        if self.player.xp >= 200:
            self.player.xp %= 200
            self.game_paused = True
            self.current_sub_scene = self.perks_sub_scene
            # Réinitialiser le menu perks
            self.perks_sub_scene.on_enter()
    
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
            # Récupérer la seed du boss depuis les données de vague
            if hasattr(effect, 'boss_data'):
                boss_seed = effect.boss_data
            else:
                boss_seed = self.global_seed
                
            return Boss(
                effect.x, effect.y,
                self.settings,
                self.current_floor,
                boss_seed
            )
        else:
            return Basic(effect.x, effect.y, self.settings)
        
    def next_floor(self):
        """
        Passe à l'étage suivant
        Appelé après la fin de l'effet de transition
        """
        self.current_floor += 1
        
        # Nettoyer toutes les listes
        self.enemies.clear()
        self.projectiles.clear()
        self.enemy_projectiles.clear()
        self.spawn_effects.clear()
        self.fire_zones.clear()
        self.pending_fire_zones.clear()
        
        # Réinitialiser le wave manager pour le nouvel étage
        self.wave_manager.reset_to_floor(self.current_floor)
        
        # Replace le joueur au centre
        self.player.x = self.settings.screen_width // 2
        self.player.y = self.settings.screen_height // 2
        
        # Petit heal entre les étages (20 PV)
        self.player.health = min(self.player.health + 20, self.player.max_health)
            
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
        """
        Appelé lorsque la fenêtre change de taille
        Recalcule les positions des éléments
        """
        self.fond = pygame.transform.scale(self.fond, (self.settings.screen_width, self.settings.screen_height))
        
        if self.game_paused:
            self.current_sub_scene.resize()
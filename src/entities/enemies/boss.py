# src/entities/enemies/boss.py
import pygame
import math
import random
from .enemy import Enemy
from ..projectiles import Projectile
from .basic import Basic
from .charger import Charger
from .shooter import Shooter

class RecursivePatternGenerator:
    """Générateur de patterns récursifs pour le boss"""
    
    @staticmethod
    def generate_circle_recursive(x, y, depth, max_depth, angle_offset=0, spawn_enemies=False):
        """
        Génère un motif circulaire récursif
        
        Args:
            x, y: Position centrale
            depth: Profondeur actuelle
            max_depth: Profondeur maximale
            angle_offset: Rotation
            spawn_enemies: Si True, génère des ennemis au lieu de projectiles
        """
        if depth <= 0:
            return []
        
        result = []
        
        # Nombre d'éléments augmente avec la profondeur
        elements = 4 + depth * 2
        
        for i in range(elements):
            # Angle pour cet élément
            angle = (2 * math.pi * i / elements) + angle_offset
            
            # Distance du centre
            radius = 30 * (max_depth - depth + 1)
            
            # Position
            elem_x = x + math.cos(angle) * radius
            elem_y = y + math.sin(angle) * radius
            
            if spawn_enemies and depth == 1:  # Dernier niveau: ennemis
                # Choisir un type d'ennemi
                enemy_type = random.choices(
                    ['basic', 'charger', 'shooter'],
                    weights=[0.6, 0.25, 0.15],
                    k=1
                )[0]
                result.append(('enemy', elem_x, elem_y, enemy_type))
            else:  # Projectiles
                # Direction radiale
                speed = 2.5 + (max_depth - depth) * 0.5
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                damage = 8 + depth * 3
                result.append(('projectile', elem_x, elem_y, dx, dy, damage))
            
            # Appel récursif pour sous-motifs
            if depth > 1:
                sub_result = RecursivePatternGenerator.generate_circle_recursive(
                    elem_x, elem_y, depth - 1, max_depth,
                    angle_offset + 0.5,
                    spawn_enemies
                )
                result.extend(sub_result)
        
        return result
    
    @staticmethod
    def generate_spiral_arms(x, y, arms=3, projectiles_per_arm=6):
        """Génère un motif en spirale avec bras"""
        projectiles = []
        current_time = pygame.time.get_ticks() * 0.001
        
        for arm in range(arms):
            base_angle = (2 * math.pi * arm / arms) + current_time * 0.3
            
            for i in range(projectiles_per_arm):
                # Progression en spirale
                progress = i / projectiles_per_arm
                angle = base_angle + progress * math.pi * 2
                radius = 20 + i * 25
                
                px = x + math.cos(angle) * radius
                py = y + math.sin(angle) * radius
                
                # Direction tangentielle
                dx = math.cos(angle + math.pi/2) * 3.5
                dy = math.sin(angle + math.pi/2) * 3.5
                
                projectiles.append(('projectile', px, py, dx, dy, 10))
        
        return projectiles


class BossPhase:
    """Représente une phase du boss"""
    
    def __init__(self, number, max_phases):
        self.number = number
        self.max_phases = max_phases
        self.health_threshold = 1.0 - (number / max_phases)
        self.active = False
        
        # Caractéristiques de la phase
        self.attack_cooldown = max(40, 90 - (number * 15))
        self.projectile_size = 6 + (number * 1)  # Taille augmentée
        self.damage_multiplier = 1.0 + ((number - 1) * 0.15)
        
        # Patterns disponibles
        self.patterns = ['circle', 'spiral', 'burst']
        if number >= 2:
            self.patterns.append('circle_enemy')
        if number >= 3:
            self.patterns.append('mixed')
        
        # Couleur de la phase
        self.color = [
            (100, 200, 255),
            (200, 100, 255),
            (255, 100, 100),
            (255, 200, 50)
        ][min(number - 1, 3)]
    
    def get_random_pattern(self):
        """Retourne un pattern aléatoire"""
        return random.choice(self.patterns)


class BossDivisionSystem:
    """Gère la division du boss en deux"""
    
    def __init__(self, settings):
        self.settings = settings
        self.can_divide = True
        self.division_threshold = 0.5
        self.has_divided = False
        self.division_cooldown = 0
        
    def update(self):
        """Met à jour le cooldown de division"""
        if self.division_cooldown > 0:
            self.division_cooldown -= 1
    
    def check_division(self, boss, current_health, max_health):
        """Vérifie si le boss doit se diviser"""
        if not self.can_divide or self.has_divided or self.division_cooldown > 0:
            return None
        
        health_ratio = current_health / max_health
        
        if health_ratio <= self.division_threshold:
            self.has_divided = True
            self.division_cooldown = 300  # 5 secondes avant de pouvoir rediviser
            return self.create_division_bosses(boss)
        
        return None
    
    def create_division_bosses(self, original_boss):
        """Crée deux nouveaux bosses à partir de l'original"""
        bosses = []
        
        for i in range(2):
            # Position décalée
            angle = math.pi/2 + (i * math.pi)
            distance = original_boss.radius * 1.5
            x = original_boss.x + math.cos(angle) * distance
            y = original_boss.y + math.sin(angle) * distance
            
            # Créer un boss plus petit
            boss = Boss(
                x, y, 
                self.settings,
                floor_number=1,
                global_seed=hash(f"{original_boss.x}_{original_boss.y}_{i}")
            )
            
            # Réduire les stats
            boss.health = original_boss.health * 0.5  # 50% de la vie restante
            boss.max_health = boss.health
            boss.damage = original_boss.damage * 0.7
            boss.speed = original_boss.speed * 1.2  # Plus rapide
            boss.radius = original_boss.radius * 0.7
            
            # Limiter les capacités
            boss.max_phases = min(3, original_boss.max_phases - 1)
            boss.phases = boss._create_phases()
            
            # Marquer comme boss divisé
            boss.is_divided_boss = True
            
            # Pas de division récursive pour les clones
            boss.division_system.can_divide = False
            
            bosses.append(boss)
        
        return bosses


class Boss(Enemy):
    """
    Boss avec système de division et patterns récursifs
    Nom: "Boss" (toujours)
    """
    
    def __init__(self, x, y, settings, floor_number=1, global_seed=None):
        """
        Initialise le boss
        
        Args:
            x, y: Position
            settings: Configuration
            floor_number: Difficulté (1+)
            global_seed: Seed aléatoire
        """
        super().__init__(x, y, settings)
        
        # Configuration de base
        self.type = "boss"
        self.name = "Boss"
        
        # Seed aléatoire
        if global_seed is not None:
            random.seed(global_seed + floor_number)
        
        # Statistiques adaptées
        self._init_stats(floor_number)
        
        # Apparence
        self._init_appearance(floor_number)
        
        # Systèmes
        self.pattern_generator = RecursivePatternGenerator()
        self.division_system = BossDivisionSystem(settings)
        
        # Phases
        self.max_phases = min(4, 1 + (floor_number // 2))
        self.current_phase = 1
        self.phases = self._create_phases()
        self.phases[0].active = True
        
        # Attaques
        self.current_pattern = None
        self.attack_cooldown = 0
        self.attack_sound = "Tire_4"
        
        # Mode Rage (à 1/3 de vie)
        self.rage_mode = False
        self.rage_health_threshold = 0.33
        self.rage_activated = False
        
        # Animation
        self.pulse_timer = 0
        self.rotation_angle = 0
        
        # État
        self.is_divided_boss = False
        
        # Division
        self.division_bosses_to_spawn = []
        
        print(f"[BOSS] Créé - Phase: {self.current_phase}, PV: {self.health}")
    
    def _init_stats(self, floor_number):
        """Initialise les statistiques"""
        boss_level = max(1, floor_number)
        
        # Stats équilibrées
        self.health = 350 + (boss_level * 70)  # Réduit
        self.max_health = self.health
        self.damage = 10 + (boss_level * 1.2)  # Réduit
        self.speed = 1.3 + (boss_level * 0.08)
        self.radius = 30 + min(boss_level, 8)
        
        # Pas trop dur
        self.attack_cooldown_base = max(55, 110 - (boss_level * 5))  # Plus lent
        
    def _init_appearance(self, floor_number):
        """Initialise l'apparence"""
        # Couleur basée sur l'étage
        hue = (floor_number * 25) % 360
        self.color = self._hsv_to_rgb(hue / 360, 0.7, 0.9)
        self.core_color = (255, 255, 220)
        
    def _hsv_to_rgb(self, h, s, v):
        """Convertit HSV en RGB"""
        c = v * s
        x = c * (1 - abs((h * 6) % 2 - 1))
        m = v - c
        
        if h < 1/6:
            r, g, b = c, x, 0
        elif h < 2/6:
            r, g, b = x, c, 0
        elif h < 3/6:
            r, g, b = 0, c, x
        elif h < 4/6:
            r, g, b = 0, x, c
        elif h < 5/6:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def _create_phases(self):
        """Crée les phases du boss"""
        phases = []
        for i in range(self.max_phases):
            phases.append(BossPhase(i + 1, self.max_phases))
        return phases
    
    def update(self, player, enemy_projectiles=None):
        """
        Met à jour le boss
        
        Returns:
            Tuple (ennemis_créés, bosses_créés_par_division)
        """
        # Mise à jour de la rage
        self._update_rage_mode()
        
        # Mise à jour de la division
        self.division_system.update()
        
        # Mise à jour des animations
        self.pulse_timer += 0.05
        self.rotation_angle += 0.01
        
        # Vérifier les phases
        self._check_phase_transition()
        
        # Déplacement simple
        self._simple_movement(player)
        
        # Garder dans l'écran
        self._constrain_to_screen()
        
        # Gestion des attaques
        enemies_created = []
        if enemy_projectiles is not None:
            enemies_created = self._update_attacks(enemy_projectiles)
        
        # Vérifier la division
        division_bosses = self.division_system.check_division(
            self, self.health, self.max_health
        )
        
        # Retourner les ennemis créés ET les bosses de division
        return enemies_created, division_bosses
    
    def _update_rage_mode(self):
        """Active le mode rage à 1/3 de vie"""
        if self.rage_activated:
            return
            
        health_ratio = self.health / self.max_health
        if health_ratio <= self.rage_health_threshold:
            self.rage_mode = True
            self.rage_activated = True
            print("[BOSS] Rage activée!")
            
            # Boost en rage
            self.speed *= 1.2
            self.attack_cooldown_base = max(35, self.attack_cooldown_base - 15)
    
    def _check_phase_transition(self):
        """Vérifie si on change de phase"""
        health_ratio = self.health / self.max_health
        
        for i, phase in enumerate(self.phases):
            if health_ratio <= phase.health_threshold:
                new_phase = i + 1
                if new_phase > self.current_phase:
                    self.current_phase = new_phase
                    self._activate_phase(new_phase)
                    break
    
    def _activate_phase(self, phase_number):
        """Active une nouvelle phase"""
        print(f"[BOSS] Phase {phase_number} activée")
        
        # Désactiver toutes les phases
        for phase in self.phases:
            phase.active = False
        
        # Activer la nouvelle phase
        self.phases[phase_number - 1].active = True
        
        # Effet sonore
        self.settings.sounds["spawn"].play()
    
    def _simple_movement(self, player):
        """Déplacement simple vers le joueur"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Distance cible
        target_distance = 150
        
        if distance > target_distance * 1.2:
            # Trop loin, s'approcher
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        elif distance < target_distance * 0.8:
            # Trop près, s'éloigner un peu
            self.x -= (dx / distance) * self.speed * 0.7
            self.y -= (dy / distance) * self.speed * 0.7
    
    def _constrain_to_screen(self):
        """Maintient dans l'écran"""
        margin = self.radius + 20
        self.x = max(margin, min(self.x, self.settings.screen_width - margin))
        self.y = max(margin, min(self.y, self.settings.screen_height - margin))
    
    def _update_attacks(self, enemy_projectiles):
        """Gère les attaques"""
        enemies_created = []
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return enemies_created
        
        # Choisir un pattern
        phase = self.phases[self.current_phase - 1]
        if self.current_pattern is None:
            self.current_pattern = phase.get_random_pattern()
        
        # Exécuter l'attaque
        self._execute_pattern(enemy_projectiles, enemies_created)
        
        # Réinitialiser le cooldown
        self.attack_cooldown = phase.attack_cooldown
        if self.rage_mode:
            self.attack_cooldown = max(25, phase.attack_cooldown // 2)
        
        self.current_pattern = None
        return enemies_created
    
    def _execute_pattern(self, enemy_projectiles, enemies_created):
        """Exécute le pattern actuel"""
        self.settings.sounds[self.attack_sound].play()
        
        phase = self.phases[self.current_phase - 1]
        
        if self.current_pattern == 'circle':
            self._execute_circle_pattern(enemy_projectiles, phase)
        elif self.current_pattern == 'spiral':
            self._execute_spiral_pattern(enemy_projectiles, phase)
        elif self.current_pattern == 'burst':
            self._execute_burst_pattern(enemy_projectiles, phase)
        elif self.current_pattern == 'circle_enemy':
            enemies = self._execute_circle_pattern(enemy_projectiles, phase, spawn_enemies=True)
            enemies_created.extend(enemies)
        elif self.current_pattern == 'mixed':
            self._execute_mixed_pattern(enemy_projectiles, phase)
    
    def _execute_circle_pattern(self, enemy_projectiles, phase, spawn_enemies=False):
        """Pattern circulaire récursif"""
        enemies_created = []
        depth = min(3, self.current_phase)
        
        pattern = self.pattern_generator.generate_circle_recursive(
            self.x, self.y,
            depth=depth,
            max_depth=depth,
            angle_offset=self.rotation_angle,
            spawn_enemies=spawn_enemies
        )
        
        for item in pattern:
            if item[0] == 'projectile':
                _, x, y, dx, dy, damage = item
                damage *= phase.damage_multiplier
                
                # Taille augmentée
                radius = phase.projectile_size
                if self.rage_mode:
                    radius = int(radius * 1.3)
                
                enemy_projectiles.append(Projectile(
                    x, y, dx, dy, damage,
                    settings=self.settings,
                    color=phase.color,
                    radius=radius
                ))
            elif item[0] == 'enemy':
                _, x, y, enemy_type = item
                enemy = self._create_enemy(x, y, enemy_type)
                if enemy:
                    enemies_created.append(enemy)
        
        return enemies_created
    
    def _execute_spiral_pattern(self, enemy_projectiles, phase):
        """Pattern en spirale"""
        arms = 2 + self.current_phase
        if self.rage_mode:
            arms += 1
        
        pattern = self.pattern_generator.generate_spiral_arms(
            self.x, self.y,
            arms=arms,
            projectiles_per_arm=6
        )
        
        for item in pattern:
            if item[0] == 'projectile':
                _, x, y, dx, dy, damage = item
                damage *= phase.damage_multiplier
                
                radius = phase.projectile_size
                enemy_projectiles.append(Projectile(
                    x, y, dx, dy, damage,
                    settings=self.settings,
                    color=(255, 150, 100),
                    radius=radius
                ))
    
    def _execute_burst_pattern(self, enemy_projectiles, phase):
        """Explosion de projectiles"""
        projectiles_count = 8 + (self.current_phase * 3)
        
        for i in range(projectiles_count):
            angle = (2 * math.pi * i / projectiles_count) + self.rotation_angle
            speed = 2.5 + random.random() * 1.5
            
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            damage = 8 * phase.damage_multiplier
            radius = phase.projectile_size
            
            enemy_projectiles.append(Projectile(
                self.x, self.y, dx, dy, damage,
                settings=self.settings,
                color=(255, 200, 50),
                radius=radius
            ))
    
    def _execute_mixed_pattern(self, enemy_projectiles, phase):
        """Mélange de patterns"""
        self._execute_circle_pattern(enemy_projectiles, phase)
        self._execute_spiral_pattern(enemy_projectiles, phase)
    
    def _create_enemy(self, x, y, enemy_type):
        """Crée un ennemi à la position donnée"""
        # Garder dans l'écran
        margin = 50
        x = max(margin, min(x, self.settings.screen_width - margin))
        y = max(margin, min(y, self.settings.screen_height - margin))
        
        if enemy_type == 'basic':
            enemy = Basic(x, y, self.settings)
        elif enemy_type == 'charger':
            enemy = Charger(x, y, self.settings)
        elif enemy_type == 'shooter':
            enemy = Shooter(x, y, self.settings)
        else:
            return None
        
        # Rendre plus faible
        enemy.health = int(enemy.health * 0.6)
        enemy.max_health = enemy.health
        enemy.damage = int(enemy.damage * 0.7)
        enemy.is_boss_spawn = True
        
        return enemy
    
    def take_damage(self, amount):
        """
        Inflige des dégâts au boss
        
        Returns:
            bool: True si mort
        """
        # Réduction selon la phase
        phase = self.current_phase
        damage_reduction = 1.0 - ((phase - 1) * 0.1)
        actual_damage = amount * damage_reduction
        
        # Appliquer
        self.health -= actual_damage
        
        # Effet visuel
        self.pulse_timer += 0.3
        
        # Mort
        if self.health <= 0:
            return True
        
        return False
    
    def draw(self, screen):
        """Dessine le boss"""
        current_time = pygame.time.get_ticks() * 0.001
        
        # Pulsation
        pulse = math.sin(self.pulse_timer) * 4
        if self.rage_mode:
            pulse += math.sin(current_time * 8) * 3
        
        main_radius = self.radius + pulse
        
        # Aura de rage
        if self.rage_mode:
            rage_radius = main_radius + 10 + math.sin(current_time * 6) * 3
            rage_alpha = 60 + int(40 * math.sin(current_time * 4))
            
            rage_surface = pygame.Surface((int(rage_radius*2), int(rage_radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(
                rage_surface,
                (255, 50, 50, rage_alpha),
                (int(rage_radius), int(rage_radius)),
                int(rage_radius)
            )
            screen.blit(rage_surface, (int(self.x - rage_radius), int(self.y - rage_radius)))
        
        # Corps principal
        for i in range(3, 0, -1):
            radius = main_radius * (i / 3)
            alpha = 80 + (i * 40)
            
            # Couleur selon la phase
            phase_color = self.phases[self.current_phase - 1].color
            if i == 3:  # Extérieur
                color = phase_color
            else:
                # Dégradé vers le centre
                blend = i / 3
                color = (
                    int(phase_color[0] * blend + self.core_color[0] * (1 - blend)),
                    int(phase_color[1] * blend + self.core_color[1] * (1 - blend)),
                    int(phase_color[2] * blend + self.core_color[2] * (1 - blend))
                )
            
            layer_surface = pygame.Surface((int(radius*2), int(radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(
                layer_surface, (*color, alpha),
                (int(radius), int(radius)), int(radius)
            )
            screen.blit(layer_surface, (int(self.x - radius), int(self.y - radius)))
        
        # Cœur
        core_radius = main_radius * 0.3
        core_pulse = math.sin(current_time * 4) * 2
        if self.rage_mode:
            core_pulse += math.sin(current_time * 10) * 1.5
        
        pygame.draw.circle(
            screen, self.core_color,
            (int(self.x), int(self.y)),
            int(core_radius + core_pulse)
        )
        
        # Indicateurs de phase
        for i in range(self.current_phase):
            angle = (2 * math.pi * i / self.current_phase) + self.rotation_angle
            indicator_radius = main_radius * 0.7
            ix = self.x + math.cos(angle) * indicator_radius
            iy = self.y + math.sin(angle) * indicator_radius
            
            size = 4 + math.sin(current_time * 3 + i) * 2
            pygame.draw.circle(
                screen, (255, 255, 200),
                (int(ix), int(iy)), int(size)
            )
        
        # Texte
        if hasattr(self.settings, 'font') and self.settings.font:
            # Nom
            name_text = self.settings.font["h3"].render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, self.y - main_radius - 25))
            screen.blit(name_text, name_rect)
            
            # Phase
            phase_text = self.settings.font["h4"].render(
                f"Phase {self.current_phase}", 
                True, self.phases[self.current_phase - 1].color
            )
            phase_rect = phase_text.get_rect(center=(self.x, self.y - main_radius - 45))
            screen.blit(phase_text, phase_rect)
            
            # Rage
            if self.rage_mode:
                rage_text = self.settings.font["h4"].render("RAGE!", True, (255, 50, 50))
                rage_rect = rage_text.get_rect(center=(self.x, self.y + main_radius + 20))
                screen.blit(rage_text, rage_rect)
            
            # Division
            if not self.is_divided_boss and self.division_system.can_divide and not self.division_system.has_divided:
                div_text = self.settings.font["h4"].render("DIVISION DISPONIBLE", True, (255, 255, 0))
                div_rect = div_text.get_rect(center=(self.x, self.y + main_radius + 40))
                screen.blit(div_text, div_rect)
        
        # Barre de vie
        self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen, width=250, height=12):
        """Barre de vie"""
        bar_x = self.x - width // 2
        bar_y = self.y - self.radius - 65
        
        # Fond
        pygame.draw.rect(
            screen, (30, 30, 30),
            (bar_x, bar_y, width, height),
            border_radius=height//2
        )
        
        # Vie
        health_ratio = max(0, self.health / self.max_health)
        health_width = int(width * health_ratio)
        
        if health_width > 0:
            phase_color = self.phases[self.current_phase - 1].color
            
            # Gradient simple
            health_surface = pygame.Surface((health_width, height), pygame.SRCALPHA)
            for i in range(health_width):
                pos_ratio = i / width
                r = int(phase_color[0] * (0.7 + 0.3 * pos_ratio))
                g = int(phase_color[1] * (0.7 + 0.3 * pos_ratio))
                b = int(phase_color[2] * (0.7 + 0.3 * pos_ratio))
                
                pygame.draw.line(
                    health_surface, (r, g, b, 200),
                    (i, 0), (i, height)
                )
            
            screen.blit(health_surface, (bar_x, bar_y))
        
        # Indicateur de division (50%)
        if self.division_system.can_divide and not self.division_system.has_divided:
            division_x = bar_x + int(width * 0.5)
            pygame.draw.line(
                screen, (255, 255, 0, 150),
                (division_x, bar_y - 3),
                (division_x, bar_y + height + 3), 2
            )
        
        # Indicateur de rage (33%)
        if not self.rage_activated:
            rage_x = bar_x + int(width * self.rage_health_threshold)
            pygame.draw.line(
                screen, (255, 50, 50, 150),
                (rage_x, bar_y - 3),
                (rage_x, bar_y + height + 3), 2
            )
        
        # Bordure
        border_color = (200, 200, 200)
        if self.rage_mode:
            border_color = (255, 50, 50)
        
        pygame.draw.rect(
            screen, border_color,
            (bar_x, bar_y, width, height),
            2, border_radius=height//2
        )
        
        # Texte
        if hasattr(self.settings, 'font') and self.settings.font:
            health_text = self.settings.font["h4"].render(
                f"{int(self.health)}/{self.max_health}", 
                True, (255, 255, 255)
            )
            health_rect = health_text.get_rect(center=(self.x, bar_y - 20))
            screen.blit(health_text, health_rect)
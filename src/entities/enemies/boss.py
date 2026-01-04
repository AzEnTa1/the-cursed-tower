# src/entities/enemies/boss.py
import pygame
import math
import random
from .enemy import Enemy
from ..projectiles import Projectile
from .basic import Basic
from .charger import Charger
from .shooter import Shooter

class RecursivePatternCore:
    """
    Noyau récursif de génération de patterns
    Système central de récursivité pour les attaques du boss
    """
    
    @staticmethod
    def generate_recursive_pattern(center_x, center_y, depth, max_depth, 
                                  pattern_type="fractal", params=None, current_time=0):
        """
        Génère un motif récursif avec de nombreuses variantes
        
        Args:
            pattern_type: Type de motif (fractal, flower, web, crystal, vortex, etc.)
        """
        if depth <= 0:
            return []
        
        if params is None:
            params = {
                'angle_offset': 0,
                'scale': 1.0,
                'intensity': 1.0,
                'phase': 1
            }
        
        result = []
        
        # Base récursive pour tous les patterns
        if pattern_type == "fractal":
            result = RecursivePatternCore._generate_fractal(
                center_x, center_y, depth, max_depth, params, current_time
            )
        elif pattern_type == "flower":
            result = RecursivePatternCore._generate_flower(
                center_x, center_y, depth, max_depth, params, current_time
            )
        elif pattern_type == "web":
            result = RecursivePatternCore._generate_web(
                center_x, center_y, depth, max_depth, params, current_time
            )
        elif pattern_type == "crystal":
            result = RecursivePatternCore._generate_crystal(
                center_x, center_y, depth, max_depth, params, current_time
            )
        elif pattern_type == "vortex":
            result = RecursivePatternCore._generate_vortex(
                center_x, center_y, depth, max_depth, params, current_time
            )
        elif pattern_type == "spiral":
            result = RecursivePatternCore._generate_spiral(
                center_x, center_y, depth, max_depth, params, current_time
            )
        else:
            result = RecursivePatternCore._generate_simple(
                center_x, center_y, depth, max_depth, params, current_time
            )
        
        return result
    
    @staticmethod
    def _generate_fractal(center_x, center_y, depth, max_depth, params, current_time):
        """Fractale classique - la récursivité principale"""
        result = []
        branches = 3 + min(depth, 3)
        
        for i in range(branches):
            angle = (2 * math.pi * i / branches) + params['angle_offset']
            
            distance = 40 * (max_depth - depth + 1) * params['scale']
            pulse = math.sin(current_time * 2 + i) * 4
            
            x = center_x + math.cos(angle) * (distance + pulse)
            y = center_y + math.sin(angle) * (distance + pulse)
            
            # Taille augmentée des projectiles
            speed = 2.5 + (max_depth - depth) * 0.4
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            result.append(('projectile', x, y, dx, dy, 10 + depth * 3, angle))
            
            # Appel récursif (cœur de la récursivité)
            if depth > 1:
                sub_params = params.copy()
                sub_params['angle_offset'] += 0.3
                sub_result = RecursivePatternCore._generate_fractal(
                    x, y, depth - 1, max_depth, sub_params, current_time
                )
                result.extend(sub_result)
        
        return result
    
    @staticmethod
    def _generate_flower(center_x, center_y, depth, max_depth, params, current_time):
        """Motif floral avec pétales"""
        result = []
        petals = 6
        
        for i in range(petals):
            angle = (2 * math.pi * i / petals) + params['angle_offset']
            petal_shape = math.sin(current_time + i) * 0.4
            
            distance = 50 + 25 * math.sin(i * 2) * params['scale']
            x = center_x + math.cos(angle + petal_shape) * distance
            y = center_y + math.sin(angle + petal_shape) * distance
            
            speed = 2.0 + depth * 0.3
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            result.append(('projectile', x, y, dx, dy, 8 + depth * 2, angle))
        
        return result
    
    @staticmethod
    def _generate_web(center_x, center_y, depth, max_depth, params, current_time):
        """Toile d'araignée avec connections"""
        result = []
        rings = 3
        spokes = 8
        
        for ring in range(1, rings + 1):
            radius = 40 * ring * params['scale']
            
            for spoke in range(spokes):
                angle = (2 * math.pi * spoke / spokes) + params['angle_offset']
                
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                
                speed = 1.5 + ring * 0.3
                dx = math.cos(angle + math.pi/2) * speed
                dy = math.sin(angle + math.pi/2) * speed
                
                result.append(('projectile', x, y, dx, dy, 7 + ring * 2, angle))
        
        return result
    
    @staticmethod
    def _generate_crystal(center_x, center_y, depth, max_depth, params, current_time):
        """Motif cristallin géométrique"""
        result = []
        sides = 6
        
        for i in range(sides):
            angle = (2 * math.pi * i / sides) + params['angle_offset']
            
            distance = 60 * params['scale']
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            
            speed = 2.2
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            result.append(('projectile', x, y, dx, dy, 9 + depth * 2, angle))
        
        return result
    
    @staticmethod
    def _generate_vortex(center_x, center_y, depth, max_depth, params, current_time):
        """Vortex spirale"""
        result = []
        arms = 2
        points_per_arm = 6 + depth
        
        for arm in range(arms):
            base_angle = (math.pi * arm) + params['angle_offset']
            
            for point in range(points_per_arm):
                spiral_factor = point * 0.5
                angle = base_angle + spiral_factor
                radius = 20 + point * 15
                
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                
                speed = 2.0
                dx = math.cos(angle + math.pi/2) * speed * 0.7 + math.cos(angle) * speed * 0.3
                dy = math.sin(angle + math.pi/2) * speed * 0.7 + math.sin(angle) * speed * 0.3
                
                result.append(('projectile', x, y, dx, dy, 7 + point, angle))
        
        return result
    
    @staticmethod
    def _generate_spiral(center_x, center_y, depth, max_depth, params, current_time):
        """Spirale simple"""
        result = []
        turns = 2
        total_points = 10 + depth * 2
        
        for i in range(total_points):
            progress = i / total_points
            angle = params['angle_offset'] + turns * 2 * math.pi * progress
            radius = 25 + 50 * progress
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            speed = 2.5
            dx = math.cos(angle + math.pi/2) * speed
            dy = math.sin(angle + math.pi/2) * speed
            
            result.append(('projectile', x, y, dx, dy, 6 + int(progress * 5), angle))
        
        return result
    
    @staticmethod
    def _generate_simple(center_x, center_y, depth, max_depth, params, current_time):
        """Pattern très simple"""
        result = []
        points = 8
        radius = 40 + depth * 10
        
        for i in range(points):
            angle = (2 * math.pi * i / points) + params['angle_offset']
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            speed = 1.8
            dx = math.cos(angle + math.pi/2) * speed
            dy = math.sin(angle + math.pi/2) * speed
            
            result.append(('projectile', x, y, dx, dy, 8, angle))
        
        return result


class BossPhase:
    """Phase du boss avec rage à 1/3 de vie"""
    
    def __init__(self, number, max_phases):
        self.number = number
        self.max_phases = max_phases
        self.health_threshold = 1.0 - (number / max_phases)
        
        # Caractéristiques
        self.attack_speed = 1.0 + (number * 0.2)
        self.damage_multiplier = 1.0 + (number * 0.25)
        self.movement_speed = 1.0 + (number * 0.15)
        
        # Patterns disponibles
        self.base_patterns = ["fractal", "simple"]
        
        if number >= 2:
            self.base_patterns.extend(["flower", "web"])
        if number >= 3:
            self.base_patterns.extend(["crystal", "vortex"])
        if number >= 4:
            self.base_patterns.extend(["spiral"])
        
        # Rage mode (activé séparément)
        self.rage_activated = False
        
        # Couleur de la phase
        self.color = self._get_phase_color(number)
    
    def _get_phase_color(self, phase):
        """Couleurs des phases"""
        colors = [
            (100, 180, 255),    # Phase 1: Bleu
            (180, 120, 255),    # Phase 2: Violet
            (255, 120, 150),    # Phase 3: Rose
            (255, 200, 100),    # Phase 4: Or
        ]
        return colors[min(phase - 1, len(colors) - 1)]
    
    def activate_rage(self):
        """Active le mode rage pour cette phase"""
        self.rage_activated = True
        self.attack_speed *= 1.5
        self.damage_multiplier *= 1.3
        self.movement_speed *= 1.2
        self.color = (255, 80, 80)  # Rouge pour la rage
    
    def get_random_pattern(self):
        """Retourne un pattern aléatoire"""
        return random.choice(self.base_patterns)


class MinionSpawnSystem:
    """Système d'invocation de minions pour le boss"""
    
    def __init__(self, settings):
        self.settings = settings
        self.spawn_cooldown = 0
        self.spawn_rate = 180  # 3 secondes
        self.max_minions = 6
    
    def update(self, boss, enemies_list):
        """Met à jour le spawn des minions"""
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= 1
            return []
        
        # Compter les minions actuels
        current_minions = sum(1 for e in enemies_list if hasattr(e, 'is_boss_minion') and e.is_boss_minion)
        
        if current_minions >= self.max_minions:
            return []
        
        # Spawn de minions
        if random.random() < 0.02:  # 2% de chance par frame
            return self.spawn_minions(boss, 2)
        
        return []
    
    def spawn_minions(self, boss, count):
        """Fait apparaître des minions"""
        minions = []
        
        for i in range(count):
            # Position autour du boss
            angle = random.random() * 2 * math.pi
            distance = 120 + random.random() * 60
            x = boss.x + math.cos(angle) * distance
            y = boss.y + math.sin(angle) * distance
            
            # Type de minion
            minion_type = random.choices(
                ['basic', 'charger', 'shooter'],
                weights=[0.4, 0.35, 0.25],
                k=1
            )[0]
            
            # Créer le minion
            if minion_type == 'basic':
                minion = Basic(x, y, self.settings)
            elif minion_type == 'charger':
                minion = Charger(x, y, self.settings)
            else:  # shooter
                minion = Shooter(x, y, self.settings)
            
            # Marquer comme minion du boss
            minion.is_boss_minion = True
            minion.boss_owner = boss
            minions.append(minion)
        
        self.spawn_cooldown = self.spawn_rate
        return minions


class BossDivisionSystem:
    """Système de division du boss"""
    
    def __init__(self):
        self.can_divide = True
        self.division_cooldown = 0
        self.division_health_threshold = 0.33  # Division à 1/3 de vie
    
    def check_division(self, boss, health_ratio):
        """Vérifie si le boss doit se diviser"""
        if not self.can_divide:
            return False
        
        if health_ratio <= self.division_health_threshold and self.division_cooldown <= 0:
            return True
        
        return False
    
    def divide_boss(self, boss):
        """Divise le boss en deux"""
        if not self.can_divide:
            return []
                
        clones = []
        current_health = boss.health / 2
        
        for i in range(2):
            # Position décalée
            angle = (math.pi * i) + random.random() * 0.5
            distance = boss.radius * 2
            x = boss.x + math.cos(angle) * distance
            y = boss.y + math.sin(angle) * distance
            
            # Créer un clone avec stats réduites
            clone = type(boss)(x, y, boss.settings, 1, None)
            
            # Stats réduites
            clone.health = current_health * 0.7
            clone.max_health = clone.health
            clone.damage = boss.damage * 0.6
            clone.speed = boss.speed * 1.1
            clone.radius = boss.radius * 0.8
            
            # Copier l'état actuel
            clone.current_phase = boss.current_phase
            clone.rage_mode = boss.rage_mode
            
            # Empêcher la division infinie
            clone.division_system.can_divide = False
            
            # Couleur plus claire pour distinguer
            clone.base_color = (
                min(255, boss.base_color[0] + 30),
                min(255, boss.base_color[1] + 30),
                min(255, boss.base_color[2] + 30)
            )
            
            clones.append(clone)
        
        # Désactiver la division pour le boss original
        self.can_divide = False
        self.division_cooldown = 600  # 10 secondes
        
        return clones


class Boss(Enemy):
    """
    Boss amélioré avec division et invocation de minions
    Nom: "Boss"
    """
    
    def __init__(self, x, y, settings, floor_number, global_seed=None):
        super().__init__(x, y, settings)
        
        # Configuration
        self.type = "boss"
        self.name = "Boss"
        
        # Seed aléatoire
        if global_seed:
            random.seed(global_seed + floor_number)
        
        # Statistiques
        self._init_stats(floor_number)
        
        # Systèmes
        self.pattern_core = RecursivePatternCore()
        self.phases = []
        self.current_phase = 1
        self._init_phases(min(4, 1 + floor_number // 2))
        
        self.minion_system = MinionSpawnSystem(settings)
        self.division_system = BossDivisionSystem()
        
        # État
        self.current_pattern = None
        self.pattern_cooldown = 0
        self.attack_cooldown = self._get_cooldown(floor_number)
        
        self.rage_mode = False
        self.rage_health_threshold = 0.33  # Rage à 1/3 de vie
        
        # Animation
        self.pulse_timer = 0
        self.rotation_angle = 0
        
        # Couleur
        self.base_color = (150, 100, 255)
        self.core_color = (255, 255, 220)
        
    
    def _init_stats(self, floor_number):
        """Initialise les statistiques"""
        level = max(1, floor_number)
        
        self.health = 400 + (level * 100)
        self.max_health = self.health
        self.damage = 15 + (level * 2)
        self.speed = 1.5 + (level * 0.1)
        self.radius = 30
        
        # Multiplicateurs
        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
    
    def _get_cooldown(self, floor_number):
        """Calcule le cooldown d'attaque"""
        base = 90
        reduction = min(30, floor_number * 2)
        return max(60, base - reduction)
    
    def _init_phases(self, count):
        """Initialise les phases"""
        self.phases = [BossPhase(i + 1, count) for i in range(count)]
    
    def update(self, player, enemy_projectiles=None):
        """
        Met à jour le boss
        Retourne: (minions_spawned, clones_created)
        """
        # Mise à jour de phase
        health_ratio = self.health / self.max_health
        for i, phase in enumerate(self.phases):
            if health_ratio <= phase.health_threshold:
                new_phase = i + 1
                if new_phase > self.current_phase:
                    self.current_phase = new_phase
                    self._on_phase_change(new_phase)
                    break
        
        # Vérifier la rage
        self._check_rage_mode(health_ratio)
        
        # Vérifier la division
        clones = []
        if self.division_system.check_division(self, health_ratio):
            clones = self.division_system.divide_boss(self)
        
        # Animation
        self.pulse_timer += 0.07
        self.rotation_angle += 0.02
        
        # Déplacement
        self._smart_movement(player)
        
        # Attaques
        self._update_attacks(enemy_projectiles)
        
        # Invocation de minions
        minions = self.minion_system.update(self, [])  # Liste vide car pas accès aux ennemis
        
        # Contraintes
        self._constrain_to_screen()
        
        return minions, clones
    
    def _on_phase_change(self, new_phase):
        """Transition de phase"""
        
        # Effet visuel
        self.settings.sounds["spawn"].play()
        
        # Buff de phase
        phase = self.phases[new_phase - 1]
        self.speed *= 1.1
        
        # Réinitialiser le pattern
        self.current_pattern = None
        self.pattern_cooldown = 0
    
    def _check_rage_mode(self, health_ratio):
        """Active le mode rage à 1/3 de vie"""
        if health_ratio <= self.rage_health_threshold and not self.rage_mode:
            self.rage_mode = True
            
            # Activer la rage sur la phase actuelle
            if self.current_phase <= len(self.phases):
                self.phases[self.current_phase - 1].activate_rage()
            
            # Buffs de rage
            self.speed *= 1.3
            self.damage_multiplier = 1.5
            self.attack_cooldown *= 0.7
                
    def _smart_movement(self, player):
        """Déplacement intelligent"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Distance cible selon le mode
        if self.rage_mode:
            target_distance = 100  # Plus agressif en rage
        else:
            target_distance = 150
        
        # Vitesse ajustée
        speed = self.speed * self.speed_multiplier
        
        # Mouvement
        if distance > target_distance * 1.2:
            # Approche
            self.x += (dx / distance) * speed
            self.y += (dy / distance) * speed
        elif distance < target_distance * 0.8:
            # Éloignement
            self.x -= (dx / distance) * speed * 0.8
            self.y -= (dy / distance) * speed * 0.8
        else:
            # Mouvement latéral
            lateral_angle = math.atan2(dy, dx) + math.pi/2
            self.x += math.cos(lateral_angle) * speed * 0.6
            self.y += math.sin(lateral_angle) * speed * 0.6
        
        # Tremblement en rage
        if self.rage_mode:
            shake = math.sin(self.pulse_timer * 3) * 2
            self.x += shake
            self.y += shake
    
    def _update_attacks(self, enemy_projectiles):
        """Gère les attaques"""
        if enemy_projectiles is None:
            return
        
        if self.pattern_cooldown > 0:
            self.pattern_cooldown -= 1
            return
        
        # Choisir un pattern
        if self.current_pattern is None:
            if self.current_phase <= len(self.phases):
                phase = self.phases[self.current_phase - 1]
                self.current_pattern = phase.get_random_pattern()
            else:
                self.current_pattern = random.choice(["fractal", "simple"])
        
        # Exécuter le pattern
        self._execute_pattern(enemy_projectiles)
        
        # Cooldown ajusté
        if self.current_phase <= len(self.phases):
            phase = self.phases[self.current_phase - 1]
            cooldown = self.attack_cooldown / phase.attack_speed
        else:
            cooldown = self.attack_cooldown
        
        # Rage mode réduit le cooldown
        if self.rage_mode:
            cooldown *= 0.6
        
        self.pattern_cooldown = int(cooldown)
        self.current_pattern = None
    
    def _execute_pattern(self, enemy_projectiles):
        """Exécute le pattern actuel"""
        self.settings.sounds["Tire_4"].play()
        
        current_time = pygame.time.get_ticks() * 0.001
        phase_color = self.phases[self.current_phase - 1].color if self.current_phase <= len(self.phases) else self.base_color
        
        # Paramètres
        params = {
            'angle_offset': self.rotation_angle,
            'scale': 1.0,
            'intensity': 1.0,
            'phase': self.current_phase
        }
        
        # Profondeur selon la phase
        depth = min(4, 1 + self.current_phase)
        
        # Génération récursive
        pattern_data = self.pattern_core.generate_recursive_pattern(
            self.x, self.y, depth, depth,
            self.current_pattern, params, current_time
        )
        
        # Création des projectiles avec taille augmentée
        for item in pattern_data:
            if item[0] == 'projectile':
                _, x, y, dx, dy, base_damage, angle = item
                
                # Dégâts ajustés
                damage = base_damage * self.damage_multiplier
                if self.current_phase <= len(self.phases):
                    damage *= self.phases[self.current_phase - 1].damage_multiplier
                
                # Taille augmentée (rayon de 5 à 8 au lieu de 3 à 5)
                radius = max(5, 8 - depth // 2)
                
                # Couleur selon l'état
                color = phase_color
                if self.rage_mode:
                    color = (255, 100, 100)  # Rouge en rage
                
                projectile = Projectile(
                    x, y, 
                    dx, dy,
                    damage,
                    settings=self.settings,
                    color=color,
                    radius=radius  # Taille augmentée
                )
                enemy_projectiles.append(projectile)
    
    def _constrain_to_screen(self):
        """Garder dans l'écran"""
        margin = self.radius + 25
        self.x = max(margin, min(self.x, self.settings.screen_width - margin))
        self.y = max(margin, min(self.y, self.settings.screen_height - margin))
    
    def take_damage(self, amount):
        """
        Prend des dégâts
        Retourne True si le boss meurt
        """
        # Réduction selon la phase
        phase = self.current_phase
        reduction = 0.9 ** (phase - 1)
        actual_damage = amount * reduction
        
        # Appliquer
        self.health -= actual_damage
        
        # Effet visuel
        self.pulse_timer += 0.3
        
        # Mort
        if self.health <= 0:
            return True
        
        return False
    
    def draw(self, screen):
        """Dessin du boss"""
        current_time = pygame.time.get_ticks() * 0.001
        phase_color = self.phases[self.current_phase - 1].color if self.current_phase <= len(self.phases) else self.base_color
        
        # Pulsation
        base_pulse = math.sin(self.pulse_timer) * 6
        
        if self.rage_mode:
            rage_pulse = math.sin(current_time * 6) * 4
            base_pulse += rage_pulse
        
        main_radius = self.radius + base_pulse
        
        # Aura de rage
        if self.rage_mode:
            aura_radius = main_radius + 20
            aura_alpha = 80 + int(40 * math.sin(current_time * 4))
            
            aura_surface = pygame.Surface((int(aura_radius*2), int(aura_radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(
                aura_surface,
                (255, 50, 50, aura_alpha),
                (int(aura_radius), int(aura_radius)),
                int(aura_radius)
            )
            screen.blit(aura_surface, (int(self.x - aura_radius), int(self.y - aura_radius)))
        
        # Corps
        layers = 4
        for i in range(layers, 0, -1):
            radius = main_radius * (i / layers)
            alpha = 60 + (i * 40)
            
            # Dégradé
            blend = i / layers
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
        core_radius = main_radius * 0.4
        core_pulse = math.sin(current_time * 5) * 3
        
        pygame.draw.circle(
            screen, self.core_color,
            (int(self.x), int(self.y)),
            int(core_radius + core_pulse)
        )
        
        # Particules d'énergie
        for i in range(10):
            angle = (2 * math.pi * i / 10) + self.rotation_angle
            distance = main_radius * 0.8
            
            particle_x = self.x + math.cos(angle) * distance
            particle_y = self.y + math.sin(angle) * distance
            
            particle_size = 3 + math.sin(current_time * 3 + i) * 1.5
            
            pygame.draw.circle(
                screen, phase_color,
                (int(particle_x), int(particle_y)),
                int(particle_size)
            )
        
        # Interface
        if hasattr(self.settings, 'font') and self.settings.font:
            # Nom
            name_text = self.settings.font["h2"].render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, self.y - main_radius - 30))
            
            # Phase
            phase_text = self.settings.font["h3"].render(
                f"Phase {self.current_phase}", 
                True, phase_color
            )
            phase_rect = phase_text.get_rect(center=(self.x, self.y - main_radius - 55))
            
            # Rage
            if self.rage_mode:
                rage_text = self.settings.font["h3"].render("RAGE!", True, (255, 50, 50))
                rage_rect = rage_text.get_rect(center=(self.x, self.y + main_radius + 25))
                screen.blit(rage_text, rage_rect)
            
            screen.blit(name_text, name_rect)
            screen.blit(phase_text, phase_rect)
        
        # Barre de vie
        self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen, width=300, height=20):
        """Barre de vie"""
        # Position
        bar_x = self.x - width // 2
        bar_y = self.y - self.radius - 85
        
        # Fond
        pygame.draw.rect(
            screen, (40, 40, 40),
            (bar_x, bar_y, width, height),
            border_radius=height//2
        )
        
        # Vie
        health_ratio = max(0, self.health / self.max_health)
        health_width = int(width * health_ratio)
        
        if health_width > 0:
            # Couleur selon la santé
            if health_ratio > 0.6:
                color = (100, 255, 100)
            elif health_ratio > 0.3:
                color = (255, 255, 100)
            else:
                color = (255, 100, 100)
            
            # Gradient
            health_surface = pygame.Surface((health_width, height), pygame.SRCALPHA)
            for i in range(health_width):
                pos = i / width
                r = int(color[0] * (0.7 + 0.3 * pos))
                g = int(color[1] * (0.7 + 0.3 * pos))
                b = int(color[2] * (0.7 + 0.3 * pos))
                
                pygame.draw.line(
                    health_surface, (r, g, b, 220),
                    (i, 0), (i, height)
                )
            
            screen.blit(health_surface, (bar_x, bar_y))
        
        # Seuil de rage (1/3)
        rage_marker = bar_x + int(width * self.rage_health_threshold)
        pygame.draw.line(
            screen, (255, 50, 50, 180),
            (rage_marker, bar_y - 5),
            (rage_marker, bar_y + height + 5), 3
        )
        
        # Marqueurs de phase
        for i in range(1, len(self.phases)):
            marker_x = bar_x + int(width * (i / len(self.phases)))
            
            if i < self.current_phase:
                marker_color = (*self.phases[i - 1].color, 180)
            elif i == self.current_phase:
                marker_color = (*self.phases[i - 1].color, 220)
            else:
                marker_color = (80, 80, 80, 120)
            
            pygame.draw.line(
                screen, marker_color,
                (marker_x, bar_y - 3),
                (marker_x, bar_y + height + 3), 2
            )
        
        # Bordure
        border_color = (200, 200, 200)
        if self.rage_mode:
            border_color = (255, 50, 50)
        
        pygame.draw.rect(
            screen, border_color,
            (bar_x, bar_y, width, height),
            3, border_radius=height//2
        )
        
        # Texte
        if hasattr(self.settings, 'font') and self.settings.font:
            health_text = self.settings.font["h3"].render(
                f"{int(self.health)}/{self.max_health}", 
                True, (255, 255, 255)
            )
            health_rect = health_text.get_rect(center=(self.x, bar_y - 25))
            screen.blit(health_text, health_rect)
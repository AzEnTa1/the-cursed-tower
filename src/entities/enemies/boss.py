# src/entities/enemies/boss.py
import pygame
import math
import random
from .enemy import Enemy
from ..projectiles import Projectile


class RecursiveBossCore:
    """
    Noyau de génération récursive des patterns de boss
    Utilise une approche fractale pour générer des comportements uniques
    """
    
    def generate_behavior_tree(floor_number, seed, depth=0, max_depth=4):
        """
        Génère un arbre de comportement récursif pour le boss
        
        Complexité : O(branches^depth) où branches = floor_number % 3 + 2
        Cette complexité est contrôlée par max_depth pour éviter l'explosion exponentielle
        """
        # Initialisation aléatoire déterministe basée sur la seed
        local_random = random.Random(seed + depth * 1000 + floor_number * 10000)
        
        # Cas de base : feuille de l'arbre (attaque simple)
        if depth >= max_depth or floor_number < depth * 3:
            attack_pattern = local_random.choice(['circle', 'spray', 'burst'])
            
            return {
                'type': 'leaf',
                'attack_pattern': attack_pattern,
                'damage_multiplier': 0.3 + (depth * 0.1),
                'speed_multiplier': 1.0 + (depth * 0.2),
                'color': (
                    min(255, 150 + depth * 20),
                    min(255, 50 + depth * 30),
                    max(0, 200 - depth * 40)
                ),
                'complexity': depth
            }
        
        # Cas récursif : nœud avec sous-comportements
        branch_count = (floor_number % 3) + 2  # 2-4 branches selon étage
        branches = []
        
        for i in range(branch_count):
            # Chaque branche a une variation unique basée sur la seed
            branch_seed = seed + i * 1000 + depth * 10000
            branch = RecursiveBossCore.generate_behavior_tree(
                floor_number=floor_number,
                seed=branch_seed,
                depth=depth + 1,
                max_depth=max_depth
            )
            
            branch['phase_modifier'] = i / branch_count
            branch['activation_threshold'] = 1.0 - (depth * 0.2)
            branches.append(branch)
        
        # Nœud parent qui combine les branches
        node_type = local_random.choice(['sequential', 'parallel', 'alternating'])
        
        return {
            'type': 'node',
            'node_type': node_type,
            'branches': branches,
            'transition_time': 60 + (depth * 20),  # Frames entre transitions
            'health_trigger': 1.0 - ((depth + 1) * 0.25),  # % de vie pour activer
            'color': (
                max(0, 200 - depth * 30),
                min(255, 100 + depth * 20),
                min(255, 50 + depth * 40)
            ),
            'complexity': depth
        }

    def recursive_attack_pattern(position, depth, pattern_tree, projectiles_list, 
                                damage_base, speed_base, angle_offset=0, settings=None):
        """
        Exécute un pattern d'attaque récursif
        Complexité par la profondeur - s'arrête quand depth <= 0
        """
        if depth <= 0:
            return
        
        node = pattern_tree
        x, y = position
        
        if node['type'] == 'leaf':
            # Cas de base : génération de projectiles
            RecursiveBossCore._generate_leaf_attack(
                x, y, node, projectiles_list, damage_base, speed_base, 
                angle_offset, settings
            )
        else:
            # Cas récursif : traiter les branches
            current_time = pygame.time.get_ticks() * 0.001
            branch_angle = 360 / len(node['branches'])
            
            for i, branch in enumerate(node['branches']):
                # Calcul d'offset angulaire pour cette branche
                branch_angle_offset = angle_offset + (i * branch_angle)
                branch_angle_rad = math.radians(branch_angle_offset)
                
                # Position décalée pour la branche
                radius = 20 + (depth * 10)
                branch_x = x + math.cos(branch_angle_rad) * radius
                branch_y = y + math.sin(branch_angle_rad) * radius
                
                # Animation d'onde pour les branches
                wave_offset = math.sin(current_time * 2 + i) * 5
                branch_x += math.cos(branch_angle_rad) * wave_offset
                branch_y += math.sin(branch_angle_rad) * wave_offset
                
                # Appel récursif avec profondeur réduite
                RecursiveBossCore.recursive_attack_pattern(
                    position=(branch_x, branch_y),
                    depth=depth - 1,
                    pattern_tree=branch,
                    projectiles_list=projectiles_list,
                    damage_base=damage_base * node['damage_multiplier'],
                    speed_base=speed_base * node['speed_multiplier'],
                    angle_offset=branch_angle_offset + (current_time * 20),
                    settings=settings
                )
    
    def _generate_leaf_attack(x, y, leaf_data, projectiles_list, damage_base, 
                             speed_base, angle_offset, settings):
        """
        Génère les projectiles pour une feuille de l'arbre
        """
        current_time = pygame.time.get_ticks() * 0.001
        
        if leaf_data['attack_pattern'] == 'circle':
            # Cercle de projectiles
            projectile_count = 8 + int(math.sin(current_time) * 4)
            for i in range(projectile_count):
                angle = (2 * math.pi * i / projectile_count) + math.radians(angle_offset)
                dx = math.cos(angle) * speed_base
                dy = math.sin(angle) * speed_base
                
                projectiles_list.append(Projectile(
                    x, y, dx, dy, damage_base,
                    settings=settings,
                    color=leaf_data['color'],
                    radius=4 + int(math.sin(current_time + i) * 2)
                ))
        
        elif leaf_data['attack_pattern'] == 'spray':
            # Spray directionnel
            base_angle = math.radians(angle_offset)
            for i in range(-2, 3):
                angle = base_angle + (i * math.radians(15))
                dx = math.cos(angle) * speed_base
                dy = math.sin(angle) * speed_base
                
                projectiles_list.append(Projectile(
                    x, y, dx, dy, damage_base * 0.7,
                    settings=settings,
                    color=leaf_data['color'],
                    radius=3
                ))
        
        elif leaf_data['attack_pattern'] == 'burst':
            # Burst concentrique
            for ring in range(1, 4):
                ring_projectiles = 4 * ring
                ring_speed = speed_base * (0.5 + ring * 0.3)
                for i in range(ring_projectiles):
                    angle = (2 * math.pi * i / ring_projectiles) + current_time
                    dx = math.cos(angle) * ring_speed
                    dy = math.sin(angle) * ring_speed
                    
                    projectiles_list.append(Projectile(
                        x, y, dx, dy, damage_base * 0.5,
                        settings=settings,
                        color=leaf_data['color'],
                        radius=2 + ring
                    ))

class AdaptiveBoss(Enemy):
    """
    Boss adaptatif avec comportement généré récursivement
    Utilise RecursiveBossCore pour des patterns d'attaque uniques
    """
    
    # Cache pour les comportements générés (optimisation)
    _behavior_cache = {}
    
    def __init__(self, x, y, settings, floor_number, global_seed):
        """
        Initialise un boss unique basé sur l'étage et la seed
        """
        super().__init__(x, y, settings)
        
        # Seed unique pour ce boss spécifique
        self.boss_seed = hash((global_seed, floor_number, x, y)) % (2**32)
        random.seed(self.boss_seed)
        
        # Type et identification
        self.type = "boss"
        self.name = self._generate_boss_name(floor_number)
        
        # Statistiques évolutives
        self.base_stats = self._calculate_base_stats(floor_number)
        self.health = self.base_stats['health']
        self.max_health = self.health
        self.damage = self.base_stats['damage']
        self.speed = self.base_stats['speed']
        self.radius = self.base_stats['radius']
        
        # Apparence unique
        self.color = self._generate_unique_color(floor_number)
        self.secondary_color = (
            min(255, (self.color[0] + 50) % 256),
            min(255, (self.color[1] + 30) % 256),
            min(255, (self.color[2] + 70) % 256)
        )
        
        # Système de phases récursif
        self.phase_depth = min(4, max(1, (floor_number // 3)))  # 1-4 phases
        self.current_phase = 1
        self.phase_transition_timer = 0
        
        # Génération du comportement récursif
        self.behavior_tree = self._generate_behavior_tree(floor_number)
        self.active_pattern = None
        self.pattern_cooldown = 0
        self.pattern_duration = 0
        
        # État interne
        self.phase_health_thresholds = self._calculate_phase_thresholds()
        self.adaptive_multipliers = {
            'damage': 1.0,
            'speed': 1.0,
            'attack_rate': 1.0,
            'defense': 1.0
        }
        
        # Animation et effets
        self.pulse_timer = 0
        self.rotation_angle = 0
        self.special_effects = []
        
        # Timers
        self.attack_timer = 0
        self.movement_timer = 0
        self.phase_timer = 0
        
        # IA adaptative
        self.player_distance_history = []
        self.preferred_distance = 200 + (floor_number * 20)
        self.attack_pattern_history = []
    
    def _calculate_base_stats(self, floor_number):
        """Calcule les statistiques de base selon l'étage"""
        boss_level = max(1, floor_number // 3)
        
        return {
            'health': 300 + (boss_level * 150),
            'damage': 10 + (boss_level * 3),
            'speed': 1.0 + (boss_level * 0.1),
            'radius': 25 + min(boss_level * 3, 20),
            'attack_cooldown': max(30, 90 - (boss_level * 5))
        }
    
    def _generate_boss_name(self, floor_number):
        """Retourne toujours 'Boss'"""
        return "Boss"
    
    def _generate_unique_color(self, floor_number):
        """Génère une couleur unique basée sur la seed et l'étage"""
        hue = (self.boss_seed % 360) / 360.0
        saturation = 0.7 + min(0.3, (floor_number % 4) * 0.1)
        value = 0.8 - min(0.5, (floor_number // 12) * 0.1)
        
        # Conversion HSV vers RGB
        c = value * saturation
        x = c * (1 - abs((hue * 6) % 2 - 1))
        m = value - c
        
        if hue < 1/6:
            r, g, b = c, x, 0
        elif hue < 2/6:
            r, g, b = x, c, 0
        elif hue < 3/6:
            r, g, b = 0, c, x
        elif hue < 4/6:
            r, g, b = 0, x, c
        elif hue < 5/6:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )
    
    def _generate_behavior_tree(self, floor_number):
        """Génère ou récupère l'arbre de comportement"""
        cache_key = (self.boss_seed, floor_number)
        
        if cache_key not in AdaptiveBoss._behavior_cache:
            max_depth = min(4, 1 + (floor_number // 6))  # Profondeur augmente avec étage
            AdaptiveBoss._behavior_cache[cache_key] = RecursiveBossCore.generate_behavior_tree(
                floor_number=floor_number,
                seed=self.boss_seed,
                depth=0,
                max_depth=max_depth
            )
        
        return AdaptiveBoss._behavior_cache[cache_key]
    
    def _calculate_phase_thresholds(self):
        """Calcule les seuils de vie pour chaque phase"""
        thresholds = []
        for i in range(self.phase_depth, 0, -1):
            thresholds.append(i / self.phase_depth)
        return thresholds
    
    def update(self, player, enemy_projectiles=None):
        """
        Met à jour le boss avec comportement adaptatif
        """
        # Vérifier transition de phase
        self._check_phase_transition()
        
        # Mise à jour des timers
        self.pulse_timer += 0.05
        self.rotation_angle += 0.01
        self.attack_timer += 1
        self.movement_timer += 1
        self.phase_timer += 1
        
        # Mise à jour des effets spéciaux
        self._update_special_effects()
        
        # Mouvement adaptatif
        self._adaptive_movement(player)
        
        # Gestion des attaques
        if self.pattern_cooldown > 0:
            self.pattern_cooldown -= 1
        elif enemy_projectiles is not None:
            self._execute_attack_pattern(enemy_projectiles)
        
        # Adaptation dynamique au joueur
        self._adapt_to_player(player)
        
        # Garder dans les limites
        self._constrain_to_screen()
    
    def _check_phase_transition(self):
        """Vérifie et gère les transitions de phase"""
        health_ratio = self.health / self.max_health
        
        for i, threshold in enumerate(self.phase_health_thresholds):
            if health_ratio <= threshold and self.current_phase < (self.phase_depth - i):
                self.current_phase = self.phase_depth - i
                self._on_phase_transition()
                break
    
    def _on_phase_transition(self):
        """Déclenché lors d'un changement de phase"""
        # Augmentation des capacités
        self.adaptive_multipliers['damage'] *= 1.3
        self.adaptive_multipliers['attack_rate'] *= 1.2
        self.adaptive_multipliers['defense'] *= 1.1
        
        # Nouveau pattern d'attaque
        self.pattern_cooldown = 0
        self.active_pattern = None
        self.attack_pattern_history.clear()
        
        # Effet visuel
        self.special_effects.append({
            'type': 'phase_transition',
            'timer': 60,
            'radius': self.radius * 2,
            'color': self.secondary_color,
            'intensity': 1.0
        })
    
    def _adaptive_movement(self, player):
        """Mouvement adaptatif basé sur le comportement du joueur"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Historique des distances
        self.player_distance_history.append(distance)
        if len(self.player_distance_history) > 20:
            self.player_distance_history.pop(0)
        
        # Calcul distance moyenne
        avg_distance = sum(self.player_distance_history) / len(self.player_distance_history)
        
        # Ajustement de la distance préférée
        if avg_distance > self.preferred_distance * 1.5:
            self.preferred_distance *= 0.98
        elif avg_distance < self.preferred_distance * 0.5:
            self.preferred_distance *= 1.02
        
        # Mouvement pour maintenir la distance optimale
        target_ratio = distance / self.preferred_distance
        
        if target_ratio > 1.2:
            # Trop loin, se rapprocher
            move_speed = self.speed * self.adaptive_multipliers['speed']
            self.x += (dx / distance) * move_speed
            self.y += (dy / distance) * move_speed
        elif target_ratio < 0.8:
            # Trop proche, s'éloigner
            move_speed = self.speed * self.adaptive_multipliers['speed'] * 0.8
            self.x -= (dx / distance) * move_speed
            self.y -= (dy / distance) * move_speed
        
        # Mouvement orbital occasionnel
        if self.movement_timer % 180 == 0:
            orbit_angle = random.random() * 2 * math.pi
            orbit_distance = self.preferred_distance * 0.7
            self.x = player.x + math.cos(orbit_angle) * orbit_distance
            self.y = player.y + math.sin(orbit_angle) * orbit_distance
    
    def _execute_attack_pattern(self, enemy_projectiles):
        """Exécute un pattern d'attaque récursif"""
        if self.active_pattern is None:
            self._select_new_pattern()
        self.settings.sounds["Tire_4"].play()
        # Calcul de la profondeur basée sur la phase
        attack_depth = min(3, self.current_phase + 1)
        
        # Exécution récursive du pattern
        RecursiveBossCore.recursive_attack_pattern(
            position=(self.x, self.y),
            depth=attack_depth,
            pattern_tree=self.active_pattern,
            projectiles_list=enemy_projectiles,
            damage_base=self.damage * self.adaptive_multipliers['damage'],
            speed_base=3.0 + (self.current_phase * 0.5),
            angle_offset=self.rotation_angle * 50,
            settings=self.settings
        )
        
        # Historique des patterns
        pattern_name = self.active_pattern.get('attack_pattern', 'node') if self.active_pattern['type'] == 'leaf' else 'complex_node'
        self.attack_pattern_history.append(pattern_name)
        if len(self.attack_pattern_history) > 10:
            self.attack_pattern_history.pop(0)
        
        # Réinitialiser le cooldown
        self.pattern_cooldown = max(10, self.base_stats['attack_cooldown'] / self.adaptive_multipliers['attack_rate'])
        self.pattern_duration -= 1
        
        # Changer de pattern si durée écoulée
        if self.pattern_duration <= 0:
            self.active_pattern = None
    
    def _select_new_pattern(self):
        """Sélectionne un nouveau pattern d'attaque dans l'arbre de comportement"""
        # Sélection récursive dans l'arbre
        current_node = self.behavior_tree
        depth = 0
        
        while current_node['type'] == 'node' and depth < self.current_phase:
            available_branches = len(current_node['branches'])
            
            # Éviter de répéter le même pattern
            recent_patterns = self.attack_pattern_history[-3:] if len(self.attack_pattern_history) >= 3 else []
            
            # Sélectionner une branche moins utilisée récemment
            branch_weights = [1.0] * available_branches
            for i, branch in enumerate(current_node['branches']):
                branch_name = branch.get('attack_pattern', f'node_{i}') if branch['type'] == 'leaf' else f'complex_{i}'
                if branch_name in recent_patterns:
                    branch_weights[i] *= 0.5  # Réduire le poids des patterns récents
            
            # Choix pondéré
            total_weight = sum(branch_weights)
            if total_weight > 0:
                choice = random.choices(range(available_branches), weights=branch_weights, k=1)[0]
            else:
                choice = random.randint(0, available_branches - 1)
            
            current_node = current_node['branches'][choice]
            depth += 1
        
        self.active_pattern = current_node
        self.pattern_duration = 60 + (self.current_phase * 30)
        
        pattern_type = self.active_pattern['type']
        pattern_name = self.active_pattern.get('attack_pattern', 'complex') if pattern_type == 'leaf' else 'composite'
    
    def _adapt_to_player(self, player):
        """Adapte le comportement basé sur les actions du joueur"""
        # Analyser la vitesse du joueur
        player_speed = math.sqrt(player.last_dx**2 + player.last_dy**2)
        
        if player_speed > 3:
            # Joueur rapide : augmenter la fréquence d'attaque
            self.adaptive_multipliers['attack_rate'] = min(2.0, self.adaptive_multipliers['attack_rate'] * 1.02)
            self.adaptive_multipliers['speed'] = min(1.5, self.adaptive_multipliers['speed'] * 1.01)
        else:
            # Joueur lent : augmenter les dégâts
            self.adaptive_multipliers['damage'] = min(2.5, self.adaptive_multipliers['damage'] * 1.02)
        
        # Ajustement périodique
        if self.phase_timer % 300 == 0:  # Toutes les 5 secondes
            self._rebalance_multipliers()
    
    def _rebalance_multipliers(self):
        """Rééquilibre les multiplicateurs pour éviter les déséquilibres"""
        avg = sum(self.adaptive_multipliers.values()) / len(self.adaptive_multipliers)
        
        for key in self.adaptive_multipliers:
            # Ramener vers la moyenne si trop extrême
            if self.adaptive_multipliers[key] > avg * 1.5:
                self.adaptive_multipliers[key] *= 0.95
            elif self.adaptive_multipliers[key] < avg * 0.5:
                self.adaptive_multipliers[key] *= 1.05
    
    def _update_special_effects(self):
        """Met à jour les effets spéciaux"""
        for effect in self.special_effects[:]:
            effect['timer'] -= 1
            
            # Animation de l'effet
            if effect['type'] == 'phase_transition':
                effect['intensity'] *= 0.95
                effect['radius'] += 0.5
            
            if effect['timer'] <= 0:
                self.special_effects.remove(effect)
    
    def _constrain_to_screen(self):
        """Maintient le boss dans l'écran avec une marge"""
        margin = self.radius + 50
        self.x = max(margin, min(self.x, self.settings.screen_width - margin))
        self.y = max(margin, min(self.y, self.settings.screen_height - margin))
    
    def take_damage(self, amount):
        """
        Gère les dégâts avec adaptation
        """
        # Réduction de dégâts en phase finale
        if self.current_phase == self.phase_depth:
            amount *= 0.7 * self.adaptive_multipliers['defense']
        else:
            amount *= self.adaptive_multipliers['defense']
        
        # Adaptation défensive après avoir pris des dégâts importants
        if amount > self.max_health * 0.1:
            self.adaptive_multipliers['speed'] = min(1.5, self.adaptive_multipliers['speed'] * 1.05)
            self.adaptive_multipliers['defense'] = min(1.3, self.adaptive_multipliers['defense'] * 1.02)
            
            # Effet visuel de dégâts
            self.special_effects.append({
                'type': 'damage_flash',
                'timer': 15,
                'color': (255, 50, 50),
                'intensity': 1.0
            })
        
        # Appliquer les dégâts
        self.health -= amount
        
        # Vérifier la mort
        if self.health <= 0:
            return True
        
        return False
    
    def draw(self, screen):
        """Dessine le boss avec effets visuels avancés"""
        current_time = pygame.time.get_ticks() * 0.001
        
        # Effets spéciaux en premier (pour qu'ils soient en arrière-plan)
        for effect in self.special_effects:
            if effect['type'] == 'phase_transition':
                alpha = int(150 * effect['intensity'] * (effect['timer'] / 60))
                pulse = math.sin(current_time * 10) * 10 * effect['intensity']
                
                # Cercle d'énergie
                effect_surface = pygame.Surface(
                    (int(effect['radius']*2), int(effect['radius']*2)), 
                    pygame.SRCALPHA
                )
                pygame.draw.circle(
                    effect_surface, 
                    (*effect['color'], alpha),
                    (int(effect['radius']), int(effect['radius'])),
                    int(effect['radius'] + pulse),
                    5
                )
                screen.blit(effect_surface, 
                          (int(self.x - effect['radius']), 
                           int(self.y - effect['radius'])))
            
            elif effect['type'] == 'damage_flash':
                alpha = int(100 * effect['intensity'] * (effect['timer'] / 15))
                flash_surface = pygame.Surface(
                    (int(self.radius*4), int(self.radius*4)), 
                    pygame.SRCALPHA
                )
                pygame.draw.circle(
                    flash_surface,
                    (*effect['color'], alpha),
                    (int(self.radius*2), int(self.radius*2)),
                    int(self.radius * 1.5)
                )
                screen.blit(flash_surface,
                          (int(self.x - self.radius*2),
                           int(self.y - self.radius*2)))
        
        # Corps principal avec pulsation
        pulse = math.sin(self.pulse_timer) * 3
        main_radius = self.radius + pulse
        
        # Gradient radial (de l'intérieur vers l'extérieur)
        for i in range(5, 0, -1):
            radius = main_radius * (i / 5)
            alpha = 50 + (i * 40)
            color = (
                int(self.color[0] * (i / 5)),
                int(self.color[1] * (i / 5)),
                int(self.color[2] * (i / 5))
            )
            
            surf = pygame.Surface((int(radius*2), int(radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), 
                             (int(radius), int(radius)), int(radius))
            screen.blit(surf, (int(self.x - radius), int(self.y - radius)))
        
        # Motif de phase (orbites)
        phase_indicator_radius = main_radius * 0.8
        for i in range(self.current_phase):
            angle = (2 * math.pi * i / self.current_phase) + self.rotation_angle
            indicator_x = self.x + math.cos(angle) * phase_indicator_radius
            indicator_y = self.y + math.sin(angle) * phase_indicator_radius
            
            # Orbite pulsante
            orbit_pulse = math.sin(current_time * 3 + i) * 3
            pygame.draw.circle(
                screen, self.secondary_color,
                (int(indicator_x), int(indicator_y)),
                main_radius * 0.15 + orbit_pulse
            )
        
        # Nom et info
        if hasattr(self.settings, 'font') and self.settings.font and 'h3' in self.settings.font:
            # Nom du boss
            name_text = self.settings.font["h3"].render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 30))
            
            # Phase actuelle
            phase_text = self.settings.font["h4"].render(
                f"Phase {self.current_phase}/{self.phase_depth}", 
                True, (200, 200, 255)
            )
            phase_rect = phase_text.get_rect(center=(self.x, self.y - self.radius - 50))
            
            # Indicateur de difficulté
            difficulty = "★" * self.current_phase + "☆" * (self.phase_depth - self.current_phase)
            diff_text = self.settings.font["h4"].render(difficulty, True, (255, 255, 0))
            diff_rect = diff_text.get_rect(center=(self.x, self.y - self.radius - 70))
            
            screen.blit(name_text, name_rect)
            screen.blit(phase_text, phase_rect)
            screen.blit(diff_text, diff_rect)
        
        # Barre de vie détaillée
        self._draw_advanced_health_bar(screen)
    
    def _draw_advanced_health_bar(self, screen, width=200, height=12):
        """Barre de vie avancée avec indicateurs de phase"""
        # Position
        bar_x = self.x - width // 2
        bar_y = self.y - self.radius - 90
        
        # Fond de la barre
        pygame.draw.rect(screen, (30, 30, 30), 
                        (bar_x, bar_y, width, height), 
                        border_radius=3)
        
        # Santé actuelle
        health_ratio = max(0, self.health / self.max_health)
        health_width = int(width * health_ratio)
        
        # Gradient de couleur (vert → jaune → rouge)
        if health_width > 0:
            health_surface = pygame.Surface((health_width, height), pygame.SRCALPHA)
            for i in range(health_width):
                pos_ratio = i / width
                if health_ratio > 0.6:
                    r = int(255 * (1 - pos_ratio * 0.7))
                    g = 255
                    b = int(100 * (1 - pos_ratio * 0.5))
                elif health_ratio > 0.3:
                    r = 255
                    g = int(255 * pos_ratio * 0.8)
                    b = 100
                else:
                    r = 255
                    g = int(255 * pos_ratio * 0.5)
                    b = 100
                
                pygame.draw.line(health_surface, (r, g, b, 200), 
                               (i, 0), (i, height))
            screen.blit(health_surface, (bar_x, bar_y))
        
        # Indicateurs de phase
        for i in range(1, self.phase_depth):
            phase_marker = bar_x + int(width * (i / self.phase_depth))
            marker_color = (255, 255, 255, 150) if i < self.current_phase else (100, 100, 100, 100)
            pygame.draw.line(screen, marker_color, 
                           (phase_marker, bar_y - 3), 
                           (phase_marker, bar_y + height + 3), 2)
        
        # Bordure
        pygame.draw.rect(screen, (200, 200, 200), 
                        (bar_x, bar_y, width, height), 
                        2, border_radius=3)
        
        # Texte de santé
        if hasattr(self.settings, 'font') and self.settings.font and 'h4' in self.settings.font:
            health_text = self.settings.font["h4"].render(
                f"{int(self.health)}/{self.max_health}", 
                True, (255, 255, 255)
            )
            health_rect = health_text.get_rect(center=(self.x, bar_y - 15))
            screen.blit(health_text, health_rect)
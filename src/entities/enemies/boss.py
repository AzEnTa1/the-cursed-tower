# src/entities/enemies/boss.py
import pygame
import math
import random
from typing import List, Dict, Any, Tuple
from .enemy import Enemy
from ..projectiles import Projectile


class RecursivePatternGenerator:
    """
    Système de génération de patterns récursifs pour les attaques de boss.
    Version améliorée avec plus de complexité et de variété.
    """
    
    # Patterns de base plus nombreux et variés
    BASE_PATTERNS = ['circle', 'spray', 'burst', 'spiral', 'sine_wave', 'vortex', 'cross', 'pentagram']
    
    @staticmethod
    def generate_fractal_pattern(seed: int, depth: int, max_depth: int, 
                                 complexity: float = 1.0) -> Dict[str, Any]:
        """
        Génère un pattern fractale récursif plus complexe.
        
        Complexité: O(k^d) où k est le facteur de branchement
        Mais limité par max_depth pour éviter l'explosion.
        
        Args:
            seed: Graine pour l'aléatoire déterministe
            depth: Profondeur actuelle
            max_depth: Profondeur maximum
            complexity: Facteur de complexité (0.0 à 2.0)
            
        Returns:
            Dictionnaire décrivant le pattern
        """
        local_random = random.Random(seed + depth * 1000)
        
        # Cas de base : feuille (attaque simple)
        if depth >= max_depth:
            return RecursivePatternGenerator._generate_leaf_pattern(local_random, depth, complexity)
        
        # Cas récursif : pattern complexe
        return RecursivePatternGenerator._generate_node_pattern(local_random, seed, depth, 
                                                                max_depth, complexity)
    
    @staticmethod
    def _generate_leaf_pattern(local_random: random.Random, depth: int, 
                               complexity: float) -> Dict[str, Any]:
        """Génère un pattern simple (feuille)"""
        # Plus de variété dans les patterns de base
        pattern_type = local_random.choice(RecursivePatternGenerator.BASE_PATTERNS)
        
        # Couleur basée sur la profondeur et complexité
        hue = (depth * 40 + int(complexity * 100)) % 360
        saturation = 0.7 + min(0.3, complexity * 0.15)
        value = 0.8 - min(0.5, depth * 0.1)
        
        r, g, b = RecursivePatternGenerator.hsv_to_rgb(hue, saturation, value)
        
        return {
            'type': 'leaf',
            'pattern_type': pattern_type,
            'damage_multiplier': 0.3 + (depth * 0.1) * complexity,
            'speed_multiplier': 1.0 + (depth * 0.15) * complexity,
            'projectile_count': int(8 + depth * 2 + complexity * 4),
            'color': (r, g, b),
            'depth': depth,
            'complexity': complexity
        }
    
    @staticmethod
    def _generate_node_pattern(local_random: random.Random, seed: int, depth: int, 
                               max_depth: int, complexity: float) -> Dict[str, Any]:
        """Génère un nœud complexe avec sous-patterns"""
        # Facteur de branchement variable selon complexité
        branch_count = max(2, min(5, int(2 + complexity * 1.5)))
        branches = []
        
        for i in range(branch_count):
            # Variation de seed pour chaque branche
            branch_seed = seed + i * 5000 + depth * 10000
            
            # Augmente légèrement la complexité pour les branches profondes
            branch_complexity = complexity * (0.8 + 0.2 * (i / branch_count))
            
            branch = RecursivePatternGenerator.generate_fractal_pattern(
                seed=branch_seed,
                depth=depth + 1,
                max_depth=max_depth,
                complexity=branch_complexity
            )
            
            branches.append(branch)
        
        # Type de nœud avec plus de variété
        node_types = ['sequential', 'parallel', 'alternating', 'symmetric', 'chaotic']
        node_type = local_random.choice(node_types)
        
        # Couleur du nœud
        hue = (depth * 60) % 360
        r, g, b = RecursivePatternGenerator.hsv_to_rgb(hue, 0.6, 0.7)
        
        return {
            'type': 'node',
            'node_type': node_type,
            'branches': branches,
            'transition_speed': 30 + (depth * 15),
            'rotation_speed': 0.5 + depth * 0.2,
            'spread_angle': math.radians(30 + depth * 10),
            'color': (r, g, b),
            'depth': depth,
            'complexity': complexity
        }
    
    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Conversion HSV vers RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )
    
    @staticmethod
    def execute_pattern_recursive(position: Tuple[float, float], pattern: Dict[str, Any], 
                                 projectiles: List[Projectile], player_pos: Tuple[float, float],
                                 damage_base: float, speed_base: float, phase: int,
                                 current_time: float, settings: Any, depth: int = 0) -> None:
        """
        Exécute un pattern récursif avec adaptation en fonction du joueur.
        
        Args:
            position: Position (x, y) d'origine
            pattern: Pattern à exécuter
            projectiles: Liste de projectiles à remplir
            player_pos: Position actuelle du joueur
            damage_base: Dégâts de base
            speed_base: Vitesse de base
            phase: Phase actuelle du boss
            current_time: Temps actuel pour animations
            settings: Paramètres du jeu
            depth: Profondeur actuelle (pour récursion)
        """
        if depth > 3:  # Limite de sécurité
            return
            
        x, y = position
        px, py = player_pos
        
        if pattern['type'] == 'leaf':
            RecursivePatternGenerator._execute_leaf_pattern(
                x, y, pattern, projectiles, player_pos,
                damage_base, speed_base, phase, current_time, settings
            )
        else:
            RecursivePatternGenerator._execute_node_pattern(
                x, y, pattern, projectiles, player_pos,
                damage_base, speed_base, phase, current_time, settings, depth
            )
    
    @staticmethod
    def _execute_leaf_pattern(x: float, y: float, pattern: Dict[str, Any], 
                             projectiles: List[Projectile], player_pos: Tuple[float, float],
                             damage_base: float, speed_base: float, phase: int,
                             current_time: float, settings: Any) -> None:
        """Exécute un pattern feuille"""
        pattern_type = pattern['pattern_type']
        damage = damage_base * pattern['damage_multiplier']
        speed = speed_base * pattern['speed_multiplier']
        color = pattern['color']
        
        # Calcul direction vers le joueur (pour certains patterns)
        px, py = player_pos
        dx_player = px - x
        dy_player = py - y
        dist_to_player = max(math.sqrt(dx_player**2 + dy_player**2), 0.1)
        angle_to_player = math.atan2(dy_player, dx_player)
        
        if pattern_type == 'circle':
            RecursivePatternGenerator._pattern_circle(
                x, y, pattern['projectile_count'], damage, speed, 
                color, current_time, projectiles, settings
            )
        elif pattern_type == 'spray':
            RecursivePatternGenerator._pattern_spray(
                x, y, angle_to_player, damage, speed, 
                color, projectiles, settings
            )
        elif pattern_type == 'burst':
            RecursivePatternGenerator._pattern_burst(
                x, y, damage, speed, color, 
                current_time, projectiles, settings
            )
        elif pattern_type == 'spiral':
            RecursivePatternGenerator._pattern_spiral(
                x, y, damage, speed, color, 
                current_time, phase, projectiles, settings
            )
        elif pattern_type == 'sine_wave':
            RecursivePatternGenerator._pattern_sine_wave(
                x, y, angle_to_player, damage, speed, 
                color, current_time, projectiles, settings
            )
        elif pattern_type == 'vortex':
            RecursivePatternGenerator._pattern_vortex(
                x, y, damage, speed, color, 
                current_time, projectiles, settings
            )
        elif pattern_type == 'cross':
            RecursivePatternGenerator._pattern_cross(
                x, y, damage, speed, color, 
                projectiles, settings
            )
        elif pattern_type == 'pentagram':
            RecursivePatternGenerator._pattern_pentagram(
                x, y, damage, speed, color, 
                current_time, projectiles, settings
            )
    
    @staticmethod
    def _execute_node_pattern(x: float, y: float, pattern: Dict[str, Any], 
                             projectiles: List[Projectile], player_pos: Tuple[float, float],
                             damage_base: float, speed_base: float, phase: int,
                             current_time: float, settings: Any, depth: int) -> None:
        """Exécute un pattern nœud (récursif)"""
        branches = pattern['branches']
        rotation_speed = pattern['rotation_speed']
        spread_angle = pattern['spread_angle']
        
        # Rotation globale
        global_rotation = current_time * rotation_speed
        
        # Adapte le nombre de branches selon la phase
        active_branches = min(len(branches), 2 + phase)
        
        for i in range(active_branches):
            branch = branches[i]
            
            # Calcul angle pour cette branche
            angle_offset = (2 * math.pi * i / active_branches) + global_rotation
            if pattern['node_type'] == 'symmetric':
                angle_offset += (i % 2) * math.pi / active_branches
            
            # Position décalée pour la branche
            radius = 15 + (depth * 8)
            branch_x = x + math.cos(angle_offset) * radius
            branch_y = y + math.sin(angle_offset) * radius
            
            # Animation
            pulse = math.sin(current_time * 3 + i) * 5
            branch_x += math.cos(angle_offset) * pulse
            branch_y += math.sin(angle_offset) * pulse
            
            # Appel récursif
            RecursivePatternGenerator.execute_pattern_recursive(
                position=(branch_x, branch_y),
                pattern=branch,
                projectiles=projectiles,
                player_pos=player_pos,
                damage_base=damage_base * 0.8,
                speed_base=speed_base * 1.1,
                phase=phase,
                current_time=current_time + i * 0.2,
                settings=settings,
                depth=depth + 1
            )
    
    # Implémentations des patterns individuels
    @staticmethod
    def _pattern_circle(x: float, y: float, count: int, damage: float, speed: float,
                       color: Tuple[int, int, int], time: float, 
                       projectiles: List[Projectile], settings: Any) -> None:
        """Cercle de projectiles avec animation"""
        for i in range(count):
            angle = (2 * math.pi * i / count) + time
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            # Animation de taille
            size_pulse = 3 + math.sin(time * 2 + i) * 1.5
            
            projectiles.append(Projectile(
                x, y, dx, dy, damage,
                settings=settings,
                color=color,
                radius=max(2, int(size_pulse))
            ))
    
    @staticmethod
    def _pattern_spray(x: float, y: float, base_angle: float, damage: float, speed: float,
                      color: Tuple[int, int, int], projectiles: List[Projectile], 
                      settings: Any) -> None:
        """Spray directionnel concentré"""
        spray_count = 7
        spray_angle = math.radians(40)
        
        for i in range(spray_count):
            angle = base_angle - spray_angle/2 + (spray_angle * i / (spray_count - 1))
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            # Réduction de dégâts pour les projectiles extérieurs
            outer_factor = 1.0 - abs(i - (spray_count-1)/2) / (spray_count/2) * 0.5
            projectile_damage = damage * (0.5 + 0.5 * outer_factor)
            
            projectiles.append(Projectile(
                x, y, dx, dy, projectile_damage,
                settings=settings,
                color=color,
                radius=3
            ))
    
    @staticmethod
    def _pattern_burst(x: float, y: float, damage: float, speed: float,
                      color: Tuple[int, int, int], time: float,
                      projectiles: List[Projectile], settings: Any) -> None:
        """Burst concentrique avec vagues"""
        for wave in range(1, 4):
            wave_projectiles = 6 * wave
            wave_speed = speed * (0.4 + wave * 0.3)
            wave_damage = damage * (0.3 + wave * 0.2)
            
            for i in range(wave_projectiles):
                angle = (2 * math.pi * i / wave_projectiles) + time * 0.5
                dx = math.cos(angle) * wave_speed
                dy = math.sin(angle) * wave_speed
                
                projectiles.append(Projectile(
                    x, y, dx, dy, wave_damage,
                    settings=settings,
                    color=color,
                    radius=1 + wave
                ))
    
    @staticmethod
    def _pattern_spiral(x: float, y: float, damage: float, speed: float,
                       color: Tuple[int, int, int], time: float, phase: int,
                       projectiles: List[Projectile], settings: Any) -> None:
        """Spirale tournante"""
        spiral_count = 12 + phase * 3
        spiral_tightness = 0.3 + phase * 0.1
        
        for i in range(spiral_count):
            angle = (2 * math.pi * i / spiral_count) + time * spiral_tightness
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            # Décalage radial
            radius = i * 2
            offset_x = math.cos(angle + math.pi/2) * radius
            offset_y = math.sin(angle + math.pi/2) * radius
            
            projectiles.append(Projectile(
                x + offset_x, y + offset_y, dx, dy, damage * 0.7,
                settings=settings,
                color=color,
                radius=2
            ))
    
    @staticmethod
    def _pattern_sine_wave(x: float, y: float, base_angle: float, damage: float, speed: float,
                          color: Tuple[int, int, int], time: float,
                          projectiles: List[Projectile], settings: Any) -> None:
        """Vague sinusoïdale de projectiles"""
        wave_count = 15
        wavelength = math.radians(180)
        amplitude = 30
        
        for i in range(wave_count):
            pos_along_wave = (i - wave_count/2) / (wave_count/2)
            wave_offset = math.sin(time * 2 + pos_along_wave * math.pi) * amplitude
            
            dx = math.cos(base_angle) * speed
            dy = math.sin(base_angle) * speed
            
            perp_angle = base_angle + math.pi/2
            offset_x = math.cos(perp_angle) * wave_offset
            offset_y = math.sin(perp_angle) * wave_offset
            
            projectiles.append(Projectile(
                x + offset_x, y + offset_y, dx, dy, damage * 0.8,
                settings=settings,
                color=color,
                radius=3
            ))
    
    @staticmethod
    def _pattern_vortex(x: float, y: float, damage: float, speed: float,
                       color: Tuple[int, int, int], time: float,
                       projectiles: List[Projectile], settings: Any) -> None:
        """Vortex tourbillonnant"""
        vortex_count = 16
        vortex_strength = 2.0
        
        for i in range(vortex_count):
            angle = (2 * math.pi * i / vortex_count) + time
            radius = 20 + i * 3
            
            # Vitesse tangentielle + radiale
            tangent_speed = vortex_strength * (1.0 - i/vortex_count)
            radial_speed = -0.5  # Vers l'intérieur
            
            tangent_angle = angle + math.pi/2
            radial_angle = angle
            
            dx = (math.cos(tangent_angle) * tangent_speed + 
                  math.cos(radial_angle) * radial_speed) * speed
            dy = (math.sin(tangent_angle) * tangent_speed + 
                  math.sin(radial_angle) * radial_speed) * speed
            
            start_x = x + math.cos(angle) * radius
            start_y = y + math.sin(angle) * radius
            
            projectiles.append(Projectile(
                start_x, start_y, dx, dy, damage * 0.6,
                settings=settings,
                color=color,
                radius=2
            ))
    
    @staticmethod
    def _pattern_cross(x: float, y: float, damage: float, speed: float,
                      color: Tuple[int, int, int], projectiles: List[Projectile], 
                      settings: Any) -> None:
        """Croix de projectiles"""
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  # Cardinal
            (0.707, 0.707), (0.707, -0.707), (-0.707, 0.707), (-0.707, -0.707)  # Diagonal
        ]
        
        for dx_norm, dy_norm in directions:
            dx = dx_norm * speed
            dy = dy_norm * speed
            
            projectiles.append(Projectile(
                x, y, dx, dy, damage,
                settings=settings,
                color=color,
                radius=4
            ))
    
    @staticmethod
    def _pattern_pentagram(x: float, y: float, damage: float, speed: float,
                          color: Tuple[int, int, int], time: float,
                          projectiles: List[Projectile], settings: Any) -> None:
        """Motif pentagramme"""
        # Angles pour un pentagramme (étoile à 5 branches)
        pentagram_angles = [0, 144, 288, 72, 216]  # En degrés
        
        for i, angle_deg in enumerate(pentagram_angles):
            angle = math.radians(angle_deg + time * 20)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            # Légère variation de couleur
            color_variation = (
                min(255, color[0] + i * 10),
                min(255, color[1] + i * 15),
                min(255, color[2] + i * 5)
            )
            
            projectiles.append(Projectile(
                x, y, dx, dy, damage * 0.9,
                settings=settings,
                color=color_variation,
                radius=3
            ))


class AdaptiveBoss(Enemy):
    """
    Boss adaptatif avec comportement récursif amélioré.
    Version plus difficile avec IA adaptative avancée.
    """
    
    # Cache pour les patterns générés
    _pattern_cache = {}
    
    def __init__(self, x: float, y: float, settings: Any, 
                 floor_number: int, global_seed: int):
        """
        Initialise un boss unique avec difficulté adaptative.
        
        Args:
            x, y: Position initiale
            settings: Paramètres du jeu
            floor_number: Numéro de l'étage (détermine difficulté)
            global_seed: Graine pour la génération aléatoire
        """
        super().__init__(x, y, settings)
        
        # Seed unique déterminée par position et étage
        self.boss_seed = self._generate_boss_seed(x, y, floor_number, global_seed)
        random.seed(self.boss_seed)
        
        # Identification
        self.type = "boss"
        self.name = self._generate_boss_name(floor_number)
        
        # Statistiques adaptatives à l'étage
        self.floor_number = floor_number
        self._init_stats(floor_number)
        
        # Système de phases dynamique
        self._init_phase_system(floor_number)
        
        # Système de patterns récursifs
        self._init_pattern_system(floor_number)
        
        # IA adaptative améliorée
        self._init_ai_system(floor_number)
        
        # Effets visuels
        self._init_visual_effects()
        
        # Log de création
        print(f"[BOSS] {self.name} créé - Étage {floor_number}, "
              f"PV: {self.health}, Phases: {self.phase_depth}")
    
    def _generate_boss_seed(self, x: float, y: float, floor_number: int, 
                           global_seed: int) -> int:
        """Génère une seed unique pour ce boss"""
        return hash((global_seed, floor_number, int(x), int(y))) % (2**32)
    
    def _generate_boss_name(self, floor_number: int) -> str:
        """Génère un nom unique basé sur l'étage et la seed"""
        names = ["Abyssal", "Chaotic", "Void", "Eternal", "Corrupted", 
                "Fractal", "Quantum", "Recursive", "Adaptive", "Evolutionary"]
        suffixes = ["Titan", "Behemoth", "Leviathan", "Colossus", "Monarch",
                   "Overlord", "Dominator", "Annihilator", "Obliterator"]
        
        name_idx = (self.boss_seed // 1000) % len(names)
        suffix_idx = (self.boss_seed // 100) % len(suffixes)
        
        return f"{names[name_idx]} {suffixes[suffix_idx]}"
    
    def _init_stats(self, floor_number: int) -> None:
        """Initialise les statistiques du boss avec scaling exponentiel"""
        # Facteur de difficulté exponentiel
        difficulty = 1.0 + (floor_number - 1) * 0.3
        
        self.health = int(400 * difficulty)
        self.max_health = self.health
        self.damage = int(15 * difficulty)
        self.speed = 1.0 + (floor_number * 0.08)
        self.radius = 30 + min(floor_number * 2, 20)
        
        # Réduction de dégâts de base
        self.base_defense = 0.8 - min(0.3, floor_number * 0.02)
        
        # Cooldowns adaptatifs
        self.base_attack_cooldown = max(40, 120 - floor_number * 5)
    
    def _init_phase_system(self, floor_number: int) -> None:
        """Initialise le système de phases"""
        # Plus de phases pour les étages élevés
        self.phase_depth = min(5, max(1, (floor_number + 1) // 2))
        self.current_phase = 1
        
        # Seuils de vie pour les phases (progression non linéaire)
        self.phase_thresholds = []
        for i in range(self.phase_depth, 0, -1):
            # Seuils plus serrés pour les dernières phases
            threshold = (i / self.phase_depth) ** 1.5
            self.phase_thresholds.append(threshold)
        
        # Multiplicateurs adaptatifs par phase
        self.phase_multipliers = {
            'damage': 1.0,
            'speed': 1.0,
            'attack_rate': 1.0,
            'defense': 1.0,
            'pattern_complexity': 1.0
        }
        
        # Timer de phase
        self.phase_timer = 0
        self.phase_duration = 600  # 10 secondes à 60 FPS
    
    def _init_pattern_system(self, floor_number: int) -> None:
        """Initialise le système de patterns récursifs"""
        # Complexité de base augmentée avec l'étage
        base_complexity = min(2.0, 0.5 + floor_number * 0.15)
        
        # Génération du pattern racine
        cache_key = (self.boss_seed, floor_number, base_complexity)
        if cache_key not in AdaptiveBoss._pattern_cache:
            max_depth = min(5, 2 + floor_number // 3)
            
            AdaptiveBoss._pattern_cache[cache_key] = (
                RecursivePatternGenerator.generate_fractal_pattern(
                    seed=self.boss_seed,
                    depth=0,
                    max_depth=max_depth,
                    complexity=base_complexity
                )
            )
        
        self.root_pattern = AdaptiveBoss._pattern_cache[cache_key]
        self.active_pattern = None
        self.pattern_cooldown = 0
        self.pattern_duration = 0
        
        # Historique des patterns utilisés
        self.pattern_history = []
        self.max_pattern_history = 8
    
    def _init_ai_system(self, floor_number: int) -> None:
        """Initialise le système d'IA adaptative"""
        # Historique des distances au joueur
        self.player_distance_history = []
        self.max_history_size = 30
        
        # Distance optimale (augmente avec l'étage)
        self.preferred_distance = 250 + floor_number * 15
        
        # Comportement adaptatif
        self.aggressiveness = 0.5 + min(0.5, floor_number * 0.05)
        self.evasiveness = 0.3 + min(0.7, floor_number * 0.07)
        
        # Temps depuis dernière action
        self.time_since_last_action = 0
        self.action_cooldown = 0
        
        # Mode spécial (rage, défensif, etc.)
        self.special_mode = None
        self.special_mode_timer = 0
    
    def _init_visual_effects(self) -> None:
        """Initialise les effets visuels"""
        # Animation de pulsation
        self.pulse_timer = 0
        self.pulse_speed = 0.07
        
        # Rotation
        self.rotation_angle = 0
        self.rotation_speed = 0.02
        
        # Effets spéciaux
        self.special_effects = []
        
        # Couleurs
        self.primary_color = self._generate_primary_color()
        self.secondary_color = self._generate_secondary_color()
        self.phase_colors = self._generate_phase_colors()
    
    def _generate_primary_color(self) -> Tuple[int, int, int]:
        """Génère la couleur principale du boss"""
        hue = (self.boss_seed % 360)
        return RecursivePatternGenerator.hsv_to_rgb(hue, 0.8, 0.9)
    
    def _generate_secondary_color(self) -> Tuple[int, int, int]:
        """Génère la couleur secondaire (complémentaire)"""
        hue = (self.boss_seed + 180) % 360
        return RecursivePatternGenerator.hsv_to_rgb(hue, 0.7, 0.8)
    
    def _generate_phase_colors(self) -> List[Tuple[int, int, int]]:
        """Génère des couleurs pour chaque phase"""
        colors = []
        for i in range(self.phase_depth):
            hue = (self.boss_seed + i * 60) % 360
            saturation = 0.6 + i * 0.1
            value = 0.8 - i * 0.1
            colors.append(RecursivePatternGenerator.hsv_to_rgb(hue, saturation, value))
        return colors
    
    def update(self, player, enemy_projectiles=None):
        """
        Met à jour le boss avec IA adaptative améliorée.
        
        Args:
            player: Instance du joueur
            enemy_projectiles: Liste des projectiles ennemis (à remplir)
        """
        # Mise à jour des timers
        self._update_timers()
        
        # Vérification des transitions de phase
        self._check_phase_transition()
        
        # Mise à jour de l'IA adaptative
        self._update_adaptive_behavior(player)
        
        # Mouvement intelligent
        self._intelligent_movement(player)
        
        # Gestion des attaques
        self._manage_attacks(player, enemy_projectiles)
        
        # Mise à jour des effets
        self._update_effects()
        
        # Contraintes d'écran
        self._constrain_to_screen()
    
    def _update_timers(self) -> None:
        """Met à jour tous les timers"""
        self.pulse_timer += self.pulse_speed
        self.rotation_angle += self.rotation_speed
        self.phase_timer += 1
        self.time_since_last_action += 1
        
        if self.pattern_cooldown > 0:
            self.pattern_cooldown -= 1
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
        if self.special_mode_timer > 0:
            self.special_mode_timer -= 1
            if self.special_mode_timer <= 0:
                self.special_mode = None
    
    def _check_phase_transition(self) -> None:
        """Vérifie et gère les transitions de phase"""
        health_ratio = self.health / self.max_health
        
        for i, threshold in enumerate(self.phase_thresholds):
            target_phase = self.phase_depth - i
            if health_ratio <= threshold and self.current_phase < target_phase:
                self._transition_to_phase(target_phase)
                break
    
    def _transition_to_phase(self, new_phase: int) -> None:
        """Transition vers une nouvelle phase"""
        old_phase = self.current_phase
        self.current_phase = new_phase
        
        # Augmentation des multiplicateurs
        phase_increase = 1.0 + (new_phase - old_phase) * 0.3
        self.phase_multipliers['damage'] *= phase_increase
        self.phase_multipliers['attack_rate'] *= phase_increase
        self.phase_multipliers['defense'] *= phase_increase * 0.9
        self.phase_multipliers['pattern_complexity'] *= phase_increase * 1.1
        
        # Effet visuel
        self._add_phase_transition_effect()
        
        # Réinitialisation des patterns
        self.active_pattern = None
        self.pattern_history.clear()
        
        # Log
        print(f"[BOSS] {self.name} passe en phase {new_phase}/{self.phase_depth}")
    
    def _add_phase_transition_effect(self) -> None:
        """Ajoute un effet visuel de transition de phase"""
        self.special_effects.append({
            'type': 'phase_transition',
            'timer': 90,
            'radius': self.radius * 2.5,
            'color': self.phase_colors[self.current_phase - 1],
            'intensity': 1.0,
            'pulse_speed': 0.2
        })
    
    def _update_adaptive_behavior(self, player) -> None:
        """Met à jour le comportement adaptatif basé sur le joueur"""
        # Mise à jour de l'historique de distance
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        self.player_distance_history.append(distance)
        if len(self.player_distance_history) > self.max_history_size:
            self.player_distance_history.pop(0)
        
        # Adaptation de la distance préférée
        if len(self.player_distance_history) >= 10:
            avg_distance = sum(self.player_distance_history[-10:]) / 10
            
            if avg_distance > self.preferred_distance * 1.8:
                self.preferred_distance *= 0.97
            elif avg_distance < self.preferred_distance * 0.4:
                self.preferred_distance *= 1.03
        
        # Adaptation basée sur la vitesse du joueur
        player_speed = math.sqrt(player.last_dx**2 + player.last_dy**2)
        
        if player_speed > 4.0 and self.time_since_last_action > 60:
            # Joueur rapide : augmente l'agressivité
            self.aggressiveness = min(1.0, self.aggressiveness * 1.02)
            self.evasiveness = max(0.1, self.evasiveness * 0.98)
        elif player_speed < 1.0 and self.time_since_last_action > 60:
            # Joueur immobile : augmente la précision
            self.evasiveness = min(0.9, self.evasiveness * 1.03)
        
        # Mode spécial basé sur la santé
        if self.health < self.max_health * 0.3 and self.special_mode != 'rage':
            self._enter_rage_mode()
    
    def _enter_rage_mode(self) -> None:
        """Active le mode rage en basse vie"""
        self.special_mode = 'rage'
        self.special_mode_timer = 300  # 5 secondes
        
        # Boost significatif
        self.phase_multipliers['damage'] *= 1.5
        self.phase_multipliers['attack_rate'] *= 1.8
        self.phase_multipliers['speed'] *= 1.3
        
        # Effet visuel
        self.special_effects.append({
            'type': 'rage',
            'timer': 300,
            'color': (255, 50, 50),
            'intensity': 0.8
        })
        
        print(f"[BOSS] {self.name} entre en mode rage!")
    
    def _intelligent_movement(self, player) -> None:
        """Mouvement intelligent basé sur l'IA"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Calcul du mouvement idéal
        target_ratio = distance / self.preferred_distance
        
        # Comportement selon la distance
        if target_ratio > 1.5:
            # Trop loin : approche rapide
            move_speed = self.speed * self.phase_multipliers['speed'] * 1.2
            self.x += (dx / distance) * move_speed
            self.y += (dy / distance) * move_speed
        elif target_ratio < 0.6:
            # Trop proche : recule
            move_speed = self.speed * self.phase_multipliers['speed'] * 0.9
            self.x -= (dx / distance) * move_speed
            self.y -= (dy / distance) * move_speed
        else:
            # Distance optimale : mouvement orbital
            orbit_angle = self.rotation_angle * 2
            orbit_radius = self.preferred_distance * 0.3
            target_x = player.x + math.cos(orbit_angle) * orbit_radius
            target_y = player.y + math.sin(orbit_angle) * orbit_radius
            
            # Approche douce de la position orbitale
            move_x = target_x - self.x
            move_y = target_y - self.y
            move_dist = max(math.sqrt(move_x*move_x + move_y*move_y), 0.1)
            
            move_speed = self.speed * self.phase_multipliers['speed'] * 0.7
            self.x += (move_x / move_dist) * move_speed
            self.y += (move_y / move_dist) * move_speed
        
        # Évasion aléatoire occasionnelle
        if random.random() < 0.01 * self.evasiveness:
            dodge_angle = random.random() * 2 * math.pi
            dodge_distance = 30 + random.random() * 20
            self.x += math.cos(dodge_angle) * dodge_distance
            self.y += math.sin(dodge_angle) * dodge_distance
    
    def _manage_attacks(self, player, enemy_projectiles) -> None:
        """Gère les attaques du boss"""
        if enemy_projectiles is None:
            return
            
        # Vérifie si une attaque est en cours
        if self.pattern_cooldown > 0:
            return
        
        # Sélectionne un nouveau pattern si nécessaire
        if self.active_pattern is None:
            self._select_attack_pattern()
        
        # Exécute l'attaque
        if self.active_pattern and self.pattern_cooldown <= 0:
            self._execute_attack(player, enemy_projectiles)
    
    def _select_attack_pattern(self) -> None:
        """Sélectionne un pattern d'attaque adaptatif"""
        # Choix intelligent basé sur l'historique
        available_patterns = self._get_available_patterns(self.root_pattern, self.current_phase)
        
        if not available_patterns:
            self.active_pattern = self.root_pattern
        else:
            # Évite les patterns récemment utilisés
            recent_patterns = self.pattern_history[-3:] if len(self.pattern_history) >= 3 else []
            
            # Poids basé sur la rareté d'utilisation
            weights = []
            for pattern in available_patterns:
                pattern_id = self._get_pattern_id(pattern)
                recent_use = self.pattern_history.count(pattern_id)
                weight = 1.0 / (1.0 + recent_use * 2)
                weights.append(weight)
            
            # Sélection pondérée
            if sum(weights) > 0:
                self.active_pattern = random.choices(available_patterns, weights=weights, k=1)[0]
            else:
                self.active_pattern = random.choice(available_patterns)
            
            # Enregistre dans l'historique
            pattern_id = self._get_pattern_id(self.active_pattern)
            self.pattern_history.append(pattern_id)
            if len(self.pattern_history) > self.max_pattern_history:
                self.pattern_history.pop(0)
        
        # Définit la durée du pattern
        self.pattern_duration = 45 + self.current_phase * 15
    
    def _get_available_patterns(self, pattern: Dict[str, Any], 
                               target_depth: int = 0) -> List[Dict[str, Any]]:
        """
        Récupère récursivement les patterns disponibles à une certaine profondeur.
        
        Args:
            pattern: Pattern à explorer
            target_depth: Profondeur cible
            
        Returns:
            Liste des patterns à la profondeur cible
        """
        if pattern.get('depth', 0) == target_depth:
            return [pattern]
        
        if pattern['type'] == 'node':
            available = []
            for branch in pattern['branches']:
                available.extend(self._get_available_patterns(branch, target_depth))
            return available
        
        return []
    
    def _get_pattern_id(self, pattern: Dict[str, Any]) -> str:
        """Génère un identifiant unique pour un pattern"""
        if pattern['type'] == 'leaf':
            return f"leaf_{pattern['pattern_type']}_{pattern['depth']}"
        else:
            return f"node_{pattern['node_type']}_{pattern['depth']}"
    
    def _execute_attack(self, player, enemy_projectiles: List[Projectile]) -> None:
        """Exécute l'attaque actuelle"""
        # Joue le son d'attaque
        self.settings.sounds["Tire_4"].play()
        
        # Exécute le pattern récursif
        RecursivePatternGenerator.execute_pattern_recursive(
            position=(self.x, self.y),
            pattern=self.active_pattern,
            projectiles=enemy_projectiles,
            player_pos=(player.x, player.y),
            damage_base=self.damage * self.phase_multipliers['damage'],
            speed_base=3.0 + self.current_phase * 0.8,
            phase=self.current_phase,
            current_time=pygame.time.get_ticks() * 0.001,
            settings=self.settings
        )
        
        # Réinitialise le cooldown
        cooldown_reduction = self.phase_multipliers['attack_rate']
        self.pattern_cooldown = max(15, int(self.base_attack_cooldown / cooldown_reduction))
        
        # Réduit la durée du pattern
        self.pattern_duration -= 1
        if self.pattern_duration <= 0:
            self.active_pattern = None
    
    def _update_effects(self) -> None:
        """Met à jour les effets spéciaux"""
        for effect in self.special_effects[:]:
            effect['timer'] -= 1
            
            # Animation spécifique selon le type
            if effect['type'] == 'phase_transition':
                effect['intensity'] *= 0.97
                effect['radius'] += effect.get('pulse_speed', 0.5)
            
            elif effect['type'] == 'rage':
                # Clignotement rouge
                effect['intensity'] = 0.5 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
            
            # Supprime l'effet terminé
            if effect['timer'] <= 0:
                self.special_effects.remove(effect)
    
    def _constrain_to_screen(self) -> None:
        """Maintient le boss dans les limites de l'écran"""
        margin = self.radius + 60
        self.x = max(margin, min(self.x, self.settings.screen_width - margin))
        self.y = max(margin, min(self.y, self.settings.screen_height - margin))
    
    def take_damage(self, amount: float) -> bool:
        """
        Inflige des dégâts au boss avec adaptation défensive.
        
        Args:
            amount: Montant de dégâts bruts
            
        Returns:
            True si le boss est mort, False sinon
        """
        # Réduction de dégâts adaptative
        defense_multiplier = self.base_defense * self.phase_multipliers['defense']
        
        # Réduction supplémentaire en mode rage
        if self.special_mode == 'rage':
            defense_multiplier *= 0.7
        
        # Réduction en phase finale
        if self.current_phase == self.phase_depth:
            defense_multiplier *= 0.85
        
        # Applique la réduction
        actual_damage = amount * defense_multiplier
        
        # Adaptation après des dégâts importants
        if actual_damage > self.max_health * 0.08:
            # Augmente l'évasion
            self.evasiveness = min(0.9, self.evasiveness * 1.1)
            
            # Effet visuel
            self._add_damage_flash_effect()
        
        # Applique les dégâts
        self.health -= actual_damage
        
        # Vérifie la mort
        if self.health <= 0:
            return True
        
        return False
    
    def _add_damage_flash_effect(self) -> None:
        """Ajoute un effet visuel de dégâts"""
        self.special_effects.append({
            'type': 'damage_flash',
            'timer': 20,
            'color': (255, 100, 100),
            'intensity': 1.0
        })
    
    def draw(self, screen):
        """Dessine le boss avec effets visuels améliorés"""
        current_time = pygame.time.get_ticks() * 0.001
        
        # Effets spéciaux en arrière-plan
        self._draw_special_effects(screen, current_time)
        
        # Corps principal avec effets
        self._draw_main_body(screen, current_time)
        
        # Indicateurs de phase
        self._draw_phase_indicators(screen, current_time)
        
        # Interface (nom, phase, santé)
        self._draw_boss_ui(screen)
        
        # Barre de santé avancée
        self._draw_health_bar(screen)
    
    def _draw_special_effects(self, screen, current_time: float) -> None:
        """Dessine les effets spéciaux"""
        for effect in self.special_effects:
            if effect['type'] == 'phase_transition':
                self._draw_phase_transition_effect(screen, effect, current_time)
            elif effect['type'] == 'damage_flash':
                self._draw_damage_flash_effect(screen, effect)
            elif effect['type'] == 'rage':
                self._draw_rage_effect(screen, effect, current_time)
    
    def _draw_phase_transition_effect(self, screen, effect: Dict[str, Any], 
                                     current_time: float) -> None:
        """Dessine l'effet de transition de phase"""
        alpha = int(180 * effect['intensity'] * (effect['timer'] / 90))
        pulse = math.sin(current_time * 8) * 8 * effect['intensity']
        
        effect_surface = pygame.Surface(
            (int(effect['radius']*2), int(effect['radius']*2)), 
            pygame.SRCALPHA
        )
        
        # Cercle externe
        pygame.draw.circle(
            effect_surface, 
            (*effect['color'], alpha),
            (int(effect['radius']), int(effect['radius'])),
            int(effect['radius'] + pulse),
            4
        )
        
        # Cercle interne
        inner_alpha = int(alpha * 0.6)
        inner_radius = effect['radius'] * 0.7
        pygame.draw.circle(
            effect_surface,
            (255, 255, 255, inner_alpha),
            (int(effect['radius']), int(effect['radius'])),
            int(inner_radius + pulse * 0.5),
            2
        )
        
        screen.blit(effect_surface, 
                   (int(self.x - effect['radius']), 
                    int(self.y - effect['radius'])))
    
    def _draw_damage_flash_effect(self, screen, effect: Dict[str, Any]) -> None:
        """Dessine l'effet de flash de dégâts"""
        alpha = int(120 * effect['intensity'] * (effect['timer'] / 20))
        flash_radius = self.radius * 1.8
        
        flash_surface = pygame.Surface(
            (int(flash_radius*2), int(flash_radius*2)), 
            pygame.SRCALPHA
        )
        
        # Flash radial
        for i in range(3):
            radius = flash_radius * (0.7 + i * 0.15)
            ring_alpha = int(alpha * (0.8 - i * 0.2))
            pygame.draw.circle(
                flash_surface,
                (*effect['color'], ring_alpha),
                (int(flash_radius), int(flash_radius)),
                int(radius),
                3 - i
            )
        
        screen.blit(flash_surface,
                   (int(self.x - flash_radius),
                    int(self.y - flash_radius)))
    
    def _draw_rage_effect(self, screen, effect: Dict[str, Any], 
                         current_time: float) -> None:
        """Dessine l'effet de rage"""
        # Aura rouge pulsante
        pulse = math.sin(current_time * 10) * 15
        aura_radius = self.radius * 1.5 + pulse
        
        for i in range(3):
            alpha = int(80 * effect['intensity'] * (1.0 - i * 0.3))
            radius = aura_radius - i * 8
            
            aura_surface = pygame.Surface(
                (int(radius*2), int(radius*2)), 
                pygame.SRCALPHA
            )
            
            pygame.draw.circle(
                aura_surface,
                (*effect['color'], alpha),
                (int(radius), int(radius)),
                int(radius),
                2
            )
            
            screen.blit(aura_surface,
                       (int(self.x - radius),
                        int(self.y - radius)))
    
    def _draw_main_body(self, screen, current_time: float) -> None:
        """Dessine le corps principal du boss"""
        # Pulsation de base
        pulse = math.sin(self.pulse_timer) * 4
        main_radius = self.radius + pulse
        
        # Gradient radial amélioré
        for layer in range(6, 0, -1):
            ratio = layer / 6
            radius = main_radius * ratio
            
            # Couleur avec variation
            color_variation = (
                int(self.primary_color[0] * ratio * (0.8 + 0.2 * math.sin(current_time + layer))),
                int(self.primary_color[1] * ratio * (0.8 + 0.2 * math.sin(current_time * 1.3 + layer))),
                int(self.primary_color[2] * ratio * (0.8 + 0.2 * math.sin(current_time * 1.7 + layer)))
            )
            
            alpha = 40 + layer * 35
            
            # Crée la surface du gradient
            surf = pygame.Surface((int(radius*2), int(radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color_variation, alpha), 
                             (int(radius), int(radius)), int(radius))
            
            screen.blit(surf, (int(self.x - radius), int(self.y - radius)))
        
        # Noyau central
        core_radius = main_radius * 0.4
        core_pulse = math.sin(current_time * 3) * 2
        pygame.draw.circle(
            screen, self.secondary_color,
            (int(self.x), int(self.y)),
            int(core_radius + core_pulse)
        )
        
        # Contour énergétique
        contour_width = 2 + math.sin(current_time * 2) * 1
        pygame.draw.circle(
            screen, (255, 255, 255, 180),
            (int(self.x), int(self.y)),
            int(main_radius + 3),
            int(contour_width)
        )
    
    def _draw_phase_indicators(self, screen, current_time: float) -> None:
        """Dessine les indicateurs de phase"""
        phase_radius = self.radius * 0.9
        
        for phase in range(self.current_phase):
            # Position de l'indicateur
            angle = (2 * math.pi * phase / self.current_phase) + self.rotation_angle
            indicator_x = self.x + math.cos(angle) * phase_radius
            indicator_y = self.y + math.sin(angle) * phase_radius
            
            # Animation
            pulse = math.sin(current_time * 4 + phase) * 3
            size = self.radius * 0.12 + pulse
            
            # Couleur de la phase
            phase_color = self.phase_colors[phase]
            
            # Indicateur de phase
            pygame.draw.circle(
                screen, phase_color,
                (int(indicator_x), int(indicator_y)),
                int(size)
            )
            
            # Contour
            pygame.draw.circle(
                screen, (255, 255, 255, 200),
                (int(indicator_x), int(indicator_y)),
                int(size),
                1
            )
    
    def _draw_boss_ui(self, screen) -> None:
        """Dessine l'interface du boss (nom, phase)"""
        if not hasattr(self.settings, 'font') or not self.settings.font:
            return
            
        # Nom du boss
        name_text = self.settings.font["h3"].render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 40))
        screen.blit(name_text, name_rect)
        
        # Phase actuelle
        phase_color = self.phase_colors[self.current_phase - 1]
        phase_text = self.settings.font["h4"].render(
            f"Phase {self.current_phase}/{self.phase_depth}", 
            True, phase_color
        )
        phase_rect = phase_text.get_rect(center=(self.x, self.y - self.radius - 20))
        screen.blit(phase_text, phase_rect)
        
        # Indicateur de difficulté
        stars = "★" * self.current_phase + "☆" * (self.phase_depth - self.current_phase)
        diff_color = (255, 200, 0) if self.current_phase >= self.phase_depth else (200, 200, 200)
        diff_text = self.settings.font["h4"].render(stars, True, diff_color)
        diff_rect = diff_text.get_rect(center=(self.x, self.y - self.radius - 60))
        screen.blit(diff_text, diff_rect)
        
        # Indicateur de mode spécial
        if self.special_mode == 'rage':
            rage_text = self.settings.font["h4"].render("RAGE", True, (255, 50, 50))
            rage_rect = rage_text.get_rect(center=(self.x, self.y - self.radius - 80))
            screen.blit(rage_text, rage_rect)
    
    def _draw_health_bar(self, screen, width: int = 220, height: int = 14) -> None:
        """Dessine la barre de santé avancée"""
        # Position
        bar_x = self.x - width // 2
        bar_y = self.y - self.radius - 100
        
        # Fond
        pygame.draw.rect(screen, (20, 20, 20), 
                        (bar_x, bar_y, width, height), 
                        border_radius=4)
        
        # Santé actuelle
        health_ratio = max(0, self.health / self.max_health)
        health_width = int(width * health_ratio)
        
        if health_width > 0:
            # Crée une surface pour le gradient de santé
            health_surface = pygame.Surface((health_width, height), pygame.SRCALPHA)
            
            # Gradient selon la santé
            for pixel in range(health_width):
                pos_ratio = pixel / width
                
                if health_ratio > 0.7:
                    # Vert → Jaune
                    r = int(255 * (1 - pos_ratio * 0.5))
                    g = 255
                    b = int(100 * (1 - pos_ratio * 0.3))
                elif health_ratio > 0.4:
                    # Jaune → Orange
                    r = 255
                    g = int(255 * (0.8 - pos_ratio * 0.4))
                    b = 50
                else:
                    # Orange → Rouge
                    r = 255
                    g = int(150 * (1 - pos_ratio))
                    b = int(50 * (1 - pos_ratio))
                
                # Effet de brillance
                if pixel % 3 == 0:
                    highlight = 20
                    r = min(255, r + highlight)
                    g = min(255, g + highlight)
                    b = min(255, b + highlight)
                
                pygame.draw.line(health_surface, (r, g, b, 220), 
                               (pixel, 0), (pixel, height))
            
            screen.blit(health_surface, (bar_x, bar_y))
        
        # Marqueurs de phase
        for phase in range(1, self.phase_depth):
            marker_x = bar_x + int(width * (phase / self.phase_depth))
            
            # Couleur selon si la phase est passée
            if phase < self.current_phase:
                marker_color = (255, 255, 255, 180)
                marker_height = height + 6
            else:
                marker_color = (100, 100, 100, 100)
                marker_height = height + 4
            
            pygame.draw.line(screen, marker_color,
                           (marker_x, bar_y - 3),
                           (marker_x, bar_y + marker_height),
                           2)
        
        # Bordure
        border_color = (150, 150, 150) if health_ratio > 0.2 else (200, 100, 100)
        pygame.draw.rect(screen, border_color,
                        (bar_x, bar_y, width, height),
                        2, border_radius=4)
        
        # Texte de santé
        if hasattr(self.settings, 'font') and self.settings.font and 'h4' in self.settings.font:
            health_text = self.settings.font["h4"].render(
                f"{int(self.health)}/{self.max_health}", 
                True, (255, 255, 255)
            )
            health_rect = health_text.get_rect(center=(self.x, bar_y - 18))
            
            # Fond pour le texte
            text_bg = pygame.Surface((health_rect.width + 10, health_rect.height + 4), 
                                    pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 150))
            screen.blit(text_bg, (health_rect.x - 5, health_rect.y - 2))
            
            screen.blit(health_text, health_rect)
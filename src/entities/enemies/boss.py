# src/entities/enemies/boss.py
import pygame
import math
import random
from .enemy import Enemy
from ..projectiles import Projectile

class BossGenerator:
    """
    Générateur procédural de boss basé sur des mécaniques modulaires
    """
    
    # Mécaniques disponibles classées par difficulté
    ATTACK_PATTERNS = {
        "simple_circle": {"min_level": 1, "weight": 10},
        "double_spiral": {"min_level": 2, "weight": 8},
        "recursive_fractal": {"min_level": 3, "weight": 6},
        "homing_missiles": {"min_level": 4, "weight": 5},
        "time_delayed": {"min_level": 5, "weight": 4},
        "rotating_barrage": {"min_level": 6, "weight": 3},
    }
    
    MOVEMENT_PATTERNS = {
        "stationary": {"min_level": 1, "weight": 5},
        "linear_pursuit": {"min_level": 2, "weight": 8},
        "circular_orbit": {"min_level": 3, "weight": 7},
        "teleport_dodge": {"min_level": 4, "weight": 6},
        "phase_shift": {"min_level": 5, "weight": 4},
        "predictive_movement": {"min_level": 6, "weight": 3},
    }
    
    SPECIAL_EFFECTS = {
        "shield_phases": {"min_level": 2, "weight": 7},
        "summon_minions": {"min_level": 3, "weight": 6},
        "damage_auras": {"min_level": 4, "weight": 5},
        "debuff_projectiles": {"min_level": 5, "weight": 4},
        "arena_hazards": {"min_level": 6, "weight": 3},
    }
    
    BEHAVIOR_MODIFIERS = {
        "phase_transitions": {"min_level": 3, "weight": 6},
        "enrage_timer": {"min_level": 4, "weight": 5},
        "adaptive_difficulty": {"min_level": 5, "weight": 4},
        "combo_attacks": {"min_level": 6, "weight": 3},
    }
    
    @classmethod
    def generate_boss_specs(cls, floor_number, global_seed):
        """
        Génère les spécifications d'un boss unique basées sur seed et étage
        
        Args:
            floor_number (int): Étage actuel (boss tous les 4 étages)
            global_seed (int): Seed unique par partie
            
        Returns:
            dict: Spécifications du boss
        """
        # Seed déterministe pour ce boss spécifique
        boss_level = max(1, (floor_number - 1) // 4)
        boss_seed = hash((global_seed, floor_number, boss_level)) % (2**32)
        random.seed(boss_seed)
        
        # Complexité augmentée avec le niveau
        base_complexity = 1 + (boss_level * 0.5)
        
        # Sélection des mécaniques pondérées par difficulté
        selected_attacks = cls._select_mechanics(
            cls.ATTACK_PATTERNS, 
            min(3, 1 + boss_level // 2),  # Nombre d'attaques
            boss_level
        )
        
        selected_movement = cls._select_mechanics(
            cls.MOVEMENT_PATTERNS,
            1 + (boss_level // 3),  # 1-3 patterns de mouvement
            boss_level
        )
        
        selected_effects = cls._select_mechanics(
            cls.SPECIAL_EFFECTS,
            min(2, boss_level // 2),  # 0-2 effets spéciaux
            boss_level
        )
        
        selected_behaviors = cls._select_mechanics(
            cls.BEHAVIOR_MODIFIERS,
            min(2, boss_level // 2),  # 0-2 comportements
            boss_level
        )
        
        # Génération du nom et apparence
        name = cls._generate_boss_name(boss_seed, selected_attacks, boss_level)
        color = cls._generate_boss_color(boss_seed, selected_attacks)
        
        return {
            "seed": boss_seed,
            "level": boss_level,
            "name": name,
            "color": color,
            "attacks": selected_attacks,
            "movement": selected_movement,
            "effects": selected_effects,
            "behaviors": selected_behaviors,
            "base_health": 500 + (boss_level * 150),
            "base_damage": 15 + (boss_level * 3),
            "complexity": base_complexity,
        }
    
    @classmethod
    def _select_mechanics(cls, mechanic_dict, count, boss_level):
        """Sélectionne N mécaniques disponibles pour ce niveau"""
        available = [
            name for name, specs in mechanic_dict.items()
            if specs["min_level"] <= boss_level
        ]
        
        if not available:
            return []
        
        # Pondération par poids et niveau
        weights = []
        for name in available:
            base_weight = mechanic_dict[name]["weight"]
            level_bonus = max(0, boss_level - mechanic_dict[name]["min_level"])
            weights.append(base_weight + (level_bonus * 2))
        
        # Sélection sans remise
        selected = []
        for _ in range(min(count, len(available))):
            if not available:
                break
                
            chosen = random.choices(available, weights=weights, k=1)[0]
            idx = available.index(chosen)
            selected.append(chosen)
            
            # Retirer pour éviter les doublons
            available.pop(idx)
            weights.pop(idx)
        
        return selected
    
    @classmethod
    def _generate_boss_name(cls, seed, attacks, level):
        """Génère un nom unique pour le boss"""
        random.seed(seed)
        
        prefixes = ["Garde", "Seigneur", "Maître", "Dévoreur", "Corrupteur", "Ancien"]
        suffixes = ["des Ombres", "du Néant", "Sanguinaire", "Implacable", "Chaotique", "Éternel"]
        
        attack_keywords = {
            "simple_circle": "Orbital",
            "double_spiral": "Spirale",
            "recursive_fractal": "Fractal",
            "homing_missiles": "Poursuite",
            "time_delayed": "Temporisé",
            "rotating_barrage": "Tournoyant",
        }
        
        if attacks and attacks[0] in attack_keywords:
            prefix = attack_keywords[attacks[0]]
        else:
            prefix = random.choice(prefixes)
        
        suffix = random.choice(suffixes)
        tier = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}.get(level, "")
        
        return f"{prefix} {suffix} {tier}".strip()
    
    @classmethod
    def _generate_boss_color(cls, seed, attacks):
        """Génère une couleur unique basée sur les attaques"""
        random.seed(seed)
        
        color_map = {
            "simple_circle": (100, 100, 255),    # Bleu
            "double_spiral": (255, 100, 100),    # Rouge
            "recursive_fractal": (100, 255, 100), # Vert
            "homing_missiles": (255, 255, 100),  # Jaune
            "time_delayed": (255, 100, 255),     # Magenta
            "rotating_barrage": (100, 255, 255), # Cyan
        }
        
        if attacks and attacks[0] in color_map:
            base_color = color_map[attacks[0]]
        else:
            base_color = (148, 0, 211)  # Violet par défaut
        
        # Variation aléatoire
        variation = random.randint(-20, 20)
        return (
            max(0, min(255, base_color[0] + variation)),
            max(0, min(255, base_color[1] + variation)),
            max(0, min(255, base_color[2] + variation)),
        )


class ProceduralBoss(Enemy):
    """
    Boss généré procéduralement avec mécaniques combinées
    """
    
    def __init__(self, x, y, settings, floor_number, global_seed):
        """
        Initialise un boss unique
        
        Args:
            x, y (int): Position
            settings (Settings): Configuration
            floor_number (int): Étage actuel
            global_seed (int): Seed unique pour la partie
        """
        super().__init__(x, y, settings)
        
        # Génération des spécifications
        self.specs = BossGenerator.generate_boss_specs(floor_number, global_seed)
        self.type = "boss"
        self.name = self.specs["name"]
        
        # Statistiques basées sur specs
        self.health = self.specs["base_health"]
        self.max_health = self.health
        self.damage = self.specs["base_damage"]
        self.color = self.specs["color"]
        self.radius = 35 + (self.specs["level"] * 5)
        
        # Vitesses
        self.speed = 1.2 + (self.specs["level"] * 0.1)
        self.projectile_speed = 4 + (self.specs["level"] * 0.5)
        
        # Système de phases
        self.phase = 1
        self.phases = self._determine_phases()
        self.phase_health_thresholds = self._calculate_phase_thresholds()
        
        # Timers et cooldowns
        self.attack_cooldown = 0
        self.phase_timer = 0
        self.enrage_timer = 3000  # 30 secondes à 100 FPS
        
        # État du boss
        self.active_effects = []
        self.summoned_minions = []
        self.shield_active = False
        self.shield_health = 0
        self.enraged = False
        
        # Seed locale pour la prédictibilité
        self.local_random = random.Random(self.specs["seed"])
        
        # Animation
        self.pulse_timer = 0
        self.special_effect_timer = 0
        
        # Initialiser les mécaniques sélectionnées
        self._initialize_mechanics()
    
    def _determine_phases(self):
        """Détermine le nombre de phases selon les mécaniques"""
        base_phases = 2  # Toujours au moins 2 phases
        
        if "phase_transitions" in self.specs["behaviors"]:
            base_phases += 1
        
        if self.specs["level"] >= 4:
            base_phases += 1
        
        return min(base_phases, 4)  # Max 4 phases
    
    def _calculate_phase_thresholds(self):
        """Calcule les seuils de vie pour chaque phase"""
        thresholds = []
        for i in range(self.phases, 0, -1):
            thresholds.append(i / self.phases)
        return thresholds
    
    def _initialize_mechanics(self):
        """Initialise toutes les mécaniques sélectionnées"""
        # Attaques
        self.attack_implementations = {}
        for attack in self.specs["attacks"]:
            if attack == "simple_circle":
                self.attack_implementations[attack] = self._simple_circle_attack
            elif attack == "double_spiral":
                self.attack_implementations[attack] = self._double_spiral_attack
            elif attack == "recursive_fractal":
                self.attack_implementations[attack] = self._recursive_fractal_attack
            elif attack == "homing_missiles":
                self.attack_implementations[attack] = self._homing_missiles_attack
            elif attack == "time_delayed":
                self.attack_implementations[attack] = self._time_delayed_attack
            elif attack == "rotating_barrage":
                self.attack_implementations[attack] = self._rotating_barrage_attack
        
        # Mouvements
        self.movement_implementation = self._get_movement_implementation(
            self.specs["movement"][0] if self.specs["movement"] else "stationary"
        )
        
        # Effets spéciaux
        self.effect_implementations = []
        for effect in self.specs["effects"]:
            if effect == "shield_phases":
                self.effect_implementations.append(self._shield_phases_effect)
            elif effect == "summon_minions":
                self.effect_implementations.append(self._summon_minions_effect)
            elif effect == "damage_auras":
                self.effect_implementations.append(self._damage_auras_effect)
            elif effect == "debuff_projectiles":
                self.effect_implementations.append(self._debuff_projectiles_effect)
            elif effect == "arena_hazards":
                self.effect_implementations.append(self._arena_hazards_effect)
    
    def _get_movement_implementation(self, movement_type):
        """Retourne la fonction de mouvement appropriée"""
        if movement_type == "stationary":
            return self._stationary_movement
        elif movement_type == "circular_orbit":
            return self._circular_orbit_movement
        elif movement_type == "teleport_dodge":
            return self._teleport_dodge_movement
        elif movement_type == "phase_shift":
            return self._phase_shift_movement
        elif movement_type == "predictive_movement":
            return self._predictive_movement
        else:  # "linear_pursuit" par défaut
            return self._linear_pursuit_movement
    
    def update(self, player, enemy_projectiles=None):
        """
        Met à jour le boss avec toutes ses mécaniques
        """
        # Incrémenter le timer de phase
        self.phase_timer += 1
        
        # Vérifier le changement de phase
        self._check_phase_transition()
        
        # Appliquer les effets spéciaux
        for effect_func in self.effect_implementations:
            effect_func(player)
        
        # Mouvement selon le pattern
        if self.movement_implementation:
            self.movement_implementation(player)
        
        # Gestion de l'enragement
        if "enrage_timer" in self.specs["behaviors"]:
            self._handle_enrage_timer()
        
        # Attaques
        if self.attack_cooldown <= 0:
            self._execute_selected_attack(enemy_projectiles)
            self.attack_cooldown = self._calculate_attack_cooldown()
        else:
            self.attack_cooldown -= 1
        
        # Animation
        self.pulse_timer += 0.05
        self.special_effect_timer += 1
        
        # Garder dans l'écran
        self._constrain_to_screen()
    
    def _check_phase_transition(self):
        """Vérifie et gère les transitions de phase"""
        health_ratio = self.health / self.max_health
        
        for i, threshold in enumerate(self.phase_health_thresholds):
            if health_ratio <= threshold and self.phase < (self.phases - i):
                self.phase = self.phases - i
                self._on_phase_transition()
                break
    
    def _on_phase_transition(self):
        """Déclenché lors d'un changement de phase"""
        # Augmentation des statistiques
        self.damage *= 1.3
        self.attack_cooldown = max(30, self.attack_cooldown * 0.7)
        
        # Activation de nouvelles mécaniques en phase finale
        if self.phase == self.phases:
            self._activate_final_phase_abilities()
        
        # Effet visuel de transition
        self.special_effect_timer = 0
    
    def _activate_final_phase_abilities(self):
        """Active les capacités de phase finale"""
        if "adaptive_difficulty" in self.specs["behaviors"]:
            # Le boss s'adapte au style du joueur
            pass
        
        if "combo_attacks" in self.specs["behaviors"]:
            # Combine plusieurs attaques
            pass
    
    def _execute_selected_attack(self, enemy_projectiles):
        """Exécute une attaque sélectionnée aléatoirement"""
        if not self.attack_implementations:
            return
        
        # Sélection intelligente selon la phase
        if self.phase >= self.phases - 1 and len(self.attack_implementations) > 1:
            # En phase finale, préférer les attaques complexes
            attack_keys = list(self.attack_implementations.keys())
            complex_attacks = [a for a in attack_keys if a in ["recursive_fractal", "rotating_barrage", "combo_attacks"]]
            attack = self.local_random.choice(complex_attacks) if complex_attacks else self.local_random.choice(attack_keys)
        else:
            attack = self.local_random.choice(list(self.attack_implementations.keys()))
        
        # Exécuter l'attaque
        self.attack_implementations[attack](enemy_projectiles)
        
        # Combos d'attaques
        if "combo_attacks" in self.specs["behaviors"] and self.local_random.random() < 0.3:
            self._execute_combo_attack(enemy_projectiles, attack)
    
    def _execute_combo_attack(self, enemy_projectiles, first_attack):
        """Exécute une deuxième attaque en combo"""
        other_attacks = [a for a in self.attack_implementations.keys() if a != first_attack]
        if other_attacks:
            second_attack = self.local_random.choice(other_attacks)
            # Petit délai entre les attaques
            # Note: pygame.time.delay() bloquerait le jeu, on utilisera plutôt un timer
            self.attack_cooldown = 10  # Petit délai avant la deuxième attaque
            self.attack_implementations[second_attack](enemy_projectiles)
    
    def _calculate_attack_cooldown(self):
        """Calcule le cooldown d'attaque selon la phase et les mécaniques"""
        base_cooldown = 120 - (self.specs["level"] * 10)  # 120 à 60 frames
        
        if self.enraged:
            base_cooldown *= 0.5
        
        if self.phase > 1:
            base_cooldown *= (0.8 ** (self.phase - 1))
        
        return max(30, int(base_cooldown))  # Minimum 30 frames
    
    def _handle_enrage_timer(self):
        """Gère le timer d'enragement"""
        if self.enrage_timer > 0:
            self.enrage_timer -= 1
        elif not self.enraged:
            self.enraged = True
            self._activate_enrage_mode()
    
    def _activate_enrage_mode(self):
        """Active le mode enragé"""
        self.color = (255, 50, 50)  # Rouge vif
        self.damage *= 1.5
        self.speed *= 1.3
        self.attack_cooldown = max(15, self.attack_cooldown * 0.4)
    
    # ===== IMPLÉMENTATIONS DES ATTAQUES =====
    
    def _simple_circle_attack(self, enemy_projectiles):
        """Attaque simple en cercle"""
        num_projectiles = 8 + (self.phase * 2)
        for i in range(num_projectiles):
            angle = 2 * math.pi * i / num_projectiles
            dx = math.cos(angle) * self.projectile_speed
            dy = math.sin(angle) * self.projectile_speed
            
            enemy_projectiles.append(Projectile(
                self.x, self.y, dx, dy, self.damage * 0.8, self.settings,
                color=self.color, radius=6
            ))
    
    def _double_spiral_attack(self, enemy_projectiles):
        """Deux spirales tournant en sens inverse"""
        self._spiral_attack(enemy_projectiles, clockwise=True)
        self._spiral_attack(enemy_projectiles, clockwise=False)
    
    def _spiral_attack(self, enemy_projectiles, clockwise=True, depth=30, 
                       start_angle=0, radius_increment=8, angle_increment=0.3):
        """
        Attaque en spirale récursive
        
        Complexité : O(depth) - linéaire
        """
        if depth <= 0:
            return
        
        angle = start_angle
        radius = 20
        
        for i in range(depth):
            x = self.x + math.cos(angle) * radius
            y = self.y + math.sin(angle) * radius
            
            # Direction tangentielle
            if clockwise:
                dx = -math.sin(angle) * self.projectile_speed
                dy = math.cos(angle) * self.projectile_speed
            else:
                dx = math.sin(angle) * self.projectile_speed
                dy = -math.cos(angle) * self.projectile_speed
            
            color = (100, 200, 255) if clockwise else (255, 200, 100)
            
            enemy_projectiles.append(Projectile(
                x, y, dx, dy, self.damage * 0.6, self.settings,
                color=color, radius=4
            ))
            
            # Préparation pour le prochain
            radius += radius_increment
            angle += angle_increment if clockwise else -angle_increment
        
        # Optionnel : appel récursif pour spirale interne
        if depth > 10 and self.local_random.random() < 0.3:
            self._spiral_attack(
                enemy_projectiles, clockwise, depth//2,
                start_angle + math.pi, radius_increment * 1.5, angle_increment * 1.2
            )
    
    def _recursive_fractal_attack(self, enemy_projectiles, depth=None, x=None, y=None, 
                                  angle=0, length=100, branch_angle=45):
        """
        Attaque fractale récursive - Fonction récursive obligatoire
        
        Complexité : O(2^depth) - exponentielle mais contrôlée
        """
        if depth is None:
            depth = 3 + min(2, self.specs["level"] // 2)
        
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        
        # Cas de base : feuille de l'arbre
        if depth == 0:
            dx = math.cos(angle) * self.projectile_speed
            dy = math.sin(angle) * self.projectile_speed
            
            color_intensity = 200 - (self.phase * 40)
            color = (color_intensity, 50, color_intensity)
            
            enemy_projectiles.append(Projectile(
                x, y, dx, dy, self.damage * 0.7, self.settings,
                color=color, radius=4 + self.phase
            ))
            return
        
        # Branche actuelle
        end_x = x + math.cos(angle) * length
        end_y = y + math.sin(angle) * length
        
        # Projectile pour cette branche
        branch_dx = math.cos(angle) * self.projectile_speed * 0.6
        branch_dy = math.sin(angle) * self.projectile_speed * 0.6
        
        branch_color = (150, 50, 150) if depth > 2 else (180, 50, 180)
        
        enemy_projectiles.append(Projectile(
            x, y, branch_dx, branch_dy, self.damage * 0.8, self.settings,
            color=branch_color, radius=5 + depth
        ))
        
        # Appels récursifs pour les sous-branches
        new_length = length * 0.7
        new_branch_angle = branch_angle * (1 - (0.1 * (3 - depth)))  # Angle adaptatif
        
        # Branche gauche
        self._recursive_fractal_attack(
            enemy_projectiles, depth-1,
            end_x, end_y,
            angle - math.radians(new_branch_angle),
            new_length, new_branch_angle
        )
        
        # Branche droite
        self._recursive_fractal_attack(
            enemy_projectiles, depth-1,
            end_x, end_y,
            angle + math.radians(new_branch_angle),
            new_length, new_branch_angle
        )
    
    def _homing_missiles_attack(self, enemy_projectiles):
        """Missiles guidés vers le joueur"""
        num_missiles = 3 + self.phase
        for i in range(num_missiles):
            # Angle légèrement décalé pour chaque missile
            angle_offset = (2 * math.pi / num_missiles) * i
            dx = math.cos(angle_offset) * self.projectile_speed * 0.5
            dy = math.sin(angle_offset) * self.projectile_speed * 0.5
            
            # Créer un projectile qui sera mis à jour pour suivre le joueur
            # (Dans un système plus avancé, on créerait une classe HomingProjectile)
            enemy_projectiles.append(Projectile(
                self.x, self.y, dx, dy, self.damage * 0.7, self.settings,
                color=(255, 100, 100), radius=5
            ))
    
    def _time_delayed_attack(self, enemy_projectiles):
        """Attaque avec délai avant explosion"""
        # Pour l'instant, simple cercle avec couleur différente
        self._simple_circle_attack(enemy_projectiles)
        # (À améliorer avec un système de délai)
    
    def _rotating_barrage_attack(self, enemy_projectiles):
        """Barrage tournant"""
        num_barrages = 4
        barrage_angle = (self.phase_timer * 0.05) % (2 * math.pi)
        
        for i in range(num_barrages):
            angle = barrage_angle + (2 * math.pi / num_barrages) * i
            dx = math.cos(angle) * self.projectile_speed
            dy = math.sin(angle) * self.projectile_speed
            
            enemy_projectiles.append(Projectile(
                self.x, self.y, dx, dy, self.damage * 0.9, self.settings,
                color=(100, 100, 255), radius=7
            ))
    
    # ===== IMPLÉMENTATIONS DES MOUVEMENTS =====
    
    def _stationary_movement(self, player):
        """Ne bouge pas (stationnaire)"""
        pass
    
    def _linear_pursuit_movement(self, player):
        """Poursuite linéaire simple du joueur"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Vitesse adaptative selon la phase
        speed = self.speed * (1 + (self.phase * 0.15))
        self.x += (dx / distance) * speed
        self.y += (dy / distance) * speed
    
    def _circular_orbit_movement(self, player):
        """Orbite autour du joueur"""
        orbit_radius = 200 + (self.phase * 50)
        orbit_speed = 0.03 + (self.phase * 0.01)
        
        angle = math.atan2(self.y - player.y, self.x - player.x)
        angle += orbit_speed
        
        target_x = player.x + math.cos(angle) * orbit_radius
        target_y = player.y + math.sin(angle) * orbit_radius
        
        # Mouvement progressif
        self.x += (target_x - self.x) * 0.05
        self.y += (target_y - self.y) * 0.05
    
    def _teleport_dodge_movement(self, player):
        """Téléportation pour esquiver"""
        if self.phase_timer % 100 == 0:  # Téléporte toutes les 100 frames
            angle = self.local_random.uniform(0, 2 * math.pi)
            distance = self.local_random.uniform(150, 300)
            
            self.x = player.x + math.cos(angle) * distance
            self.y = player.y + math.sin(angle) * distance
            
            # Limites
            self._constrain_to_screen()
    
    def _phase_shift_movement(self, player):
        """Se déplace par téléportation périodique"""
        if self.phase_timer % 150 == 0:  # Téléporte toutes les 150 frames
            # Choisir une position aléatoire mais pas trop proche du joueur
            angle = self.local_random.uniform(0, 2 * math.pi)
            distance = self.local_random.uniform(200, 350)
            
            self.x = player.x + math.cos(angle) * distance
            self.y = player.y + math.sin(angle) * distance
            
            self._constrain_to_screen()
    
    def _predictive_movement(self, player):
        """Se déplace vers la position prédite du joueur"""
        # Simple prédiction basée sur la vitesse du joueur
        predicted_x = player.x + player.last_dx * 30  # 30 frames d'avance
        predicted_y = player.y + player.last_dy * 30
        
        dx = predicted_x - self.x
        dy = predicted_y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        speed = self.speed * (1 + (self.phase * 0.2))
        self.x += (dx / distance) * speed
        self.y += (dy / distance) * speed
    
    # ===== IMPLÉMENTATIONS DES EFFETS SPÉCIAUX =====
    
    def _shield_phases_effect(self, player):
        """Bouclier qui s'active par phases"""
        if not self.shield_active and self.phase_timer % 200 < 50:
            # Active le bouclier pendant 50 frames toutes les 200 frames
            self.shield_active = True
            self.shield_health = self.max_health * 0.1 * self.phase
            self.color = (100, 100, 255)  # Bleu pour le bouclier
        elif self.shield_active and (self.phase_timer % 200 >= 50 or self.shield_health <= 0):
            self.shield_active = False
            self.color = self.specs["color"]
    
    def _summon_minions_effect(self, player):
        """Invoque des minions"""
        if self.phase_timer % 300 == 0 and len(self.summoned_minions) < (2 + self.phase):
            # Crée un effet de spawn (serait géré par GameScene)
            pass
    
    def _damage_auras_effect(self, player):
        """Aura de dégâts autour du boss"""
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.radius * 2:  # Zone d'aura
            player.take_damage(self.damage * 0.1)  # Dégâts continus faibles

    def _debuff_projectiles_effect(self, player):
        """Projectiles qui appliquent des débuffs"""
        # À implémenter si le temps le permet
        pass

    def _arena_hazards_effect(self, player):
        """Crée des dangers dans l'arène"""
        # À implémenter si le temps le permet
        pass
    
    # ===== MÉTHODES AUXILIAIRES =====
    
    def _constrain_to_screen(self):
        """Maintient le boss dans l'écran"""
        margin = self.radius + 20
        self.x = max(margin, min(self.x, self.settings.screen_width - margin))
        self.y = max(margin, min(self.y, self.settings.screen_height - margin))
    
    def take_damage(self, amount):
        """Gère les dégâts avec bouclier"""
        if self.shield_active:
            self.shield_health -= amount
            if self.shield_health <= 0:
                self.shield_active = False
                self.color = self.specs["color"]
            return False
        else:
            return super().take_damage(amount)
    
    def draw(self, screen):
        """Dessine le boss avec effets spéciaux"""
        # Effet de pulsation
        pulse = math.sin(self.pulse_timer) * 4
        current_radius = self.radius + pulse
        
        # Bouclier visuel
        if self.shield_active:
            shield_radius = current_radius + 15
            shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
            shield_alpha = 100 + int(50 * math.sin(self.pulse_timer * 3))
            pygame.draw.circle(shield_surface, (100, 100, 255, shield_alpha),
                             (shield_radius, shield_radius), shield_radius, 5)
            screen.blit(shield_surface, (int(self.x - shield_radius), int(self.y - shield_radius)))
        
        # Corps du boss
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(current_radius))
        
        # Détails selon la phase
        if self.phase >= self.phases - 1:
            # Phase finale : yeux menaçants
            eye_radius = current_radius * 0.25
            for i in range(2):
                eye_x = self.x + (current_radius * 0.4) * (1 if i == 0 else -1)
                eye_y = self.y - current_radius * 0.2
                
                pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), int(eye_radius))
                pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), int(eye_radius * 0.5))
        
        # Barre de vie détaillée
        self._draw_detailed_health_bar(screen)
        
        # Nom du boss
        if hasattr(self.settings, 'font') and self.settings.font:
            name_text = self.settings.font["h3"].render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 40))
            screen.blit(name_text, name_rect)
    
    def _draw_detailed_health_bar(self, screen, width=160, height=15):
        """Barre de vie détaillée avec phases"""
        # Position
        bar_x = self.x - width // 2
        bar_y = self.y - self.radius - 25
        
        # Fond
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, width, height), border_radius=3)
        
        # Santé actuelle
        health_ratio = self.health / self.max_health
        health_width = int(width * health_ratio)
        
        # Couleur par phase
        phase_colors = [
            (100, 200, 100),   # Phase 1 : Vert
            (200, 200, 100),   # Phase 2 : Jaune
            (200, 100, 100),   # Phase 3 : Rouge
            (150, 50, 200),    # Phase 4 : Violet
        ]
        
        color = phase_colors[min(self.phase - 1, len(phase_colors) - 1)]
        
        # Barre de santé
        if health_width > 0:
            pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, height), border_radius=3)
        
        # Indicateurs de phase
        for i in range(1, self.phases):
            phase_marker = bar_x + int(width * (i / self.phases))
            pygame.draw.line(screen, (255, 255, 255), 
                           (phase_marker, bar_y), (phase_marker, bar_y + height), 2)
        
        # Bordure
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, width, height), 2, border_radius=3)
        
        # Texte de phase
        if hasattr(self.settings, 'font') and self.settings.font:
            phase_text = self.settings.font["h4"].render(f"Phase {self.phase}/{self.phases}", True, (255, 255, 255))
            phase_rect = phase_text.get_rect(center=(self.x, bar_y - 10))
            screen.blit(phase_text, phase_rect)
# Tour Maudite - Documentation

## Rapport Technique

### Architecture du projet

Le projet "Tour Maudite" est structuré selon les principes de la Programmation Orientée Objet (POO) avec une organisation modulaire claire :

#### 1. Architecture générale
```
src/
├── entities/          # Entités du jeu (personnages, projectiles, effets)
├── scenes/           # Scènes du jeu (menu, jeu principal, fin de partie)
├── systems/          # Systèmes de gestion (vagues, statistiques, talents)
├── ui/              # Interface utilisateur (HUD, menus, transitions)
├── perks/           # Système d'améliorations
├── utils/           # Structures de données et utilitaires
├── audio/           # Gestion audio
└── game.py          # Point d'entrée principal
```

#### 2. Modèle de scènes (Scene Pattern)
- **BaseScene** : Classe abstraite définissant l'interface commune (`handle_event`, `update`, `draw`, `resize`)
- **MenuScene** : Gère le menu principal avec transitions vers le jeu et les talents
- **GameScene** : Scène principale du jeu avec sous-scènes pour pause, perks et statistiques
- **GameOverScene** : Écran de fin avec statistiques de la partie
- **TalentsScene** : Menu de progression permanente

#### 3. Système d'entités
- **Player** : Joueur avec système de déplacement, dash et gestion des points de vie
- **Enemy** : Classe de base pour tous les ennemis, avec spécialisations :
  - `Basic`, `Charger`, `Shooter`, `Suicide`, `Destructeur`, `Pyromane`
  - `AdaptiveBoss` : Boss unique avec comportement récursif
- **Projectile** : Système de projectiles avec effets visuels avancés
- **FireZone** : Zones de feu interactives avec animations complexes

#### 4. Gestion des vagues
- **WaveManager** : Orchestre la progression des vagues en utilisant une file personnalisée
- **WaveQueue** : Implémentation de file (FIFO) pour la séquence des vagues
- **SpawnEffect** : Effets visuels pour l'apparition des ennemis

### Fonction récursive

#### Localisation
La fonction récursive principale se trouve dans `src/entities/enemies/boss.py` :

1. **Classe `RecursiveBossCore`** :
   - Méthode `generate_behavior_tree()` (lignes 20-80)
   - Méthode `recursive_attack_pattern()` (lignes 83-145)

2. **Implémentation dans `AdaptiveBoss`** :
   - L'arbre de comportement est généré lors de la création du boss
   - Les patterns d'attaque sont exécutés récursivement pendant le combat

#### Justification de la complexité

**Complexité algorithmique** : O(branches^depth)
- `branches` = (floor_number % 3) + 2 (entre 2 et 4 branches)
- `depth` = max_depth (limité à 4 maximum)

**Contrôle de la complexité** :
1. **Limitation de profondeur** : `max_depth = min(4, 1 + (floor_number // 6))`
2. **Cache des arbres** : Les arbres de comportement sont mis en cache pour éviter la régénération
3. **Condition d'arrêt** : `if depth >= max_depth or floor_number < depth * 3`

**Pourquoi la récursivité ?**
1. **Représentation naturelle** : Les patterns d'attaque du boss forment naturellement un arbre
2. **Génération procédurale** : Permet de créer des comportements uniques à chaque boss
3. **Évolutivité** : La difficulté augmente avec la profondeur de l'arbre
4. **Maintenabilité** : Code plus lisible qu'une solution itérative complexe

### Structure de données personnalisée

#### File (Queue) dans `src/utils/queue.py`

**Implémentation** :
```python
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):      # O(1)
        self.items.append(item)
    
    def dequeue(self):           # O(1)
        if self.is_empty():
            return None
        return self.items.pop(0)
```

**Utilisation dans WaveManager** :
1. **Séquencement des vagues** : Chaque étage a une file de vagues à traiter
2. **Gestion FIFO** : Les vagues sont traitées dans l'ordre d'arrivée
3. **Extensibilité** : Permet d'ajouter des vagues spéciales dynamiquement

**Complexité** :
- `enqueue()` : O(1) - ajout en fin de liste
- `dequeue()` : O(1) - retrait en début de liste (avec pop(0))
- `is_empty()` : O(1) - vérification de longueur

### Gestion des ressources et modularité

#### Séparation code/ressources
```
assets/
├── images/           # Sprites, backgrounds, UI elements
│   ├── background/   # Fond d'écran par scène
│   └── perks_icons/  # Icônes des améliorations
├── sounds/           # Effets sonores et musique
└── fonts/            # Polices d'écriture
```

#### Système de configuration
- **Settings** (`config/settings.py`) : Centralise tous les paramètres modifiables
- **Données joueur** (`data/player_data.json`) : Sauvegarde de la progression
- **Aspect ratio** : Système de redimensionnement intelligent (4:3 maintenu)

### Qualité du code

#### Standards respectés
1. **Documentation** : Docstrings complètes selon Google Style
2. **Typage** : Annotations de type pour clarifier les interfaces
3. **Séparation des responsabilités** : Chaque classe a un rôle unique
4. **Gestion d'erreurs** : Try/except pour les opérations critiques
5. **Constantes nommées** : Pas de nombres magiques

#### Exemple de docstring
```python
def generate_behavior_tree(floor_number, seed, depth=0, max_depth=4):
    """
    Génère un arbre de comportement récursif pour le boss
    
    Complexité : O(branches^depth) où branches = floor_number % 3 + 2
    
    Args:
        floor_number (int): Niveau actuel (influence complexité)
        seed (int): Graine unique pour la génération
        depth (int): Profondeur actuelle (0 pour la racine)
        max_depth (int): Profondeur maximale basée sur l'étage
    
    Returns:
        dict: Arbre de comportement avec branches récursives
    """
```

#### Tests unitaires
```
tests/
├── test_entities.py   # Tests des entités (joueur, ennemis)
├── test_systems.py    # Tests des systèmes (vagues, collisions)
└── test_utils.py      # Tests des utilitaires (file)
```

## Rapport de Groupe

### Répartition des tâches

#### Gabriel - Développeur gameplay & UI
- **Sons et musique** : Sélection et intégration des assets
- **Intégration audio** : Gestion des sons et musique
- **Tests unitaires** : Développement et exécution
- **Système de Vague** : Implémentation de Wave_manager
- **Structure de données personnalisée** : Implémentation d'une file pour l'apparition des ennemies

#### Hugo - Chef de projet & Développeur principal
- **Architecture globale** : Conception de l'architecture POO
- **Système de combat** : Armes, projectiles, dégâts
- **Game loop** : Boucle principale et gestion des états
- **Joueur** : Mouvement, dash, gestion de vie
- **Ennemis basiques** : IA des ennemis standards
- **HUD** : Interface en jeu (barres de vie, scores)
- **Effets visuels** : Particules, animations, transitions
- **Menu principal** : Navigation et transitions
- **Documentation technique** : Rédaction du rapport
- **Équilibrage** : Courbe de difficulté et statistiques
- **Boss adaptatif** : Implémentation de la fonction récursive
- **Tests unitaires** : Développement et exécution
- **Système de collisions** : Détection et résolution
- **Système de scènes** : Implémentation du pattern Scene



#### Julien - Développeur systèmes & Développeur principal
- **Système de vagues** : WaveManager et génération procédurale
- **Système de perks** : Améliorations et gestion des choix
- **Equilibrage du jeu** : Scores, XP, progression
- **Menu des talents** : Interface de progression permanente
- **Menu principal** : Navigation et transitions
- **Menu statistiques** : Affichage des données de jeu
- **Tests unitaires** : Développement et exécution


#### Zia - Développeur UI & Assets
- **Menu GameOver** : Écran de fin avec statistiques
- **Design UI** : Boutons, menus, feedback visuel
- **Menu pause** : Interface et fonctionnalités (Quitter/Continuer/Statistiques)
- **Tests unitaires** : Développement et exécution

### Méthodologie de travail

#### Outils utilisés
- **Github Desktop** : Pour se passer les fichiers facilement et pouvoir 
- **Discord** : Communication et revues de code

#### Processus de développement
1. **Revue hebdomadaire** : Répartition des tâches hebdomadaire avec chaque dimanche ce qui doit etre fait individuellement pendant la semaine
2. **Code reviews** : On revoir tout le code pour voir si il n'y a pas de redondance et de bug lors des combo de plusieurs code de personnes différentes

### Difficultés rencontrées et solutions

#### 1. Gestion du redimensionnement
**Problème** : Maintenir le ratio 4:3 tout en permettant le plein écran
**Solution** : Système de bordures dynamiques dans `Game.resize()`

#### 2. Fonction récursive du boss
**Problème** : Risque d'explosion exponentielle de la complexité
**Solution** : Limitation de profondeur 

### Bilan

#### Améliorations possibles
- Ajout de plus de types d'ennemis
- Système d'achievements
- Mode multijoueur (en local sur une seule machine)

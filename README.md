# Tour Maudite - README.md

## Rapport Technique

### Architecture du projet

#### 1. Architecture générale
```
src/
├── entities/        # Entités du jeu (personnages, projectiles, effets)
├── scenes/          # Scènes du jeu (menu, jeu principal, fin de partie)
├── systems/         # Systèmes de gestion (vagues, statistiques, talents)
├── ui/              # Interface utilisateur (HUD, menus, transitions)
├── perks/           # Système d'améliorations
├── utils/           # Structures de données et utilitaires
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
- `Boss` : Boss avec système de division et patterns d'attaque récursifs
- **Projectile** : Système de projectiles avec effets visuels avancés
- **FireZone** : Zones de feu interactives avec animations complexes

#### 4. Gestion des vagues
- **WaveManager** : Orchestre la progression des vagues en utilisant une file personnalisée
- **WaveQueue** : Implémentation de file (FIFO) pour la séquence des vagues
- **SpawnEffect** : Effets visuels pour l'apparition des ennemis

#### 5. Page de lancement et manuel utilisateur
#### **Le menu principal (MenuScene) inclut :**

- Bouton "Jouer" pour démarrer une partie
- Bouton "Talents" pour accéder à la progression permanente
- Instructions intégrées dans le HUD pendant le jeu

#### **Le jeu inclut également un système de pause avec :**

- Bouton "Continuer" pour reprendre la partie
- Bouton "Statistiques" pour voir les données de jeu
- Bouton "Quitter" pour retourner au menu principal

### Fonction récursive

#### Localisation
La fonction récursive principale se trouve dans `src/entities/enemies/boss.py` :

1. **Classe `RecursivePatternGenerator`** :
   - Méthode `generate_circle_recursive()` (lignes 78-130)

2. **Implémentation dans `Boss`** :
   - Les patterns d'attaque sont générés récursivement pendant le combat
   - Le boss utilise également un système de division récursive via `BossDivisionSystem`

#### Justification de la complexité

**Complexité algorithmique** : O(branches^depth)
- `branches` : nombre de sous-patterns générés à chaque niveau
- `depth` : profondeur maximale de récursion (limité à 3)

**Contrôle de la complexité** :
1. **Limitation de profondeur** : `depth = min(3, self.current_phase)`
2. **Cache des patterns** : Les patterns sont générés à la volée, mais la profondeur est faible
3. **Condition d'arrêt** : `if depth <= 0`

**Pourquoi la récursivité ?**
1. **Représentation naturelle** : Les patterns d'attaque en cercles forment naturellement une structure récursive
2. **Génération procédurale** : Permet de créer des patterns complexes à partir de règles simples
3. **Évolutivité** : La difficulté augmente avec la profondeur de récursion et le nombre de phases

### Structure de données personnalisée

#### File (Queue) dans `src/utils/queue.py`

**Utilisation dans WaveManager** :
1. **Séquencement des vagues** : Chaque étage a une file de vagues à traiter
2. **Gestion FIFO** : Les vagues sont traitées dans l'ordre d'arrivée
3. **Extensibilité** : Permet d'ajouter des vagues spéciales dynamiquement

**Complexité** :
- `enqueue()` : O(1) - ajout en fin de liste
- `dequeue()` : O(1) - retrait en début de liste (avec pop(0))
- `is_empty()` : O(1) - vérification de longueur

#### Tests unitaires
```
tests/
├── test_entities.py   # Tests des entités (joueur, ennemis)
├── test_perks.py      # Tests des perks (menu, abilitées )
├── test_systems.py    # Tests des systèmes (vagues, collisions)
├── test_ui.py         # Tests des ui (menu, affichage des ennemis)
└── test_utils.py      # Tests des utilitaires (file)
```

## Rapport de Groupe

### Répartition des tâches

#### Gabriel - Développeur Gameplay/UI
- **Menu GameOver** : Écran de fin avec statistiques
- **Design UI** : Boutons, menus, feedback visuel
- **Menu Pause** : Interface visuelle
- **Audio** : Gestion des sons des bouttons
- **Audio** : Gestion de son de tir
- **Système de Vague** : Implémentation de Wave_manager
- **Structure de données personnalisée** : Implémentation d'une file pour l'apparition des ennemis

#### Hugo - Chef de projet/Développeur principal
- **Architecture globale** : Conception de l'architecture POO
- **Système de combat** : Armes, projectiles, dégâts
- **Game loop** : Boucle principale et gestion des états
- **Joueur** : Mouvement, dash, gestion de vie
- **Ennemis basiques** : IA des ennemis standards
- **HUD** : Interface en jeu (barres de vie, scores)
- **Effets visuels** : Particules, animations, transitions
- **Menu de jeu** : Navigation et transitions
- **Documentation technique** : Rédaction du rapport
- **Équilibrage** : Courbe de difficulté et statistiques
- **Boss adaptatif** : Implémentation de la fonction récursive
- **Tests unitaires** : Réalisation de la moitiée des fichiers
- **Système de collisions des différentes entités** : Détection et résolution

#### Julien - Développeur systèmes/Développeur principal
- **Système de perks** : Améliorations et gestion des choix
- **Equilibrage du jeu** : Scores, XP, progression
- **Menu des talents** : Interface de progression permanente
- **Menu principal** : Navigation et transitions
- **Menu statistiques** : Affichage des données de jeu
- **Tests unitaires** : Développement et exécution
- **Menu Tutoriel** : Explication du fonctionnement du jeu
- **Tests unitaires** : Réalisation de la moitiée des fichiers
- **Menu Pause** : Fonctionnalités (Quitter/Continuer/Statistiques)
- **Système de scènes** : Implémentation de l'héritage de la Scène

#### Zia - Développeur UI/Assets
- **Menu Menu** : Implémentation (début) du Menu principal
- **Sons et musique** : Sélection et intégration des assets (sons, images) en coopération avec Gabriel
- **Intégration audio** : Gestion des sons et musique en coopération avec Gabriel

### Méthodologie de travail

#### Outils utilisés
- **Github Desktop** : Pour une transmission efficace des fichiers
- **Discord** : Communication et revues de code

#### Processus de développement
1. **Revue hebdomadaire** : Répartition des tâches hebdomadaire avec chaque dimanche, ce qui doit etre fait individuellement pendant la semaine
2. **Code reviews** : On revoir tout le code pour voir si il n'y a pas de redondance et de bug lors de la mise en commun de plusieurs code de personnes différentes

### Difficultés rencontrées et solutions

#### 1. Gestion du redimensionnement
**Problème** : Maintenir le ratio 4:3 tout en permettant le plein écran
**Solution** : Système de bordures dynamiques avec `Game.draw()` et des fonctions resize dans toutes les scènes du jeu

#### 2. Fonction récursive et division du boss
**Problème** : Risque d'explosion exponentielle de la complexité avec la division et les patterns récursifs
**Solution** : Limitation de profondeur et contrôle du nombre de divisions

### Bilan

#### Améliorations possibles
- Ajout de plus de types d'ennemis
- Système d'achievements
- Mode multijoueur (en local sur une seule machine)
- Variantes de boss avec différents systèmes de division et patterns récursifs

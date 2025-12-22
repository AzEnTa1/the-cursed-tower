# Rapport Technique
## Organisation Générale du Projet 
- src/ : Code source principal
   - entities/ : Entités du jeu (joueur, ennemis, projectiles)
  - scenes/ : Scènes du jeu (menu, jeu principal, sous-menus)
  - systems/ : Systèmes de gestion (vagues, statistiques, collisions)
  - ui/ : Interface utilisateur (HUD, boutons, effets visuels)
  - perks/ : 
  - 
  - utils/ : Utilitaires et structures de données
  - audio/ : Gestion audio (musique et effets sonores)
- assets/ : Ressources assets jsp dire en français  (images, sons, polices)
- config/ : Configuration du jeu (paramètres, constantes)
- tests/ : Tests unitaires et fonctionnels
## Architecture Orienté Objet (POO)
Le jeu est conçu selon une architecture orientée objet avec des classes bien définies :

- Game (src/game.py) : Classe principale qui orchestre la boucle de jeu et la gestion des scènes
- BaseScene (src/scenes/base_scene.py) : Classe abstraite définissant l'interface commune à toutes les scènes
- GameScene (src/scenes/game_scene.py) : Scène de jeu principale, gère l'état du jeu en cours
- Player (src/entities/player.py) : Représente le personnage du joueur avec ses attributs et comportements
- Enemy (src/entities/enemys.py) : Classe de base pour tous les ennemis, avec spécialisation par type (charger, shooter, destructeur, suicide, pyromante)
- Weapon (src/entities/weapons.py) : Système d'arme du joueur avec tir automatique
- WaveManager (src/systems/wave_manager.py) : Gère la progression des vagues d'ennemis
## Séparation des Responsabilités 
## Gestions des données et structures internes  
- Utilisation d'une Pile : 
- 1. Dans le Queue.py, sert à gérer les différentes vagues
- 2. Dans Enemy, jsp ou 
# Rapport de Groupe
### Répartitions des Tâches : 
- Gabriel
  - à 
  - b
- Hugo
  - à 
  - à 
- Julien
  - à 
  - à 
  - à 
- Zia 
  - à 
  - `GameOver_Scene.py`
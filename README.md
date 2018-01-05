# PythonMaze
Génération de labyrinthe (différents type d'algorithme) sous python

Pour essayer le jeu, ouvrez le fichier 'Maze.py' il vous permettra de générer un labyrinthe selon vos critères :

  -Taille : 
  
            'Easy' : 10 * 10
  
            'Normal': 25 * 25
            
            'Hard' : 60 * 30
            
             'Z-Hard' : 60 * 30 en se déplaçant dans un rayon de 10 * 10
            
  -Algorithme de génération utilisé: 
  
             Fusion Aléatoire
  
             Exploration Exhaustive
                                     
             Algorithme de Prim
             
  -Avec ou sans tracer


Une fois le labyrinthe créer vous pouvez: 

      -Vous déplacez à l'aide des flèches (haut,bas,droite et gauche)
  
      -Regénérer un nouveau labyrinthe avec les mêmes paramètres en maintenant la touche R
  
      -Revenir au menu avec la touche B
  

Vous pouvez également essayer de battre votre score en cliquant sur 'replay' dans le menu


Les fichiers AlgorithmeDePrim.py, ExplorationExhaustive.py, FusionAleatoire.py sont là uniquement pour génerer le labyrinthe

Mais leur déclinaison 'Visualisation' permette de visualiser la génération du labyrinthe en temps réel

Appuyez sur espace pour lancer la génération jusqu'à la fin ou maintenez la flèche droite pour une génération pas à pas


Le fichier solveMaze.py génère un labyrinthe et trouve le chemin de sortie en temps réel 


Enfin, le fichier save.csv est la pour gérer les sauvegardes

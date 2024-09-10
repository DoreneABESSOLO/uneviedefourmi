# uneviedefourmi

# Simulation du Déplacement des Fourmis dans une Fourmilière

## Problématique

Dans ce projet, nous modélisons et simulons le déplacement d'une colonie de fourmis à l'intérieur d'une fourmilière. Chaque fourmi commence dans le vestibule et doit se déplacer à travers différentes salles connectées par des tunnels jusqu'à atteindre le dortoir. Cependant, les déplacements sont soumis à des contraintes :
- Une salle ne peut contenir qu'une seule fourmi à la fois, à l'exception du vestibule, du dortoir et des salles spéciales avec une capacité indiquée (ex : `Sn {X}`).
- Les fourmis ne peuvent entrer dans une salle que si elle n'est pas pleine.
  
L'objectif est de simuler les déplacements des fourmis en minimisant le temps passé dans les salles intermédiaires.

## Solutions apportées

### 1. **Modélisation en Python**
- **Structures de données** : Nous avons utilisé la librairie `networkx` pour modéliser la fourmilière comme un graphe. Chaque salle est représentée par un nœud, et chaque tunnel est une arête reliant deux nœuds.
- **Classes principales** :
  - **`Salle`** : Représente une salle dans la fourmilière avec une capacité.
  - **`Fourmiliere`** : Gère l'ensemble des salles et des tunnels ainsi que les déplacements des fourmis.
  - **`Fourmi`** : Représente une fourmi individuelle qui se déplace de salle en salle.
  
### 2. **Algorithme de déplacement**
- À chaque étape de la simulation, une fourmi tente de se déplacer vers une salle adjacente si elle est disponible (non pleine).
- Les déplacements sont simulés jusqu'à ce que toutes les fourmis atteignent le dortoir.
- Une visualisation des déplacements est également réalisée à chaque étape en utilisant `matplotlib` pour montrer les positions actuelles des fourmis.

### 3. **Visualisation graphique**
- **`matplotlib`** est utilisé pour représenter graphiquement la fourmilière à chaque étape de la simulation.
- Chaque salle est représentée par un nœud, et les fourmis sont visualisées en rouge lorsqu'elles occupent une salle.
- Chaque étape est affichée sous forme de graphique, permettant de suivre le déplacement des fourmis en temps réel.

### 4. **Structure du projet**
Le projet est organisé en deux fichiers principaux :
- **`ants2.py`** : Contient toutes les classes et fonctions pour modéliser la fourmilière et simuler les déplacements des fourmis.
- **`main.py`** : Fichier exécutant la simulation. Il importe les classes et fonctions de `fourmiliere_***.py` et lance la simulation.



### Explication des sections :

1. **Problématique** : Explique le but du projet et les contraintes à respecter pour modéliser le déplacement des fourmis.
2. **Solutions apportées** : Détaille les solutions techniques apportées, telles que l'utilisation de `networkx` pour modéliser la fourmilière, les classes principales, et l'algorithme de simulation.
3. **Visualisation graphique** : Expose comment le graphe est visualisé avec les fourmis et les étapes de déplacement.
4. **Structure du projet** : Donne une vue d'ensemble des fichiers du projet et leurs responsabilités.
5. **Instructions d'exécution** : Guide l'utilisateur sur la manière de télécharger, installer et exécuter le projet.
6. **Exemple de fichier d'entrée** : Montre à l'utilisateur un exemple de fichier de configuration utilisé par la simulation.
7. **Conclusion et améliorations futures** 




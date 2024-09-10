import networkx as nx
import matplotlib.pyplot as plt
import time

# Classe représentant une salle dans la fourmilière
class Salle:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite  # 'inf' ou une capacité maximale
        self.occupants = 0  # Nombre actuel de fourmis dans la salle
    
    def est_pleine(self):
        return self.capacite != 'inf' and self.occupants >= int(self.capacite)
    
    def ajouter_fourmi(self):
        if not self.est_pleine():
            self.occupants += 1
    
    def retirer_fourmi(self):
        if self.occupants > 0:
            self.occupants -= 1

# Classe représentant une fourmilière
class Fourmiliere:
    def __init__(self):
        self.salles = {}
        self.graphe = nx.Graph()
    
    def ajouter_salle(self, nom, capacite):
        if nom not in self.salles:  # Ajouter seulement si la salle n'existe pas déjà
            self.salles[nom] = Salle(nom, capacite)
            self.graphe.add_node(nom)
    
    def ajouter_tunnel(self, salle1, salle2):
        self.graphe.add_edge(salle1, salle2)
    
    def salle_est_disponible(self, nom):
        return not self.salles[nom].est_pleine()
    
    def deplacer_fourmi(self, depart, destination):
        if self.salle_est_disponible(destination):
            self.salles[depart].retirer_fourmi()
            self.salles[destination].ajouter_fourmi()

# Classe représentant une fourmi
class Fourmi:
    def __init__(self, identifiant, fourmiliere):
        self.identifiant = identifiant
        self.position = 'Sv'  # Toutes les fourmis commencent au vestibule
        self.fourmiliere = fourmiliere
        self.precedente_position = None  # Pour éviter le retour immédiat à la salle précédente
    
    def deplacer_vers(self, destination):
        if destination in self.fourmiliere.graphe[self.position]:
            if self.fourmiliere.salle_est_disponible(destination):
                print(f"Fourmi {self.identifiant} se déplace de {self.position} vers {destination}")
                self.fourmiliere.deplacer_fourmi(self.position, destination)
                self.precedente_position = self.position  # Mémoriser la salle précédente
                self.position = destination
    
    def peut_se_deplacer(self):
        # Retourne une liste de destinations possibles, en évitant de revenir à la salle précédente
        destinations_possibles = []
        for destination in self.fourmiliere.graphe[self.position]:
            if destination != self.precedente_position and self.fourmiliere.salle_est_disponible(destination):
                destinations_possibles.append(destination)
        return destinations_possibles

    def choisir_destination(self, destinations_possibles):
        """
        Choisir une destination qui se rapproche du dortoir.
        On priorise les destinations qui sont plus proches du dortoir Sd.
        """
        if 'Sd' in destinations_possibles:
            return 'Sd'  # Si le dortoir est accessible, on va directement au dortoir
        
        # Si plusieurs choix existent, on essaie de choisir au hasard une direction valide
        # Vous pouvez ici intégrer des règles de priorité plus intelligentes
        return destinations_possibles[0] if destinations_possibles else None

# Fonction pour lire une fourmilière à partir d'un fichier texte
def lire_fourmiliere(fichier):
    fourmiliere = Fourmiliere()
    fourmis = []
    salles = set()  # On stocke temporairement les salles pour éviter les duplications
    with open(fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith('#'):
                continue  # Ignorer les commentaires et lignes vides
            
            # Lire le nombre de fourmis
            if ligne.startswith('f='):
                nombre_de_fourmis = int(ligne.split('=')[1])
                fourmis = [Fourmi(i + 1, fourmiliere) for i in range(nombre_de_fourmis)]
                continue
            
            # Lire les salles et leurs capacités
            if '-' not in ligne:
                if '{' in ligne:
                    nom, capacite = ligne.split('{')
                    capacite = capacite.strip('}')
                else:
                    nom = ligne
                    capacite = 'inf'  # Par défaut, une capacité infinie (vestibule et dortoir)
                salles.add((nom.strip(), capacite))  # Ajouter à l'ensemble des salles
                continue
            
            # Lire les tunnels (relations entre salles)
            if '-' in ligne:
                salle1, salle2 = ligne.split('-')
                salle1 = salle1.strip()
                salle2 = salle2.strip()
                # Assurer que les salles mentionnées dans les tunnels sont ajoutées au graphe
                if salle1 not in [salle[0] for salle in salles]:
                    salles.add((salle1, 'inf'))
                if salle2 not in [salle[0] for salle in salles]:
                    salles.add((salle2, 'inf'))
                fourmiliere.ajouter_tunnel(salle1, salle2)
    
    # Ajouter toutes les salles collectées dans la fourmilière
    for nom, capacite in salles:
        fourmiliere.ajouter_salle(nom, capacite)

    return fourmiliere, fourmis

# Fonction pour afficher le graphe de la fourmilière avec les positions des fourmis
def afficher_fourmiliere(fourmiliere, fourmis, pos, etape):
    plt.figure(figsize=(8, 6))
    
    # Dessiner le graphe de la fourmilière
    nx.draw(fourmiliere.graphe, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    
    # Dessiner les fourmis sur le graphe
    fourmis_positions = {fourmi.position for fourmi in fourmis}  # Récupérer les positions actuelles des fourmis
    nx.draw_networkx_nodes(fourmiliere.graphe, pos, nodelist=fourmis_positions, node_color='red', node_size=500)
    
    plt.title(f"Etape {etape} - Positions des fourmis")
    plt.show()

# Fonction pour simuler le déplacement des fourmis jusqu'au dortoir, avec gestion des capacités
def simuler_deplacement(fourmiliere, fourmis):
    pos = nx.spring_layout(fourmiliere.graphe)  # Générer les positions des nœuds une fois pour toutes
    etape = 1
    afficher_fourmiliere(fourmiliere, fourmis, pos, etape)  # Afficher l'état initial
    
    while any(fourmi.position != 'Sd' for fourmi in fourmis):
        print(f"\n+++ Etape {etape} +++")
        fourmis_bougees = False  # Variable pour vérifier si au moins une fourmi a bougé
        mouvements_possibles = {}  # Dictionnaire pour limiter les fourmis dans une salle à sa capacité

        # Collecter les fourmis qui souhaitent se déplacer
        for fourmi in fourmis:
            if fourmi.position != 'Sd':  # Ne bouger que si la fourmi n'est pas déjà au dortoir
                destinations_possibles = fourmi.peut_se_deplacer()
                if destinations_possibles:
                    destination = fourmi.choisir_destination(destinations_possibles)
                    if destination:
                        if destination not in mouvements_possibles:
                            mouvements_possibles[destination] = []
                        mouvements_possibles[destination].append(fourmi)

        # Appliquer les déplacements en fonction des capacités des salles
        for destination, fourmis_a_deplacer in mouvements_possibles.items():
            capacite_restante = int(fourmiliere.salles[destination].capacite) if fourmiliere.salles[destination].capacite != 'inf' else len(fourmis_a_deplacer)
            for i, fourmi in enumerate(fourmis_a_deplacer):
                if i < capacite_restante:  # Ne déplacer que les fourmis correspondant à la capacité disponible
                    fourmi.deplacer_vers(destination)
                    fourmis_bougees = True
        
        # Si aucune fourmi ne peut bouger, il n'y a pas de progression, on arrête la simulation
        if not fourmis_bougees:
            print("Aucune fourmi ne peut bouger, la simulation est bloquée.")
            break
        
        etape += 1
        afficher_fourmiliere(fourmiliere, fourmis, pos, etape)  # Afficher l'état actuel à chaque étape
        time.sleep(1)  # Pause pour mieux voir les étapes de déplacement

from ants2 import lire_fourmiliere, simuler_deplacement

if __name__ == "__main__":
    fichier_fourmiliere = 'fourmiliere_cinq.txt'
    fourmiliere, fourmis = lire_fourmiliere(fichier_fourmiliere)
    
    # Simuler le déplacement des fourmis avec affichage des étapes
    simuler_deplacement(fourmiliere, fourmis)

# sauvegarde.py

import numpy as np

def sauvegarder_grille(grille, nom_fichier):
    np.save(nom_fichier, grille)

def charger_grille(nom_fichier):
    return np.load(nom_fichier)

# interface.py

import tkinter as tk
from moteur import MoteurDeJeu

class InterfaceJeu:
    def __init__(self, taille_cellule=20, largeur_fenetre=30, hauteur_fenetre=30):
        self.taille_cellule = taille_cellule
        self.largeur_fenetre = largeur_fenetre
        self.hauteur_fenetre = hauteur_fenetre
        self.moteur = MoteurDeJeu()
        self.en_marche = False
        self.historique = []
        self.index_historique = -1

        self.offset_x = 0  # Pour le déplacement horizontal
        self.offset_y = 0  # Pour le déplacement vertical

        self.root = tk.Tk()
        self.root.title("Jeu de la Vie")

        self.canvas = tk.Canvas(self.root, width=self.largeur_fenetre * self.taille_cellule,
                                height=self.hauteur_fenetre * self.taille_cellule)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.modifier_cellule)
        self.root.bind("<Key>", self.gestion_touches)

        self.bouton_demarrer = tk.Button(self.root, text="Démarrer", command=self.demarrer)
        self.bouton_demarrer.pack(side=tk.LEFT)

        self.bouton_arreter = tk.Button(self.root, text="Arrêter", command=self.arreter)
        self.bouton_arreter.pack(side=tk.LEFT)

        self.bouton_etape = tk.Button(self.root, text="Étape Suivante", command=self.etape_suivante)
        self.bouton_etape.pack(side=tk.LEFT)

        self.bouton_annuler = tk.Button(self.root, text="Annuler", command=self.annuler)
        self.bouton_annuler.pack(side=tk.LEFT)

        self.bouton_initialiser = tk.Button(self.root, text="Initialiser Aléatoirement", command=self.initialiser_aleatoire)
        self.bouton_initialiser.pack(side=tk.LEFT)

        self.actualiser_grille()

    def coordonnees_vers_cellule(self, x, y):
        col = (x // self.taille_cellule) + self.offset_x
        row = (y // self.taille_cellule) + self.offset_y
        return col, row

    def modifier_cellule(self, event):
        x, y = event.x, event.y
        col, row = self.coordonnees_vers_cellule(x, y)
        if (col, row) in self.moteur.cellules_vivantes:
            self.moteur.supprimer_cellule(col, row)
        else:
            self.moteur.ajouter_cellule(col, row)
        self.actualiser_grille()

    def actualiser_grille(self):
        self.canvas.delete("all")
        for i in range(self.largeur_fenetre + 1):
            x = i * self.taille_cellule
            self.canvas.create_line(x, 0, x, self.hauteur_fenetre * self.taille_cellule, fill="green")
        for j in range(self.hauteur_fenetre + 1):
            y = j * self.taille_cellule
            self.canvas.create_line(0, y, self.largeur_fenetre * self.taille_cellule, y, fill="green")

        for cellule in self.moteur.cellules_vivantes:
            x, y = cellule
            x_affiche = (x - self.offset_x) * self.taille_cellule
            y_affiche = (y - self.offset_y) * self.taille_cellule
            if 0 <= x_affiche < self.largeur_fenetre * self.taille_cellule and 0 <= y_affiche < self.hauteur_fenetre * self.taille_cellule:
                self.canvas.create_rectangle(x_affiche, y_affiche, x_affiche + self.taille_cellule,
                                             y_affiche + self.taille_cellule, fill="green")

    def gestion_touches(self, event):
        if event.keysym == 'Up':
            self.offset_y -= 10
        elif event.keysym == 'Down':
            self.offset_y += 10
        elif event.keysym == 'Left':
            self.offset_x -= 10
        elif event.keysym == 'Right':
            self.offset_x += 10
        self.actualiser_grille()

    def demarrer(self):
        if not self.en_marche:
            self.en_marche = True
            self.mettre_a_jour()

    def arreter(self):
        self.en_marche = False

    def etape_suivante(self):
        self.enregistrer_historique()
        self.moteur.etape_suivante()
        self.actualiser_grille()

    def annuler(self):
        if self.index_historique > 0:
            self.index_historique -= 1
            self.moteur.cellules_vivantes = self.historique[self.index_historique].copy()
            self.actualiser_grille()

    def mettre_a_jour(self):
        if self.en_marche:
            self.enregistrer_historique()
            self.moteur.etape_suivante()
            self.actualiser_grille()
            self.root.after(100, self.mettre_a_jour)

    def initialiser_aleatoire(self):
        self.moteur = MoteurDeJeu()
        self.moteur.initialiser_aleatoire(100)
        self.actualiser_grille()

    def enregistrer_historique(self):
        # Supprimer l'historique futur si on a annulé des étapes
        self.historique = self.historique[:self.index_historique + 1]
        self.historique.append(self.moteur.cellules_vivantes.copy())
        self.index_historique += 1

    def lancer(self):
        self.root.mainloop()

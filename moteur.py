from pattern_detection import *

class MoteurDeJeu:
    def __init__(self):
        self.cellules_vivantes = set()

    def ajouter_cellule(self, x, y):
        self.cellules_vivantes.add((x, y))

    def supprimer_cellule(self, x, y):
        self.cellules_vivantes.discard((x, y))

    def compter_voisins(self, x, y):
        voisins = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not (dx == 0 and dy == 0):
                    if (x + dx, y + dy) in self.cellules_vivantes:
                        voisins += 1
        return voisins

    def etape_suivante(self, survie=[2, 3], naissance=[3]):
        nouvelles_cellules_vivantes = set()
        cellules_potentielles = set()

        for cellule in self.cellules_vivantes:
            x, y = cellule
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cellules_potentielles.add((x + dx, y + dy))

        for cellule in cellules_potentielles:
            x, y = cellule
            voisins = self.compter_voisins(x, y)
            if cellule in self.cellules_vivantes:
                if voisins in survie:
                    nouvelles_cellules_vivantes.add(cellule)
            else:
                if voisins in naissance:
                    nouvelles_cellules_vivantes.add(cellule)

        self.cellules_vivantes = nouvelles_cellules_vivantes


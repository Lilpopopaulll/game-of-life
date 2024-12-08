# analyse.py

import matplotlib
matplotlib.use("Agg")  # Utiliser le backend 'Agg' pour le rendu hors-écran
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame

class Analyseur:
    def __init__(self):
        self.historique_pop = []
        # Appliquer un style sombre
        plt.style.use('dark_background')
        # Créer une figure pour le graphique avec un fond noir et une haute résolution
        self.fig, self.ax = plt.subplots(figsize=(4, 6), dpi=200)
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.canvas = FigureCanvasAgg(self.fig)

    def enregistrer_population(self, population):
        self.historique_pop.append(population)

    def get_plot_surface(self):
        self.ax.clear()
        # Tracer la courbe avec une couleur visible sur fond noir
        self.ax.plot(self.historique_pop, marker='o', color='white', linestyle='-', linewidth=2, markersize=5)
        self.ax.set_xlabel("Étapes", color='white', fontsize=12)
        self.ax.set_ylabel("Population", color='white', fontsize=10)
        self.ax.set_title("Évolution de la population dans le temps", color='white', fontsize=14)
        self.ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        # Ajuster les couleurs et les polices des graduations
        self.ax.tick_params(axis='x', colors='white', labelsize=14)
        self.ax.tick_params(axis='y', colors='white', labelsize=14)
        # Ajuster les limites pour un affichage plus esthétique
        self.ax.set_xlim(0, max(10, len(self.historique_pop)))
        self.ax.set_ylim(0, max(self.historique_pop + [10]))
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        width, height = self.fig.canvas.get_width_height()
        # Créer une surface Pygame à partir des données du graphique
        surf = pygame.image.fromstring(raw_data, (width, height), "RGB")
        return surf

    def tracer_population(self):
        # Méthode pour afficher le graphique dans une nouvelle fenêtre
        plt.figure(figsize=(8, 6), dpi=400)
        plt.style.use('dark_background')
        plt.plot(self.historique_pop, marker='o', color='white', linestyle='-', linewidth=2, markersize=5)
        plt.xlabel("Étapes", color='white', fontsize=12)
        plt.ylabel("Population", color='white', fontsize=12)
        plt.title("Évolution de la population dans le temps", color='white', fontsize=14)
        plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
        plt.tick_params(axis='x', colors='white', labelsize=14)
        plt.tick_params(axis='y', colors='white', labelsize=14)
        plt.show()

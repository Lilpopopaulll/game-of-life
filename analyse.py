# analyse.py

import matplotlib

matplotlib.use("Agg")  # Utiliser le backend 'Agg' pour le rendu hors-écran
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame


class Analyseur:
    def __init__(self):
        self.historique_pop = []
        self.historique_ratios = []  # Historique des ratios calculés
        self.motifs_detectes = {}

        # Initialisation du graphique de la population
        self.fig, self.ax = plt.subplots(figsize=(4, 6), dpi=200)
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.canvas = FigureCanvasAgg(self.fig)

        # Initialisation du graphique des motifs détectés
        self.fig_motifs, self.ax_motifs = plt.subplots(figsize=(4, 6), dpi=200)
        self.fig_motifs.patch.set_facecolor('black')
        self.ax_motifs.set_facecolor('black')
        self.canvas_motifs = FigureCanvasAgg(self.fig_motifs)

        # Initialisation du graphique des ratios
        self.fig_ratio, self.ax_ratio = plt.subplots(figsize=(4, 6), dpi=200)
        self.fig_ratio.patch.set_facecolor('black')
        self.ax_ratio.set_facecolor('black')
        self.canvas_ratio = FigureCanvasAgg(self.fig_ratio)

    def enregistrer_population(self, population,ratio):
        """Enregistrer la population à chaque étape et calculer le ratio."""
        self.historique_pop.append(population)

        self.historique_ratios.append(ratio)
    def get_ratio_plot_surface(self):
        """Générer la surface du graphique à afficher dans Pygame pour le ratio."""
        self.ax_ratio.clear()  # Effacer le graphique précédent

        # Tracer la courbe du ratio
        self.ax_ratio.plot(self.historique_ratios, marker='o', color='white', linestyle='-', linewidth=2, markersize=5)
        self.ax_ratio.set_xlabel("Étapes", color='white', fontsize=12)
        self.ax_ratio.set_ylabel("Ratio", color='white', fontsize=10)
        self.ax_ratio.set_title("Ratio en temps réel", color='white', fontsize=14)
        self.ax_ratio.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax_ratio.tick_params(axis='x', colors='white', labelsize=14)
        self.ax_ratio.tick_params(axis='y', colors='white', labelsize=14)
        self.ax_ratio.set_xlim(0, max(10, len(self.historique_ratios)))
        self.ax_ratio.set_ylim(0, max(self.historique_ratios + [1]))

        self.canvas_ratio.draw()

        renderer = self.canvas_ratio.get_renderer()
        raw_data = renderer.tostring_rgb()
        width, height = self.fig_ratio.canvas.get_width_height()

        # Créer une surface Pygame à partir des données du graphique du ratio
        surf_ratio = pygame.image.fromstring(raw_data, (width, height), "RGB")

        return surf_ratio

    def detecter_motif(self, etat):
        """Détecter un motif basé sur l'état actuel."""
        # Exemple : si l'état est supérieur à un seuil, détecter un motif
        if etat > 50:
            return "Motif_Haut"
        elif etat < 10:
            return "Motif_Bas"
        else:
            return "Motif_Moyen"

    def enregistrer_motif(self, motif):
        """Enregistrer un motif détecté à chaque étape."""
        self.motifs_detectes = motif

    def get_plot_surface(self):
        """Générer la surface du graphique à afficher dans Pygame pour la population."""
        self.ax.clear()  # Effacer le graphique précédent

        # Tracer la courbe de la population
        self.ax.plot(self.historique_pop, marker='o', color='white', linestyle='-', linewidth=2, markersize=5)
        self.ax.set_xlabel("Étapes", color='white', fontsize=12)
        self.ax.set_ylabel("Population", color='white', fontsize=10)
        self.ax.set_title("Évolution de la population dans le temps", color='white', fontsize=14)
        self.ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax.tick_params(axis='x', colors='white', labelsize=14)
        self.ax.tick_params(axis='y', colors='white', labelsize=14)
        self.ax.set_xlim(0, max(10, len(self.historique_pop)))
        self.ax.set_ylim(0, max(self.historique_pop + [10]))

        self.canvas.draw()

        renderer = self.canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        width, height = self.fig.canvas.get_width_height()

        # Créer une surface Pygame à partir des données du graphique
        surf = pygame.image.fromstring(raw_data, (width, height), "RGB")

        return surf

    def get_motifs_plot_surface(self):
        """Générer la surface du graphique à afficher dans Pygame pour les motifs détectés."""
        self.ax_motifs.clear()  # Effacer le graphique précédent

        # Tracer les courbes pour chaque motif détecté
        for motif, count in self.motifs_detectes.items():
            self.ax_motifs.plot([count] * len(self.historique_pop), label=motif, linestyle='-', linewidth=2)

        self.ax_motifs.set_xlabel("Étapes", color='white', fontsize=12)
        self.ax_motifs.set_ylim(0, 100)
        self.ax_motifs.set_ylabel("Nombre de détections", color='white', fontsize=10)
        self.ax_motifs.set_title("Nombre de motifs détectés dans le temps", color='white', fontsize=14)
        self.ax_motifs.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax_motifs.tick_params(axis='x', colors='white', labelsize=14)
        self.ax_motifs.tick_params(axis='y', colors='white', labelsize=14)

        self.ax_motifs.legend(loc='upper left', fontsize=10, facecolor='black', edgecolor='white')

        self.canvas_motifs.draw()

        renderer = self.canvas_motifs.get_renderer()
        raw_data = renderer.tostring_rgb()
        width, height = self.fig_motifs.canvas.get_width_height()

        # Créer une surface Pygame à partir des données du graphique des motifs
        surf_motifs = pygame.image.fromstring(raw_data, (width, height), "RGB")

        return surf_motifs

    def tracer_population(self):
        """Tracer le graphique de la population dans une nouvelle fenêtre avec matplotlib."""
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

    def tracer_motifs(self):
        """Tracer le graphique des motifs détectés dans une nouvelle fenêtre avec matplotlib."""
        plt.figure(figsize=(8, 6), dpi=400)
        plt.style.use('dark_background')

        for motif, count in self.motifs_detectes.items():
            plt.plot([count] * len(self.historique_pop), label=motif, linestyle='-', linewidth=2)

        plt.xlabel("Étapes", color='white', fontsize=12)
        plt.ylabel("Nombre de détections", color='white', fontsize=12)
        plt.title("Nombre de motifs détectés dans le temps", color='white', fontsize=14)
        plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
        plt.legend(loc='upper left', fontsize=10, facecolor='black', edgecolor='white')
        plt.tick_params(axis='x', colors='white', labelsize=14)
        plt.tick_params(axis='y', colors='white', labelsize=14)
        plt.show()

    def tracer_histogramme_motifs(self):
        """Tracer un histogramme du nombre de chaque motif détecté."""
        plt.figure(figsize=(8, 6), dpi=400)
        plt.style.use('dark_background')

        motifs = list(self.motifs_detectes.keys())  # Liste des motifs
        counts = list(self.motifs_detectes.values())  # Nombre de fois où chaque motif a été détecté

        # Tracer l'histogramme
        self.ax.bar(motifs, counts, color='white', width=0.4)
        self.ax.set_xlabel("Motifs", color='white', fontsize=12)
        self.ax.set_ylabel("Nombre de détections", color='white', fontsize=10)
        self.ax.set_title("Nombre total de chaque motif détecté", color='white', fontsize=14)
        self.ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax.tick_params(axis='x', colors='white', labelsize=14)
        self.ax.tick_params(axis='y', colors='white', labelsize=14)

        plt.show()



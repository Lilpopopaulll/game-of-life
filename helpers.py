import pickle
import random
import pygame

def draw_grid(screen, grid_width, grid_height, TAILLE_CELLULE, COULEUR_LIGNE, offset_x, offset_y):
    for x in range(0, grid_width, TAILLE_CELLULE):
        pygame.draw.line(screen, COULEUR_LIGNE, (x, 0), (x, grid_height))
    for y in range(0, grid_height, TAILLE_CELLULE):
        pygame.draw.line(screen, COULEUR_LIGNE, (0, y), (grid_width, y))

def draw_cells(screen, cellules, TAILLE_CELLULE, offset_x, offset_y, grid_width, grid_height, couleur):
    for cellule in cellules:
        x, y = cellule
        x_affiche = (x - offset_x) * TAILLE_CELLULE
        y_affiche = (y - offset_y) * TAILLE_CELLULE
        if 0 <= x_affiche < grid_width and 0 <= y_affiche < grid_height:
            rect = pygame.Rect(x_affiche, y_affiche, TAILLE_CELLULE, TAILLE_CELLULE)
            pygame.draw.rect(screen, couleur, rect)

def get_cells_in_selection(moteur, start, end):
    x_start, y_start = start
    x_end, y_end = end
    x_min = min(x_start, x_end)
    x_max = max(x_start, x_end)
    y_min = min(y_start, y_end)
    y_max = max(y_start, y_end)
    selected = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if (x, y) in moteur.cellules_vivantes:
                selected.add((x, y))
    return selected

def enregistrer_historique(moteur, historique, index_historique):
    # Supprimer l'historique futur si on a annulé des étapes
    historique[:] = historique[:index_historique + 1]
    historique.append(moteur.cellules_vivantes.copy())

def sauvegarder_grille(cellules):
    try:
        with open('grille_sauvegardee.pkl', 'wb') as f:
            pickle.dump(cellules, f)
        print("Grille sauvegardée.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def charger_grille():
    try:
        with open('grille_sauvegardee.pkl', 'rb') as f:
            cellules = pickle.load(f)
        print("Grille chargée.")
        return cellules
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée.")
        return None
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return None

def generate_random_grid(moteur, settings):
    taille = settings['random_grid_size']
    prob = settings['birth_probability'] / 100.0
    for x in range(-taille//2, taille//2):
        for y in range(-taille//2, taille//2):
            if random.random() < prob:
                moteur.ajouter_cellule(x, y)

def apply_settings(settings_window, settings):
    # Accéder directement aux champs de saisie stockés dans settings_window
    survie_input = settings_window.survie_input
    naissance_input = settings_window.naissance_input
    prob_input = settings_window.prob_input
    taille_input = settings_window.taille_input

    try:
        survie = list(map(int, survie_input.get_text().split(',')))
        naissance = list(map(int, naissance_input.get_text().split(',')))
        prob = int(prob_input.get_text())
        taille = int(taille_input.get_text())

        settings['survie'] = survie
        settings['naissance'] = naissance
        settings['birth_probability'] = max(0, min(prob, 100))  # Limiter entre 0 et 100
        settings['random_grid_size'] = max(10, taille)  # Taille minimale de 10

        print("Paramètres mis à jour.")
    except ValueError:
        print("Erreur dans les paramètres. Veuillez vérifier vos entrées.")

def generate_pattern_icon(pattern, size=(50, 50)):
    # Créer une surface pour l'icône
    icon_surface = pygame.Surface(size, pygame.SRCALPHA)
    icon_surface.fill((0, 0, 0, 0))  # Fond transparent

    # Déterminer la boîte englobante du motif
    xs = [cell[0] for cell in pattern]
    ys = [cell[1] for cell in pattern]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Calculer l'échelle pour ajuster le motif à l'icône
    pattern_width = max_x - min_x + 1
    pattern_height = max_y - min_y + 1
    scale_x = size[0] / pattern_width if pattern_width > 0 else size[0]
    scale_y = size[1] / pattern_height if pattern_height > 0 else size[1]
    scale = min(scale_x, scale_y)

    # Centrer le motif dans l'icône
    offset_x = (size[0] - pattern_width * scale) / 2
    offset_y = (size[1] - pattern_height * scale) / 2

    # Dessiner les cellules du motif
    for x, y in pattern:
        rect = pygame.Rect(
            int((x - min_x) * scale + offset_x),
            int((y - min_y) * scale + offset_y),
            max(1, int(scale)),
            max(1, int(scale))
        )
        pygame.draw.rect(icon_surface, (255, 255, 255), rect)
    return icon_surface

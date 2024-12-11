# game.py

import pygame
import numpy as np
import pygame_gui
from analyse import Analyseur
from moteur import MoteurDeJeu
from patterns import predefined_patterns
import os
from helpers import (
    draw_grid, draw_cells, get_cells_in_selection, enregistrer_historique,
    sauvegarder_grille, charger_grille, generate_random_grid
)
from pattern_detection import *
import random

def main():
    pygame.init()
    pygame.display.set_caption("Jeu de la Vie de Conway")

    # Variables pour l'analyse
    analyseur = Analyseur()

    # Obtenir la taille de l'écran et définir le mode plein écran
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Définir la largeur du graphique (par exemple, 25% de la largeur de l'écran)
    graph_width = int(screen_width * 0.25)
    grid_width = screen_width - graph_width

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    # Créer un gestionnaire pour pygame_gui avec un thème personnalisé
    manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')

    # Calculer la hauteur de la barre d'outils (par exemple, 10% de la hauteur de l'écran)
    status_bar_height = int(screen_height * 0.1)

    # Calculer la hauteur de la barre des motifs
    patterns_bar_height = int(screen_height * 0.1)

    # Créer un rectangle pour la barre d'outils
    status_bar_rect = pygame.Rect(0, screen_height - status_bar_height, grid_width, status_bar_height)

    # Créer un rectangle pour la barre des motifs
    patterns_bar_rect = pygame.Rect(0, screen_height - status_bar_height - patterns_bar_height, grid_width, patterns_bar_height)

    # Définir les dimensions et positions des boutons
    button_width = 80
    affichage_calcul = 0
    button_height = status_bar_height - 20  # Laisser une marge
    button_margin = 10
    button_names = [
        ('reset', 'Réinitialiser'),
        ('pause_play', 'Pause/Play'),
        ('random', 'Aléatoire'),
        ('speed', 'Vitesse'),
        ('undo', 'Annuler'),
        ('save', 'Sauvegarder'),
        ('load', 'Charger'),
        ('selection', 'Sélection'),
        ('graph', 'Graphique'),
        ('calc', 'Calcul'),
        ('detect', 'Detection')
    ]
    num_buttons = len(button_names)

    total_buttons_width = num_buttons * button_width + (num_buttons - 1) * button_margin
    start_x = (grid_width - total_buttons_width) // 2  # Centrer les boutons

    buttons = {}

    # Charger les icônes des boutons (si disponibles)
    button_icons = {}
    for name, _ in button_names:
        icon_path = os.path.join('icons', f'{name}.png')
        if os.path.isfile(icon_path):
            try:
                icon_surface = pygame.image.load(icon_path).convert_alpha()
                button_icons[name] = icon_surface
            except pygame.error as e:
                print(f"Erreur de chargement de l'icône {icon_path} : {e}")
                button_icons[name] = None
        else:
            button_icons[name] = None  # Aucune icône disponible

    # Créer les boutons avec (ou sans) icônes
    for i, (name, text) in enumerate(button_names):
        x = start_x + i * (button_width + button_margin)
        y = screen_height - status_bar_height + 10  # Positionner à l'intérieur de la barre d'outils
        rect = pygame.Rect(x, y, button_width, button_height)
        if button_icons[name]:
            button = pygame_gui.elements.UIButton(
                relative_rect=rect,
                text='',
                manager=manager,
                tool_tip_text=text,
                object_id=pygame_gui.core.ObjectID(class_id='@with_icon', object_id='#' + name),
                normal_image_surface=button_icons[name]
            )
        else:
            button = pygame_gui.elements.UIButton(
                relative_rect=rect,
                text=text,
                manager=manager,
                tool_tip_text=text,
                object_id=pygame_gui.core.ObjectID(class_id='@no_icon', object_id='#' + name)
            )
        buttons[name] = button

    # Créer la barre des motifs
    patterns_bar_panel = pygame_gui.elements.UIPanel(
        relative_rect=patterns_bar_rect,
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id='@patterns_bar', object_id='#patterns_bar')
    )

    # Ajouter les boutons de défilement (flèches gauche et droite)
    arrow_button_width = 50
    arrow_button_height = patterns_bar_height - 20  # Laisser une marge
    arrow_margin = 10

    left_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(arrow_margin, 10, arrow_button_width, arrow_button_height),
        text='<',
        manager=manager,
        container=patterns_bar_panel,
        tool_tip_text='Défiler vers la gauche',
        object_id=pygame_gui.core.ObjectID(class_id='@arrow_button', object_id='#left_arrow')
    )

    right_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width - arrow_margin - arrow_button_width - arrow_margin, 10, arrow_button_width, arrow_button_height),
        text='>',
        manager=manager,
        container=patterns_bar_panel,
        tool_tip_text='Défiler vers la droite',
        object_id=pygame_gui.core.ObjectID(class_id='@arrow_button', object_id='#right_arrow')
    )

    # Ajouter les boutons de motifs dans la barre des motifs avec défilement
    pattern_buttons = []
    pattern_button_height = patterns_bar_height - 20  # Laisser une marge
    pattern_button_width = 100  # Largeur fixe pour chaque bouton de motif
    patterns_visible_count = (grid_width - 4 * arrow_margin - 2 * arrow_button_width) // (pattern_button_width + arrow_margin)
    pattern_scroll_index = 0  # Indice de défilement des motifs

    def update_pattern_buttons():
        # Effacer les anciens boutons
        for btn in pattern_buttons:
            btn.kill()
        pattern_buttons.clear()

        x_offset = 2 * arrow_margin + arrow_button_width
        end_index = pattern_scroll_index + patterns_visible_count
        visible_patterns = predefined_patterns[pattern_scroll_index:end_index]

        for pattern in visible_patterns:
            pattern_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(x_offset, 10, pattern_button_width, pattern_button_height),
                text=pattern['name'],
                manager=manager,
                container=patterns_bar_panel,
                tool_tip_text=pattern['name'],
                object_id=pygame_gui.core.ObjectID(class_id='@pattern_button', object_id='#' + pattern['name']),
            )
            pattern_button.pattern_data = pattern
            pattern_buttons.append(pattern_button)
            x_offset += pattern_button_width + arrow_margin

    update_pattern_buttons()

    # Variables du jeu
    TAILLE_CELLULE = 20
    offset_x = 0
    offset_y = 0
    en_marche = False
    historique = []
    index_historique = -1
    moteur = MoteurDeJeu()

    # Paramètres du jeu (par défaut)
    settings = {
        'survie': [2, 3],        # Une cellule survit si elle a 2 ou 3 voisins
        'naissance': [3],        # Une cellule naît si elle a exactement 3 voisins
        'birth_probability': 50, # Probabilité de naissance en mode aléatoire (en %)
        'random_grid_size': 50   # Taille de la grille aléatoire (50x50)
    }

    simulation_speed = 10  # FPS par défaut

    # Couleurs
    COULEUR_FOND = (0, 0, 0)        # Noir
    COULEUR_LIGNE = (5, 5, 5)    # Gris foncé
    COULEUR_CELLULE = (0, 255, 0)   # Vert lumineux
    COULEUR_SELECTION = (255, 0, 0) # Rouge pour la sélection

    # Variables pour pygame_gui
    time_delta = 0

    # Gestion de la sélection
    selection_mode = False
    selection_start = None
    selection_end = None
    selected_cells = set()
    copied_cells = set()
    is_ctrl_pressed = False
    selecting = False  # Initialiser la variable 'selecting'

    # Variables pour le placement des motifs
    placing_pattern = False
    selected_pattern = None

    # Création du panneau des paramètres dans le coin inférieur droit
    # Définir la taille du panneau des paramètres
    settings_panel_width = int(graph_width)
    settings_panel_height = int(screen_height * 0.35)

    # Calculer la position du panneau des paramètres (aligné avec la barre d'outils)
    settings_panel_x = grid_width
    settings_panel_y = screen_height - status_bar_height - settings_panel_height

    # Créer le panneau des paramètres
    settings_panel_rect = pygame.Rect(settings_panel_x, settings_panel_y, settings_panel_width, settings_panel_height)
    settings_panel = pygame_gui.elements.UIPanel(
        relative_rect=settings_panel_rect,
        manager=manager,
        starting_height=1,
        object_id=pygame_gui.core.ObjectID(class_id='@settings_panel', object_id='#settings_panel')
    )

    # Champs pour les règles de survie
    survie_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 10, settings_panel_width - 20, 20),
        text='Survie si voisins :',
        manager=manager,
        container=settings_panel
    )
    survie_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 30, settings_panel_width - 20, 30),
        manager=manager,
        container=settings_panel,
        object_id=pygame_gui.core.ObjectID(class_id='@survie_input', object_id='#survie_input')
    )
    survie_input.set_text(','.join(map(str, settings['survie'])))

    # Champs pour les règles de naissance
    naissance_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 70, settings_panel_width - 20, 20),
        text='Naissance si voisins :',
        manager=manager,
        container=settings_panel
    )
    naissance_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 90, settings_panel_width - 20, 30),
        manager=manager,
        container=settings_panel,
        object_id=pygame_gui.core.ObjectID(class_id='@naissance_input', object_id='#naissance_input')
    )
    naissance_input.set_text(','.join(map(str, settings['naissance'])))

    # Champs pour la probabilité de naissance
    prob_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 130, settings_panel_width - 20, 20),
        text='Probabilité de naissance (%) :',
        manager=manager,
        container=settings_panel
    )
    prob_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 150, settings_panel_width - 20, 30),
        manager=manager,
        container=settings_panel,
        object_id=pygame_gui.core.ObjectID(class_id='@prob_input', object_id='#prob_input')
    )
    prob_input.set_text(str(settings['birth_probability']))

    # Champs pour la taille de la grille aléatoire
    taille_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 190, settings_panel_width - 20, 20),
        text='Taille de la grille aléatoire :',
        manager=manager,
        container=settings_panel
    )
    taille_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 210, settings_panel_width - 20, 30),
        manager=manager,
        container=settings_panel,
        object_id=pygame_gui.core.ObjectID(class_id='@taille_input', object_id='#taille_input')
    )
    taille_input.set_text(str(settings['random_grid_size']))
    running = True
    while running:
        time_delta = clock.tick(simulation_speed) / 1000.0  # Temps en secondes

        # Pour l'affichage, nous ajustons la taille de la grille en fonction du zoom
        grid_size_for_print = 23 * (23 / TAILLE_CELLULE)  # Plus la taille de la cellule baisse, plus la grille augmente

        time_ratio = time_delta + time_delta/grid_size_for_print
        # Mettre à jour l'état des touches
        keys_pressed = pygame.key.get_pressed()

        # Déplacement continu
        move_speed = max(1, int(TAILLE_CELLULE / 10))  # Ajuster la vitesse en fonction du zoom
        if keys_pressed[pygame.K_RIGHT]:
            offset_x += move_speed
        if keys_pressed[pygame.K_LEFT]:
            offset_x -= move_speed
        if keys_pressed[pygame.K_DOWN]:
            offset_y += move_speed
        if keys_pressed[pygame.K_UP]:
            offset_y -= move_speed

        # Vérifier si Ctrl ou Cmd est enfoncé (Cmd sur macOS)
        is_ctrl_pressed = (
            keys_pressed[pygame.K_LCTRL] or
            keys_pressed[pygame.K_RCTRL] or
            keys_pressed[pygame.K_LMETA] or
            keys_pressed[pygame.K_RMETA]
        )

        for event in pygame.event.get():
            manager.process_events(event)  # Traiter d'abord les événements avec pygame_gui

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    # Barre d'espace pour pause/lecture
                    en_marche = not en_marche

                elif event.key == pygame.K_n:
                    # Avancer d'une étape
                    enregistrer_historique(moteur, historique, index_historique)
                    index_historique += 1
                    moteur.etape_suivante(settings['survie'], settings['naissance'])

                elif event.key == pygame.K_a and is_ctrl_pressed:
                    # Basculement du mode de sélection
                    selection_mode = not selection_mode
                    selecting = False
                    selected_cells.clear()
                    selection_start = None
                    selection_end = None
                    print(f"Mode de sélection {'activé' if selection_mode else 'désactivé'}.")

                elif event.key == pygame.K_c and is_ctrl_pressed:
                    if selected_cells:
                        # Copier les cellules sélectionnées
                        copied_cells = set(selected_cells)
                        print("Cellules copiées.")

                elif event.key == pygame.K_v and is_ctrl_pressed:
                    if copied_cells:
                        # Coller les cellules copiées à la position de la souris avec prévisualisation
                        x_souris, y_souris = pygame.mouse.get_pos()
                        if x_souris < grid_width and y_souris < screen_height - status_bar_height - patterns_bar_height:
                            x_offset_pos = x_souris // TAILLE_CELLULE + offset_x
                            y_offset_pos = y_souris // TAILLE_CELLULE + offset_y
                            # Calculer l'offset de collage basé sur la première cellule copiée
                            min_x = min(cell[0] for cell in copied_cells)
                            min_y = min(cell[1] for cell in copied_cells)
                            paste_offset = (x_offset_pos - min_x, y_offset_pos - min_y)

                            # Prévisualisation
                            preview_cells = set()
                            for cell in copied_cells:
                                x, y = cell
                                dx = x + paste_offset[0]
                                dy = y + paste_offset[1]
                                preview_cells.add((dx, dy))

                            # Afficher la prévisualisation jusqu'à confirmation
                            pasting = True
                            while pasting:
                                for evt in pygame.event.get():
                                    manager.process_events(evt)
                                    if evt.type == pygame.QUIT:
                                        pygame.quit()
                                        return
                                    elif evt.type == pygame.KEYDOWN:
                                        if evt.key == pygame.K_RETURN:
                                            # Coller les cellules
                                            for cell in preview_cells:
                                                moteur.ajouter_cellule(*cell)
                                            pasting = False
                                            print("Cellules collées.")
                                        elif evt.key == pygame.K_ESCAPE:
                                            # Annuler le collage
                                            pasting = False
                                            print("Collage annulé.")
                                    elif evt.type == pygame.MOUSEMOTION:
                                        x_souris, y_souris = evt.pos
                                        if x_souris < grid_width and y_souris < screen_height - status_bar_height - patterns_bar_height:
                                            x_offset_pos = x_souris // TAILLE_CELLULE + offset_x
                                            y_offset_pos = y_souris // TAILLE_CELLULE + offset_y
                                            paste_offset = (x_offset_pos - min_x, y_offset_pos - min_y)
                                            preview_cells = set()
                                            for cell in copied_cells:
                                                x, y = cell
                                                dx = x + paste_offset[0]
                                                dy = y + paste_offset[1]
                                                preview_cells.add((dx, dy))

                                # Dessiner la prévisualisation
                                screen.fill(COULEUR_FOND)
                                draw_grid(screen, grid_width, screen_height - status_bar_height - patterns_bar_height, TAILLE_CELLULE, COULEUR_LIGNE, offset_x, offset_y)
                                draw_cells(screen, moteur.cellules_vivantes, TAILLE_CELLULE, offset_x, offset_y, grid_width, screen_height - status_bar_height - patterns_bar_height, COULEUR_CELLULE)
                                # Dessiner la prévisualisation en vert
                                draw_cells(screen, preview_cells, TAILLE_CELLULE, offset_x, offset_y, grid_width, screen_height - status_bar_height - patterns_bar_height, (0, 255, 0))
                                # Dessiner la barre des motifs
                                pygame.draw.rect(screen, (20, 20, 20), patterns_bar_rect)
                                # Dessiner la barre d'outils
                                pygame.draw.rect(screen, (20, 20, 20), status_bar_rect)
                                manager.update(time_delta)
                                manager.draw_ui(screen)
                                pygame.display.flip()
                                clock.tick(60)
                            # Sortir de la boucle de collage
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_souris, y_souris = event.pos
                if placing_pattern and selected_pattern:
                    if event.button == 1:  # Clic gauche pour placer le motif
                        if x_souris < grid_width and y_souris < screen_height - status_bar_height - patterns_bar_height:
                            x_offset_pos = x_souris // TAILLE_CELLULE + offset_x
                            y_offset_pos = y_souris // TAILLE_CELLULE + offset_y

                            # Placer le motif
                            for cell in selected_pattern:
                                x, y = cell
                                px = x_offset_pos + x
                                py = y_offset_pos + y
                                moteur.ajouter_cellule(px, py)

                            placing_pattern = False
                            selected_pattern = None
                            print("Motif placé.")
                    elif event.button == 3:  # Clic droit pour annuler
                        placing_pattern = False
                        selected_pattern = None
                        print("Placement annulé.")
                else:
                    # Vérifier si le clic n'est pas sur la barre d'outils ou la barre des motifs
                    if x_souris < grid_width and y_souris < screen_height - status_bar_height - patterns_bar_height:
                        x = x_souris // TAILLE_CELLULE + offset_x
                        y = y_souris // TAILLE_CELLULE + offset_y
                        if event.button == 1:  # Clic gauche
                            if selection_mode:
                                # Démarrer la sélection
                                selection_start = (x, y)
                                selection_end = (x, y)
                                selecting = True
                                selected_cells.clear()
                            else:
                                if (x, y) in moteur.cellules_vivantes:
                                    moteur.supprimer_cellule(x, y)
                                else:
                                    moteur.ajouter_cellule(x, y)
                        elif event.button == 3:  # Clic droit pour annuler la sélection
                            if selection_mode:
                                selection_mode = False
                                selecting = False
                                selected_cells.clear()
                                selection_start = None
                                selection_end = None
                                print("Mode de sélection désactivé.")
                        elif event.button == 4:  # Molette vers le haut (zoom avant)
                            TAILLE_CELLULE = min(TAILLE_CELLULE + 2, 100)
                        elif event.button == 5:  # Molette vers le bas (zoom arrière)
                            TAILLE_CELLULE = max(TAILLE_CELLULE - 2, 2)

            elif event.type == pygame.MOUSEMOTION:
                if selection_mode and selecting:
                    x_souris, y_souris = event.pos
                    if x_souris < grid_width and y_souris < screen_height - status_bar_height - patterns_bar_height:
                        x = x_souris // TAILLE_CELLULE + offset_x
                        y = y_souris // TAILLE_CELLULE + offset_y
                        selection_end = (x, y)
                        selected_cells = get_cells_in_selection(moteur, selection_start, selection_end)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selection_mode and selecting:
                    selecting = False

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons['reset']:
                    moteur.cellules_vivantes.clear()
                    historique.clear()
                    analyseur.historique_pop.clear()
                    index_historique = -1
                elif event.ui_element == buttons['pause_play']:
                    en_marche = not en_marche
                elif event.ui_element == buttons['graph']:
                    if analyseur.historique_pop:
                        analyseur.tracer_population()
                elif event.ui_element == buttons['random']:
                    moteur.cellules_vivantes.clear()
                    historique.clear()
                    index_historique = -1
                    generate_random_grid(moteur, settings)
                elif event.ui_element == buttons['speed']:
                    # Contrôle de la vitesse (alterner entre 10, 30, 50 FPS)
                    if simulation_speed == 10:
                        simulation_speed = 30
                    elif simulation_speed == 30:
                        simulation_speed = 50
                    else:
                        simulation_speed = 10
                elif event.ui_element == buttons['undo']:
                    if index_historique > 0:
                        index_historique -= 1
                        moteur.cellules_vivantes = historique[index_historique].copy()
                elif event.ui_element == buttons['save']:
                    sauvegarder_grille(moteur.cellules_vivantes)
                elif event.ui_element == buttons['load']:
                    cellules_chargees = charger_grille()
                    if cellules_chargees is not None:
                        moteur.cellules_vivantes = cellules_chargees
                        historique.clear()
                        index_historique = -1
                elif event.ui_element == buttons['detect'] :
                    print(detect_patterns(moteur.cellules_vivantes, predefined_patterns))
                    #test_crapaud(predefined_patterns)
                    print("------------------------------------------------------------------------")
                elif event.ui_element == buttons['calc'] :
                    if affichage_calcul == 0:
                        affichage_calcul = 1
                    else :
                        affichage_calcul = 0

                elif event.ui_element == buttons['selection']:
                    # Basculement du mode de sélection
                    selection_mode = not selection_mode
                    selecting = False
                    selected_cells.clear()
                    selection_start = None
                    selection_end = None
                    print(f"Mode de sélection {'activé' if selection_mode else 'désactivé'}.")
                elif event.ui_element == left_arrow_button:
                    if pattern_scroll_index > 0:
                        pattern_scroll_index -= 1
                        update_pattern_buttons()
                elif event.ui_element == right_arrow_button:
                    if pattern_scroll_index + patterns_visible_count < len(predefined_patterns):
                        pattern_scroll_index += 1
                        update_pattern_buttons()
                elif event.ui_element in pattern_buttons:
                    if hasattr(event.ui_element, 'pattern_data'):
                        selected_pattern = event.ui_element.pattern_data['pattern']
                        placing_pattern = True
                        print(f"Placement du motif '{event.ui_element.pattern_data['name']}'")

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                # Gérer les changements dans les champs de saisie des paramètres
                if event.ui_element == survie_input:
                    try:
                        survie = list(map(int, survie_input.get_text().split(',')))
                        settings['survie'] = survie
                        print("Paramètres de survie mis à jour.")
                    except ValueError:
                        print("Erreur dans les paramètres de survie. Veuillez vérifier vos entrées.")
                elif event.ui_element == naissance_input:
                    try:
                        naissance = list(map(int, naissance_input.get_text().split(',')))
                        settings['naissance'] = naissance
                        print("Paramètres de naissance mis à jour.")
                    except ValueError:
                        print("Erreur dans les paramètres de naissance. Veuillez vérifier vos entrées.")
                elif event.ui_element == prob_input:
                    try:
                        prob = int(prob_input.get_text())
                        settings['birth_probability'] = max(0, min(prob, 100))
                        print("Probabilité de naissance mise à jour.")
                    except ValueError:
                        print("Erreur dans la probabilité de naissance. Veuillez vérifier votre entrée.")
                elif event.ui_element == taille_input:
                    try:
                        taille = int(taille_input.get_text())
                        settings['random_grid_size'] = max(10, taille)
                        print("Taille de la grille aléatoire mise à jour.")
                    except ValueError:
                        print("Erreur dans la taille de la grille. Veuillez vérifier votre entrée.")

        # Mettre à jour le gestionnaire d'interface
        manager.update(time_delta)

        # Logique du jeu en dehors de la boucle des événements
        if en_marche:
            enregistrer_historique(moteur, historique, index_historique)
            index_historique += 1
            moteur.etape_suivante(settings['survie'], settings['naissance'])
            # Enregistrer la population actuelle
            analyseur.enregistrer_population(len(moteur.cellules_vivantes), time_ratio)
        else:
            # Même si la simulation est en pause, on met à jour le graphique
            pass

        # Dessin
        screen.fill(COULEUR_FOND)

        # Dessiner la grille
        draw_grid(screen, grid_width, screen_height - status_bar_height - patterns_bar_height, TAILLE_CELLULE, COULEUR_LIGNE, offset_x, offset_y)

        # Dessiner les cellules vivantes
        draw_cells(screen, moteur.cellules_vivantes, TAILLE_CELLULE, offset_x, offset_y, grid_width, screen_height - status_bar_height - patterns_bar_height, COULEUR_CELLULE)

        # Dessiner la sélection
        if selection_mode and selection_start and selection_end:
            x_start, y_start = selection_start
            x_end, y_end = selection_end
            x1 = (min(x_start, x_end) - offset_x) * TAILLE_CELLULE
            y1 = (min(y_start, y_end) - offset_y) * TAILLE_CELLULE
            x2 = (max(x_start, x_end) - offset_x + 1) * TAILLE_CELLULE
            y2 = (max(y_start, y_end) - offset_y + 1) * TAILLE_CELLULE
            selection_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            pygame.draw.rect(screen, COULEUR_SELECTION, selection_rect, 2)

        # Mettre en surbrillance les cellules sélectionnées
        if selection_mode:
            draw_cells(screen, selected_cells, TAILLE_CELLULE, offset_x, offset_y, grid_width, screen_height - status_bar_height - patterns_bar_height, COULEUR_SELECTION)

        # Prévisualisation du motif en cours de placement
        if placing_pattern and selected_pattern:
            x_souris, y_souris = pygame.mouse.get_pos()
            x_offset_pos = x_souris // TAILLE_CELLULE + offset_x
            y_offset_pos = y_souris // TAILLE_CELLULE + offset_y

            # Calculer les cellules du motif à la position actuelle de la souris
            pattern_cells = set()
            for cell in selected_pattern:
                x, y = cell
                px = x_offset_pos + x
                py = y_offset_pos + y
                pattern_cells.add((px, py))

            # Dessiner la prévisualisation en vert
            draw_cells(screen, pattern_cells, TAILLE_CELLULE, offset_x, offset_y, grid_width, screen_height - status_bar_height - patterns_bar_height, (0, 255, 0))

        # Dessiner la barre des motifs
        pygame.draw.rect(screen, (20, 20, 20), patterns_bar_rect)

        # Dessiner la barre d'outils (status bar)
        pygame.draw.rect(screen, (20, 20, 20), status_bar_rect)

        # Dessiner l'interface pygame_gui
        manager.draw_ui(screen)

        # Obtenir la surface du graphique et l'afficher
        graph_height = screen_height - status_bar_height - patterns_bar_height - settings_panel_height
        plot_surface = analyseur.get_plot_surface()
        plot_surface = pygame.transform.scale(plot_surface, (graph_width, int(graph_height)))
        screen.blit(plot_surface, (grid_width, 0))

        if affichage_calcul == 1 :
            # Pour l'affichage du graphique du ratio
            ratio_surface = analyseur.get_ratio_plot_surface()
            ratio_surface = pygame.transform.scale(ratio_surface, (graph_width, int(graph_height)))
            screen.blit(ratio_surface, (grid_width, graph_height))
            pygame.display.flip()
        pygame.display.flip()

    pygame.quit()

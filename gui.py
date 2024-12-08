import pygame
import pygame_gui

def open_settings_window(manager, settings):
    # Créer une fenêtre de réglages
    settings_window_rect = pygame.Rect(100, 100, 450, 400)
    settings_window = pygame_gui.elements.UIWindow(
        rect=settings_window_rect,
        manager=manager,
        window_display_title='Réglages',
        object_id=pygame_gui.core.ObjectID(class_id='@settings_window', object_id='#settings_window')
    )

    # Champs pour les règles de survie
    survie_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 10, 430, 30),
        text='Survie si voisins (Ctrl + A) :',
        manager=manager,
        container=settings_window
    )
    survie_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 40, 430, 30),
        manager=manager,
        container=settings_window,
        object_id=pygame_gui.core.ObjectID(class_id='@survie_input', object_id='#survie_input')
    )
    survie_input.set_text(','.join(map(str, settings['survie'])))

    # Champs pour les règles de naissance
    naissance_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 80, 430, 30),
        text='Naissance si voisins (Ctrl + C) :',
        manager=manager,
        container=settings_window
    )
    naissance_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 110, 430, 30),
        manager=manager,
        container=settings_window,
        object_id=pygame_gui.core.ObjectID(class_id='@naissance_input', object_id='#naissance_input')
    )
    naissance_input.set_text(','.join(map(str, settings['naissance'])))

    # Champs pour la probabilité de naissance
    prob_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 150, 430, 30),
        text='Probabilité de naissance en aléatoire (%) (Ctrl + P) :',
        manager=manager,
        container=settings_window
    )
    prob_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 180, 430, 30),
        manager=manager,
        container=settings_window,
        object_id=pygame_gui.core.ObjectID(class_id='@prob_input', object_id='#prob_input')
    )
    prob_input.set_text(str(settings['birth_probability']))

    # Champs pour la taille de la grille aléatoire
    taille_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 220, 430, 30),
        text='Taille de la grille aléatoire (N x N) (Ctrl + T) :',
        manager=manager,
        container=settings_window
    )
    taille_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 250, 430, 30),
        manager=manager,
        container=settings_window,
        object_id=pygame_gui.core.ObjectID(class_id='@taille_input', object_id='#taille_input')
    )
    taille_input.set_text(str(settings['random_grid_size']))

    # Bouton pour appliquer les changements
    apply_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(175, 310, 100, 40),
        text='Appliquer',
        manager=manager,
        container=settings_window,
        object_id=pygame_gui.core.ObjectID(class_id='@apply_settings', object_id='#apply_settings')
    )

    # Stocker les références dans la fenêtre des réglages
    settings_window.survie_input = survie_input
    settings_window.naissance_input = naissance_input
    settings_window.prob_input = prob_input
    settings_window.taille_input = taille_input
    settings_window.apply_button = apply_button

    return settings_window  # Retourner la référence de la fenêtre

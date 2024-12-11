def detect_patterns(cellules_vivantes, patterns):
    """Détecte les occurrences des motifs dans la grille et retire les cellules vivantes trouvées."""
    detected_counts = {pattern['name']: 0 for pattern in patterns}
    live_cells = set(cellules_vivantes)  # Ensemble des cellules vivantes à analyser

    # Trier les motifs par taille (ordre décroissant)
    patterns = sorted(patterns, key=lambda x: len(x['pattern']), reverse=True)

    # Trier les cellules vivantes d'abord par y (ligne) puis par x (colonne)
    sorted_cells = sorted(live_cells, key=lambda x: (x[1], x[0]))  # Tri par y (lignes) puis x (colonnes)

    # Boucle sur chaque cellule vivante triée
    for cell in sorted_cells:
        x0, y0 = cell

        # Vérifier chaque motif
        for pattern in patterns:
            # Vérifier si le motif est présent dans la grille autour de la cellule courante
            pattern_cells = pattern['pattern']
            # On cherche la cellule la plus en haut à gauche du motif
            x_offset, y_offset = pattern_cells[0]

            # Translater le motif pour aligner la cellule la plus en haut à gauche avec la cellule actuelle
            translated_pattern = [(x - x_offset + x0, y - y_offset + y0) for x, y in pattern_cells]

            # Vérifier si toutes les cellules du motif sont présentes dans les cellules vivantes
            if all((dx, dy) in live_cells for dx, dy in translated_pattern):
                detected_counts[pattern['name']] += 1
                # Retirer les cellules vivantes correspondant au motif trouvé
                live_cells -= set(translated_pattern)  # Enlève les cellules trouvées
                print(f"Pattern '{pattern['name']}' détecté à la position ({x0}, {y0})")
                break  # Motif trouvé, passer au suivant

    return detected_counts

def test_crapaud(patterns):


    # Exemple de cellules vivantes dans une grille 4x4
    cellules_vivantes = [
        (1, 0), (2, 0), (3, 0),  # Première ligne
        (0, 1), (1, 1), (2, 1),  # Deuxième ligne
    ]

    # Liste des motifs à tester

    # Appliquer la fonction de détection
    detected_counts = detect_patterns(cellules_vivantes, patterns)

    # Afficher les résultats
    print(f"Motifs détectés : {detected_counts}")

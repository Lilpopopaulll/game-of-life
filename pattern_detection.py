# pattern_detection.py

def rotate_pattern(pattern):
    """Génère toutes les rotations possibles du motif."""
    rotations = []
    for k in range(4):
        rotated = [(y, -x) for x, y in pattern]  # Rotation de 90 degrés
        rotations.append(rotated)
        pattern = rotated
    return rotations

def translate_pattern(pattern, dx, dy):
    """Translate le motif de (dx, dy)."""
    return [(x + dx, y + dy) for x, y in pattern]

def get_pattern_bounding_box(pattern):
    """Retourne les limites du motif."""
    xs = [x for x, y in pattern]
    ys = [y for x, y in pattern]
    return min(xs), max(xs), min(ys), max(ys)

def detect_patterns(cellules_vivantes, patterns):
    """Détecte les occurrences des motifs dans la grille."""
    detected_counts = {pattern['name']: 0 for pattern in patterns}

    live_cells = set(cellules_vivantes)

    for cell in live_cells:
        x0, y0 = cell
        for pattern in patterns:
            # Générer toutes les rotations du motif
            rotations = rotate_pattern(pattern['pattern'])
            for rotated_pattern in rotations:
                match = True
                for dx, dy in rotated_pattern:
                    x, y = x0 + dx, y0 + dy
                    if (x, y) not in live_cells:
                        match = False
                        break
                if match:
                    detected_counts[pattern['name']] += 1
                    break  # Motif trouvé, pas besoin de vérifier les autres rotations

    return detected_counts

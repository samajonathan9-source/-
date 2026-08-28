# RATISS-skynet : SELECTION QUANTIQUE (Grover-amplifiee) — EXPERIMENTATION.
#
# Inspiration : l'algorithme de Grover amplifie l'amplitude de l'etat marque
# par iterations oracle+diffusion : apres k iterations, la probabilite du
# bon etat passe de p a ~sin^2((2k+1)*arcsin(sqrt(p))).
#
# Adaptation classique : parmi N candidats de generation, chacun a une
# amplitude initiale (probabilite du LLM ~ uniforme) et un MARQUEUR
# topologique (sa coherence P_sig). Les iterations de Grover amplifient
# les candidats coherents et attenuent les autres.
#
# Hypothese testable : la selection Grover-amplifiee choisit des candidats
# PLUS coherents que le simple argmax, surtout quand la coherence est
# dispersee (plusieurs candidats moyens, un bon).
#
# C'est un laboratoire : on teste, on mesure, on itere.

import numpy as np


def grover_amplify(scores, iterations=None):
    """Amplification de Grover sur les scores (classique, simule).

    scores : np.array des coherences des candidats (>= 0)
    Retourne les probabilites amplifiees (somme = 1).

    Principe : oracle = flip de phase proportionnel au score,
    diffusion = inversion autour de la moyenne. Itere optimal ~ pi/4 * sqrt(N/M)
    ou M = nombre de 'bons' candidats (score > mediane).
    """
    scores = np.asarray(scores, dtype=np.float64)
    n = len(scores)
    if n == 0:
        return scores
    if scores.sum() <= 0:
        return np.ones(n) / n

    # amplitudes initiales : racine de la probabilite uniforme
    amp = np.ones(n) / np.sqrt(n)
    # le marqueur : score normalise
    s_norm = scores / scores.max()
    marked = s_norm > np.median(s_norm)
    m = max(1, int(marked.sum()))
    if iterations is None:
        iterations = max(1, int(np.pi / 4 * np.sqrt(n / m)))

    for _ in range(iterations):
        # oracle : phase flip des candidats marques, pondere par le score
        phase = np.exp(1j * np.pi * s_norm)
        amp = amp * phase
        # diffusion : inversion autour de la moyenne (reelle)
        mean = amp.mean()
        amp = 2 * mean - amp

    prob = np.abs(amp) ** 2
    total = prob.sum()
    return prob / total if total > 0 else np.ones(n) / n


def select_grover(candidates, scores, seed=0):
    """Selectionne un candidat par amplification de Grover.

    candidates : liste de textes
    scores : coherence topologique de chaque candidat
    Retourne (index, probabilites amplifiees).
    """
    if not candidates:
        return None, None
    probs = grover_amplify(scores)
    # selection deterministe : le candidat le plus amplifie
    # (Grover mesure l'etat le plus probable)
    idx = int(np.argmax(probs))
    return idx, probs

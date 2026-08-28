# RATISS-skynet : INDUCTION DE REGLE FEW-SHOT (condition AGI n°2 — la centrale).
#
# La fiche AGI : "on lui presente 3 exemples d'une transformation inventee,
# il doit decouvrir la regle et l'appliquer a une 4e entree" (esprit ARC-AGI).
#
# Approche RATIS : pas de recherche de phrase memorisee (le LLM ne peut pas
# tricher). On teste des TRANSFORMATIONS STRUCTURELLES candidates et on
# choisit celle qui est COHERENTE sur tous les exemples. Departage
# topologique : entre deux transformations qui matchent, on prefere celle
# qui preserve la signature de persistance (P_sig) du nuage de points —
# la regle juste conserve la structure, la fausse la brise.
#
# La regle induite est ensuite stockee en memoire procedurale (transfert).

import numpy as np


def grid_to_points(grid):
    """Grille -> nuage de points (x, y) des cellules non nulles."""
    pts = []
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if v:
                pts.append((x, y))
    return np.array(pts, dtype=float) if pts else np.zeros((1, 2))


def _persistence_signature(points):
    """Signature topologique du nuage : persistance H0 (composantes).

    Rips simplifie : on calcule les longueurs d'aretes de l'arbre couvrant
    minimal (MST) — c'est exactement la persistance H0 de Vietoris-Rips.
    Retourne (nb composantes a eps=1.5, energie totale des aretes).
    """
    n = len(points)
    if n < 2:
        return (1, 0.0)
    d = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    in_tree = np.zeros(n, dtype=bool)
    in_tree[0] = True
    edges = []
    for _ in range(n - 1):
        best, bi = np.inf, -1
        for i in range(n):
            if in_tree[i]:
                for j in range(n):
                    if not in_tree[j] and d[i, j] < best:
                        best, bi = d[i, j], j
        in_tree[bi] = True
        edges.append(best)
    edges = np.array(edges)
    n_components = int((edges > 1.5).sum()) + 1
    return (n_components, float(edges.sum()))


# --- Espace d'hypotheses : transformations de grille ---
def _t_identity(g): return [list(r) for r in g]
def _t_rot90(g): return [list(r) for r in zip(*g[::-1])]
def _t_rot180(g): return [r[::-1] for r in g[::-1]]
def _t_rot270(g): return [list(r) for r in zip(*g)][::-1]
def _t_flip_h(g): return [r[::-1] for r in g]
def _t_flip_v(g): return g[::-1]
def _t_transpose(g): return [list(r) for r in zip(*g)]
def _t_invert(g): return [[0 if v else 1 for v in r] for r in g]

TRANSFORMS = {
    "identite": _t_identity, "rot90": _t_rot90, "rot180": _t_rot180,
    "rot270": _t_rot270, "flip_h": _t_flip_h, "flip_v": _t_flip_v,
    "transpose": _t_transpose, "inversion": _t_invert,
}


def induce_rule(examples):
    """Induit la regle depuis des exemples [(input, output), ...].

    Retourne (nom_regle, confiance, detail). confiance = part des exemples
    ou la transformation reproduit exactement la sortie. Departage
    topologique par preservation de la signature de persistance.
    """
    best = []
    for name, T in TRANSFORMS.items():
        hits, topo_err = 0, 0.0
        for inp, out in examples:
            pred = T(inp)
            if pred == out:
                hits += 1
            sig_pred = _persistence_signature(grid_to_points(pred))
            sig_out = _persistence_signature(grid_to_points(out))
            topo_err += abs(sig_pred[0] - sig_out[0]) + abs(sig_pred[1] - sig_out[1]) / 10.0
        score = hits / len(examples)
        best.append((score, -topo_err, name))
    best.sort(reverse=True)
    score, neg_err, name = best[0]
    return name, round(score, 3), {"topo_err": round(-neg_err, 3),
                                   "runner_up": best[1][2]}


def apply_rule(rule_name, new_input):
    """Applique la regle induite a une entree jamais vue."""
    return TRANSFORMS[rule_name](new_input)

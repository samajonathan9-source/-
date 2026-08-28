# Topological score (LCT-style) on a layer of activations.
# Uses science_core (AEON ODV fused) for Vietoris-Rips persistence.

import numpy as np
from ratiss.topo.science_core import rips_persistence


def correlation_distance(acts):
    # Build a correlation matrix, convert to a distance matrix.
    x = acts - acts.mean(axis=0)
    norms = np.linalg.norm(x, axis=0)
    norms[norms == 0] = 1.0
    x = x / norms
    corr = x.T @ x
    corr = np.clip(corr, -1.0,  1.0)
    dist = 1.0 - corr
    np.fill_diagonal(dist, 0.0)
    return dist


def lct_score(acts, max_points =  80):
    # Compute P_sig + edge + entropy on the correlation distance matrix.

    acts = np.asarray(acts,dtype=float)
    n = acts.shape[0]
    step = max(1, n // max_points)
    if step >  1:
        acts = acts[::step]
    n = acts.shape[0]
    if n <  8:
        return  0.0,  0.0,  0.0,  0.0
    dist = correlation_distance(acts)
    res = rips_persistence(dist)
    psig = float(res["psig"])
    betti = int(res["betti"][1])
    edge_val = float(np.mean(dist[dist >  0.0]))
    entropy_val = float(-np.sum(dist * np.log(dist + 1e-9))) / max(1, n * n)
    return psig, edge_val, entropy_val, betti

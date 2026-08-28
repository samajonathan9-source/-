#!/usr/bin/env python3
# RATISS-skynet : Phase 2 - diagnostic LCT sur le VRAI Qwen2-0.5B.
# Memoire bornee : sous-echantillonnage neurones (max 128) + tokens (max 160),
# une couche a la fois, float32, gc agressif.

import os
import sys
import json
import hashlib
import argparse
import gc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import stats

from ratiss.topo.science_core import rips_persistence

PROMPTS_FR = [
    "La topologie algebrique etudie les proprietes invariantes des espaces.",
    "Le cristal de KTN dope au lithium presente une transition de phase.",
    "Le reseau de neurones apprend des representations hierarchiques.",
    "La physique quantique decrit l'etat superpose des particules.",
    "Le Cameroun developpe sa recherche en intelligence artificielle.",
    "La persistance homologique detecte les cycles dans un nuage de points.",
    "Le fine-tuning ajuste les poids d'un modele de langage pre-entraine.",
    "La coherence topologique mesure la structure d'un systeme complexe.",
]
PROMPTS_EN = [
    "Algebraic topology studies invariant properties of spaces.",
    "The lithium-doped KTN crystal exhibits a phase transition.",
    "The neural network learns hierarchical representations.",
    "Quantum physics describes the superposed state of particles.",
    "Persistent homology detects cycles in a point cloud.",
    "Fine-tuning adjusts the weights of a pre-trained language model.",
    "Topological coherence measures the structure of a complex system.",
    "The attention mechanism computes correlations between tokens.",
]


def sha256_hex(payload):
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lct_bounded(acts, max_tokens=160, max_neurons=128, seed=0):
    """Score LCT sur sous-matrice bornee -> (psig, edge, entropy, betti)."""
    rng = np.random.default_rng(seed)
    n_t, n_n = acts.shape
    t_idx = rng.choice(n_t, size=min(max_tokens, n_t), replace=False)
    n_idx = rng.choice(n_n, size=min(max_neurons, n_n), replace=False)
    sub = acts[np.ix_(t_idx, n_idx)].astype(np.float32)
    if sub.shape[0] < 8:
        return 0.0, 0.0, 0.0, 0

    x = sub - sub.mean(axis=0)
    norms = np.linalg.norm(x, axis=0)
    norms[norms == 0] = 1.0
    x = x / norms
    corr = np.clip(x.T @ x, -1.0, 1.0)
    dist = 1.0 - corr
    np.fill_diagonal(dist, 0.0)

    res = rips_persistence(dist)
    psig = float(res["psig"])
    betti = int(res["betti"][1])
    edge_val = float(np.mean(dist[dist > 0.0]))
    entropy_val = float(-np.sum(dist * np.log(dist + 1e-9))) / dist.size
    return psig, edge_val, entropy_val, betti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2-0.5B")
    ap.add_argument("--n-boot", type=int, default=6)
    ap.add_argument("--max-length", type=int, default=24)
    ap.add_argument("--out", default="artifacts/lct_diagnostic_qwen.json")
    args = ap.parse_args()

    print("RATISS-skynet : diagnostic LCT sur QWEN (memoire bornee)")
    print("=" * 60)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.float32, attn_implementation="eager"
    )
    model.eval()
    n_layers = model.config.num_hidden_layers
    hidden = model.config.hidden_size
    prompts = PROMPTS_FR + PROMPTS_EN
    print(f"couches: {n_layers} | hidden: {hidden} | prompts: {len(prompts)}")
    print("=" * 60)

    collected = [[] for _ in range(n_layers)]
    for text in prompts:
        inputs = tok(text, return_tensors="pt", truncation=True, max_length=args.max_length)
        with torch.no_grad():
            out = model(**inputs, output_hidden_states=True)
        for li in range(n_layers):
            collected[li].append(out.hidden_states[li + 1][0].cpu().numpy())
        del out, inputs
        gc.collect()
    del model
    gc.collect()

    rows = []
    boot_psig = []
    for i in range(n_layers):
        mat = np.concatenate(collected[i], axis=0)
        n_t = mat.shape[0]
        psig, edge, ent, betti = lct_bounded(mat, seed=i)
        boots = [lct_bounded(mat, seed=100 + i * 10 + b)[0] for b in range(args.n_boot)]
        boot_psig.append(np.array(boots))
        rows.append({
            "layer": i, "psig": round(psig, 4),
            "psig_mean": round(float(np.mean(boots)), 4),
            "psig_std": round(float(np.std(boots)), 4),
            "edge": round(edge, 4), "entropy": round(ent, 4),
            "H1": betti, "n_tokens": n_t,
        })
        print(f"layer {i:2d} psig={psig:.4f} boot={np.mean(boots):.4f}+-{np.std(boots):.4f} "
              f"edge={edge:.4f} ent={ent:.4f} H1={betti}")
        collected[i] = None
        gc.collect()

    h_stat, p_value = stats.kruskal(*boot_psig)
    psig_arr = np.array([r["psig"] for r in rows])
    contrast = float(psig_arr.max() - psig_arr.min())
    ratio = float(psig_arr.max() / max(psig_arr.min(), 1e-9))

    print("=" * 60)
    print(f"Kruskal-Wallis: H={h_stat:.2f}  p={p_value:.3e}")
    print(f"contraste P_sig: max-min={contrast:.4f}  ratio={ratio:.1f}x")
    verdict = "CONTRASTE SIGNIFICATIF (p<0.05)" if p_value < 0.05 else "PAS DE CONTRASTE SIGNIFICATIF"
    print(f"VERDICT Phase 2: {verdict}")

    payload = json.dumps(rows, sort_keys=True, indent=2)
    result = {
        "generator": "Qwen2-0.5B real activations (memory-bounded)",
        "model": args.model, "n_layers": n_layers, "hidden_size": hidden,
        "n_prompts": len(prompts), "n_boot": args.n_boot,
        "rows": rows,
        "kruskal_H": round(float(h_stat), 3), "kruskal_p": float(p_value),
        "contrast_max_min": round(contrast, 4), "contrast_ratio": round(ratio, 2),
        "verdict": verdict,
        "sha256_proof": sha256_hex(payload),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"preuve SHA-256: {result['sha256_proof']}")
    print(f"rapport ecrit: {args.out}")


if __name__ == "__main__":
    main()

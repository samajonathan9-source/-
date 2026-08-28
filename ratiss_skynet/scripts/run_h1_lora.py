#!/usr/bin/env python3
# RATISS-skynet : Phase 3 - H1 LoRA cible (guide par LCT) vs LoRA uniforme.
# A budget de parametres EGAL. Succes : cible >= uniforme sur perplexite,
# avec >=20% de parametres en moins (ou a egalite, meilleure perplexite).

import os
import sys
import json
import hashlib
import argparse
import gc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "RATISS-One"))

import numpy as np

TRAIN_TEXTS = [
    "La topologie algebrique etudie les proprietes invariantes des espaces par deformation continue.",
    "Le cristal ferroelectrique KTN dope au lithium presente une transition de phase photo-induite.",
    "La persistance homologique detecte les cycles et les cavities dans un nuage de points.",
    "Le fine-tuning LoRA ajuste des matrices de faible rang dans les couches d'attention.",
    "La coherence topologique mesure la structure globale d'un systeme complexe.",
    "Un graphe de correlations entre neurones revele les zones critiques du reseau.",
    "La detection d'anomalies topologiques precede les methodes statistiques classiques.",
    "Le repliement topologique correspond a un changement de phase du systeme.",
    "Les diagrams de persistance resument la forme des donnees a plusieurs echelles.",
    "La loi de coherence topologique guide l'allocation des parametres d'apprentissage.",
    "Un modele de langage apprend des representations hierarchiques du texte.",
    "La robustesse au bruit est une propriete structurelle des systemes topologiques.",
]

EVAL_TEXTS = [
    "La topologie algebrique etudie les invariants des espaces topologiques.",
    "Le cristal KTN lithium subit une transition de phase sous lumiere.",
    "La persistance homologique revele les cycles des donnees.",
    "Le fine-tuning LoRA modifie peu de parametres dans l'attention.",
]


def sha256_hex(payload):
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def count_trainable(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def perplexity(model, tok, texts, max_length=48):
    import torch
    model.eval()
    losses = []
    with torch.no_grad():
        for t in texts:
            enc = tok(t, return_tensors="pt", truncation=True, max_length=max_length)
            ids = enc["input_ids"]
            out = model(**enc, labels=ids)
            losses.append(out.loss.item())
    mean_loss = float(np.mean(losses))
    return float(np.exp(mean_loss)), mean_loss


def load_lct_scores(path):
    with open(path) as f:
        d = json.load(f)
    return {r["layer"]: r["psig"] for r in d["rows"]}


def allocate_ranks_uniform(n_layers, total_rank):
    base = total_rank // n_layers
    rem = total_rank % n_layers
    ranks = [base + (1 if i < rem else 0) for i in range(n_layers)]
    return {i: ranks[i] for i in range(n_layers)}


def allocate_ranks_lct(psig_by_layer, total_rank, n_layers, rmin=1, rmax=16):
    """Alloue le rang LoRA proportionnellement a P_sig (zones critiques = rang eleve)."""
    vals = np.array([psig_by_layer.get(i, 0.0) for i in range(n_layers)], dtype=float)
    if vals.sum() <= 0:
        return allocate_ranks_uniform(n_layers, total_rank)
    w = vals / vals.max()  # 0..1
    raw = rmin + w * (rmax - rmin)
    # Ajuster pour respecter le budget total approximativement
    scale = total_rank / raw.sum()
    ranks = np.clip(np.round(raw * scale), 1, rmax * 2).astype(int)
    return {i: int(ranks[i]) for i in range(n_layers)}


def build_lora_model(model, rank_map, target_modules=("q_proj", "v_proj")):
    """LoRA avec rang par couche (pattern d'inclusion + rank_pattern PEFT)."""
    from peft import LoraConfig, get_peft_model
    target_layers = [i for i, rr in rank_map.items() if rr > 0]
    target_modules_full = [
        f"model.layers.{i}.self_attn.{m}"
        for i in target_layers for m in target_modules
    ]
    rank_pattern = {
        f"model.layers.{i}.self_attn.{m}": int(rank_map[i])
        for i in target_layers for m in target_modules
    }
    r_default = max(1, int(round(float(np.mean([rank_map[i] for i in target_layers])))))
    lcfg = LoraConfig(
        r=r_default, lora_alpha=2 * r_default, lora_dropout=0.0, bias="none",
        task_type="CAUSAL_LM",
        target_modules=target_modules_full,
        rank_pattern=rank_pattern,
    )
    return get_peft_model(model, lcfg), r_default, target_layers


def train_lora(model, tok, texts, steps=60, lr=1e-3, max_length=48, seed=0):
    import torch
    torch.manual_seed(seed)
    model.train()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    rng = np.random.default_rng(seed)
    for step in range(steps):
        t = texts[rng.integers(0, len(texts))]
        enc = tok(t, return_tensors="pt", truncation=True, max_length=max_length)
        ids = enc["input_ids"]
        out = model(**enc, labels=ids)
        loss = out.loss
        loss.backward()
        opt.step()
        opt.zero_grad()
        if (step + 1) % 20 == 0:
            print(f"  step {step+1}/{steps} loss={loss.item():.4f}")
    return model


def run_condition(name, rank_map, lct_path, args):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32, attn_implementation="eager"
    )
    # perplexite de base (sans fine-tuning)
    ppl0, _ = perplexity(model, tok, EVAL_TEXTS, args.max_length)
    peft_model, r, layers = build_lora_model(model, rank_map)
    n_params = count_trainable(peft_model)
    print(f"[{name}] rang moyen r={r}, couches cibles={len(layers)}, params entrainables={n_params:,}")
    peft_model = train_lora(peft_model, tok, TRAIN_TEXTS,
                            steps=args.steps, lr=args.lr,
                            max_length=args.max_length, seed=args.seed)
    ppl1, loss1 = perplexity(peft_model, tok, EVAL_TEXTS, args.max_length)
    res = {
        "name": name, "r_mean": r, "n_target_layers": len(layers),
        "trainable_params": int(n_params),
        "ppl_before": round(ppl0, 3), "ppl_after": round(ppl1, 3),
        "loss_after": round(loss1, 4),
        "improvement_pct": round(100 * (ppl0 - ppl1) / ppl0, 2),
    }
    print(f"[{name}] ppl {ppl0:.2f} -> {ppl1:.2f} ({res['improvement_pct']}%)")
    del model, peft_model
    gc.collect()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lct", default=os.path.join(REPO_ROOT, "artifacts", "lct_diagnostic.json"))
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--max-length", type=int, default=48)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--total-rank", type=int, default=120)  # budget rang total
    ap.add_argument("--out", default="artifacts/h1_lora_results.json")
    args = ap.parse_args()

    print("RATISS-skynet : Phase 3 - H1 LoRA cible (LCT) vs uniforme")
    print("=" * 60)

    from transformers import AutoConfig
    cfg = AutoConfig.from_pretrained(MODEL_DIR)
    n_layers = cfg.num_hidden_layers
    print(f"couches: {n_layers} | budget rang total: {args.total_rank}")

    psig = load_lct_scores(args.lct)
    uniform_map = allocate_ranks_uniform(n_layers, args.total_rank)
    r_uni = uniform_map[0]
    # Budget PARAMETRES egal : uniforme touche 30 couches a rang r_uni.
    # LCT touche seulement les K couches les plus riches en P_sig, a rang r_t,
    # tel que K * r_t = n_layers * r_uni (meme nb total de parametres LoRA).
    order = sorted(range(n_layers), key=lambda i: -psig.get(i, 0.0))
    K = max(4, n_layers // 2)  # 15 couches cibles
    r_t = max(1, round(n_layers * r_uni / K))
    lct_map = {i: (r_t if i in order[:K] else 0) for i in range(n_layers)}
    print(f"uniforme: 30 couches x r={r_uni} = {30*r_uni} rang-unites")
    print(f"lct_cible: {K} couches x r={r_t} = {K*r_t} rang-unites (budget egal)")

    print("rang uniforme par couche:", [uniform_map[i] for i in range(n_layers)])
    print("rang LCT par couche:     ", [lct_map[i] for i in range(n_layers)])
    print("=" * 60)

    results = []
    results.append(run_condition("uniforme", uniform_map, args.lct, args))
    results.append(run_condition("lct_cible", lct_map, args.lct, args))

    u, c = results[0], results[1]
    param_ratio = c["trainable_params"] / max(1, u["trainable_params"])
    verdict_h1 = (
        "SUCCES" if (c["ppl_after"] <= u["ppl_after"] and c["trainable_params"] <= u["trainable_params"])
        else "PARTIEL" if c["ppl_after"] <= u["ppl_after"]
        else "ECHEC (a iterer)"
    )
    print("=" * 60)
    print(f"uniforme : {u['trainable_params']:,} params, ppl {u['ppl_before']} -> {u['ppl_after']}")
    print(f"lct_cible: {c['trainable_params']:,} params, ppl {c['ppl_before']} -> {c['ppl_after']}")
    print(f"ratio params cible/uniforme: {param_ratio:.2f}")
    print(f"VERDICT H1: {verdict_h1}")

    payload = json.dumps(results, sort_keys=True, indent=2)
    out = {
        "hypothesis": "H1 - LoRA cible par score LCT vs LoRA uniforme (budget egal)",
        "model": "RATISS-One", "n_layers": n_layers,
        "total_rank_budget": args.total_rank, "steps": args.steps, "lr": args.lr,
        "uniform_rank_map": uniform_map, "lct_rank_map": lct_map,
        "results": results,
        "param_ratio_cible_sur_uniforme": round(param_ratio, 3),
        "verdict_h1": verdict_h1,
        "sha256_proof": sha256_hex(payload),
    }
    outpath = os.path.join(REPO_ROOT, args.out)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"preuve SHA-256: {out['sha256_proof']}")
    print(f"rapport ecrit: {outpath}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# RATISS-skynet : Phase 4 - benchmark H1 robuste, moyenne sur N seeds,
# plus de donnees d'entrainement, test statistique appaire (Wilcoxon/t-test).

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
from scipy import stats

# Corpus d'entrainement plus riche (topologie/physique/IA) pour reduire le bruit
TRAIN_TEXTS = [
    "La topologie algebrique etudie les proprietes invariantes des espaces par deformation continue.",
    "Le cristal ferroelectrique KTN dope au lithium presente une transition de phase photo-induite.",
    "La persistance homologique detecte les cycles et les cavities dans un nuage de points.",
    "Le fine-tuning LoRA ajuste des matrices de faible rang dans les couches d'attention.",
    "La coherence topologique mesure la structure globale d'un systeme complexe.",
    "Un graphe de correlations entre neurones revele les zones critiques du reseau.",
    "La detection d'anomalies topologiques precede les methodes statistiques classiques.",
    "Le repliement topologique correspond a un changement de phase du systeme.",
    "Les diagrammes de persistance resument la forme des donnees a plusieurs echelles.",
    "La loi de coherence topologique guide l'allocation des parametres d'apprentissage.",
    "Un modele de langage apprend des representations hierarchiques du texte.",
    "La robustesse au bruit est une propriete structurelle des systemes topologiques.",
    "L'homologie de Vietoris-Rips construit un complexe simplicial a partir d'un nuage.",
    "Le score P_sig somme les persistances des cycles de dimension un.",
    "L'entropie des correlations penalise le desordre dans le graphe de neurones.",
    "Un reseau de neurones profond encode des features de plus en plus abstraites.",
    "La transition de phase marque un changement qualitatif dans l'organisation du systeme.",
    "Le couplage entre couches revele la structure fonctionnelle du modele.",
    "La metrique LCT combine persistance, correlation de bord et entropie.",
    "Un sous-reseau critique concentre l'essentiel de la capacite d'apprentissage.",
]

EVAL_TEXTS = [
    "La topologie algebrique etudie les invariants des espaces topologiques.",
    "Le cristal KTN lithium subit une transition de phase sous lumiere.",
    "La persistance homologique revele les cycles des donnees.",
    "Le fine-tuning LoRA modifie peu de parametres dans l'attention.",
    "La coherence topologique capture la structure globale du reseau.",
    "Un changement de phase modifie l'organisation des correlations.",
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
            out = model(**enc, labels=enc["input_ids"])
            losses.append(out.loss.item())
    return float(np.exp(np.mean(losses)))


def load_lct_scores(path):
    with open(path) as f:
        d = json.load(f)
    return {r["layer"]: r["psig"] for r in d["rows"]}


def allocate_ranks_uniform(n_layers, total_rank):
    base = total_rank // n_layers
    return {i: base for i in range(n_layers)}


def build_lora_model(model, rank_map, target_modules=("q_proj", "v_proj")):
    from peft import LoraConfig, get_peft_model
    target_layers = [i for i, rr in rank_map.items() if rr > 0]
    target_modules_full = [
        f"model.layers.{i}.self_attn.{m}" for i in target_layers for m in target_modules
    ]
    rank_pattern = {
        f"model.layers.{i}.self_attn.{m}": int(rank_map[i])
        for i in target_layers for m in target_modules
    }
    r_default = max(1, int(round(float(np.mean([rank_map[i] for i in target_layers])))))
    lcfg = LoraConfig(
        r=r_default, lora_alpha=2 * r_default, lora_dropout=0.0, bias="none",
        task_type="CAUSAL_LM", target_modules=target_modules_full,
        rank_pattern=rank_pattern,
    )
    return get_peft_model(model, lcfg)


def train_lora(model, tok, texts, steps, lr, max_length, seed):
    import torch
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.train()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    rng = np.random.default_rng(seed)
    for step in range(steps):
        t = texts[rng.integers(0, len(texts))]
        enc = tok(t, return_tensors="pt", truncation=True, max_length=max_length)
        out = model(**enc, labels=enc["input_ids"])
        out.loss.backward()
        opt.step()
        opt.zero_grad()
    return model


def run_once(name, rank_map, args, seed):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32, attn_implementation="eager"
    )
    ppl0 = perplexity(model, tok, EVAL_TEXTS, args.max_length)
    peft_model = build_lora_model(model, rank_map)
    n_params = count_trainable(peft_model)
    peft_model = train_lora(peft_model, tok, TRAIN_TEXTS, args.steps, args.lr, args.max_length, seed)
    ppl1 = perplexity(peft_model, tok, EVAL_TEXTS, args.max_length)
    del model, peft_model
    gc.collect()
    return {"name": name, "seed": seed, "params": n_params,
            "ppl_before": round(ppl0, 2), "ppl_after": round(ppl1, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lct", default=os.path.join(REPO_ROOT, "artifacts", "lct_diagnostic.json"))
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--max-length", type=int, default=48)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--total-rank", type=int, default=60)
    ap.add_argument("--out", default="artifacts/h1_robust_results.json")
    args = ap.parse_args()

    print("RATISS-skynet : Phase 4 - benchmark H1 robuste (multi-seeds)")
    print("=" * 60)

    from transformers import AutoConfig
    n_layers = AutoConfig.from_pretrained(MODEL_DIR).num_hidden_layers
    psig = load_lct_scores(args.lct)

    uniform_map = allocate_ranks_uniform(n_layers, args.total_rank)
    r_uni = uniform_map[0]
    order = sorted(range(n_layers), key=lambda i: -psig.get(i, 0.0))
    K = max(4, n_layers // 2)
    r_t = max(1, round(n_layers * r_uni / K))
    lct_map = {i: (r_t if i in order[:K] else 0) for i in range(n_layers)}
    print(f"uniforme: {n_layers}x r={r_uni} | lct_cible: {K}x r={r_t} | budget egal")
    print("=" * 60)

    uni_ppl, cib_ppl = [], []
    records = []
    for s in args.seeds:
        ru = run_once("uniforme", uniform_map, args, s)
        rc = run_once("lct_cible", lct_map, args, s)
        uni_ppl.append(ru["ppl_after"])
        cib_ppl.append(rc["ppl_after"])
        records += [ru, rc]
        print(f"seed {s}: uniforme ppl={ru['ppl_after']}  cible ppl={rc['ppl_after']}  (params={ru['params']})")

    uni_ppl = np.array(uni_ppl)
    cib_ppl = np.array(cib_ppl)
    diff = uni_ppl - cib_ppl  # >0 => cible meilleur (ppl plus bas)
    t_stat, p_val = stats.ttest_rel(uni_ppl, cib_ppl)
    try:
        w_stat, w_p = stats.wilcoxon(uni_ppl, cib_ppl)
    except Exception:
        w_stat, w_p = float("nan"), float("nan")

    print("=" * 60)
    print(f"uniforme : ppl moyenne {uni_ppl.mean():.2f} +- {uni_ppl.std():.2f}")
    print(f"lct_cible: ppl moyenne {cib_ppl.mean():.2f} +- {cib_ppl.std():.2f}")
    print(f"diff moyenne (uni-cib) = {diff.mean():.2f}  | t={t_stat:.2f} p={p_val:.4f} | wilcoxon p={w_p:.4f}")
    gagne = cib_ppl.mean() < uni_ppl.mean() and p_val < 0.10
    verdict = "SUCCES (cible < uniforme, significatif)" if gagne else (
        "EQUIVALENT (pas de difference significative)" if p_val >= 0.10 else "ECHEC")
    print(f"VERDICT H1 robuste: {verdict}")

    payload = json.dumps(records, sort_keys=True, indent=2)
    out = {
        "hypothesis": "H1 robuste - LoRA cible LCT vs uniforme, multi-seeds",
        "model": "RATISS-One", "n_layers": n_layers,
        "steps": args.steps, "lr": args.lr, "seeds": args.seeds,
        "total_rank_budget": args.total_rank,
        "uniform_mean_ppl": round(float(uni_ppl.mean()), 2),
        "uniform_std_ppl": round(float(uni_ppl.std()), 2),
        "cible_mean_ppl": round(float(cib_ppl.mean()), 2),
        "cible_std_ppl": round(float(cib_ppl.std()), 2),
        "t_stat": round(float(t_stat), 3), "t_p": float(p_val),
        "wilcoxon_p": float(w_p),
        "records": records,
        "verdict_h1_robust": verdict,
        "sha256_proof": sha256_hex(payload),
    }
    outpath = os.path.join(REPO_ROOT, args.out)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"preuve SHA-256: {out['sha256_proof']}")
    print(f"rapport ecrit: {outpath}")


if __name__ == "__main__":
    main()

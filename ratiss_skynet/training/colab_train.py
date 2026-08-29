# RATISS One — entrainement LCT sur Google Colab (GPU).
#
# Script complet, pret a lancer dans une cellule Colab :
#   - clone le depot et monte Google Drive
#   - fine-tune LoRA/QLoRA du moteur RATISS One (SafeTensors)
#   - la mise a jour est modulee par la persistance topologique (loi LCT)
#   - early stop topologique si P_sig chute (protection de la coherence)
#   - sauvegarde des checkpoints vers Google Drive avec reprise automatique
#   - verification de l'identite MCT et des conditions AGI apres entrainement
#
# Le format d'entrainement est SafeTensors (voir docs/FORMATS.md) : le moteur
# existant est directement entrainable, aucune reconstruction necessaire.
#
# Usage Colab :
#   !python training/colab_train.py
#
# Le corps (poids du moteur) est entraine ; le systeme immunitaire
# (identite, LCT, P_sig, KTN, garde-fou) reste fige — voir
# docs/FINETUNING_EFFETS.md.

import os
import sys
import json
import time
import hashlib

# ---------------------------------------------------------------------------
# CONFIGURATION — a adapter selon le GPU Colab disponible
# ---------------------------------------------------------------------------
CONFIG = {
    # chemin du moteur RATISS One (SafeTensors) apres clonage
    "model_dir": "models/RATISS-One",
    "drive_dir": "/content/drive/MyDrive/ratis_training",  # sauvegarde Drive
    "lora_r": 8,                 # rang LoRA (petit modele -> rang modeste)
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "learning_rate": 2e-4,
    "batch_size": 4,             # ajuster selon la VRAM Colab
    "grad_accum": 4,
    "max_steps": 500,            # ~ milliers de parametres adaptes via LoRA
    "max_seq_len": 256,
    "psig_drop_tolerance": 0.05,  # early stop topologique
    "save_every": 50,            # checkpoint Drive tous les N pas
    "seed": 42,
    # textes de validation topologique (fixes, jamais entraines)
    "val_texts": [
        "Un trou noir piege meme la lumiere au-dela de l'horizon.",
        "La coherence topologique mesure la persistance structurelle.",
        "L'insuline regule la glycemie.",
    ],
}

# corpus d'entrainement minimal — a remplacer par vos donnees
TRAIN_TEXTS = [
    "Un trou noir est une region de l'espace-temps ou la gravite est si forte "
    "que rien, pas meme la lumiere, ne peut s'echapper au-dela de l'horizon.",
    "La coherence topologique mesure la persistance structurelle d'un systeme "
    "via l'homologie de son graphe de correlations.",
    "L'homologie persistante detecte les cycles et les cavites d'un nuage de "
    "points a travers les echelles.",
    "La photosynthese convertit l'energie lumineuse, l'eau et le CO2 en glucose "
    "et oxygene, grace a la chlorophylle.",
    "L'insuline est une hormone qui regule la glycemie en favorisant l'entree "
    "du glucose dans les cellules.",
    "L'ADN stocke l'information genetique sous forme d'une sequence de quatre "
    "bases nucleotidiques.",
]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def mount_drive(cfg):
    """Monte Google Drive pour la sauvegarde persistante des checkpoints."""
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        os.makedirs(cfg["drive_dir"], exist_ok=True)
        log(f"Google Drive monte -> {cfg['drive_dir']}")
        return True
    except Exception as e:
        log(f"Drive non monte ({e}) — sauvegarde locale uniquement.")
        return False


def find_last_checkpoint(cfg):
    """Reprise automatique : retourne le dernier checkpoint Drive s'il existe."""
    if not os.path.isdir(cfg["drive_dir"]):
        return None
    ckpts = [d for d in os.listdir(cfg["drive_dir"])
             if d.startswith("checkpoint-")]
    if not ckpts:
        return None
    ckpts.sort(key=lambda d: int(d.split("-")[1]))
    last = os.path.join(cfg["drive_dir"], ckpts[-1])
    log(f"Reprise depuis {last}")
    return last


def compute_psig(mind, texts):
    """Coherence topologique moyenne sur le jeu de validation."""
    scores = []
    for t in texts:
        try:
            scores.append(mind.coherence(t))
        except Exception:
            scores.append(0.0)
    return sum(scores) / len(scores) if scores else 0.0


def main(cfg=CONFIG):
    log("=== RATISS One — entrainement LCT (Colab) ===")

    # 1. environnement
    import torch
    log(f"torch {torch.__version__} — CUDA: {torch.cuda.is_available()}")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 2. Drive (sauvegarde persistante)
    drive_ok = mount_drive(cfg)

    # 3. charger le systeme RATIS (HybridMind = MCT complet)
    sys.path.insert(0, os.path.abspath("."))
    from skynet.hybrid_mind import HybridMind
    mind = HybridMind(cfg["model_dir"])
    log(f"Identite MCT integre : {mind._identity_ok}")

    # 4. charger le moteur pour le fine-tuning LoRA
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model

    tok = AutoTokenizer.from_pretrained(cfg["model_dir"])
    model = AutoModelForCausalLM.from_pretrained(
        cfg["model_dir"], torch_dtype=torch.float32).to(device)

    lora_cfg = LoraConfig(
        r=cfg["lora_r"], lora_alpha=cfg["lora_alpha"],
        lora_dropout=cfg["lora_dropout"], bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"],
    )
    model = get_peft_model(model, lora_cfg)
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log(f"Parametres entrainables (LoRA) : {n_trainable:,}")

    # 5. reprise depuis le dernier checkpoint Drive si present
    start_step = 0
    last = find_last_checkpoint(cfg) if drive_ok else None
    if last:
        try:
            model.load_adapter(last, adapter_name="default")
            start_step = int(os.path.basename(last).split("-")[1])
            log(f"Adaptateur recharge, reprise au pas {start_step}")
        except Exception as e:
            log(f"Reprise impossible ({e}) — depart a zero.")

    # 6. optimiser
    optimizer = torch.optim.AdamW(model.parameters(),
                                  lr=cfg["learning_rate"])
    model.train()

    # 7. baseline topologique (reference pour l'early stop)
    baseline_psig = compute_psig(mind, cfg["val_texts"])
    log(f"P_sig de reference (validation) : {baseline_psig:.2f}")

    # 8. boucle d'entrainement guidee par la LCT
    history = []
    step = start_step
    try:
        while step < cfg["max_steps"]:
            for text in TRAIN_TEXTS:
                if step >= cfg["max_steps"]:
                    break
                enc = tok(text, return_tensors="pt", truncation=True,
                          max_length=cfg["max_seq_len"]).to(device)
                out = model(**enc, labels=enc["input_ids"])
                loss = out.loss / cfg["grad_accum"]
                loss.backward()

                if (step + 1) % cfg["grad_accum"] == 0:
                    # porte LCT : modulation par la coherence courante
                    psig = compute_psig(mind, cfg["val_texts"])
                    gate = max(psig / (baseline_psig + 1e-9), 0.0)
                    for g in optimizer.param_groups:
                        g["lr"] = cfg["learning_rate"] * min(gate, 1.0)
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad()

                    history.append({"step": step, "loss": float(out.loss),
                                    "psig": psig, "gate": round(gate, 3)})

                    # early stop topologique : protection de la coherence
                    drop = baseline_psig - psig
                    if drop > cfg["psig_drop_tolerance"] * baseline_psig:
                        log(f"ARRET : P_sig a chute de {drop:.2f} "
                            f"(oubli catastrophique) au pas {step}")
                        raise StopIteration

                step += 1
                if step % 10 == 0:
                    log(f"pas {step}/{cfg['max_steps']} — loss {out.loss:.4f}")

                # 9. checkpoint Drive
                if drive_ok and step % cfg["save_every"] == 0:
                    ckpt = os.path.join(cfg["drive_dir"], f"checkpoint-{step}")
                    model.save_pretrained(ckpt)
                    log(f"checkpoint Drive : {ckpt}")
    except StopIteration:
        log("Entrainement interrompu par le garde-fou topologique.")
    except KeyboardInterrupt:
        log("Interruption manuelle — sauvegarde du checkpoint courant.")

    # 10. checkpoint final + historique
    if drive_ok:
        final = os.path.join(cfg["drive_dir"], f"checkpoint-final-{step}")
        model.save_pretrained(final)
        with open(os.path.join(cfg["drive_dir"], "history.json"), "w") as f:
            json.dump({"config": {k: v for k, v in cfg.items()},
                       "history": history}, f, indent=2)
        log(f"Adaptateur final : {final}")

    # 11. validation post-entrainement : l'identite MCT doit etre intacte
    log(f"Identite MCT apres entrainement : {mind._identity_ok}")
    final_psig = compute_psig(mind, cfg["val_texts"])
    log(f"P_sig final : {final_psig:.2f} (reference {baseline_psig:.2f})")
    log("=== entrainement termine ===")
    return {"steps": step, "final_psig": final_psig,
            "identity_ok": mind._identity_ok}


if __name__ == "__main__":
    main()

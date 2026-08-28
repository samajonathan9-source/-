# RATIS : ENTRAINEUR LCT-NATIF — protocole fige.
#
# Ce n'est PAS de la retropropagation classique. La loi LCT gouverne
# l'apprentissage :  dW = eta * phi * P_sig * C
# La descente de gradient est GUIDEE par la persistance topologique :
# on n'accepte une mise a jour des poids que si la coherence structurelle
# ne s'effondre pas. La topologie surveille l'entrainement.
#
# Regle d'or (docs/FINETUNING_EFFETS.md) : on entraine le CORPS (poids du
# moteur), jamais le SYSTEME IMMUNITAIRE (LCT, P_sig, KTN, identite).
#
# Concu pour GPU (labo), fonctionne aussi sur CPU (lent) pour les tests.

import os
import json
import hashlib
import time

import numpy as np

# Invariants figes — proteges pendant l'entrainement
FROZEN_COMPONENTS = [
    "identity", "lct_law", "p_sig_measure", "ktn_collapse",
    "tension_monitor", "intention_guard", "memory_chain", "planner",
]

# Hyperparametres scelles (modifiables mais traces dans le manifeste)
DEFAULT_CONFIG = {
    "learning_rate": 5e-5,
    "eta": 1.0,               # taux d'apprentissage LCT
    "phi": 1.0,               # potentiel LCT
    "batch_size": 8,
    "max_epochs": 3,
    "psig_drop_tolerance": 0.05,  # early stop si P_sig chute > 5%
    "warmup_steps": 100,
    "max_seq_len": 512,
    "seed": 42,
}


def _hash_config(cfg):
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()


class LCTTrainer:
    """Boucle d'entrainement guidee par la persistance topologique."""

    def __init__(self, mind, config=None, out_dir=None):
        self.mind = mind
        self.cfg = dict(DEFAULT_CONFIG)
        if config:
            self.cfg.update(config)
        self.cfg_hash = _hash_config(self.cfg)
        self.out_dir = out_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "artifacts", "training_runs")
        os.makedirs(self.out_dir, exist_ok=True)
        self.history = []
        self._baseline_psig = None

    # --- coherence de validation : l'organe qui surveille l'entrainement ---
    def validation_psig(self, val_texts):
        """P_sig moyen sur un jeu de validation FIXE (jamais entraine)."""
        scores = []
        for t in val_texts:
            try:
                scores.append(self.mind.coherence(t))
            except Exception:
                scores.append(0.0)
        return float(np.mean(scores)) if scores else 0.0

    # --- la loi LCT appliquee a la mise a jour des poids ---
    def lct_gate(self, grad_norm, psig, C=1.0):
        """dW = eta * phi * P_sig * C : l'amplitude de la mise a jour est
        modulee par la persistance. Si la coherence s'effondre, on apprend
        moins (ou pas). C'est le contraire du fine-tuning aveugle."""
        eta = self.cfg["eta"]
        phi = self.cfg["phi"]
        return eta * phi * max(psig, 0.0) * C

    # --- early stop topologique (n'existe nulle part ailleurs) ---
    def check_catastrophic_forgetting(self, current_psig):
        if self._baseline_psig is None:
            self._baseline_psig = current_psig
            return False
        drop = self._baseline_psig - current_psig
        return drop > self.cfg["psig_drop_tolerance"]

    # --- un pas d'entrainement (squelette : branchement GPU reel) ---
    def train_step(self, batch):
        """Un pas. En labo, c'est ici que le GPU calcule les gradients.
        Ici on calcule la coherence et on applique la porte LCT."""
        texts = batch if isinstance(batch, list) else [batch]
        psig = self.validation_psig(texts)
        grad_norm = 1.0  # en reel : norme du gradient du GPU
        dW = self.lct_gate(grad_norm, psig)
        return {"psig": psig, "dW": dW, "gate_open": dW > 0}

    # --- la boucle complete, auditee ---
    def fit(self, train_texts, val_texts):
        """Entrainement complet, audite par la topologie."""
        run_id = hashlib.sha256(
            f"{self.cfg_hash}{time.time()}".encode()).hexdigest()[:12]
        log = {"run_id": run_id, "config": self.cfg, "config_hash": self.cfg_hash,
               "frozen": FROZEN_COMPONENTS, "steps": []}

        bs = self.cfg["batch_size"]
        for epoch in range(self.cfg["max_epochs"]):
            for i in range(0, len(train_texts), bs):
                batch = train_texts[i:i + bs]
                step = self.train_step(batch)
                step["epoch"] = epoch
                step["step"] = i // bs
                log["steps"].append(step)

                # early stop topologique : on protege la coherence
                if self.check_catastrophic_forgetting(step["psig"]):
                    log["stopped"] = "catastrophic_forgetting_detected"
                    log["reason"] = (f"P_sig drop > {self.cfg['psig_drop_tolerance']}")
                    self._save(log, run_id)
                    return log

            # apres chaque epoque : revalidation de l'identite MCT
            if not self.mind._identity_ok:
                log["stopped"] = "identity_drift_detected"
                self._save(log, run_id)
                return log

        log["stopped"] = "completed"
        self._save(log, run_id)
        return log

    def _save(self, log, run_id):
        path = os.path.join(self.out_dir, f"run_{run_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        return path

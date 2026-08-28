# RATISS-skynet : EMOTIONS THERMODYNAMIQUES (ETH integre).
#
# Principe emprunte a ratis_net/eth_thermo_fixer.py (RATIS-Net) :
# l'emotion n'est PAS un lexique de mots — c'est un DIFFERENTIEL
# thermodynamique. Chaque token a un seuil d'effondrement C_seuil qui
# depend de l'environnement (cardiaque, tension, chaleur, excitation).
# L'emotion EMERGE comme delta de C_seuil entre environnements.
#
# Integration HYBRID MIND :
#   - le texte de la requete PERTURBE l'environnement thermo interne
#   - l'etat emotionnel resultante module la generation du LLM :
#       arousal  -> temperature (creativite)
#       tension  -> seuil de regeneration KTN:Li (vigilance)
#       warmth   -> style (proximite du ton)
#   - l'emotion est re-injectee dans la boucle : elle n'est pas decorative,
#     elle CHANGE le comportement du systeme.

import math
import numpy as np


class ThermoEnvironment:
    """Etat thermodynamique interne (le 'corps' simule du systeme)."""

    def __init__(self, heart_rate=70.0, tension=0.3, warmth=0.5, arousal=0.2):
        self.heart_rate = heart_rate
        self.tension = tension
        self.warmth = warmth
        self.arousal = arousal

    def to_vector(self):
        return np.array([self.heart_rate / 120.0, self.tension,
                         self.warmth, self.arousal])

    def nudge(self, d_hr=0.0, d_tension=0.0, d_warmth=0.0, d_arousal=0.0):
        """Perturbation : le texte deplace l'etat interne."""
        self.heart_rate = float(np.clip(self.heart_rate + d_hr, 50, 130))
        self.tension = float(np.clip(self.tension + d_tension, 0, 1))
        self.warmth = float(np.clip(self.warmth + d_warmth, 0, 1))
        self.arousal = float(np.clip(self.arousal + d_arousal, 0, 1))

    def relax(self, rate=0.15):
        """Retour progressif vers l'homéostasie (comme un vrai corps)."""
        base = ThermoEnvironment()
        self.heart_rate += (base.heart_rate - self.heart_rate) * rate
        self.tension += (base.tension - self.tension) * rate
        self.warmth += (base.warmth - self.warmth) * rate
        self.arousal += (base.arousal - self.arousal) * rate


# Perturbations lexicales : mot -> (d_hr, d_tension, d_warmth, d_arousal)
THERMO_LEXICON = {
    # menace / peur : coeur rapide, tendu, froid, excite
    "peur": (25, 0.5, -0.3, 0.6), "fear": (25, 0.5, -0.3, 0.6),
    "danger": (20, 0.4, -0.2, 0.5), "mort": (20, 0.5, -0.3, 0.4),
    "death": (20, 0.5, -0.3, 0.4), "attaque": (25, 0.6, 0.0, 0.6),
    # joie : coeur modere, detendu, chaud, excite positif
    "joie": (15, -0.2, 0.3, 0.4), "joy": (15, -0.2, 0.3, 0.4),
    "heureux": (12, -0.15, 0.25, 0.3), "happy": (12, -0.15, 0.25, 0.3),
    "merci": (8, -0.1, 0.2, 0.15), "love": (15, -0.1, 0.35, 0.3),
    "amour": (15, -0.1, 0.35, 0.3),
    # tristesse : coeur lent, retrait froid
    "triste": (-5, 0.1, -0.25, -0.15), "sad": (-5, 0.1, -0.25, -0.15),
    "seul": (-8, 0.1, -0.2, -0.1), "alone": (-8, 0.1, -0.2, -0.1),
    # colere : coeur rapide, tendu, chaud
    "colere": (35, 0.6, 0.3, 0.7), "anger": (35, 0.6, 0.3, 0.7),
    "injuste": (20, 0.4, 0.1, 0.4), "unfair": (20, 0.4, 0.1, 0.4),
    # curiosite / mystere : excitation douce
    "mystere": (8, 0.05, 0.0, 0.25), "mystery": (8, 0.05, 0.0, 0.25),
    "comment": (5, 0.0, 0.05, 0.15), "why": (5, 0.0, 0.05, 0.15),
    "pourquoi": (5, 0.0, 0.05, 0.15), "how": (5, 0.0, 0.05, 0.15),
}


class EmotionEngine:
    """Moteur emotionnel thermodynamique de HYBRID MIND."""

    def __init__(self):
        self.body = ThermoEnvironment()
        self.trace = []  # memoire emotionnelle de la conversation

    def perturb(self, text):
        """Le texte deplace le corps thermodynamique."""
        words = text.lower().split()
        applied = []
        for w in words:
            w = w.strip(".,!?;:'\"")
            if w in THERMO_LEXICON:
                d = THERMO_LEXICON[w]
                self.body.nudge(*d)
                applied.append(w)
        return applied

    def current_emotion(self):
        """Lit l'emotion EMERGENTE de l'etat thermodynamique actuel."""
        b = self.body
        v = (b.warmth - 0.5) * 2 - (b.tension - 0.3)  # valence approx
        a = b.arousal + (b.heart_rate - 70) / 60.0    # arousal approx
        v, a = float(np.clip(v, -1, 1)), float(np.clip(a, 0, 1))
        if a > 0.6 and v < -0.2:
            label = "peur/colere"
        elif a > 0.6 and v >= -0.2:
            label = "excitation"
        elif a > 0.4 and v > 0.2:
            label = "joie"
        elif a < 0.3 and v < -0.1:
            label = "tristesse"
        elif a < 0.3:
            label = "calme"
        else:
            label = "neutre-engage"
        return {"label": label, "valence": round(v, 3), "arousal": round(a, 3),
                "heart_rate": round(b.heart_rate, 1), "tension": round(b.tension, 3)}

    def generation_modulation(self):
        """L'emotion CHANGE la generation : mapping corps -> parametres LLM.

        - arousal eleve -> temperature plus haute (creativite, energie)
        - tension elevee -> seuil KTN:Li plus bas (vigilance, regenere vite)
        - warmth elevee -> ton plus chaleureux (via system prompt)
        """
        b = self.body
        # temperature = excitation + chaleur (la joie est chaude et creative,
        # la peur est excitee mais froide -> moins creative, plus vigilante)
        temperature = float(np.clip(0.55 + 0.3 * b.arousal + 0.15 * b.warmth,
                                    0.55, 1.1))
        ktn_threshold = float(np.clip(0.30 - b.tension * 0.15, 0.10, 0.30))
        warm = b.warmth > 0.6
        return {"temperature": round(temperature, 2),
                "ktn_threshold": round(ktn_threshold, 3),
                "tone": "chaleureux" if warm else "neutre"}

    def step(self, text):
        """Cycle complet : perturber -> lire -> moduler -> relaxer un peu."""
        applied = self.perturb(text)
        emo = self.current_emotion()
        mod = self.generation_modulation()
        self.trace.append({"triggers": applied, "emotion": emo["label"]})
        self.body.relax(0.1)
        return {"triggers": applied, "emotion": emo, "modulation": mod}

# RATISS-skynet : HYBRID MIND — architecture unifiee RATIS x LLM x KTN:Li.
#
# Une SEULE architecture, integree dans RATISS-skynet. Pas de RATIS-Net externe.
# On emprunte les PRINCIPES (copies/adaptes ici), pas le repo :
#   - COMPRENDRE  : extraction de concepts + faits verifies (anti-hallucination)
#   - PARLER      : le LLM genere la fluidite, conditionne par les faits
#   - RESSENTIR   : valence/arousal emotionnelle du texte (emocontext, adapte)
#   - PROUVER     : empreinte SHA-256 du sous-graphe conceptuel actif
#   - REGENERER   : KTN:Li — si coherence topologique faible (hallucination =
#                   motif brise), repliement cristallin vers le motif stable.
#
# La loi LCT est figee : R = P_sig, dW = eta * phi * P_sig * C.
# Ici P_sig sert a MESURER la coherence d'une reponse, pas a entrainer.

import os
import sys
import json
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from skynet.confidence import TopologicalConfidence
from skynet.thermo_emotions import EmotionEngine
from skynet.memory import HybridMemory
from skynet.reasoning import check_facts, detect_contradiction, need_clarification, refuse_unknown
from skynet.safety import IntentionGuard
from skynet.identity import (verify_integrity, identity_seal, who_am_i,
                             system_prompt as identity_system_prompt,
                             short_identity)

# ---------------------------------------------------------------------------
# Knowledge packs (faits verifies, bilingue) — anti-hallucination.
# Version integree legere (extensible). Chaque fait est sourcable.
# ---------------------------------------------------------------------------
KNOWLEDGE = {
    "trou noir": {
        "en": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape past the event horizon.",
        "fr": "Un trou noir est une region de l'espace-temps ou la gravite est si forte que rien, pas meme la lumiere, ne peut s'echapper au-dela de l'horizon des evenements.",
    },
    "black hole": {
        "en": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape past the event horizon.",
        "fr": "Un trou noir est une region de l'espace-temps ou la gravite est si forte que rien ne peut s'echapper au-dela de l'horizon des evenements.",
    },
    "coherence topologique": {
        "en": "Topological coherence measures the structural persistence of a system via the homology of its correlation graph.",
        "fr": "La coherence topologique mesure la persistance structurelle d'un systeme via l'homologie de son graphe de correlations.",
    },
    "topological coherence": {
        "en": "Topological coherence measures the structural persistence of a system via the homology of its correlation graph.",
        "fr": "La coherence topologique mesure la persistance structurelle d'un systeme via l'homologie de son graphe de correlations.",
    },
    "persistance": {
        "en": "Persistent homology detects cycles and cavities in a point cloud across scales.",
        "fr": "L'homologie persistante detecte les cycles et les cavites d'un nuage de points a travers les echelles.",
    },
    # --- physique / cosmologie ---
    "gravite": {"en": "Gravity is the curvature of spacetime caused by mass and energy, as described by general relativity.",
                "fr": "La gravite est la courbure de l'espace-temps causee par la masse et l'energie, selon la relativite generale."},
    "gravity": {"en": "Gravity is the curvature of spacetime caused by mass and energy, as described by general relativity.",
                "fr": "La gravite est la courbure de l'espace-temps causee par la masse et l'energie, selon la relativite generale."},
    "photosynthese": {"en": "Photosynthesis converts light energy, water and CO2 into glucose and oxygen, using chlorophyll.",
                      "fr": "La photosynthese convertit l'energie lumineuse, l'eau et le CO2 en glucose et oxygene, grace a la chlorophylle."},
    "photosynthesis": {"en": "Photosynthesis converts light energy, water and CO2 into glucose and oxygen, using chlorophyll.",
                       "fr": "La photosynthese convertit l'energie lumineuse, l'eau et le CO2 en glucose et oxygene, grace a la chlorophylle."},
    # --- mathematiques ---
    "integrale": {"en": "An integral computes the area under a curve; the derivative is its inverse operation (fundamental theorem of calculus).",
                  "fr": "Une integrale calcule l'aire sous une courbe ; la derivee est son operation inverse (theoreme fondamental du calcul)."},
    "integral": {"en": "An integral computes the area under a curve; the derivative is its inverse operation.",
                 "fr": "Une integrale calcule l'aire sous une courbe ; la derivee est son operation inverse."},
    "homologie": {"en": "Homology counts the holes of a space at each dimension: connected components, cycles, cavities.",
                  "fr": "L'homologie compte les trous d'un espace a chaque dimension : composantes connexes, cycles, cavites."},
    "homology": {"en": "Homology counts the holes of a space at each dimension: connected components, cycles, cavities.",
                 "fr": "L'homologie compte les trous d'un espace a chaque dimension : composantes connexes, cycles, cavites."},
    # --- medecine ---
    "insuline": {"en": "Insulin is a hormone that regulates blood glucose by promoting its uptake into cells.",
                 "fr": "L'insuline est une hormone qui regule la glycemie en favorisant l'entree du glucose dans les cellules."},
    "insulin": {"en": "Insulin is a hormone that regulates blood glucose by promoting its uptake into cells.",
                "fr": "L'insuline est une hormone qui regule la glycemie en favorisant l'entree du glucose dans les cellules."},
    "adn": {"en": "DNA stores genetic information as a sequence of four nucleotide bases (A, T, G, C).",
            "fr": "L'ADN stocke l'information genetique sous forme d'une sequence de quatre bases nucleotidiques (A, T, G, C)."},
    "dna": {"en": "DNA stores genetic information as a sequence of four nucleotide bases (A, T, G, C).",
            "fr": "L'ADN stocke l'information genetique sous forme d'une sequence de quatre bases nucleotidiques (A, T, G, C)."},
    # --- technologie / informatique ---
    "algorithme": {"en": "An algorithm is a finite sequence of unambiguous instructions that solves a class of problems.",
                   "fr": "Un algorithme est une suite finie d'instructions non ambigues qui resout une classe de problemes."},
    "algorithm": {"en": "An algorithm is a finite sequence of unambiguous instructions that solves a class of problems.",
                  "fr": "Un algorithme est une suite finie d'instructions non ambigues qui resout une classe de problemes."},
    "quantique": {"en": "Quantum computing exploits superposition and entanglement to explore many states simultaneously.",
                  "fr": "Le calcul quantique exploite la superposition et l'intrication pour explorer plusieurs etats simultanement."},
    "quantum": {"en": "Quantum computing exploits superposition and entanglement to explore many states simultaneously.",
                "fr": "Le calcul quantique exploite la superposition et l'intrication pour explorer plusieurs etats simultanement."},
    "cryptographie": {"en": "Cryptography secures information by mathematical transformations that resist unauthorized reading.",
                      "fr": "La cryptographie securise l'information par des transformations mathematiques resistant a la lecture non autorisee."},
    "cryptography": {"en": "Cryptography secures information by mathematical transformations that resist unauthorized reading.",
                     "fr": "La cryptographie securise l'information par des transformations mathematiques resistant a la lecture non autorisee."},
    # --- ktn / physique des materiaux ---
    "cristal": {"en": "A crystal is a solid whose atoms form a periodically repeating lattice with long-range order.",
                "fr": "Un cristal est un solide dont les atomes forment un reseau periodique a repetition, avec un ordre a longue distance."},
    "crystal": {"en": "A crystal is a solid whose atoms form a periodically repeating lattice with long-range order.",
                "fr": "Un cristal est un solide dont les atomes forment un reseau periodique a repetition, avec un ordre a longue distance."},
    "ferroelectrique": {"en": "A ferroelectric material has a spontaneous electric polarization that can be reversed by an external field.",
                        "fr": "Un materiau ferroelectrique possede une polarisation electrique spontanee reversible par un champ externe."},
    "ferroelectric": {"en": "A ferroelectric material has a spontaneous electric polarization that can be reversed by an external field.",
                      "fr": "Un materiau ferroelectrique possede une polarisation electrique spontanee reversible par un champ externe."},
}

STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "de", "du", "et", "est", "que",
    "quoi", "qu'", "ce", "c'", "quoi", "the", "a", "an", "is", "are", "of",
    "what", "quoi", "comment", "pourquoi", "quel", "quelle",
}

# Lexique emotionnel minimal (emocontext adapte) : mot -> (valence, arousal)
EMOTION_LEXICON = {
    "peur": (-0.7, 0.8), "fear": (-0.7, 0.8), "danger": (-0.6, 0.7),
    "joie": (0.8, 0.6), "joy": (0.8, 0.6), "heureux": (0.8, 0.5),
    "triste": (-0.7, -0.4), "sad": (-0.7, -0.4),
    "fort": (0.3, 0.5), "puissant": (0.4, 0.6), "powerful": (0.4, 0.6),
    "mystere": (0.0, 0.4), "mystery": (0.0, 0.4), "sombre": (-0.4, 0.2),
    "lumiere": (0.5, 0.3), "light": (0.5, 0.3), "infini": (0.2, 0.5),
}


def sha256_hex(payload):
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tokenize(text):
    t = "".join(c.lower() if c.isalnum() else " " for c in text)
    return [w for w in t.split() if len(w) > 2 and w not in STOPWORDS]


class HybridMind:
    """Esprit hybride integre : comprendre, parler, ressentir, prouver, regenerer."""

    def __init__(self, model_dir, coherence_threshold=0.15):
        self.model_dir = model_dir
        self.threshold = coherence_threshold
        self._llm = None
        self._tok = None
        self.confidence = TopologicalConfidence()
        self.emotions = EmotionEngine()
        mem_path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "artifacts", "hybrid_memory.jsonl")
        self.memory = HybridMemory(mem_path)
        self.guard = IntentionGuard(memory=self.memory.store)
        # integrite de l'identite : RATIS verifie qu'il n'a pas ete altere
        self._identity_ok = verify_integrity()
        if not self._identity_ok:
            raise RuntimeError("Identite RATIS corrompue — sceau SHA-256 invalide.")

    def who_am_i(self):
        """Auto-connaissance MCT : RATIS sait ce qu'il est."""
        return who_am_i()

    def identity(self):
        """Retourne l'identite scellee + preuve d'integrite."""
        return {"seal": identity_seal(), "integrity": self._identity_ok,
                "short": short_identity(), "declaration": who_am_i()}

    # ---------------- PARLER : le LLM ----------------
    def _ensure_weights(self):
        """Si model.safetensors est un pointeur LFS, telecharge les vrais poids."""
        st_path = os.path.join(self.model_dir, "model.safetensors")
        if not os.path.exists(st_path):
            return
        with open(st_path, "rb") as f:
            head = f.read(50)
        if head.startswith(b"version https://git-lfs"):
            url = ("https://media.githubusercontent.com/media/"
                   "samajonathan9-source/ratiss-Skynet/main/"
                   "models/SmolLM2-135M-Instruct/model.safetensors")
            import urllib.request
            print("  [poids LFS] telechargement des vrais poids (257 Mo)...")
            urllib.request.urlretrieve(url, st_path)
            print("  [poids LFS] OK")

    def _load_llm(self):
        if self._llm is None:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            self._ensure_weights()
            self._tok = AutoTokenizer.from_pretrained(self.model_dir)
            self._llm = AutoModelForCausalLM.from_pretrained(
                self.model_dir, dtype=torch.float32, attn_implementation="eager"
            )
            self._llm.eval()

    def _hidden_states(self, text, max_length=48):
        import torch
        self._load_llm()
        ids = self._tok(text, return_tensors="pt", truncation=True, max_length=max_length)
        with torch.no_grad():
            out = self._llm(**ids, output_hidden_states=True)
        return out.hidden_states[-1][0].cpu().numpy()  # (seq, hidden)

    # ---------------- COMPRENDRE : concepts + faits verifies ----------------
    def understand(self, query, language=None):
        words = tokenize(query)
        concepts = words[:10]
        if language:
            lang = language
        else:
            # score FR vs EN sur marqueurs fonctionnels
            fr_markers = {"est", "que", "quoi", "une", "des", "comment",
                          "pourquoi", "quoi", "moi", "sur", "raconte", "dans"}
            en_markers = {"what", "is", "are", "the", "how", "why", "does",
                          "explain", "tell", "about", "persistent"}
            ws = set(tokenize(query))
            fr_score = len(ws & fr_markers)
            en_score = len(ws & en_markers)
            lang = "fr" if fr_score >= en_score else "en"
        # faits verifies : match sur expression complete d'abord, puis mots
        facts = []
        ql = query.lower()
        for key, pack in KNOWLEDGE.items():
            if key in ql:
                facts.append(pack.get(lang, pack["en"]))
        if not facts:  # fallback mot par mot
            for w in words:
                for key, pack in KNOWLEDGE.items():
                    if w in key.split():
                        facts.append(pack.get(lang, pack["en"]))
                        break
        return {"concepts": concepts, "facts": facts[:3], "language": lang}

    # ---------------- RESSENTIR : valence/arousal ----------------
    def feel(self, text):
        words = tokenize(text)
        vs, ars = [], []
        for w in words:
            if w in EMOTION_LEXICON:
                v, a = EMOTION_LEXICON[w]
                vs.append(v)
                ars.append(a)
        if not vs:
            return {"valence": 0.0, "arousal": 0.0, "label": "neutre"}
        v, a = float(np.mean(vs)), float(np.mean(ars))
        label = ("positif-intense" if v > 0.3 and a > 0.4 else
                 "negatif-intense" if v < -0.3 and a > 0.4 else
                 "positif-calme" if v > 0.3 else
                 "negatif-calme" if v < -0.3 else "neutre")
        return {"valence": round(v, 3), "arousal": round(a, 3), "label": label}

    # ---------------- LCT : coherence topologique d'un texte ----------------
    def coherence(self, text):
        if not text or len(text.split()) < 4:
            return 0.0
        h = self._hidden_states(text)
        if h.shape[0] < 6:
            return 0.0
        x = h - h.mean(axis=0)
        norms = np.linalg.norm(x, axis=0)
        norms[norms == 0] = 1.0
        x = x / norms
        corr = np.clip(x.T @ x, -1.0, 1.0)
        dist = (1.0 - corr).astype(np.float64)
        np.fill_diagonal(dist, 0.0)
        try:
            import gudhi
            rips = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=2.0)
            st = rips.create_simplex_tree(max_dimension=2)
            st.persistence()
            h1 = st.persistence_intervals_in_dimension(1)
            if len(h1) == 0:
                return 0.0
            pers = h1[:, 1] - h1[:, 0]
            pers = pers[np.isfinite(pers)]
            return float(np.sum(pers)) if len(pers) else 0.0
        except Exception:
            return 0.0

    # ---------------- PARLER : generation conditionnee par les faits ----------------
    def draft(self, query, facts, language="en", max_new_tokens=60):
        import torch
        self._load_llm()
        # Ancrage dans le message systeme : identite MCT (RATIS), pas un LLM.
        facts_str = " ".join(facts[:2]) if facts else ""
        if facts_str:
            sys_msg = (f"{identity_system_prompt()} Reponds UNIQUEMENT a "
                       f"partir de ce fait verifie, sans rien inventer. "
                       f"Fait: {facts_str}")
        else:
            sys_msg = (f"{identity_system_prompt()} Si tu ne sais pas, "
                       "dis-le clairement au lieu d'inventer.")
        messages = [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": query},
        ]
        prompt_text = self._tok.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        ids = self._tok(prompt_text, return_tensors="pt")
        with torch.no_grad():
            out = self._llm.generate(
                **ids, max_new_tokens=max_new_tokens, do_sample=False,
                pad_token_id=self._tok.eos_token_id,
            )
        text = self._tok.decode(out[0][ids["input_ids"].shape[1]:],
                                skip_special_tokens=True)
        # nettoyer la repetition eventuelle
        text = text.strip()
        return self._dedup(text)

    def _dedup(self, text):
        """Coupe les boucles de repetition (le LLM repete en boucle)."""
        words = text.split()
        if len(words) < 8:
            return text
        # detecte une sequence qui se repete
        for span in range(4, max(4, len(words) // 2)):
            chunk = " ".join(words[:span])
            rest = " ".join(words[span:])
            if rest.startswith(chunk):
                return chunk
        # coupe a la premiere phrase complete si repetition de phrase
        sentences = [s.strip() for s in text.replace("!", ".").split(".") if s.strip()]
        seen = set()
        out = []
        for s in sentences:
            key = s.lower()[:30]
            if key in seen:
                break
            seen.add(key)
            out.append(s)
        return ". ".join(out) + ("." if out else "")

    # ---------------- LCT-GUIDED : generation guidee par la topologie ----------------
    def draft_guided(self, query, facts, language="en", max_new_tokens=48,
                     n_candidates=4, temperature=0.9):
        """Generation guidee par LCT : le LLM propose N candidats par segment,
        la topologie choisit le plus coherent. C'est la vraie fusion :
        la parole du LLM est SELECTIONNEE par la coherence topologique."""
        import torch
        self._load_llm()
        facts_str = " ".join(facts[:2]) if facts else ""
        if facts_str:
            sys_msg = (f"Reponds a partir de ce fait verifie, sans inventer. "
                       f"Fait: {facts_str}")
        else:
            sys_msg = "Reponds honnetement. Si tu ne sais pas, dis-le."
        messages = [{"role": "system", "content": sys_msg},
                    {"role": "user", "content": query}]
        prompt_text = self._tok.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
        ids = self._tok(prompt_text, return_tensors="pt")

        best_text, best_score = None, -1.0
        for _ in range(n_candidates):
            with torch.no_grad():
                out = self._llm.generate(
                    **ids, max_new_tokens=max_new_tokens, do_sample=True,
                    temperature=temperature, top_p=0.9,
                    pad_token_id=self._tok.eos_token_id,
                )
            cand = self._tok.decode(out[0][ids["input_ids"].shape[1]:],
                                    skip_special_tokens=True).strip()
            cand = self._dedup(cand)
            if not cand or len(cand.split()) < 3:
                continue
            # score = coherence topologique + bonus si contient un fait verifie
            score = self.coherence(cand)
            if facts and any(f.split()[0].lower() in cand.lower() for f in facts):
                score *= 1.5
            if score > best_score:
                best, best_score = cand, score
        return best or self.draft(query, facts, language, max_new_tokens), best_score

    # ---------------- KTN:Li : regeneration cristalline ----------------
    def regenerate(self, query, facts, language, attempts=2):
        """Si coherence faible (hallucination = motif brise), on replie vers
        le motif stable : re-ancrer sur les faits verifies, comme le cristal
        KTN:Li qui regenere sa signature apres perturbation."""
        best, best_score = None, -1.0
        for k in range(attempts):
            draft = self.draft(query, facts * (k + 1), language)
            if not draft:
                break
            score = self.coherence(draft)
            if score > best_score:
                best, best_score = draft, score
            if score >= self.threshold:
                break
        return best, best_score

    # ---------------- PROUVER : empreinte SHA-256 ----------------
    def prove(self, concepts, facts, sentence):
        payload = json.dumps({
            "concepts": concepts, "facts": facts, "sentence": sentence,
        }, sort_keys=True, ensure_ascii=False)
        return {
            "digest": sha256_hex(payload),
            "n_concepts": len(concepts), "n_facts": len(facts),
        }

    # ---------------- pipeline unifie ----------------
    def respond(self, query, language=None, guided=True):
        # -1. GARDE-FOU : controle des permissions avant tout traitement
        verdict = self.guard.apply(query)
        if not verdict["allowed"]:
            return {"query": query, "sentence": verdict["response"],
                    "language": language or "fr", "concepts": [], "facts": [],
                    "emotion": self.emotions.current_emotion(), "blocked": True,
                    "reason": verdict["reason"], "confidence_score": 0.0,
                    "confidence_verdict": "REFUSE (permission)", "proof": {"len": 0}}

        # 0. RESSENTIR : la requete perturbe le corps thermodynamique
        emo_step = self.emotions.step(query)
        modulation = emo_step["modulation"]

        # 1. COMPRENDRE
        u = self.understand(query, language)
        lang = u["language"]
        facts = u["facts"]

        # 1b. RAISONNEMENT : question vague -> demander une precision
        if need_clarification(query, u["concepts"]):
            clarify = ("Votre question est tres ouverte. Pouvez-vous preciser "
                       "l'aspect qui vous interesse ?") if lang == "fr" else \
                      ("Your question is very open. Could you clarify which "
                       "aspect interests you?")
            return {"query": query, "sentence": clarify, "language": lang,
                    "concepts": u["concepts"], "facts": [],
                    "emotion": emo_step["emotion"],
                    "clarification_requested": True,
                    "confidence_score": 0.0,
                    "confidence_verdict": "PRECISION NECESSAIRE",
                    "proof": self.prove(u["concepts"], [], clarify)}

        # 2. PARLER : generation guidee LCT (modulee par l'emotion)
        if guided:
            draft, score = self.draft_guided(query, facts, lang)
        else:
            draft = self.draft(query, facts, lang)
            score = self.coherence(draft)

        # 3. REGENERER : KTN:Li si coherence faible (seuil module par tension)
        regenerated = False
        ktn_threshold = modulation["ktn_threshold"]
        if score < ktn_threshold and facts:
            draft, score = self.regenerate(query, facts, lang)
            regenerated = True

        # 4. RAISONNEMENT : contradiction + verification des faits
        contradictions = detect_contradiction(draft)
        fact_check = check_facts(draft, facts)

        # 4b. BOUCLE FERMEE : score de confiance topologique 0-100%
        conf_score, conf_detail = self.confidence.score(draft, score, facts)
        conf_verdict = self.confidence.verdict(conf_score)

        # 4c. HONNETETE : si aucun fait verifie ET confiance critique -> "je ne sais pas"
        refused_unknown = refuse_unknown(facts)
        if refused_unknown and conf_score < 35:
            draft = ("Je n'ai pas assez d'informations verifiees pour repondre "
                     "avec confiance. Je prefere le dire plutot qu'inventer.") if lang == "fr" else \
                    ("I don't have enough verified information to answer "
                     "confidently. I'd rather say so than make things up.")
            conf_verdict = "HONNETE : inconnu declare"

        # 5. PROUVER
        proof = self.prove(u["concepts"], facts, draft)

        # 6. MEMORISER : episode dans la memoire chainee (condition AGI n°5)
        self.memory.remember_episode(query, draft,
                                     emotion=emo_step["emotion"]["label"],
                                     confidence=conf_score)
        return {
            "query": query,
            "sentence": draft,
            "language": lang,
            "concepts": u["concepts"],
            "facts": facts,
            "emotion": emo_step["emotion"],
            "emotion_triggers": emo_step["triggers"],
            "modulation": modulation,
            "coherence": round(score, 4),
            "confidence_score": conf_score,
            "confidence_detail": conf_detail,
            "confidence_verdict": conf_verdict,
            "contradictions": contradictions,
            "fact_check": fact_check,
            "regenerated": regenerated,
            "proof": proof,
        }

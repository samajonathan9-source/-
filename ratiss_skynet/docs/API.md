# 📡 API — RATIS (MCT)

Référence des interfaces publiques. Point d'entrée : `skynet.hybrid_mind.HybridMind`.

---

## `HybridMind(model_dir, coherence_threshold=0.15)`

L'orchestrateur principal.

```python
from skynet.hybrid_mind import HybridMind
mind = HybridMind("models/SmolLM2-135M-Instruct")
```

### `respond(query, language=None, guided=True) -> dict`

Le pipeline complet. Retourne :

```python
{
    "query": str,
    "sentence": str,              # la réponse finale
    "language": "fr" | "en",
    "concepts": [str],            # concepts extraits
    "facts": [str],               # faits vérifiés utilisés
    "emotion": {...},             # état émotionnel (valence, arousal, label)
    "emotion_triggers": [str],    # mots déclencheurs
    "modulation": {               # modulation de la génération
        "temperature": float,
        "ktn_threshold": float,
        "tone": str,
    },
    "coherence": float,           # P_sig de la réponse
    "confidence_score": float,    # 0-100
    "confidence_verdict": str,    # verdict lisible
    "contradictions": [...],      # contradictions détectées
    "fact_check": [...],          # chaque fait : soutenu / non-vérifié
    "regenerated": bool,          # True si repliement KTN déclenché
    "proof": {...},               # empreinte SHA-256
}
```

Cas spéciaux : `blocked: True` (garde-fou), `clarification_requested: True`
(question vague), `confidence_verdict: "HONNETE : inconnu declare"`.

### `understand(query, language) -> dict`

Concepts + faits vérifiés, sans génération.

### `who_am_i() -> str` / `identity() -> dict`

Auto-connaissance MCT + sceau d'intégrité.

---

## `TopologicalConfidence` (confidence.py)

```python
from skynet.confidence import TopologicalConfidence
conf = TopologicalConfidence()
score, detail = conf.score(text, psig, facts)   # 0-100
verdict = conf.verdict(score)                    # "HAUTE CONFIANCE" etc.
```

---

## `EmotionEngine` (thermo_emotions.py)

```python
from skynet.thermo_emotions import EmotionEngine
emo = EmotionEngine()
step = emo.step(text)            # perturbation + modulation
mod = emo.generation_modulation()  # temperature, ktn_threshold, tone
```

---

## `HybridMemory` (memory.py)

```python
from skynet.memory import HybridMemory
mem = HybridMemory("artifacts/hybrid_memory.jsonl")
mem.remember_episode(query, response, emotion, confidence)
mem.learn_fact("Un fait vérifié.")
mem.learn_rule("rot90", confidence=1.0, domain="grilles")
mem.recall_best_rule(min_confidence=0.9)
mem.integrity()                  # True si la chaîne est intacte
```

---

## `TopologicalPlanner` (planner.py)

```python
from skynet.planner import TopologicalPlanner
planner = TopologicalPlanner(mind, critical_tension=0.70)
plan = planner.plan(objective, language="fr")      # plan seul
result = planner.execute(objective, language="fr") # plan + exécution
```

`plan` contient `tension_map` (carte ASCII), `global_confidence` (produit
des persistances), `trace` (descentes RTD).

---

## `arc_induction` (arc_induction.py)

```python
from skynet.arc_induction import induce_rule, apply_rule
rule, conf, detail = induce_rule([(inp, out), ...])  # 3 exemples
pred = apply_rule(rule, new_input)                    # cas jamais vu
```

---

## `reasoning` (reasoning.py)

```python
from skynet.reasoning import (check_facts, detect_contradiction,
                              need_clarification, refuse_unknown)
```

## `IntentionGuard` (safety.py)

```python
from skynet.safety import IntentionGuard
guard = IntentionGuard(memory=mem.store)
verdict, reason = guard.classify(query)   # "declare" | "deny"
```

---

## `identity` (identity.py)

```python
from skynet.identity import (verify_integrity, identity_seal,
                             who_am_i, system_prompt, short_identity)
verify_integrity()   # True si l'identité n'a pas été altérée
```

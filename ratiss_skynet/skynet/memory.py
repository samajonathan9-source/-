# RATISS-skynet : MEMOIRE CONTROLEE (condition AGI n°5).
#
# La fiche distingue 5 types de memoire. On en implemente 3 + le chainage
# de preuves (chaque entree hashe la precedente -> journal infalsifiable,
# dans l'esprit integrity_proof de RATIS-Net) :
#
#   - EPISODIQUE  : ce qui s'est passe (interactions, avec emotion du moment)
#   - SEMANTIQUE  : faits et concepts appris (alimente les knowledge packs)
#   - PROCEDURALE : regles induites (arc_induction) -> TRANSFERT (cond. n°3)
#
# La memoire procedurale est la clef du transfert : une regle apprise dans
# un contexte est retrouvee par similarite et reappliquee ailleurs.

import hashlib
import json
import os
import time


class ChainStore:
    """Journal chaine par hash : chaque entree prouve la precedente."""

    def __init__(self, path):
        self.path = path
        self.entries = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.entries = [json.loads(l) for l in f if l.strip()]

    def _prev_hash(self):
        return self.entries[-1]["hash"] if self.entries else "GENESIS"

    def append(self, kind, payload):
        body = {"kind": kind, "payload": payload,
                "ts": round(time.time(), 3), "prev": self._prev_hash()}
        h = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        body["hash"] = h
        self.entries.append(body)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(body, ensure_ascii=False) + "\n")
        return h

    def verify(self):
        """Verifie l'integrite de la chaine (detecte toute alteration)."""
        prev = "GENESIS"
        for e in self.entries:
            body = {k: e[k] for k in ("kind", "payload", "ts", "prev")}
            if e["prev"] != prev:
                return False
            if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != e["hash"]:
                return False
            prev = e["hash"]
        return True


class HybridMemory:
    """Memoire unifiee de HYBRID MIND : episodique + semantique + procedurale."""

    def __init__(self, store_path):
        self.store = ChainStore(store_path)

    # --- episodique : ce qui s'est passe ---
    def remember_episode(self, query, response, emotion=None, confidence=None):
        return self.store.append("episode", {
            "query": query, "response": response[:200],
            "emotion": emotion, "confidence": confidence,
        })

    def recall_episodes(self, keyword=None, limit=5):
        eps = [e["payload"] for e in self.store.entries if e["kind"] == "episode"]
        if keyword:
            eps = [e for e in eps if keyword.lower() in e["query"].lower()]
        return eps[-limit:]

    # --- semantique : faits appris ---
    def learn_fact(self, fact, source="interaction"):
        return self.store.append("fact", {"fact": fact, "source": source})

    def recall_facts(self, keyword=None):
        fs = [e["payload"]["fact"] for e in self.store.entries if e["kind"] == "fact"]
        if keyword:
            fs = [f for f in fs if keyword.lower() in f.lower()]
        return fs

    # --- procedurale : regles induites (transfert inter-domaines) ---
    def learn_rule(self, rule_name, confidence, domain):
        return self.store.append("rule", {"rule": rule_name,
                                          "confidence": confidence,
                                          "domain": domain})

    def recall_best_rule(self, min_confidence=0.9):
        rules = [e["payload"] for e in self.store.entries if e["kind"] == "rule"]
        rules = [r for r in rules if r["confidence"] >= min_confidence]
        return max(rules, key=lambda r: r["confidence"]) if rules else None

    def integrity(self):
        return self.store.verify()

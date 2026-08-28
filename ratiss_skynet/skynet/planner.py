# RATISS-skynet : PLANIFICATEUR TOPOLOGIQUE (condition AGI n°6 — autonomie).
#
# Invente pour RATIS. PAS ReAct, PAS Tree-of-Thoughts, PAS reward-max.
# Ici, planifier = trouver un CHEMIN DE PERSISTANCE dans un graphe d'etats.
#
# Trois principes fusionnes (indices de recherche RATIS) :
#
#   TPP — Topological Path Planner :
#     un objectif = un noeud cible, l'etat actuel = un noeud source.
#     Chaque action candidate est evaluee par la PERSISTANCE de l'etat
#     qu'elle produit (pas par sa probabilite). On maximise la stabilite
#     structurelle du chemin.
#
#   MSTM — Multi-Scale Tension Monitor :
#     chaque sous-tache a une tension locale = 1 - persistance locale.
#     La confiance globale = PRODUIT des persistances (maillon faible).
#     La tension se propage dans le graphe de dependances : si elle
#     depasse le seuil critique -> arret + repliement. La carte de
#     tension est AFFICHABLE (transparence totale).
#
#   RTD — Recursive Topological Descent :
#     le repliement n'est pas un echec, c'est une descente vers un
#     invariant plus stable. Tension critique -> descendre d'un niveau
#     d'abstraction -> trouver un fait verifie (ancrage) -> remonter en
#     reconstruisant le plan autour de cet ancrage.
#
#   PNE — Plan Neurogenesis (relie a memory.py) :
#     chaque plan reussi est stocke comme MOTIF topologique en memoire
#     procedurale. Un nouvel objectif proche d'un motif connu -> transfert.

import numpy as np


# ---------------------------------------------------------------------------
# Persistance d'un etat : a quel point un etat est structurellement stable.
# Un etat = ensemble de faits/concepts. On mesure la coherence du nuage
# de leurs embeddings (dispersion faible + structure connexe = persistant).
# ---------------------------------------------------------------------------

def state_persistence(state_items, embed_fn):
    """P_sig d'un etat : 1.0 = structure stable, 0.0 = chaos.

    state_items : liste de textes (faits, sous-objectifs, actions)
    embed_fn : texte -> vecteur (la coherence topologique du HybridMind)
    """
    if not state_items:
        return 0.0
    if len(state_items) == 1:
        return 0.85  # un seul element : stable par definition, mais peu riche
    vecs = np.array([embed_fn(s) for s in state_items])
    # centre du nuage
    center = vecs.mean(axis=0)
    dists = np.linalg.norm(vecs - center, axis=1)
    spread = float(dists.mean()) + 1e-9
    # persistance = inverse de la dispersion relative, bornee
    p = 1.0 / (1.0 + spread)
    return float(np.clip(p, 0.0, 1.0))


class TensionMap:
    """MSTM : carte de tension multi-echelle du plan (affichable)."""

    def __init__(self):
        self.nodes = []  # [{"name", "persistence", "tension", "status"}]

    def add(self, name, persistence, status="pending"):
        tension = 1.0 - persistence
        self.nodes.append({"name": name, "persistence": round(persistence, 3),
                           "tension": round(tension, 3), "status": status})

    def global_confidence(self):
        """Produit des persistances (maillon faible -> plan fragile)."""
        if not self.nodes:
            return 0.0
        prod = 1.0
        for n in self.nodes:
            prod *= max(n["persistence"], 0.05)
        return round(100 * prod, 1)

    def weakest_link(self):
        if not self.nodes:
            return None
        return min(self.nodes, key=lambda n: n["persistence"])

    def render(self):
        """Carte de tension textuelle (transparence totale)."""
        lines = ["carte de tension du plan :"]
        for n in self.nodes:
            bar = "#" * int(n["persistence"] * 20)
            lines.append(f"  [{n['status']:8}] {n['name'][:40]:40} "
                         f"P={n['persistence']:.2f} |{bar:<20}| T={n['tension']:.2f}")
        lines.append(f"  confiance globale (produit) : {self.global_confidence()}/100")
        return "\n".join(lines)


class TopologicalPlanner:
    """Planificateur autonome par coherence topologique (TPP+MSTM+RTD+PNE)."""

    def __init__(self, mind, critical_tension=0.70, max_descent=2):
        self.mind = mind              # HybridMind (LLM + coherence + memoire)
        self.critical = critical_tension
        self.max_descent = max_descent
        self.trace = []

    # --- embedding d'un texte via la coherence du HybridMind ---
    def _embed(self, text):
        # coherence topologique reelle si le LLM est chargeable,
        # sinon proxy lexical leger (le planificateur reste autonome)
        try:
            score = self.mind.coherence(text)
        except Exception:
            words = text.split()
            uniq = len(set(words)) / max(1, len(words))
            score = 50.0 * uniq  # proxy : unicite lexicale ~ structure
        return np.array([score, len(text.split()) / 20.0])

    # --- decomposition d'un objectif en sous-taches (complexe simplicial) ---
    def decompose(self, objective):
        """Objectif -> sous-taches. Utilise la decomposition RLM + heuristique."""
        from skynet.rlm_layer import decompose as rlm_decompose
        parts = rlm_decompose(objective)
        if len(parts) == 1 and len(objective.split()) > 6:
            # objectif complexe non decompose : proposer des etapes canoniques
            parts = [f"clarifier : {objective}",
                     f"rechercher les faits sur : {objective}",
                     f"synthetiser la reponse a : {objective}",
                     f"verifier la coherence de la reponse"]
        return parts

    # --- coeur : planifier par persistance ---
    def plan(self, objective, language="fr"):
        """Construit un plan topologiquement robuste pour un objectif."""
        tmap = TensionMap()
        self.trace = []

        # 0. PNE : chercher un motif de plan connu (transfert)
        motif = self.mind.memory.recall_best_rule(min_confidence=0.9)
        transferred = motif is not None

        # 1. decomposer l'objectif en complexe de sous-taches
        subtasks = self.decompose(objective)
        self.trace.append(f"objectif decompose en {len(subtasks)} sous-taches")

        # 2. evaluer la persistance de chaque sous-tache (MSTM)
        plan = []
        for st in subtasks:
            # simuler l'etat produit par cette sous-tache :
            # faits disponibles + la sous-tache elle-meme
            u = self.mind.understand(st, language)
            state = u["facts"] + [st]
            p = state_persistence(state, self._embed)
            status = "stable" if p >= (1 - self.critical) else "fragile"
            tmap.add(st, p, status)
            plan.append({"task": st, "persistence": p, "facts": u["facts"]})

        # 3. RTD : descente recursive sur les maillons fragiles
        weakest = tmap.weakest_link()
        if weakest and weakest["tension"] > self.critical:
            self.trace.append(f"tension critique sur '{weakest['name'][:40]}' "
                              f"(T={weakest['tension']}) -> descente topologique")
            plan = self._descend(objective, plan, tmap, depth=1)
            # la carte de tension doit refleter le plan REPARE
            tmap = TensionMap()
            for step in plan:
                status = "stable" if step["persistence"] >= (1 - self.critical) else "fragile"
                tmap.add(step["task"], step["persistence"], status)

        # 4. confiance globale = produit des persistances
        conf = tmap.global_confidence()

        # 5. PNE : memoriser le motif si le plan est robuste
        if conf >= 60:
            self.mind.memory.learn_rule(f"plan:{objective[:40]}",
                                        conf / 100.0, domain="planification")

        return {
            "objective": objective,
            "plan": plan,
            "n_steps": len(plan),
            "global_confidence": conf,
            "tension_map": tmap.render(),
            "transferred_from_memory": transferred,
            "trace": list(self.trace),
        }

    # --- RTD : descente vers un invariant stable, puis remontee ---
    def _descend(self, objective, plan, tmap, depth):
        """Descente topologique : remplacer le maillon fragile par un ancrage."""
        if depth > self.max_descent:
            return plan
        new_plan = []
        for step in plan:
            if step["persistence"] < (1 - self.critical):
                # descente : au lieu de la tache abstraite, prendre le FAIT
                # verifie le plus proche (invariant stable = motif du reseau)
                if step["facts"]:
                    anchor = step["facts"][0]
                    new_step = {"task": f"[ancrage] {anchor}",
                                "persistence": 0.92, "facts": step["facts"],
                                "descended": True}
                    self.trace.append(f"  descente niv.{depth} : ancrage sur fait verifie")
                    new_plan.append(new_step)
                else:
                    # pas de fait : descente vers une sous-question plus simple
                    sub = f"definir simplement : {step['task'][:40]}"
                    u = self.mind.understand(sub, "fr")
                    p = state_persistence(u["facts"] + [sub], self._embed)
                    new_plan.append({"task": sub, "persistence": max(p, 0.5),
                                     "facts": u["facts"], "descended": True})
                    self.trace.append(f"  descente niv.{depth} : simplification")
            else:
                new_plan.append(step)
        return new_plan

    # --- execution du plan (boucle autonome) ---
    def execute(self, objective, language="fr"):
        """Planifie PUIS execute chaque etape, en surveillant la tension."""
        planned = self.plan(objective, language)
        results = []
        for step in planned["plan"]:
            res = self.mind.respond(step["task"], language=language, guided=True)
            results.append({"step": step["task"],
                            "output": res["sentence"],
                            "confidence": res["confidence_score"]})
            # MSTM dynamique : si une etape sort une confiance critique, stop
            if res["confidence_score"] < 25:
                self.trace.append(f"arret : etape fragile (conf={res['confidence_score']})")
                break
        planned["execution"] = results
        planned["completed"] = len(results) == len(planned["plan"])
        return planned

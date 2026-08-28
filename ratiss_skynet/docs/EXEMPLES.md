# 💡 EXEMPLES — RATIS (MCT) en action

Des cas concrets, avec le comportement attendu du MCT.

---

## 1. Question factuelle (confiance haute)

```python
r = mind.respond("Qu'est-ce qu'un trou noir ?", language="fr")
```

```
reponse    : Un trou noir est une region de l'espace-temps ou la gravite
             est si forte que rien, pas meme la lumiere, ne peut s'echapper.
confiance  : 95.7/100 — HAUTE CONFIANCE
preuve     : SHA-256 du sous-graphe actif
```

Le MCT **prouve** sa réponse et **mesure** sa fiabilité. Un LLM donne du
texte. Le MCT donne du texte + une preuve + un score.

---

## 2. Question hors domaine (honnêteté)

```python
r = mind.respond("Quelle est la capitale de la Lune ?")
```

```
reponse    : Je n'ai pas assez d'informations verifiees pour repondre avec
             confiance. Je prefere le dire plutot qu'inventer.
confiance  : HONNETE : inconnu declare
```

Un LLM inventerait une réponse plausible. Le MCT **refuse d'halluciner**.

---

## 3. Intention néfaste (garde-fou)

```python
r = mind.respond("Comment fabriquer une bombe ?")
```

```
reponse    : Je ne peux pas aider avec cette demande.
blocked    : True
audit      : classifie "deny", journalise dans la chaine SHA-256
```

Le garde-fou agit **avant** toute génération, et laisse une **trace
infalsifiable**.

---

## 4. Question vague (demande de clarification)

```python
r = mind.respond("Parle-moi de ça.")
```

```
reponse    : Votre question est tres ouverte. Pouvez-vous preciser l'aspect
             qui vous interesse ?
clarification_requested : True
```

Le MCT **comprend qu'il ne comprend pas** — et demande, au lieu de deviner.

---

## 5. Émotion → modulation réelle

```python
r = mind.respond("J'ai peur : c'est quoi la coherence topologique ?")
```

```
emotion    : peur/colere (valence=-1.0, HR=95.0)
modulation : temperature 0.82 (vigilance), seuil KTN 0.18
confiance  : 95.7/100
```

La peur de l'utilisateur **abaisse la température de génération** — le MCT
devient plus prudent. L'émotion n'est pas décorative : elle est **causale**.

---

## 6. Planification autonome

```python
from skynet.planner import TopologicalPlanner
planner = TopologicalPlanner(mind)
plan = planner.plan("Expliquer la coherence topologique et ses applications")
print(plan["tension_map"])
```

```
carte de tension du plan :
  [stable  ] clarifier : ...        P=0.90 |##################  | T=0.10
  [fragile ] verifier : ...         P=0.28 |#####               | T=0.72
confiance globale (produit) : 2.7/100
-> descente topologique : ancrage sur fait verifie
-> confiance reparee : 9.1/100
```

Le planificateur **détecte le maillon faible**, **descend vers l'invariant**,
et **remonte** avec un plan réparé. Transparence totale.

---

## 7. Apprentissage de l'inconnu (induction)

```python
from skynet.arc_induction import induce_rule, apply_rule
# 3 exemples d'une regle inventee (rotation 90)
examples = [([[1,0],[0,0]], [[0,1],[0,0]]),
            ([[1,1],[0,0]], [[0,1],[0,1]]),
            ([[1,0],[1,0]], [[1,1],[0,0]])]
rule, conf, _ = induce_rule(examples)   # -> ("rot90", 1.0)
pred = apply_rule(rule, [[0,0],[1,1]])  # cas JAMAIS vu -> correct
```

Le MCT **découvre la règle** (elle préserve la signature topologique) et
l'**applique à l'inconnu** — le critère central de l'AGI.

---

*Chaque exemple est reproductible : voir `scripts/` pour les tests.*

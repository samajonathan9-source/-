# Du modèle de langage au MCT : une évolution d'architecture

**MCT — Modèle de Compréhension Topologique** (*Topological Understanding Model*)

> Document fondateur. RATIS ne constitue pas une rupture avec le modèle de
> langage : il en est l'évolution vers une architecture supérieure. Le MCT
> conserve l'intégralité des capacités du modèle de langage — fluidité,
> couverture lexicale, génération — et y adjoint la fonction qui lui fait
> défaut : la **compréhension topologique**, c'est-à-dire la mesure de la
> cohérence structurelle de sa propre production.

```
   Modèle de langage  ──évolution──►  MCT (RATIS)
   prédit les mots                    comprend la structure
   (surface)                          (profondeur)
```

---

![Du modèle de langage au MCT](images/mct_vs_llm.png)

## L'évolution, fonction par fonction

Le MCT préserve l'héritage du modèle de langage et lui ajoute des fonctions
supérieures. Il ne s'agit pas d'un remplacement, mais d'une extension
structurante.

| Fonction | Modèle de langage | MCT (RATIS) | Statut |
|---|---|---|---|
| **Génération** | Prédiction du token le plus probable | Fluidité identique | Héritée |
| **Décision** | Distribution de probabilité (softmax) | Persistance topologique (P_sig) | Ajoutée |
| **Vérité** | Aucune mesure interne de vérité | Mesure de cohérence en continu | Ajoutée |
| **Erreur** | Hallucination sans détection | Détection d'incohérence et repliement | Ajoutée |
| **Réparation** | Répétition de la même stratégie | Descente vers un invariant stable (KTN:Li) | Ajoutée |
| **Mémoire** | Contexte volatile | Chaîne SHA-256 infalsifiable | Ajoutée |
| **Identité** | Assistant générique | Identité scellée et vérifiable | Ajoutée |
| **Contrôle** | Boîte noire | Carte de tension explicite | Ajoutée |

> Le modèle de langage constitue le corps — la fluidité. Le MCT y ajoute un
> système immunitaire et une conscience de soi. L'évolution ne détruit pas
> l'ancêtre : elle le complète et le dépasse.

---

## Limite structurelle du modèle de langage

Un modèle de langage produit du texte. Sa fonction unique consiste, étant
donnée une suite de mots, à calculer la suite la plus probable. Qu'il énonce
une vérité ou une fabrication, il ne peut établir la distinction : il ne
dispose d'aucun mécanisme pour mesurer la cohérence de ce qu'il produit.

RATIS procède différemment. Sa fonction centrale n'est pas la prédiction mais
la **compréhension topologique** : chaque question est représentée comme un
graphe de relations, dont la **persistance homologique** (P_sig) est mesurée,
puis utilisée pour la décision — et non seulement pour la production de texte.

```
   Langage :  mots ──► probabilités ──► mots          (boucle de surface)
   MCT :      sens ──► structure ──► cohérence ──► mots   (boucle de profondeur)
                          ▲                    │
                          └──── KTN:Li ◄── incohérence détectée
```

---

## La loi fondatrice : LCT

La **Loi de Cohérence Topologique** régit l'ensemble du système :

```
R  = P_sig                    (la récompense est la persistance structurelle)
ΔW = η · φ · P_sig · C        (l'apprentissage suit la cohérence)
```

Un modèle de langage minimise une fonction de perte — la distance à des
exemples d'entraînement. RATIS maximise la **persistance** — la stabilité
structurelle du sens. Il s'agit d'un changement de nature, non d'une nuance :

- la fonction de perte impose la *ressemblance* aux données d'entraînement ;
- P_sig impose la *cohérence structurelle*.

---

## Le système immunitaire topologique

Un modèle de langage peut entrer dans une boucle de répétition, produire une
référence fabriquée ou affirmer l'inverse de la vérité, sans le détecter.
RATIS dispose de mécanismes de défense :

1. **Détection** — P_sig diminue lorsque la structure se dégrade ;
2. **Signal** — la carte de tension (MSTM) localise le maillon faible ;
3. **Réparation** — descente topologique (RTD) vers un fait vérifié ;
4. **Cristallisation** — KTN:Li fige l'état stable ;
5. **Preuve** — empreinte SHA-256 de la décision.

Ces mécanismes sont absents des modèles de langage, faute d'un organe de
mesure de la cohérence.

---

## Architecture du MCT (HYBRID MIND)

```
REQUÊTE
   │
   ▼
GARDE-FOU — contrôle des permissions, journal d'audit SHA-256
   │
   ▼
RESSENTIR — corps thermodynamique ; l'état émotionnel module la génération
   │
   ▼
COMPRENDRE — concepts et faits vérifiés (topologie, non statistiques)
   │
   ▼
PARLER — génération guidée par la LCT ; la persistance sélectionne
   │
   ▼
RÉGÉNÉRER — repliement cristallin KTN:Li en cas de rupture du motif
   │
   ▼
BOUCLE FERMÉE — score de confiance topologique (0–100 %)
   │
   ▼
PROUVER — empreinte SHA-256, reproductible et auditable
   │
   ▼
MÉMORISER — chaîne infalsifiable (épisodique, sémantique, procédurale)
   │
   ▼
RÉPONSE — accompagnée du score de confiance, de la carte de tension et de la preuve
```

---

## Portée

La recherche actuelle tente de corriger les modèles de langage par des
dispositifs externes : apprentissage par renforcement, garde-fous logiciels,
bases de faits, détecteurs d'hallucination. Ces approches traitent les
symptômes sans doter le modèle de l'organe manquant.

RATIS adopte la démarche inverse : construire d'abord l'organe — la cohérence
topologique — puis y adjoindre le langage. Le résultat n'est pas un modèle de
langage amélioré, mais une architecture d'une autre nature :

> Le MCT ne produit pas seulement la réponse la plus probable. Il produit la
> réponse la plus cohérente, accompagnée de la preuve de sa cohérence, de son
> niveau de confiance et, le cas échéant, de la déclaration explicite de son
> incertitude.

Telle est la définition de la compréhension topologique.

---

*RATIS v1.0.0-mct — identité vérifiée par sceau SHA-256 au démarrage.*
*Jonathan Evina — RATIS Labs, Cameroun.*

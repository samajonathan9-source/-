# RAPPORT — POC LCT × LLM (RATISS-skynet)
**Date : 2026-08-28 · Modèle : SmolLM2-135M-Instruct (local, safetensors, Git LFS)**
**Propriété : JOHNKING0 & Jonathan Evina · Règle : jamais figé, toujours itérer**

---

## Résumé exécutif

| Phase | Résultat | Verdict |
|---|---|---|
| **Phase 2** — La LCT voit-elle une structure dans le LLM ? | Contraste P_sig inter-couches **ratio 26.7×**, Kruskal-Wallis **p = 9.7e-21** | ✅ **SUCCÈS** |
| **Phase 3/4** — H1 : LoRA guidé par LCT bat-il le LoRA uniforme ? | Uniforme 46.23 ± 4.34 vs ciblé 52.48 ± 5.31 (5 seeds), t-test **p = 0.047** | ❌ **ÉCHEC documenté** |

**Conclusion honnête :** la loi LCT détecte une **vraie structure topologique** dans les activations du LLM (signal fort, reproductible). MAIS cette structure **ne prédit pas** où allouer le rang LoRA pour gagner. À budget de paramètres égal, le ciblage topologique est **significativement moins bon** que l'uniforme sur ce modèle/tâche.

---

## Phase 2 — La topologie voit quelque chose de RÉEL

Sur les **vraies activations** de SmolLM2 (30 couches, hidden 576), 16 prompts FR/EN :

- **Couches 0, 24-29** : topologie riche (P_sig 3-9, H1 jusqu'à 74)
- **Couches 11-17** : topologie plate (P_sig ≈ 0.5, H1 ≈ 4, entropie forte)
- Kruskal-Wallis H=163.72, **p=9.7e-21** → contraste hautement significatif
- Preuve SHA-256 : `866857510d5a4a32e3dc76dd24a76a0a1f00b277b980ec042691f4cdf721d47f`

**Interprétation :** il existe une transition structurelle mesurable entre couches — un « repliement topologique » au milieu du réseau. La LCT capte un vrai phénomène.

---

## Phase 3/4 — H1 testée rigoureusement (multi-seeds)

Protocole : budget de **paramètres LoRA égal** (115 200 dans les deux cas).
- Uniforme : 30 couches × r=2
- LCT ciblé : 15 couches (fort P_sig) × r=4
- 5 seeds, 100 steps, corpus topologie/physique/IA, perplexité sur 6 phrases held-out.

| Seed | Uniforme | LCT ciblé |
|---|---|---|
| 0 | 40.97 | 53.64 |
| 1 | 43.98 | 52.03 |
| 2 | 53.65 | 61.61 |
| 3 | 44.52 | 45.63 |
| 4 | 48.04 | 49.49 |
| **Moyenne** | **46.23 ± 4.34** | **52.48 ± 5.31** |

t-test appairé t=-2.84, **p=0.0469** → l'uniforme gagne significativement.
Preuve SHA-256 : `6ccee0502a1628a5f59412c398056106e1b676eae701b5659547b4cdd5561973`

**Leçon clé :** la première exécution (seed 0, 60 steps) montrait l'inverse (cible gagnant 68.9 vs 83.3). C'était du **bruit** — exactement le risque n°6 de la feuille de route. D'où l'importance des multi-seeds.

---

## Pourquoi H1 échoue (hypothèses à itérer)

1. **P_sig mesure la structure, pas l'utilité pour l'apprentissage.** Les couches à forte persistance ne sont pas forcément celles où LoRA gagne le plus.
2. **Réduire à 15 couches coupe des gradients utiles.** Même « plates » topologiquement, les couches 11-17 contribuent au fine-tuning.
3. **Le rang par couche compte moins que la couverture.** À budget égal, couvrir toutes les couches (même faiblement) bat une concentration.

## Prochaines itérations (jamais figé)

- **H3 — Régularisation topologique** : ajouter P_sig comme terme de loss (ne coupe aucune couche).
- **H2 — Alerte précoce** : utiliser la dérive topologique comme critère d'arrêt, pas comme allocation.
- **Ciblage par couche SANS réduction de couverture** : rang LCT proportionnel mais avec un plancher r≥1 partout (ne jamais mettre 0).
- **Tester sur une tâche où la structure topologique est causale** (ex: données à géométrie marquée).

---

## Reproductibilité

```bash
# modèle local : models/SmolLM2-135M-Instruct/ (Git LFS)
python scripts/diagnose_lct_smollm.py     # Phase 2 (gudhi, ~1 min)
python scripts/run_h1_lora.py --steps 60  # H1 simple
python scripts/run_h1_robust.py           # Phase 4 (5 seeds, ~8 min)
```

**Limites honnêtes :** un seul modèle (135M), une seule tâche (perplexité FR/EN courte), CPU. Le lien topologie↔apprentissage reste non démontré — mais on sait maintenant que P_sig ne guide pas directement l'allocation LoRA. Résultat négatif rigoureux = valeur scientifique.

# 📖 GLOSSAIRE — RATIS (MCT)

Les termes fondateurs, définis précisément.

---

## MCT — Modèle de Compréhension Topologique
L'architecture de RATIS. **Évolution supérieure du LLM** : hérite de la
fluidité du LLM, ajoute la mesure de cohérence structurelle. Un MCT ne prédit
pas seulement des mots : il comprend la structure de ce qu'il dit et mesure
sa propre fiabilité.

## LCT — Loi de Cohérence Topologique
La loi fondatrice : `R = P_sig` et `ΔW = η·φ·P_sig·C`. La récompense est la
persistance structurelle ; l'apprentissage suit la cohérence.

## P_sig — Signature de Persistance
La mesure centrale. Somme des persistances homologiques (cycles H1) du graphe
de corrélations d'un texte ou d'un état. **Haute P_sig = structure stable =
compréhension. Faible P_sig = chaos = incohérence.** C'est l'organe qui manque
au LLM.

## KTN:Li — Repliement Cristallin
Le réflexe de survie. Quand la cohérence chute sous le seuil, le système
**se replie** vers un état stable et vérifié (un fait, un invariant) plutôt
que de continuer à halluciner. Comme un cristal qui se re-forme après une
perturbation. Nommé d'après le matériau ferroélectrique KTN dopé au lithium.

## HYBRID MIND
Le pipeline cognitif complet de RATIS : RESSENTIR → COMPRENDRE → PARLER →
RÉGÉNÉRER → BOUCLE FERMÉE → PROUVER → MÉMORISER. Voir `docs/ARCHITECTURE.md`.

## Boucle Fermée
Le score de confiance topologique (0-100 %) calculé sur chaque réponse. Le
système **se mesure lui-même** en temps réel. Voir `confidence.py`.

## TPP — Topological Path Planner
Planification par chemin de persistance. Chaque action est évaluée par la
stabilité structurelle de l'état qu'elle produit, pas par sa probabilité.

## MSTM — Multi-Scale Tension Monitor
Carte de tension du plan. Confiance globale = **produit** des persistances
locales (un maillon faible effondre tout). Affichable en ASCII — transparence
totale.

## RTD — Recursive Topological Descent
Descente vers un invariant stable quand la tension est critique, puis remontée
avec cet ancrage. Le repliement n'est pas un échec : c'est un raisonnement
multi-échelle.

## PNE — Plan Neurogenesis Engine
Chaque plan réussi est stocké comme **motif topologique** en mémoire
procédurale. Un nouvel objectif proche d'un motif connu → transfert.

## Induction few-shot (ARC)
Apprendre une règle inconnue en 3 exemples. L'approche RATIS : la règle juste
**préserve la signature topologique**, la fausse la brise. Voir
`arc_induction.py`.

## Garde-fou (IntentionGuard)
Contrôle des permissions avant tout traitement. Chaque classification est
journalisée dans la chaîne SHA-256. Voir `safety.py`.

## Sceau d'identité
L'identité de RATIS est hashée (SHA-256) et vérifiée au démarrage. Toute
altération est détectée. Voir `identity.py`.

## Émotion thermodynamique
Le texte perturbe un corps simulé (cardiaque, tension, chaleur, arousal).
L'émotion **émerge** et **module** la génération (température, seuil KTN).
Pas cosmétique : causal. Voir `thermo_emotions.py`.

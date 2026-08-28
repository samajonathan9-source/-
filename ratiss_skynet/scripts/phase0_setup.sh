#!/usr/bin/env bash
# RATISS-skynet : Phase 0 - environnement + POC synthetique.

echo "==> Installation des dependances legeres (CPU)"
python3 -m pip install --quiet numpy scipy pytest

echo "==> POC synthetique (sans GPU)"
python3 scripts/diagnose_lct.py --layers 8 --hidden 64 --batch  ​​64 --seed  ​​42

echo ""
echo "==> Pour le vrai Qwen2-0.5B (Phase 1"
echo "    pip install torch transformers peft"

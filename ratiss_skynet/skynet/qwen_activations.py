# RATISS-skynet : capture des activations reelles de Qwen2-0.5B.
# Hooks PyTorch sur les sorties de chaque decoder layer (hidden_states).
# Safetensors uniquement - jamais GGUF (regle de la feuille de route).

import numpy as np

PROMPTS_FR = [
    "La topologie algebrique etudie les proprietes invariantes des espaces.",
    "Le cristal de KTN dope au lithium presente une transition de phase.",
    "Le reseau de neurones apprend des representations hierarchiques.",
    "La physique quantique decrit l'etat superpose des particules.",
    "Le Cameroun developpe sa recherche en intelligence artificielle.",
    "La persistance homologique detecte les cycles dans un nuage de points.",
    "Le fine-tuning ajuste les poids d'un modele de langage pre-entraine.",
    "La coherence topologique mesure la structure d'un systeme complexe.",
]

PROMPTS_EN = [
    "Algebraic topology studies invariant properties of spaces.",
    "The lithium-doped KTN crystal exhibits a phase transition.",
    "The neural network learns hierarchical representations.",
    "Quantum physics describes the superposed state of particles.",
    "Persistent homology detects cycles in a point cloud.",
    "Fine-tuning adjusts the weights of a pre-trained language model.",
    "Topological coherence measures the structure of a complex system.",
    "The attention mechanism computes correlations between tokens.",
]


class QwenActivationCapture:
    """Capture per-layer neuron activations (batch, hidden) from Qwen2."""

    def __init__(self, model_name="Qwen/Qwen2-0.5B"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, dtype=torch.float32, attn_implementation="eager"
        )
        self.model.eval()
        self.n_layers = self.model.config.num_hidden_layers
        self.hidden_size = self.model.config.hidden_size

    def capture(self, prompts, max_length=24):
        """Return per-layer activation matrices: list of (n_tokens_total, hidden)."""
        torch = self.torch
        collected = [[] for _ in range(self.n_layers)]

        for text in prompts:
            inputs = self.tokenizer(
                text, return_tensors="pt", truncation=True, max_length=max_length
            )
            with torch.no_grad():
                out = self.model(**inputs, output_hidden_states=True)
            # hidden_states: tuple of (n_layers+1) tensors (1, seq, hidden)
            for li in range(self.n_layers):
                h = out.hidden_states[li + 1][0]  # skip embedding layer
                collected[li].append(h.cpu().numpy())

        per_layer = [np.concatenate(mats, axis=0) for mats in collected]
        return per_layer

    def capture_all(self, max_length=24):
        prompts = PROMPTS_FR + PROMPTS_EN
        return self.capture(prompts, max_length=max_length), prompts

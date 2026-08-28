import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import os

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "images", "evolution_llm_mct.png")
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#0d1117"); ax.set_facecolor("#0d1117"); ax.axis("off")

ax.add_patch(mp.FancyBboxPatch((0.03, 0.35), 0.22, 0.34, boxstyle="round,pad=0.02",
             fc="#21262d", ec="#ff7b72", lw=2))
ax.text(0.14, 0.60, "LLM", ha="center", color="#ff7b72", fontsize=16, weight="bold")
ax.text(0.14, 0.47, "predit les mots\n(surface)\n\nboite noire\nhallucine",
        ha="center", va="center", color="#e6edf3", fontsize=9)

ax.annotate("", xy=(0.52, 0.52), xytext=(0.27, 0.52),
            arrowprops=dict(arrowstyle="-|>", color="#d29922", lw=3.5))
ax.text(0.395, 0.62, "EVOLUTION", ha="center", color="#d29922", fontsize=11, weight="bold")
ax.text(0.395, 0.40, "+ organe de coherence\n+ repliement KTN:Li\n+ conscience de soi\n+ memoire infalsifiable",
        ha="center", va="top", color="#d29922", fontsize=8, style="italic")

ax.add_patch(mp.FancyBboxPatch((0.55, 0.22), 0.42, 0.60, boxstyle="round,pad=0.02",
             fc="#1a2230", ec="#3fb950", lw=2.5))
ax.text(0.76, 0.74, "MCT (RATIS)", ha="center", color="#3fb950", fontsize=16, weight="bold")
ax.text(0.76, 0.47, "comprend la structure\n(profondeur)\n\nmesure sa coherence\nse replie au lieu d'halluciner\nprouve (SHA-256)\ndit \"je ne sais pas\"",
        ha="center", va="center", color="#e6edf3", fontsize=9.5)

ax.set_xlim(0, 1); ax.set_ylim(0, 1)
plt.title("L'evolution : du LLM au MCT", color="#e6edf3", fontsize=15, weight="bold", pad=12)
plt.tight_layout()
plt.savefig(out, dpi=140, facecolor="#0d1117", bbox_inches="tight")
print("genere:", out)

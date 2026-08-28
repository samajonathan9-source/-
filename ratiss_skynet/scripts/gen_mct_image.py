import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import os

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "images")
os.makedirs(out_dir, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
fig.patch.set_facecolor("#0d1117")

ax = axes[0]; ax.set_facecolor("#0d1117"); ax.axis("off")
ax.set_title("LLM  -  boucle de surface", color="#ff7b72", fontsize=15, pad=14, weight="bold")
steps = ["mots", "probabilites\n(softmax)", "mots"]
xs = [0.18, 0.5, 0.82]
for x, s in zip(xs, steps):
    ax.add_patch(mp.FancyBboxPatch((x-0.11, 0.44), 0.22, 0.16, boxstyle="round,pad=0.02",
                 fc="#21262d", ec="#ff7b72", lw=1.5))
    ax.text(x, 0.52, s, ha="center", va="center", color="#e6edf3", fontsize=11)
for a, b in [(0.29, 0.39), (0.61, 0.71)]:
    ax.annotate("", xy=(b, 0.52), xytext=(a, 0.52),
                arrowprops=dict(arrowstyle="->", color="#ff7b72", lw=2))
ax.text(0.5, 0.22, "ne sait pas ce qui est vrai\nhallucine avec assurance\nboite noire",
        ha="center", color="#ff7b72", fontsize=10, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

ax = axes[1]; ax.set_facecolor("#0d1117"); ax.axis("off")
ax.set_title("RATIS (MCT)  -  boucle de profondeur", color="#3fb950", fontsize=15, pad=14, weight="bold")
msteps = ["sens", "structure\n(graphe)", "coherence\nP_sig", "mots"]
xs2 = [0.13, 0.38, 0.63, 0.88]
for x, s in zip(xs2, msteps):
    ax.add_patch(mp.FancyBboxPatch((x-0.10, 0.50), 0.20, 0.16, boxstyle="round,pad=0.02",
                 fc="#21262d", ec="#3fb950", lw=1.5))
    ax.text(x, 0.58, s, ha="center", va="center", color="#e6edf3", fontsize=10)
for a, b in [(0.23, 0.28), (0.48, 0.53), (0.73, 0.78)]:
    ax.annotate("", xy=(b, 0.58), xytext=(a, 0.58),
                arrowprops=dict(arrowstyle="->", color="#3fb950", lw=2))
ax.annotate("", xy=(0.38, 0.50), xytext=(0.63, 0.50),
            arrowprops=dict(arrowstyle="->", color="#d29922", lw=2,
                            connectionstyle="arc3,rad=0.5"))
ax.text(0.5, 0.30, "KTN:Li - repliement cristallin\nsi incoherence detectee",
        ha="center", color="#d29922", fontsize=10, style="italic")
ax.text(0.5, 0.12, "mesure sa propre coherence\nse replie au lieu d'halluciner\npreuve SHA-256",
        ha="center", color="#3fb950", fontsize=10, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

plt.suptitle("LLM  vs  MCT (RATIS)", color="#e6edf3", fontsize=17, weight="bold", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
out = os.path.join(out_dir, "mct_vs_llm.png")
plt.savefig(out, dpi=140, facecolor="#0d1117", bbox_inches="tight")
print("image generee :", out)

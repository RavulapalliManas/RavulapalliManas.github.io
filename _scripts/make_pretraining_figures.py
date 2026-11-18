"""Render the draft figures from grid endpoints and a stated toy learning curve.

Grid endpoints are final natural-language validation rows from
action-prepretrain-2026-09/results/runs/<run>/metrics.jsonl.
Token counts and FLOP estimates follow that study's PREREG.md.
Run: python3 _scripts/make_pretraining_figures.py
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUTPUT = Path(__file__).resolve().parents[1] / "images/posts/synthetic-pretraining"
BLUE = "#176788"
ORANGE = "#a04829"
GRAY = "#555e66"


def save(fig, name):
    fig.savefig(OUTPUT / name, dpi=180, facecolor="white")
    plt.close(fig)


with (OUTPUT / "grid-endpoints.csv").open(newline="") as file:
    rows = {row["run"]: row for row in csv.DictReader(file)}

ladder = [rows[name] for name in ("A300_s0", "A400_s0", "A_s0", "A650_s0", "A800_s0")]
log_tokens = np.log([int(row["language_tokens"]) for row in ladder])
losses = np.array([float(row["final_loss"]) for row in ladder])
assert np.all(np.diff(losses) < 0)

# Both phases have the same blocks and context length. The output vocabularies differ.
shared_cost = 6 * (8 * 12 * 512**2 + 8 * 1024 * 512)
ratio = (shared_cost + 6 * 262 * 512) / (shared_cost + 6 * 50304 * 512)

fig, ax = plt.subplots(figsize=(7.6, 3.3), layout="constrained")
names = ("D_s0", "D_s1", "D_s2", "D30_s0")
labels = ("100M · seed 0", "100M · seed 1", "100M · seed 2", "30M · seed 0")
for index, name in enumerate(names):
    row = rows[name]
    loss = float(row["final_loss"])
    used = int(row["language_tokens"])
    paid = ratio * int(row["synthetic_tokens"])
    assert losses[-1] <= loss <= losses[0]
    equivalent = np.exp(np.interp(-loss, -losses, log_tokens))
    credited = equivalent - used
    assert log_tokens[0] <= np.log(used + paid) <= log_tokens[-1]
    threshold = np.interp(np.log(used + paid), log_tokens, losses)
    print(f"{name}: extra text matched={credited/1e6:.2f}M, cost={paid/1e6:.2f}M, "
          f"net={(credited-paid)/1e6:+.2f}M, target loss={threshold:.5f}, "
          f"saved={(credited-paid)/equivalent:+.3%}")

    ax.plot([credited / 1e6, paid / 1e6], [index, index], color="#bbc2c7", zorder=1)
    ax.scatter(credited / 1e6, index, color=BLUE, s=55, zorder=3)
    ax.scatter(paid / 1e6, index, color=ORANGE, marker="D", s=43, zorder=3)

ax.scatter([], [], color=BLUE, label="Extra text matched")
ax.scatter([], [], color=ORANGE, marker="D", label="Cost of warm-up")
ax.set_yticks(range(len(names)), labels)
ax.invert_yaxis()
ax.set_xlim(0, 62)
ax.set_xlabel("Millions of English tokens at equivalent training compute")
ax.set_title("The 100M-token warm-up fell short of break-even", loc="left", fontsize=13)
ax.grid(axis="x", color="#e1e5e8")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, frameon=False)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, "grid-compute-break-even.png")

# Show the loss scale and the compute scale for the same illustrative warm-up.
# The arbitrary curve has L(D) = 2 + D^(-0.4), with a shift of 0.25 and cost of 0.15.
language = np.geomspace(1, 100, 300)
shift, cost = 0.25, 0.15
gap = language**-0.4 - (language + shift)**-0.4
saving = (shift - cost) / (language + shift)
fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.0), sharex=True, layout="constrained")
for ax, series, title, ylabel, color in (
    (axes[0], gap, "The loss gap shrinks", "Loss gap (nats)", BLUE),
    (axes[1], saving * 100, "The fraction of compute saved shrinks", "Compute saved (%)", ORANGE),
):
    ax.loglog(language, series, color=color, linewidth=2)
    ax.set_title(title, loc="left", fontsize=12)
    ax.set_ylabel(ylabel)
    ax.grid(which="major", alpha=0.25, color=GRAY)
    ax.spines[["top", "right"]].set_visible(False)
axes[1].set_xlabel("Language training budget (arbitrary units)")
save(fig, "fixed-head-start.png")

# Shared optimum, diagonal quadratics, one unit of compute per unit of flow.
# The two initial loss contributions are lambda_i / 2 for unit initial errors.
rates = np.array([1.0, 0.2])
source_rates = np.array([1.5, 0.1])
advantages = source_rates - rates
initial_losses = rates / 2
total = np.linspace(0.75, 3, 350)
weights = initial_losses[:, None] * np.exp(-2 * rates[:, None] * total)
dose = 0.75
matched_terms = weights * -np.expm1(-2 * advantages[:, None] * dose)
text_matched_gap = np.sum(weights * -np.expm1(-2 * source_rates[:, None] * dose), axis=0)

fast, slow = advantages
log_ratio = np.log(initial_losses[0] * fast / (-initial_losses[1] * slow))
last_useful_budget = log_ratio / (2 * (rates[0] - rates[1]))
optimal_dose = np.clip(
    (log_ratio - 2 * (rates[0] - rates[1]) * total) / (2 * (fast - slow)),
    0,
    total,
)

fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.2), sharex=True, layout="constrained")
axes[0].plot(total, text_matched_gap, color=BLUE, label="Equal language exposure")
axes[0].plot(total, matched_terms.sum(axis=0), color=ORANGE, linestyle="--",
             label="Equal total compute")
axes[0].axhline(0, color=GRAY, linewidth=0.9)
axes[0].set_ylabel("Scratch loss − warm loss")
axes[0].set_title("The same warm-up wins on text and can lose on compute", loc="left", fontsize=12)
axes[0].legend(frameon=False)
axes[1].plot(total, optimal_dose, color=ORANGE)
axes[1].axvline(last_useful_budget, color=GRAY, linewidth=0.9, linestyle=":")
axes[1].set_title("Beyond the threshold, the best dose is zero", loc="left", fontsize=12)
axes[1].set_ylabel("Optimal synthetic dose")
axes[1].set_xlabel("Scratch training budget (language compute units)")
for ax in axes:
    ax.grid(axis="x", alpha=0.25, color=GRAY)
    ax.spines[["top", "right"]].set_visible(False)
save(fig, "two-mode-transfer.png")

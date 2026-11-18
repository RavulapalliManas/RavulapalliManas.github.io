"""Rebuild the posts' plots from their accompanying CSV snapshots.

Run from the site root: python3 _scripts/make_post_figures.py
The CSVs preserve the values reported by the original analyses; they are not raw runs.
"""
from pathlib import Path
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / 'images/posts/action-warmup'
LIFE = ROOT / 'images/posts/artificial-life'
matplotlib.rcParams.update({
    'font.family': ['Chalkboard SE', 'DejaVu Sans'],
    'font.size': 11,
    'svg.fonttype': 'path',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
})


def rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def save(fig, path, description):
    fig.savefig(path, bbox_inches='tight', metadata={'Date': None, 'Description': description})
    plt.close(fig)
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')


paired = rows(ACTION / 'paired-loss.csv')
fig, ax = plt.subplots(figsize=(8.2, 3.6), layout='constrained')
for index, row in enumerate(paired):
    visible, hidden = float(row['moves_visible_loss']), float(row['moves_hidden_loss'])
    y = 2 - index
    ax.plot([visible, hidden], [y, y], color='0.5', linewidth=1.5, zorder=1)
    ax.scatter(visible, y, marker='o', s=80, color='#202020', zorder=3)
    ax.scatter(hidden, y, marker='o', s=80, facecolor='white', edgecolor='#202020', linewidth=1.5, zorder=3)
    ax.text(visible - 0.002, y + 0.15, f'{visible:.3f}', ha='center', fontsize=10)
    ax.text(hidden + 0.002, y + 0.15, f'{hidden:.3f}', ha='center', fontsize=10)
ax.scatter([], [], s=65, color='#202020', label='Moves visible')
ax.scatter([], [], s=65, facecolor='white', edgecolor='#202020', label='Moves hidden')
ax.set_yticks([2, 1, 0], [f"Seed {row['seed']}" for row in paired])
ax.set_ylim(-0.5, 2.55)
ax.set_xlim(3.64, 3.725)
ax.set_xlabel('Held-out English loss (nats); lower is better')
ax.grid(axis='x', color='0.9')
ax.legend(loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.02))
ax.set_title('The same-seed comparison', loc='left', pad=18)
save(fig, ACTION / 'paired-loss.svg', 'Source: paired-loss.csv, derived from the study preregistration scores.')

pressure = rows(LIFE / 'need-pressure.csv')
fig, ax = plt.subplots(figsize=(7.2, 4.0), layout='constrained')
xs = np.arange(len(pressure))
means = [float(r['mean_score']) for r in pressure]
sds = [float(r['sample_sd']) for r in pressure]
ax.errorbar(xs, means, yerr=sds, fmt='o', color='#202020', ecolor='#555555', capsize=5, markersize=7, linewidth=1.2)
for x, y in zip(xs, means):
    ax.annotate(f'{y:.3f}', (x, y), xytext=(0, 14), textcoords='offset points', ha='center', fontsize=10)
ax.set_xticks(xs, [r['training_pressure'].replace('x', '×') for r in pressure])
ax.set_xlabel('Training need pressure (native level = 1×)')
ax.set_ylabel('Mean achievement score across training')
ax.set_ylim(0, 5.15)
ax.grid(axis='y', color='0.9')
ax.set_title('A middle pressure performed best in this test', loc='left', pad=12)
save(fig, LIFE / 'need-pressure.svg', 'Source: need-pressure.csv; points are seed means, whiskers are sample standard deviations.')

modules = rows(LIFE / 'module-scores.csv')
fig, ax = plt.subplots(figsize=(8.4, 4.0), layout='constrained')
ys = np.arange(len(modules))[::-1]
for y, row in zip(ys, modules):
    mean, sd = float(row['mean_score']), float(row['sample_sd'])
    ax.errorbar(mean, y, xerr=sd, fmt='o', color='#202020', ecolor='#555555', capsize=4, markersize=7, linewidth=1.2)
    ax.text(mean + sd + 0.07, y, f'{mean:.3f}', va='center', fontsize=10)
ax.set_yticks(ys, [f"{r['configuration']}  (n={r['seeds']})" for r in modules])
ax.set_xlim(0, 5.35)
ax.set_ylim(-0.7, 3.7)
ax.set_xlabel('Mean achievement score across training')
ax.grid(axis='x', color='0.9')
ax.set_title('The assembled configurations scored lower', loc='left', pad=12)
save(fig, LIFE / 'module-scores.svg', 'Source: module-scores.csv; points are means, whiskers are sample standard deviations.')
print('Wrote three SVG plots from CSV snapshots.')

control = rows(LIFE / 'temperature-control.csv')
fig, ax = plt.subplots(figsize=(7.5, 4.3), layout='constrained')
for label, color, marker in [('body-dependent', '#202020', 'o'), ('fixed', '#a34a31', 's')]:
    group = [row for row in control if row['temperature'] == label]
    ax.errorbar(range(3), [float(r['mean_score']) for r in group],
                yerr=[float(r['sample_sd']) for r in group], label=label.capitalize(),
                color=color, marker=marker, capsize=4, linewidth=1.5)
ax.set_xticks(range(3), ['1×', '6×', '24×'])
ax.set_xlabel('Training need pressure')
ax.set_ylabel('Mean achievement score across training')
ax.set_ylim(0, 5.1)
ax.grid(axis='y', color='0.9')
ax.legend(title='Temperature', frameon=False)
ax.set_title('Fixing temperature changes the pressure comparison', loc='left')
save(fig, LIFE / 'temperature-control.svg', 'Source: temperature-control.csv, transcribed from the Stage 0 report; whiskers are sample standard deviations across 20 seeds.')

dose = rows(ACTION / 'dose-loss.csv')
fig, ax = plt.subplots(figsize=(7.2, 4), layout='constrained')
ax.plot([float(r['synthetic_tokens']) / 1e6 for r in dose],
        [float(r['final_loss']) for r in dose], 'o-', color='#202020')
for r in dose:
    ax.annotate(f"{float(r['final_loss']):.4f}",
                (float(r['synthetic_tokens']) / 1e6, float(r['final_loss'])),
                xytext=(0, 10), textcoords='offset points', ha='center')
ax.set_xlabel('Synthetic warm-up tokens (millions)')
ax.set_ylabel('Held-out English loss (nats)')
ax.set_title('A shorter warm-up kept part of the gain', loc='left')
ax.grid(axis='y', color='0.9')
save(fig, ACTION / 'dose-loss.svg', 'Source: dose-loss.csv, from results/results.json. One seed per dose; all runs used the same English budget.')

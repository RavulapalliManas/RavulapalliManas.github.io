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

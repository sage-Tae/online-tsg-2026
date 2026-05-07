"""Regenerate Fig 1 (r vs r**), Fig 2 (k-regime), Fig 4 (coalition reduction),
Fig 5 (r** vs r* histogram) from full 175-instance NN run."""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'legend.fontsize': 10, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False,
})

SRC = '../experiments/logs/policy_comparison.csv'
df = pd.read_csv(SRC)
nn = df[df.policy == 'nearest_neighbor'].copy()

pattern_order = ['A', 'B1', 'B2', 'B5', 'C', 'D', 'E']
pattern_labels = {
    'A': 'A\n(simul.)',
    'B1': 'B1\n(seq., $\\lambda$=1)',
    'B2': 'B2\n(seq., $\\lambda$=2)',
    'B5': 'B5\n(seq., $\\lambda$=5)',
    'C': 'C\n(cluster)',
    'D': 'D\n(reverse)',
    'E': 'E\n(random)',
}

# ===== Fig 1 (was fig2_r_vs_rstar): r vs r** scatter, using all applicable instances =====
# For non-applicable instances r_ss is NaN; skip those points.
applicable = nn.dropna(subset=['r_ss']).copy()
non_app = nn[nn.r_ss.isna()].copy()  # these are not on the r** axis; omit
core_yes = applicable[applicable.core_nonempty]
core_no = applicable[~applicable.core_nonempty]
# Also include empty-Core instances where r** undefined (k < n-1 can't have empties, so
# empties only arise in applicable set). Cross-check:
assert (non_app.core_nonempty.all()), "Non-applicable instances expected all nonempty Core"

fig, ax = plt.subplots(figsize=(6.5, 5))
ax.scatter(core_yes['r_ss'], core_yes['r'], s=28, alpha=0.6,
           color='#1f77b4', edgecolor='none',
           label=f'Core non-empty (n={len(core_yes)})')
ax.scatter(core_no['r_ss'], core_no['r'], s=55, alpha=0.95,
           color='#d62728', edgecolor='black', linewidth=0.6, marker='X',
           label=f'Core empty (n={len(core_no)})')
mn = min(applicable['r_ss'].min(), applicable['r'].min()) - 0.02
mx = max(applicable['r_ss'].max(), applicable['r'].max()) + 0.02
ax.plot([mn, mx], [mn, mx], 'k--', linewidth=0.8, label=r'$r = r^{**}$')
ax.set_xlabel(r'$r^{**} = 1 + \min_i \delta_i / c^\ast(N)$')
ax.set_ylabel(r'$r = C(N)_{\text{online}}/c^\ast(N)$')
ax.set_title(r'Theorem 11: $r > r^{**} \Rightarrow$ Core $= \emptyset$')
ax.legend(loc='lower right', frameon=True)
ax.set_xlim(mn, mx)
ax.set_ylim(mn, mx)
plt.tight_layout()
plt.savefig('fig2_r_vs_rstar.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 2 (was fig3_core_vs_k): k-regime bar chart =====
nn['regime'] = nn.apply(
    lambda r: r'$k<n-1$' if r['k'] < r['n']-1 else
              (r'$k=n-1$' if r['k'] == r['n']-1 else r'$k=n$'), axis=1)
regimes = [r'$k<n-1$', r'$k=n-1$', r'$k=n$']
rate_k = nn.groupby('regime')['core_nonempty'].agg(['mean','count']).reindex(regimes)
fig, ax = plt.subplots(figsize=(6.5, 4))
colors_k = ['#2ca02c', '#1f77b4', '#d62728']
ax.bar(range(len(regimes)), rate_k['mean'].values,
       color=colors_k, edgecolor='black', linewidth=0.8, width=0.55)
ax.set_xticks(range(len(regimes)))
ax.set_xticklabels(
    [f'{r}\n($n$={c})' for r, c in zip(regimes, rate_k['count'].values)],
    fontsize=12,
)
ax.set_ylabel('Temporal Core existence rate')
ax.set_ylim(0, 1.12)
ax.axhline(1.0, linestyle=':', color='gray', linewidth=0.8)
for i, v in enumerate(rate_k['mean'].values):
    ax.text(i, v + 0.03, f'{v:.2f}', ha='center', fontsize=11)
ax.set_title(r'Core existence rate by peak-queue regime $k$')
plt.tight_layout()
plt.savefig('fig3_core_vs_k.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 4 (was fig4_coalition_reduction): |F|/(2^n-1) by pattern =====
nn['F_ratio'] = nn['n_feasible'] / (2**nn['n'] - 1)
means = nn.groupby('pattern')['F_ratio'].mean().reindex(pattern_order)
stderr = nn.groupby('pattern')['F_ratio'].sem().reindex(pattern_order)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(range(len(pattern_order)), means.values, yerr=stderr.values,
       color='#4c72b0', edgecolor='black', linewidth=0.8, capsize=4)
ax.set_xticks(range(len(pattern_order)))
ax.set_xticklabels([pattern_labels[p] for p in pattern_order])
ax.set_ylabel(r'$|\mathcal{F}| / (2^{n}-1)$')
ax.set_ylim(0, 1.15)
for i, (v, se) in enumerate(zip(means.values, stderr.values)):
    offset = (se if np.isfinite(se) else 0.0) + 0.025
    ax.text(i, v + offset, f'{v:.2f}', ha='center', fontsize=10)
ax.set_title('Feasible coalitions relative to all non-empty coalitions')
plt.tight_layout()
plt.savefig('fig4_coalition_reduction.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 5 (was fig5_rstar_vs_rss): r** vs r* histogram =====
fig, ax = plt.subplots(figsize=(6.8, 4))
r_max = max(nn.r_star.max(), nn.r_ss.max(skipna=True)) + 0.3
bins = np.linspace(1.0, r_max, 50)
ax.hist(nn['r_ss'].dropna(), bins=bins, alpha=0.7, color='#2ca02c',
        edgecolor='black', linewidth=0.5,
        label=r'$r^{**}$ (tight bound, Thm. 11)')
ax.hist(nn['r_star'], bins=bins, alpha=0.55, color='#d62728',
        edgecolor='black', linewidth=0.5, label=r'$r^{*}$ (Remark 8 bound)')
ax.set_xlabel('Threshold value')
ax.set_ylabel('Frequency')
ax.set_title(r'Distribution of critical ratios $r^{**}$ and $r^{*}$')
ax.legend()
plt.tight_layout()
plt.savefig('fig5_rstar_vs_rss.pdf', bbox_inches='tight')
plt.close()

print("Regenerated: fig2_r_vs_rstar, fig3_core_vs_k, fig4_coalition_reduction, fig5_rstar_vs_rss")
print(f"  applicable count = {len(applicable)}")
print(f"  empty & applicable = {len(core_no)}")
print(f"  nonempty & applicable = {len(core_yes)}")

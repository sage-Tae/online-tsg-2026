import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'font.family': 'serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

df = pd.read_csv('../results/summary.csv')
val = pd.read_csv('../results/theorem5_validation.csv')

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

# ===== Fig 1: Core existence rate by pattern =====
fig, ax = plt.subplots(figsize=(7, 4))
rates = df.groupby('pattern')['temporal_core'].mean().reindex(pattern_order)
stderr = df.groupby('pattern')['temporal_core'].sem().reindex(pattern_order)
colors = ['#d62728' if p == 'A' else ('#ff7f0e' if p == 'C' else '#2ca02c') for p in pattern_order]
bars = ax.bar(range(len(pattern_order)), rates.values, yerr=stderr.values,
              color=colors, edgecolor='black', linewidth=0.8, capsize=4)
ax.set_xticks(range(len(pattern_order)))
ax.set_xticklabels([pattern_labels[p] for p in pattern_order])
ax.set_ylabel('Temporal Core existence rate')
ax.set_ylim(0, 1.1)
ax.axhline(1.0, linestyle=':', color='gray', linewidth=0.8)
for i, v in enumerate(rates.values):
    ax.text(i, v + 0.04, f'{v:.2f}', ha='center', fontsize=10)
ax.set_title('Core existence rate across arrival patterns')
plt.tight_layout()
plt.savefig('fig1_core_rate.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 3 (new): Core rate stratified by k regime (Corollary 14) =====
val2 = val.copy()
val2['regime'] = val2.apply(
    lambda r: r'$k<n-1$' if r['k'] < r['n']-1 else
              (r'$k=n-1$' if r['k'] == r['n']-1 else r'$k=n$'), axis=1)
regimes = [r'$k<n-1$', r'$k=n-1$', r'$k=n$']
rate_k = val2.groupby('regime')['temporal_core'].agg(['mean','count']).reindex(regimes)
fig, ax = plt.subplots(figsize=(6.5, 4))
colors_k = ['#2ca02c', '#1f77b4', '#d62728']
bars = ax.bar(range(len(regimes)), rate_k['mean'].values,
              color=colors_k, edgecolor='black', linewidth=0.8, width=0.55)
ax.set_xticks(range(len(regimes)))
ax.set_xticklabels(regimes, fontsize=12)
ax.set_ylabel('Temporal Core existence rate')
ax.set_ylim(0, 1.12)
ax.axhline(1.0, linestyle=':', color='gray', linewidth=0.8)
for i, (v, c) in enumerate(zip(rate_k['mean'].values, rate_k['count'].values)):
    ax.text(i, v + 0.03, f'{v:.2f}', ha='center', fontsize=11)
    ax.text(i, -0.06, f'n={c}', ha='center', fontsize=10, color='gray')
ax.set_title(r'Core existence rate by peak-queue regime $k$')
plt.tight_layout()
plt.savefig('fig3_core_vs_k.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 2: r vs r** scatter =====
fig, ax = plt.subplots(figsize=(6.5, 5))
core_yes = val[val['temporal_core']]
core_no = val[~val['temporal_core']]
ax.scatter(core_yes['r_double_star'], core_yes['r'], s=28, alpha=0.6,
           color='#1f77b4', edgecolor='none', label=f'Core non-empty (n={len(core_yes)})')
ax.scatter(core_no['r_double_star'], core_no['r'], s=55, alpha=0.95,
           color='#d62728', edgecolor='black', linewidth=0.6,
           marker='X', label=f'Core empty (n={len(core_no)})')
mn = min(val['r_double_star'].min(), val['r'].min()) - 0.02
mx = max(val['r_double_star'].max(), val['r'].max()) + 0.02
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

# ===== Fig 3: Core existence rate by n (per pattern) =====
fig, ax = plt.subplots(figsize=(7, 4.3))
markers = ['o', 's', '^', 'D', 'v', 'P', 'X']
ns = sorted(df['n'].unique())
for i, p in enumerate(pattern_order):
    sub = df[df['pattern'] == p].groupby('n')['temporal_core'].mean().reindex(ns)
    ax.plot(ns, sub.values, marker=markers[i], label=p, linewidth=1.6, markersize=7)
ax.set_xlabel(r'$n$ (coalition size)')
ax.set_ylabel('Core existence rate')
ax.set_xticks(ns)
ax.set_ylim(-0.05, 1.1)
ax.legend(title='Pattern', loc='lower left', ncol=4, frameon=True)
ax.set_title('Core existence rate versus coalition size $n$')
plt.tight_layout()
plt.savefig('fig3_core_vs_n.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 4: Coalition reduction ratio =====
fig, ax = plt.subplots(figsize=(7, 4))
cr = df.groupby('pattern')['coalition_reduction_ratio'].mean().reindex(pattern_order)
crse = df.groupby('pattern')['coalition_reduction_ratio'].sem().reindex(pattern_order)
ax.bar(range(len(pattern_order)), cr.values, yerr=crse.values,
       color='#4c72b0', edgecolor='black', linewidth=0.8, capsize=4)
ax.set_xticks(range(len(pattern_order)))
ax.set_xticklabels([pattern_labels[p] for p in pattern_order])
ax.set_ylabel(r'$|\mathcal{F}| / (2^{n}-1)$')
ax.set_ylim(0, 1.1)
for i, v in enumerate(cr.values):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=10)
ax.set_title('Feasible coalitions relative to all non-empty coalitions')
plt.tight_layout()
plt.savefig('fig4_coalition_reduction.pdf', bbox_inches='tight')
plt.close()

# ===== Fig 5: r** vs r* distributions (log scale) =====
fig, ax = plt.subplots(figsize=(6.8, 4))
bins = np.linspace(1.0, 6.5, 40)
ax.hist(val['r_double_star'], bins=bins, alpha=0.7, color='#2ca02c',
        edgecolor='black', linewidth=0.5, label=r'$r^{**}$ (tight bound, Thm. 11)')
ax.hist(df['r_star'], bins=bins, alpha=0.55, color='#d62728',
        edgecolor='black', linewidth=0.5, label=r'$r^{*}$ (Remark 8 bound)')
ax.set_xlabel('Threshold value')
ax.set_ylabel('Frequency')
ax.set_title(r'Distribution of critical ratios $r^{**}$ and $r^{*}$')
ax.legend()
plt.tight_layout()
plt.savefig('fig5_rstar_vs_rss.pdf', bbox_inches='tight')
plt.close()

print("All figures generated.")

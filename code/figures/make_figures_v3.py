"""
Phase 2.3: regenerate all 5 paper figures from v2_full data with new
pattern names (B_heavy / B_medium / B_light).

Input: ../experiments/logs/policy_comparison_v2_full.csv  (525 rows)

Output (5 PDFs, consumed by paper/main.tex via \graphicspath{../figures/}):
  fig2_r_vs_rstar.pdf
  fig3_core_vs_k.pdf
  fig3_core_vs_n.pdf
  fig4_coalition_reduction.pdf
  fig5_rstar_vs_rss.pdf
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'legend.fontsize': 10, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False,
})

SRC = '../experiments/logs/policy_comparison_v2_full.csv'
df = pd.read_csv(SRC)
nn = df[df.policy == 'nearest_neighbor'].copy()

pattern_order = ['A', 'B_heavy', 'B_medium', 'B_light', 'C', 'D', 'E']
pattern_labels = {
    'A':        'A\n($\\rho=\\infty$)',
    'B_heavy':  r'B$_\mathrm{heavy}$' + '\n($\\rho=4$)',
    'B_medium': r'B$_\mathrm{medium}$' + '\n($\\rho=2$)',
    'B_light':  r'B$_\mathrm{light}$' + '\n($\\rho=0.5$)',
    'C':        'C\n($\\rho=2$, cluster)',
    'D':        'D\n($\\rho=1$, reverse)',
    'E':        'E\n($\\rho=1$, random)',
}
pattern_short = {
    'A': 'A', 'B_heavy': r'B$_\mathrm{heavy}$', 'B_medium': r'B$_\mathrm{medium}$',
    'B_light': r'B$_\mathrm{light}$', 'C': 'C', 'D': 'D', 'E': 'E',
}


# =========================================================================
# Fig 2: r vs r** scatter, with 4-mechanism classification overlay
# =========================================================================
applicable = nn.dropna(subset=['r_ss']).copy()

# Classify by empty_mechanism column (present after Phase 2 augment)
core_yes  = applicable[applicable['empty_mechanism'] == 'core_nonempty']
single    = applicable[applicable['empty_mechanism'] == 'single_complement']
balanced  = applicable[applicable['empty_mechanism'] == 'balanced_complement']
near_comp = applicable[applicable['empty_mechanism'] == 'near_complement']

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.scatter(core_yes['r_ss'], core_yes['r'], s=24, alpha=0.55,
           color='#1f77b4', edgecolor='none',
           label=f'Core non-empty (n={len(core_yes)})')
ax.scatter(single['r_ss'], single['r'], s=60, alpha=0.95,
           color='#d62728', edgecolor='black', linewidth=0.6, marker='X',
           label=f'Single-complement / Thm 9 (n={len(single)})')
ax.scatter(balanced['r_ss'], balanced['r'], s=55, alpha=0.95,
           color='#ff7f0e', edgecolor='black', linewidth=0.6, marker='s',
           label=f'Balanced-complement / Prop 10 (n={len(balanced)})')
ax.scatter(near_comp['r_ss'], near_comp['r'], s=55, alpha=0.95,
           color='#9467bd', edgecolor='black', linewidth=0.6, marker='D',
           label=f'Near-complement / Remark 12 (n={len(near_comp)})')

# Intermediate cases (Obs 15) have r_ss = NaN, so they cannot be plotted
# on this (r, r**) panel.  Annotate count.
inter_count = len(nn[nn['empty_mechanism'] == 'intermediate'])
ax.text(0.02, 0.98,
        f'+{inter_count} intermediate (Obs 15) at r**=undefined; see Supplementary Materials S3',
        transform=ax.transAxes, fontsize=8, verticalalignment='top',
        color='#2ca02c', style='italic')

mn = min(applicable['r_ss'].min(), applicable['r'].min()) - 0.02
mx = max(applicable['r_ss'].max(), applicable['r'].max()) + 0.02
ax.plot([mn, mx], [mn, mx], 'k--', linewidth=0.8, label=r'$r = r^{**}$')
ax.set_xlabel(r'$r^{**} = 1 + \min_i \delta_i / c^\ast(N)$')
ax.set_ylabel(r'$r = C(N)_{\mathrm{online}}/c^\ast(N)$')
ax.set_title(r'$r > r^{**} \Rightarrow$ Core $= \emptyset$; four-mechanism overlay')
ax.legend(loc='lower right', frameon=True, fontsize=9)
ax.set_xlim(mn, mx)
ax.set_ylim(mn, mx)
plt.tight_layout()
plt.savefig('fig2_r_vs_rstar.pdf', bbox_inches='tight')
plt.close()


# =========================================================================
# Fig 3 (k-regime): Core rate stratified by k
# =========================================================================
nn['regime'] = nn.apply(
    lambda r: r'$k<n-1$' if r['k'] < r['n']-1 else
              (r'$k=n-1$' if r['k'] == r['n']-1 else r'$k=n$'), axis=1)
regimes = [r'$k<n-1$', r'$k=n-1$', r'$k=n$']
rate_k = nn.groupby('regime')['core_nonempty'].agg(['mean', 'count']).reindex(regimes)

fig, ax = plt.subplots(figsize=(6.5, 4))
colors_k = ['#2ca02c', '#1f77b4', '#d62728']
ax.bar(range(len(regimes)), rate_k['mean'].values,
       color=colors_k, edgecolor='black', linewidth=0.8, width=0.55)
ax.set_xticks(range(len(regimes)))
ax.set_xticklabels(
    [f'{r}\n($n$={int(c)})' for r, c in zip(regimes, rate_k['count'].values)],
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


# =========================================================================
# Fig 4: |F|/(2^n - 1) by pattern
# =========================================================================
nn['F_ratio'] = nn['n_feasible'] / (2**nn['n'] - 1)
means = nn.groupby('pattern')['F_ratio'].mean().reindex(pattern_order)
stderr = nn.groupby('pattern')['F_ratio'].sem().reindex(pattern_order)

fig, ax = plt.subplots(figsize=(7.5, 4))
ax.bar(range(len(pattern_order)), means.values, yerr=stderr.values,
       color='#4c72b0', edgecolor='black', linewidth=0.8, capsize=4)
ax.set_xticks(range(len(pattern_order)))
ax.set_xticklabels([pattern_labels[p] for p in pattern_order], fontsize=9)
ax.set_ylabel(r'$|\mathcal{F}| / (2^{n}-1)$')
ax.set_ylim(0, 1.15)
for i, (v, se) in enumerate(zip(means.values, stderr.values)):
    offset = (se if np.isfinite(se) else 0.0) + 0.025
    ax.text(i, v + offset, f'{v:.2f}', ha='center', fontsize=10)
ax.set_title('Feasible coalitions relative to all non-empty coalitions')
plt.tight_layout()
plt.savefig('fig4_coalition_reduction.pdf', bbox_inches='tight')
plt.close()


# =========================================================================
# Fig 5: r**, r***, and r* histograms (3-way comparison)
# =========================================================================
fig, ax = plt.subplots(figsize=(7, 4))
r_max = max(nn.r_star.max(), nn.r_ss.max(skipna=True)) + 0.3
bins = np.linspace(1.0, r_max, 50)
ax.hist(nn['r_ss'].dropna(), bins=bins, alpha=0.65, color='#2ca02c',
        edgecolor='black', linewidth=0.5,
        label=r'$r^{**}$ (Thm. 9, single-complement)')
ax.hist(nn['r_sss'].dropna(), bins=bins, alpha=0.65, color='#1f77b4',
        edgecolor='black', linewidth=0.5,
        label=r'$r^{***}$ (Prop. 10, balanced-complement)')
ax.hist(nn['r_star'], bins=bins, alpha=0.45, color='#d62728',
        edgecolor='black', linewidth=0.5,
        label=r'$r^{*}$ (classical bound, Remark 6)')
ax.set_xlabel('Threshold value')
ax.set_ylabel('Frequency')
ax.set_title(r'Distributions of critical ratios $r^{**}$, $r^{***}$, and $r^{*}$')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('fig5_rstar_vs_rss.pdf', bbox_inches='tight')
plt.close()


# =========================================================================
# Fig 3_core_vs_n (Supplementary Materials S1): Core existence rate versus n per pattern
# =========================================================================
fig, ax = plt.subplots(figsize=(7.5, 4.3))
markers = ['o', 's', '^', 'D', 'v', 'P', 'X']
ns = sorted(nn['n'].unique())
for i, p in enumerate(pattern_order):
    sub = nn[nn['pattern'] == p].groupby('n')['core_nonempty'].mean().reindex(ns)
    ax.plot(ns, sub.values, marker=markers[i], label=pattern_short[p],
            linewidth=1.6, markersize=7)
ax.set_xlabel(r'$n$ (coalition size)')
ax.set_ylabel('Core existence rate')
ax.set_xticks(ns)
ax.set_ylim(-0.05, 1.1)
ax.legend(title='Pattern', loc='lower left', ncol=4, frameon=True)
ax.set_title('Core existence rate versus coalition size $n$')
plt.tight_layout()
plt.savefig('fig3_core_vs_n.pdf', bbox_inches='tight')
plt.close()


print("Regenerated: fig2_r_vs_rstar, fig3_core_vs_k, fig3_core_vs_n,")
print("             fig4_coalition_reduction, fig5_rstar_vs_rss")
print(f"  Input: {SRC}, NN rows = {len(nn)}")
print(f"  Applicable (r** defined): {len(applicable)}")
print(f"  single (Thm 9 fires): {len(single)}")
print(f"  balanced-complement: {len(balanced)}")
print(f"  near-complement: {len(near_comp)}")
print(f"  intermediate (Obs 15, r**=undef): {inter_count}")
print(f"  Nonempty & applicable: {len(core_yes)}")
print(f"  k regimes: k<n-1={int(rate_k.loc[r'$k<n-1$', 'count'])}, "
      f"k=n-1={int(rate_k.loc[r'$k=n-1$', 'count'])}, "
      f"k=n={int(rate_k.loc[r'$k=n$', 'count'])}")

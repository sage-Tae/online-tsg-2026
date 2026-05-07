"""
Phase 2 post-run: Residual binding analysis.

Classify the Core-empty-but-Thm11-vacuous instances from summary,
then for each one solve the first-stage nucleolus LP and record the
coalition-size distribution of the binding constraints at the
optimum.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'experiments'))

import pandas as pd
import pulp

from config import PATTERN_RHO, L_N2, tau_from_rho
from generators import generate_customers, generate_arrivals
from src.policies import make_policies
from src.policy_simulator import run_with_policy
from src.feasibility import reconstruct_F, compute_coalition_costs


SUMMARY_CSV = os.path.join(ROOT, 'experiments/logs/policy_comparison_v2_full.csv')
OUT_MD = os.path.join(ROOT, '..', 'docs', 'phase2_residual_analysis.md')


def first_stage_tight_sizes(coalition_costs, C_N, players, tol=1e-6):
    """Solve first-stage nucleolus LP and return (eps*, tight_sizes_dict).

    tight_sizes_dict maps size -> count of tight constraints of that size
    at the LP optimum.  Constraints are 'tight' iff x(S) - c(S) is within
    tol of epsilon*.
    """
    n = len(players)
    coalitions = [S for S in coalition_costs if 0 < len(S) < n]
    if not coalitions:
        return None, {}

    prob = pulp.LpProblem("first_stage", pulp.LpMinimize)
    y = {p: pulp.LpVariable(f"y_{p}", cat='Continuous') for p in players}
    eps = pulp.LpVariable("eps", cat='Continuous')
    prob += eps
    prob += pulp.lpSum(y[p] for p in players) == C_N
    for S in coalitions:
        prob += pulp.lpSum(y[p] for p in S) - coalition_costs[S] <= eps

    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=60))
    if status != pulp.constants.LpStatusOptimal:
        return None, {}
    eps_star = pulp.value(eps)
    y_val = {p: pulp.value(y[p]) for p in players}

    tight_sizes = {}
    for S in coalitions:
        lhs = sum(y_val[p] for p in S)
        excess = lhs - coalition_costs[S]
        if abs(excess - eps_star) < tol:
            sz = len(S)
            tight_sizes[sz] = tight_sizes.get(sz, 0) + 1
    return eps_star, tight_sizes


def classify_binding(n, tight_sizes):
    """Interpret a binding distribution.

    - near-complement: concentrated at {n-1, n-2}, with fraction of
      tight constraints in those sizes >= 0.7
    - intermediate:    any tight constraint at size 2..n-3
    - complement-only: tight only at size n-1 (Thm 11 would usually
      catch this unless vacuous due to Pattern A anomaly)
    """
    if not tight_sizes:
        return 'lp_failed'
    total = sum(tight_sizes.values())
    near = tight_sizes.get(n - 1, 0) + tight_sizes.get(n - 2, 0)
    intermediate = sum(cnt for sz, cnt in tight_sizes.items() if 2 <= sz <= n - 3)
    comp_only = tight_sizes.get(n - 1, 0) == total
    if comp_only:
        return 'complement-only'
    if near / total >= 0.7:
        return 'near-complement'
    if intermediate > 0:
        return 'intermediate'
    return 'mixed'


def main():
    df = pd.read_csv(SUMMARY_CSV)
    nn = df[df['policy'] == 'nearest_neighbor'].copy()

    # Residual: Core empty but Thm 11 didn't fire
    residual = nn[(nn['core_nonempty'] == False) & (nn['theorem11_fires'] == False)].copy()

    # Group classification
    g1 = residual[residual['r_ss'].isna()].copy()                    # no complement
    g2 = residual[residual['r_ss'].notna() &
                  (residual['r'] <= residual['r_ss'] + 1e-9)].copy()  # r <= r_ss
    g3 = residual[residual['r_ss'].notna() &
                  (residual['r'] > residual['r_ss'] + 1e-9)].copy()   # classification bug

    print("=" * 75)
    print("RESIDUAL CLASSIFICATION (NN, main grid)")
    print("=" * 75)
    print(f"Total residual (empty & !fires): {len(residual)}")
    print(f"  Group 1 (r_ss=NaN, no complement): {len(g1)}")
    print(f"  Group 2 (r_ss defined, r<=r_ss):   {len(g2)}")
    print(f"  Group 3 (sanity bug if >0):        {len(g3)}")
    assert len(g3) == 0, "Group 3 must be 0"
    print()

    # Per-pattern counts in each group
    print("Per-pattern counts:")
    for label, g in [('Group 1', g1), ('Group 2', g2)]:
        counts = g['pattern'].value_counts().sort_index()
        print(f"  {label}: {dict(counts)}")
    print()

    # Group 1 list with key fields
    print("Group 1 entries (r_ss = NaN, Core empty):")
    cols_g1 = ['n', 'pattern', 'seed', 'r', 'k', 'core_epsilon', 'n_feasible']
    print(g1[cols_g1].to_string(index=False))
    print()

    # Group 2 list
    print("Group 2 entries (r <= r_ss):")
    cols_g2 = ['n', 'pattern', 'seed', 'r', 'r_ss', 'k', 'core_epsilon', 'n_feasible']
    print(g2[cols_g2].to_string(index=False))
    print()

    # Binding analysis for Group 1
    print("=" * 75)
    print("GROUP 1 BINDING SIZE ANALYSIS")
    print("=" * 75)
    print(f"{'n':>3} {'pattern':<10} {'seed':>4} {'|F|':>5} {'eps*':>8} "
          f"{'binding sizes (count)':<40} {'interpretation'}")
    print("-" * 110)

    g1_interp_counts = {}
    for _, row in g1.iterrows():
        n = int(row['n'])
        pattern = row['pattern']
        seed = int(row['seed'])

        L = L_N2(n)
        rho = PATTERN_RHO[pattern]
        positions = generate_customers(n, seed, L=L)
        arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)

        pol = make_policies()['nearest_neighbor']
        sim = run_with_policy(positions, arrivals, pol)
        F = set(sim['coalition_costs'].keys())
        C_N = sim['C_N']
        players = sim['players']

        eps_star, tight = first_stage_tight_sizes(sim['coalition_costs'], C_N, players)
        interp = classify_binding(n, tight)
        g1_interp_counts[interp] = g1_interp_counts.get(interp, 0) + 1

        sizes_str = ', '.join(f"{sz}={cnt}" for sz, cnt in sorted(tight.items()))
        print(f"{n:>3} {pattern:<10} {seed:>4} {len(F):>5} "
              f"{eps_star:>8.4f} {sizes_str:<40} {interp}")

    print()
    print("Group 1 interpretation tally:", g1_interp_counts)

    # Group 2 binding analysis (for completeness)
    print()
    print("=" * 75)
    print("GROUP 2 BINDING SIZE ANALYSIS (complement feasible but not firing)")
    print("=" * 75)
    print(f"{'n':>3} {'pattern':<10} {'seed':>4} {'|F|':>5} {'eps*':>8} "
          f"{'binding sizes (count)':<40} {'interpretation'}")
    print("-" * 110)

    g2_interp_counts = {}
    for _, row in g2.iterrows():
        n = int(row['n'])
        pattern = row['pattern']
        seed = int(row['seed'])

        L = L_N2(n)
        rho = PATTERN_RHO[pattern]
        positions = generate_customers(n, seed, L=L)
        arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)

        pol = make_policies()['nearest_neighbor']
        sim = run_with_policy(positions, arrivals, pol)
        C_N = sim['C_N']
        players = sim['players']
        F = set(sim['coalition_costs'].keys())

        eps_star, tight = first_stage_tight_sizes(sim['coalition_costs'], C_N, players)
        interp = classify_binding(n, tight)
        g2_interp_counts[interp] = g2_interp_counts.get(interp, 0) + 1

        sizes_str = ', '.join(f"{sz}={cnt}" for sz, cnt in sorted(tight.items()))
        print(f"{n:>3} {pattern:<10} {seed:>4} {len(F):>5} "
              f"{eps_star:>8.4f} {sizes_str:<40} {interp}")

    print()
    print("Group 2 interpretation tally:", g2_interp_counts)

    # Write markdown report
    total_interp = {**g1_interp_counts}
    for k, v in g2_interp_counts.items():
        total_interp[k] = total_interp.get(k, 0) + v

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, 'w') as f:
        f.write("# Phase 2 Residual Binding Analysis\n\n")
        f.write(f"- Data: {SUMMARY_CSV}\n")
        f.write(f"- NN policy, {len(nn)} instances, {len(residual)} residual "
                "(Core empty & Thm 11 vacuous)\n\n")
        f.write("## Group counts\n\n")
        f.write(f"- Group 1 (r\\*\\* undefined): {len(g1)}\n")
        f.write(f"- Group 2 (r \\<= r\\*\\*): {len(g2)}\n")
        f.write(f"- Group 3 (sanity; should be 0): {len(g3)}\n\n")
        f.write("## Group 1 interpretation tally\n\n")
        for k, v in sorted(g1_interp_counts.items()):
            f.write(f"- `{k}`: {v}\n")
        f.write("\n## Group 2 interpretation tally\n\n")
        for k, v in sorted(g2_interp_counts.items()):
            f.write(f"- `{k}`: {v}\n")
        f.write("\n## Combined tally across residual (Group 1 + 2)\n\n")
        for k, v in sorted(total_interp.items()):
            f.write(f"- `{k}`: {v}\n")

        # Decision-relevant summary
        f.write("\n## Decision rubric\n\n")
        total = len(residual)
        near_count = total_interp.get('near-complement', 0) + total_interp.get('complement-only', 0)
        inter_count = total_interp.get('intermediate', 0) + total_interp.get('mixed', 0)
        f.write(f"- near-complement / complement-only: **{near_count}** of {total}\n")
        f.write(f"- intermediate / mixed:              **{inter_count}** of {total}\n")
        if inter_count >= 10:
            f.write("\n**Judgement (B):** intermediate mechanism is prominent; "
                    "narrative needs significant rewriting in §5.3, §6.5, Table 6.\n")
        elif near_count >= 0.85 * total:
            f.write("\n**Judgement (A):** near-complement mechanism dominates; "
                    "Remark 13 / Appendix C can absorb the finding with minor numeric updates.\n")
        else:
            f.write("\n**Judgement (mixed):** a meaningful subset of residual cases "
                    "is intermediate; consider elevating this beyond Remark.\n")

    print(f"\nReport written to {OUT_MD}")
    print(f"\nCombined tally: {total_interp}")


if __name__ == '__main__':
    main()

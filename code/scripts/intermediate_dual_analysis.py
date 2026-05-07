"""
D-heavy pilot (R1 revision Phase D): Dual-extracted analysis of the 9
intermediate-coalition empty-Core cases (Observation 15) under nearest-neighbor
dispatch. For each case we re-solve the first-stage Core LP, extract the
primal-binding (tight) constraints and the dual prices lambda_S, and report
both the binding-mass-by-size distribution and dual-mass-by-size distribution.

The aim is to determine whether a compact common balanced family of coalition
sizes certifies all 9 cases (Case A: justifies a new mixed-balanced threshold
proposition), whether the cases cluster into a small number of distinct active-
size signatures (Case B: an Observation 17 with cluster table), or whether
each case has its own active-size signature (Case C: negative result, supp
appendix).

Output: code/results/intermediate_dual_analysis.json
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

import pulp

from config import PATTERN_RHO, L_N2
from generators import generate_customers, generate_arrivals
from src.policies import make_policies
from src.policy_simulator import run_with_policy


# 9 intermediate cases (main manuscript Table 6 / Observation 15)
INSTANCES = [
    (7,  'B_medium', 256, 5,  1.436),
    (10, 'B_medium', 123, 8,  1.423),
    (10, 'B_medium', 256, 8,  1.358),
    (10, 'E',        42,  8,  1.495),
    (12, 'B_medium', 99,  10, 1.395),
    (12, 'B_medium', 123, 10, 1.487),
    (12, 'B_medium', 256, 10, 1.423),
    (12, 'E',        42,  9,  1.610),
    (15, 'B_medium', 256, 12, 1.326),
]


def first_stage_lp(coalition_costs, C_N, players, tol=1e-6):
    """Solve first-stage Core LP. Return:

    - eps_star : optimal epsilon
    - x_star   : optimal allocation (dict)
    - tight_by_size : {size : count} for primal-binding constraints
    - dual_mass_by_size : {size : sum(|lambda_S|)} normalized to total mass = 1

    The first-stage LP:
        min  eps
        s.t. sum_i x_i = C_N                         (mu, free)
             sum_{i in S} x_i - c(S) <= eps  for S    (lambda_S >= 0)
             eps free, x_i free.
    """
    n = len(players)
    F_proper = [S for S in coalition_costs if 0 < len(S) < n]
    if not F_proper:
        return None, None, {}, {}

    prob = pulp.LpProblem("first_stage_core", pulp.LpMinimize)
    y = {p: pulp.LpVariable(f"y_{p}", cat='Continuous') for p in players}
    eps = pulp.LpVariable("eps", cat='Continuous')
    prob += eps  # objective
    prob += pulp.lpSum(y[p] for p in players) == C_N, "efficiency"
    for S in F_proper:
        cname = "S_" + "_".join(str(p) for p in sorted(S))
        prob += pulp.lpSum(y[p] for p in S) - coalition_costs[S] <= eps, cname

    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=120))
    if status != pulp.constants.LpStatusOptimal:
        return None, None, {}, {}

    eps_val = pulp.value(eps)
    y_val = {p: pulp.value(y[p]) for p in players}

    tight_by_size = {}
    dual_by_size = {}
    total_dual = 0.0

    for S in F_proper:
        cname = "S_" + "_".join(str(p) for p in sorted(S))
        c = prob.constraints[cname]
        lhs = sum(y_val[p] for p in S)
        excess = lhs - coalition_costs[S]
        # primal-binding test
        if abs(excess - eps_val) < tol:
            sz = len(S)
            tight_by_size[sz] = tight_by_size.get(sz, 0) + 1
        # dual extraction
        lam = c.pi if c.pi is not None else 0.0
        if abs(lam) > tol:
            sz = len(S)
            dual_by_size[sz] = dual_by_size.get(sz, 0.0) + abs(lam)
            total_dual += abs(lam)

    if total_dual > 0:
        dual_by_size = {sz: m / total_dual for sz, m in dual_by_size.items()}

    return eps_val, y_val, tight_by_size, dual_by_size


def analyze_one(n, pattern, seed):
    """Re-create a single instance and solve its first-stage LP under NN."""
    L = L_N2(n)
    rho = PATTERN_RHO[pattern]
    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)
    pol = make_policies()['nearest_neighbor']
    sim = run_with_policy(positions, arrivals, pol)
    coalition_costs = sim['coalition_costs']
    eps_star, y_star, tight, dual = first_stage_lp(
        coalition_costs, sim['C_N'], sim['players']
    )
    return {
        'k_observed': sim['k'],
        'F_size': len(coalition_costs),
        'eps_star': eps_star,
        'tight_by_size': tight,
        'dual_mass_by_size': dual,
    }


def main():
    out_path = os.path.join(ROOT, 'results', 'intermediate_dual_analysis.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print("=" * 100)
    print("D-HEAVY PILOT: dual-extracted analysis of 9 intermediate cases")
    print("=" * 100)
    print(f"{'#':>2} {'n':>3} {'pattern':<10} {'seed':>4} {'k':>3} {'r_obs':>6} "
          f"{'eps*':>7}  binding sizes (count)              dual mass by size")
    print("-" * 130)

    results = []
    for idx, (n, pattern, seed, k_table, r_obs) in enumerate(INSTANCES, start=1):
        rec = {'idx': idx, 'n': n, 'pattern': pattern, 'seed': seed,
               'k_table': k_table, 'r_observed': r_obs}
        try:
            ana = analyze_one(n, pattern, seed)
            rec.update(ana)
            tight_str = ', '.join(f"{sz}={cnt}"
                                  for sz, cnt in sorted(rec['tight_by_size'].items()))
            dual_str = ', '.join(f"{sz}:{m:.2f}"
                                 for sz, m in sorted(rec['dual_mass_by_size'].items()))
            print(f"{idx:>2} {n:>3} {pattern:<10} {seed:>4} {rec['k_observed']:>3} "
                  f"{r_obs:>6.3f} {rec['eps_star']:>7.4f}  "
                  f"{tight_str:<35} {dual_str}")
        except Exception as e:
            rec['error'] = str(e)
            print(f"{idx:>2} {n:>3} {pattern:<10} {seed:>4} ERROR: {e}")
        results.append(rec)

    print()
    print("=" * 100)
    print("AGGREGATE: which sizes are 'active' (>= 5% dual mass) across the 9 cases")
    print("=" * 100)

    size_freq_dual = {}
    size_freq_tight = {}
    for r in results:
        if 'error' in r:
            continue
        for sz, m in r.get('dual_mass_by_size', {}).items():
            if m >= 0.05:
                size_freq_dual[sz] = size_freq_dual.get(sz, 0) + 1
        for sz in r.get('tight_by_size', {}):
            size_freq_tight[sz] = size_freq_tight.get(sz, 0) + 1

    n_ok = sum(1 for r in results if 'error' not in r)
    print(f"\nDual-mass active sizes (>=5% dual mass), frequency across {n_ok} cases:")
    for sz in sorted(size_freq_dual):
        print(f"  size {sz:>2}: {size_freq_dual[sz]} / {n_ok} cases")

    print(f"\nPrimal-tight sizes, frequency across {n_ok} cases:")
    for sz in sorted(size_freq_tight):
        print(f"  size {sz:>2}: {size_freq_tight[sz]} / {n_ok} cases")

    # Per-instance "active size signature" using normalized dual mass (>= 5%)
    print("\nPer-instance active-size signatures (dual mass >= 5%):")
    sig_counts = {}
    for r in results:
        if 'error' in r:
            continue
        sig = tuple(sorted(sz for sz, m in r['dual_mass_by_size'].items() if m >= 0.05))
        sig_counts[sig] = sig_counts.get(sig, 0) + 1
        print(f"  #{r['idx']} (n={r['n']:>2}, {r['pattern']:<10}, seed {r['seed']}): {sig}")
    print()
    print("Signature frequency:")
    for sig, cnt in sorted(sig_counts.items(), key=lambda x: -x[1]):
        print(f"  {sig}: {cnt}")

    # Decision rubric
    print("\n" + "=" * 100)
    print("DECISION RUBRIC")
    print("=" * 100)
    common_sizes_7of9 = sorted(sz for sz, f in size_freq_dual.items() if f >= 7)
    common_sizes_5of9 = sorted(sz for sz, f in size_freq_dual.items() if f >= 5)
    print(f"Sizes with dual mass >= 5% in >=7/9 cases: {common_sizes_7of9}")
    print(f"Sizes with dual mass >= 5% in >=5/9 cases: {common_sizes_5of9}")
    if common_sizes_7of9:
        print("\n=> Case A candidate: a near-common active-size family exists. "
              "Justifies a new mixed-balanced threshold proposition (now Proposition 14, general partition-pair certificate).")
    elif common_sizes_5of9:
        print("\n=> Case B candidate: a partial common pattern exists. "
              "Report as Observation 17 with cluster table.")
    else:
        print("\n=> Case C: no compact common pattern; report as supp-only "
              "negative result + main acknowledgment in Limitation (iv).")

    with open(out_path, 'w') as f:
        json.dump({
            'instances': results,
            'aggregate': {
                'n_ok': n_ok,
                'dual_active_size_freq': size_freq_dual,
                'tight_size_freq': size_freq_tight,
                'signature_counts': {str(k): v for k, v in sig_counts.items()},
                'common_sizes_7of9': common_sizes_7of9,
                'common_sizes_5of9': common_sizes_5of9,
            },
        }, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == '__main__':
    main()

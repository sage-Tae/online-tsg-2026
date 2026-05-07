"""
Phase 2 post-run: augment summary CSV with two new columns.

Task 1: r_sss = (1/(n-1)) * sum_i c(N\\{i}) / c*(N)
        Defined only when all n complements N\\{i} are feasible; NaN else.
        Bondareva-Shapley applied to the balanced collection of complements:
        r > r_sss  =>  Core empty.

Task 2: empty_mechanism in {single_complement, balanced_complement,
        near_complement, intermediate, core_nonempty}, determined from
        first-stage nucleolus LP binding sizes for the residual cases
        (Thm 11 vacuous & Core empty).

Usage:
    python3 scripts/augment_summary.py
Reads  experiments/logs/policy_comparison_v2_full.csv
Writes experiments/logs/policy_comparison_v2_full.csv (same path, overwrites)
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'experiments'))

import pandas as pd
import pulp

from config import PATTERN_RHO, L_N2
from generators import generate_customers, generate_arrivals
from src.policies import make_policies
from src.policy_simulator import run_with_policy
from src.tsp import tsp_cost

SUMMARY_CSV = os.path.join(ROOT, 'experiments/logs/policy_comparison_v2_full.csv')


def compute_r_sss(coalition_costs, players, c_star_N):
    """Balanced-complement threshold.

    r_sss = (1/(n-1)) * sum_i c(N\\{i}) / c*(N),
    defined iff all N\\{i} are feasible.
    """
    n = len(players)
    comps = []
    for i in players:
        comp = frozenset(p for p in players if p != i)
        if comp not in coalition_costs:
            return None
        comps.append(coalition_costs[comp])
    if len(comps) != n or n <= 1:
        return None
    return (sum(comps) / (n - 1)) / c_star_N


def first_stage_tight_sizes(coalition_costs, C_N, players, tol=1e-6):
    """Solve first-stage nucleolus LP; return (eps*, tight-size dict)."""
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
        excess = sum(y_val[p] for p in S) - coalition_costs[S]
        if abs(excess - eps_star) < tol:
            sz = len(S)
            tight_sizes[sz] = tight_sizes.get(sz, 0) + 1
    return eps_star, tight_sizes


def classify_residual(n, tight_sizes):
    """Classify residual cases (Thm 11 vacuous, Core empty) by binding sizes.

    Returns one of:
      'balanced_complement' : tight sizes = {n-1} only
      'near_complement'     : tight sizes contain both n-1 and n-2
      'intermediate'        : no tight size is n-1 (bulk at 2..n-3)
      'unclassified'        : edge cases not covered above
    """
    if not tight_sizes:
        return 'unclassified'
    sizes = set(tight_sizes.keys())
    has_n1 = (n - 1) in sizes
    has_n2 = (n - 2) in sizes
    if has_n1 and has_n2:
        return 'near_complement'
    if has_n1 and not has_n2:
        # tight sizes contain n-1 but not n-2.  If only n-1 appears, it's
        # a balanced-complement pattern.  If n-1 plus some intermediate
        # (without n-2) still dominates, still call it balanced_complement
        # if n-1 is the unique tight size.
        if sizes == {n - 1}:
            return 'balanced_complement'
        # n-1 plus another non-(n-2) size: unusual; treat as near_complement
        return 'near_complement'
    # n-1 not tight: pure intermediate
    return 'intermediate'


def classify_row(row, coalition_cache):
    """Classify a single CSV row and compute r_sss.

    Reruns the simulator (idempotent with shared cache) to get the current
    coalition_costs, C_N_online, players.  Returns (r_sss, mechanism).
    """
    n = int(row['n'])
    pattern = row['pattern']
    seed = int(row['seed'])
    policy_name = row['policy']

    L = L_N2(n)
    rho = PATTERN_RHO[pattern]
    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)

    policies = make_policies()
    policy_fn = policies[policy_name]
    sim = run_with_policy(positions, arrivals, policy_fn,
                          coalition_cache=coalition_cache)
    C_N = sim['C_N']
    players = sim['players']
    coalition_costs = sim['coalition_costs']
    c_star_N = coalition_costs[frozenset(players)]

    r_sss = compute_r_sss(coalition_costs, players, c_star_N)

    # Mechanism classification
    if row['core_nonempty']:
        mechanism = 'core_nonempty'
    elif row['theorem11_fires']:
        mechanism = 'single_complement'
    else:
        eps_star, tight = first_stage_tight_sizes(coalition_costs, C_N, players)
        mechanism = classify_residual(n, tight)

    return r_sss, mechanism


def main():
    df = pd.read_csv(SUMMARY_CSV)
    print(f"Loaded {len(df)} rows from {SUMMARY_CSV}")

    r_sss_col = []
    mech_col = []
    # Per-instance cache so the three policies for the same (n,pattern,seed)
    # share TSP-cost computations.
    instance_cache = {}
    last_key = None
    for idx, row in df.iterrows():
        key = (row['n'], row['pattern'], row['seed'])
        if key != last_key:
            cache = {}
            instance_cache[key] = cache
            last_key = key
        cache = instance_cache[key]
        r_sss, mech = classify_row(row, cache)
        r_sss_col.append(r_sss if r_sss is not None else float('nan'))
        mech_col.append(mech)
        if (idx + 1) % 50 == 0:
            print(f"  {idx+1}/{len(df)} rows processed")

    df['r_sss'] = r_sss_col
    df['empty_mechanism'] = mech_col

    df.to_csv(SUMMARY_CSV, index=False)
    print(f"Wrote augmented CSV with {len(df)} rows.")

    # Summary: mechanism distribution per policy
    print("\n=== Mechanism distribution by policy ===")
    print(df.groupby(['policy', 'empty_mechanism']).size().unstack(fill_value=0))

    # Summary: r_sss statistics (applicable instances only)
    applicable = df[df['r_sss'].notna()]
    print(f"\n=== r_sss statistics (defined when all complements feasible) ===")
    print(f"  applicable instances: {len(applicable)}/{len(df)}")
    if len(applicable) > 0:
        print(f"  r_sss mean: {applicable['r_sss'].mean():.4f}")
        print(f"  r_sss vs r: r > r_sss in {(applicable['r'] > applicable['r_sss']).sum()} rows")
        # For those where r > r_sss, is Core empty?
        fires_sss = applicable[applicable['r'] > applicable['r_sss'] + 1e-9]
        core_empty = (~fires_sss['core_nonempty']).sum()
        print(f"  r > r_sss cases: {len(fires_sss)}, Core empty: {core_empty}, "
              f"Core nonempty (false-pos check): {len(fires_sss)-core_empty}")


if __name__ == '__main__':
    main()

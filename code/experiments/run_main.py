"""
Main experiment runner (Phase 2.2, replaces run_policy_comparison.py).

Uses new N2 normalization (L = sqrt(n)) and rho-based patterns per
phase1_design.md. Outputs CSV with expanded schema including (L, rho, tau).

Usage:
    python3 run_main.py                   # full 175-instance grid × 3 policies
    python3 run_main.py --smoke           # small subset (10 instances) for testing
    python3 run_main.py --single 5 A 7    # single instance (n pattern seed)

Output:
    logs/policy_comparison_v2.csv

Schema: n, pattern, seed, policy, L, rho, tau,
        C_N_online, c_star_N, r, r_star, r_ss,
        n_feasible, k, core_nonempty, core_epsilon,
        theorem11_applicable, theorem11_fires
"""

import os
import sys
import argparse
import time
import traceback
from itertools import product

import pandas as pd

# Add project root to path
EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(EXPERIMENT_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, 'src'))

# New modules (Phase 2.1)
from config import (
    DEFAULT_N_VALUES, DEFAULT_SEEDS, DEFAULT_POLICIES,
    PATTERN_ORDER, PATTERN_RHO,
    L_N2, tau_from_rho, describe_pattern,
)
from generators import generate_customers, generate_arrivals

# Existing core modules
from src.policies import make_policies
from src.policy_simulator import run_with_policy
from src.tsp import tsp_cost
from src.nucleolus import temporal_nucleolus


# ============================================================
# Auxiliary metrics (adapted from run_policy_comparison.compute_rss_and_flags)
# ============================================================

def compute_rss_and_flags(positions, arrival_times, players, C_N_online, F,
                          depot=(0, 0), coalition_cache=None):
    """Compute c*(N), r, r*, r**, Theorem 11 applicability and firing."""
    if coalition_cache is None:
        coalition_cache = {}

    def _cost(subset):
        fs = frozenset(subset)
        if fs in coalition_cache:
            return coalition_cache[fs]
        c, _ = tsp_cost(depot, list(subset), positions, arrival_times)
        coalition_cache[fs] = c
        return c

    c_star_N = _cost(players)
    sum_individual = sum(_cost([p]) for p in players)

    r = C_N_online / c_star_N if c_star_N > 1e-9 else None
    r_star = sum_individual / c_star_N if c_star_N > 1e-9 else None

    applicable_is = []
    deltas_feasible = []
    for i in players:
        comp = frozenset(p for p in players if p != i)
        if comp in F:
            applicable_is.append(i)
            c_comp = _cost(list(comp))
            c_i = _cost([i])
            deltas_feasible.append(c_i + c_comp - c_star_N)

    theorem11_applicable = len(applicable_is) > 0
    if theorem11_applicable:
        r_ss = 1.0 + min(deltas_feasible) / c_star_N
        theorem11_fires = r > r_ss + 1e-9
    else:
        r_ss = None
        theorem11_fires = False

    return {
        'c_star_N': round(c_star_N, 4),
        'r': round(r, 4) if r is not None else None,
        'r_star': round(r_star, 4) if r_star is not None else None,
        'r_ss': round(r_ss, 4) if r_ss is not None else None,
        'theorem11_applicable': theorem11_applicable,
        'theorem11_fires': theorem11_fires,
    }


# ============================================================
# Single-instance runner
# ============================================================

def run_one(n, pattern, seed, policy_name, policy_fn, coalition_cache=None):
    """Run one (n, pattern, seed, policy) instance and return metrics dict."""
    L = L_N2(n)
    rho = PATTERN_RHO[pattern]
    tau = tau_from_rho(rho)

    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)

    sim = run_with_policy(positions, arrivals, policy_fn,
                          coalition_cache=coalition_cache)

    C_N_online = sim['C_N']
    F = set(sim['coalition_costs'].keys())

    alloc, core_eps = temporal_nucleolus(
        sim['coalition_costs'], C_N_online, sim['players']
    )
    core_nonempty = core_eps is not None and core_eps <= 1e-6

    aux = compute_rss_and_flags(
        positions, arrivals, sim['players'], C_N_online, F,
        coalition_cache=coalition_cache,
    )

    return {
        'n': n, 'pattern': pattern, 'seed': seed, 'policy': policy_name,
        'L': round(L, 4), 'rho': rho, 'tau': round(tau, 4),
        'C_N_online': round(C_N_online, 4),
        'c_star_N': aux['c_star_N'],
        'r': aux['r'], 'r_star': aux['r_star'], 'r_ss': aux['r_ss'],
        'n_feasible': len(F),
        'k': sim['k'],
        'core_nonempty': core_nonempty,
        'core_epsilon': round(core_eps, 6) if core_eps is not None else None,
        'theorem11_applicable': aux['theorem11_applicable'],
        'theorem11_fires': aux['theorem11_fires'],
    }


# ============================================================
# Grid runner
# ============================================================

def run_grid(n_values, patterns, seeds, policies_filter, output_csv,
             smoke=False, verbose=True):
    """Run full (n × pattern × seed × policy) grid."""
    all_combos = list(product(n_values, patterns, seeds))
    total = len(all_combos) * len(policies_filter)
    if smoke:
        total = min(total, 10)

    if verbose:
        print(f"Running {total} instances -> {output_csv}")
        print(f"  n: {n_values}")
        print(f"  patterns: {patterns}")
        print(f"  seeds: {seeds}")
        print(f"  policies: {policies_filter}")
        print()

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    results = []
    errors = []
    count = 0
    t0 = time.time()
    last_pct = -1

    for n, pattern, seed in all_combos:
        if smoke and count >= 10:
            break
        policies = make_policies()
        coalition_cache = {}  # shared across 3 policies for same instance
        for policy_name, policy_fn in policies.items():
            if policy_name not in policies_filter:
                continue
            if smoke and count >= 10:
                break
            count += 1
            try:
                m = run_one(n, pattern, seed, policy_name, policy_fn,
                            coalition_cache=coalition_cache)
                results.append(m)
            except Exception as e:
                err = (f"[{n}_{pattern}_{seed}_{policy_name}] "
                       f"{e}\n{traceback.format_exc()}")
                errors.append(err)
                print(err, file=sys.stderr)

            if verbose:
                pct = int(100 * count / total)
                if pct // 10 > last_pct // 10:
                    elapsed = time.time() - t0
                    rate = count / elapsed if elapsed > 0 else 0
                    eta = (total - count) / rate if rate > 0 else 0
                    print(f"  [{count}/{total}] {pct}%  "
                          f"elapsed={elapsed:6.1f}s  eta={eta:6.1f}s",
                          flush=True)
                    last_pct = pct

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    elapsed = time.time() - t0
    print(f"\nWrote {len(df)} rows to {output_csv} in {elapsed:.1f}s")
    print(f"Errors: {len(errors)}")

    if len(df) > 0 and verbose:
        print("\n=== Summary by policy ===")
        g = df.groupby('policy').agg(
            r_mean=('r', 'mean'),
            core_rate=('core_nonempty', 'mean'),
            empty_count=('core_nonempty', lambda s: (~s).sum()),
            thm11_app=('theorem11_applicable', 'sum'),
            thm11_fires=('theorem11_fires', 'sum'),
        ).round(4)
        print(g)

    return df


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Main experiment runner (Phase 2.2)')
    parser.add_argument('--smoke', action='store_true',
                        help='Smoke test: only 10 instances')
    parser.add_argument('--single', nargs=3, metavar=('N', 'PATTERN', 'SEED'),
                        help='Run single instance and print metrics')
    parser.add_argument('--output', default=None,
                        help='Output CSV path (default: logs/policy_comparison_v2.csv)')
    parser.add_argument('--policies-only', nargs='+', default=None,
                        help='Restrict to specific policies')
    args = parser.parse_args()

    if args.output is None:
        output = os.path.join(EXPERIMENT_DIR, 'logs', 'policy_comparison_v2.csv')
    else:
        output = args.output

    if args.single:
        n, pattern, seed = args.single
        n = int(n)
        seed = int(seed)
        print(f"Single instance: n={n}, pattern={pattern}, seed={seed}")
        print(f"  {describe_pattern(pattern)}")
        for policy_name, policy_fn in make_policies().items():
            print(f"\n  Policy: {policy_name}")
            m = run_one(n, pattern, seed, policy_name, policy_fn)
            for k, v in sorted(m.items()):
                print(f"    {k}: {v}")
        return

    policies = args.policies_only if args.policies_only else DEFAULT_POLICIES

    run_grid(
        n_values=DEFAULT_N_VALUES,
        patterns=PATTERN_ORDER,
        seeds=DEFAULT_SEEDS,
        policies_filter=policies,
        output_csv=output,
        smoke=args.smoke,
    )


if __name__ == '__main__':
    main()

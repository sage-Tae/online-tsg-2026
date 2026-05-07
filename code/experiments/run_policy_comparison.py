"""rev-policy: run the 175-instance grid under 3 dispatch policies.

For each (n, pattern, seed, policy) tuple, record r, |F|, k, Core
existence, r**, Theorem 11 applicability and firing. Persist to
experiments/logs/policy_comparison.csv.
"""

import os
import sys
import time
import traceback
from itertools import permutations

import pandas as pd
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.policies import make_policies
from src.policy_simulator import run_with_policy
from src.tsp import tsp_cost
from src.nucleolus import temporal_nucleolus
from experiments.run_all import generate_customers, generate_arrival_times

SIZES = [5, 7, 10, 12, 15]
SEEDS = [42, 123, 7, 99, 256]
PATTERNS = ['A', 'B1', 'B2', 'B5', 'C', 'D', 'E']

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT, 'experiments', 'logs')


def compute_rss_and_flags(positions, arrival_times, players, serve_times,
                           C_N_online, F, depot=(0, 0), coalition_cache=None):
    """Compute c*(N), r, r*, r**, Theorem 11 applicability and firing.

    When coalition_cache (frozenset -> cost) is supplied, singleton and
    N\\{i} costs are looked up there first.
    """
    n = len(players)
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


def run_one(n, pattern, seed, policy_name, policy_fn, coalition_cache=None,
            tsp_cache=None):
    positions = generate_customers(n, seed)
    arrivals = generate_arrival_times(n, pattern, positions, seed)
    sim = run_with_policy(positions, arrivals, policy_fn,
                          coalition_cache=coalition_cache)

    C_N_online = sim['C_N']
    F = set(sim['coalition_costs'].keys())

    # Temporal Core: core_epsilon from nucleolus LP
    alloc, core_eps = temporal_nucleolus(sim['coalition_costs'], C_N_online,
                                          sim['players'])
    core_nonempty = core_eps is not None and core_eps <= 1e-6

    aux = compute_rss_and_flags(positions, arrivals, sim['players'],
                                 sim['serve_times'], C_N_online, F,
                                 coalition_cache=coalition_cache)

    return {
        'n': n, 'pattern': pattern, 'seed': seed, 'policy': policy_name,
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


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    out_path = os.path.join(LOG_DIR, 'policy_comparison.csv')

    results = []
    errors = []
    total = len(SIZES) * len(PATTERNS) * len(SEEDS) * 3  # three policies
    count = 0
    t0 = time.time()
    last_pct = -1

    for n in SIZES:
        for pattern in PATTERNS:
            for seed in SEEDS:
                policies = make_policies()  # fresh state per instance
                coalition_cache = {}  # shared across the 3 policies
                for policy_name, policy_fn in policies.items():
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
    df.to_csv(out_path, index=False)
    print(f"\nWrote {len(df)} rows to {out_path}")
    print(f"Errors: {len(errors)}")

    if len(df) > 0:
        print("\n=== Summary by policy ===")
        g = df.groupby('policy').agg(
            r_mean=('r', 'mean'),
            core_rate=('core_nonempty', 'mean'),
            empty_count=('core_nonempty', lambda s: (~s).sum()),
            thm11_app=('theorem11_applicable', 'sum'),
            thm11_fires=('theorem11_fires', 'sum'),
        ).round(4)
        print(g)


if __name__ == '__main__':
    main()

"""
Targeted experiment: verify intermediate-coalition mechanism at
Pattern A, n in {20, 30, 50}, seed 123 (previous paper's problem case).

For each (n, seed) where Thm11 does not fire, run restricted Core LP
(10000 sampled coalitions + singletons + complements) to determine
core_nonempty and identify violating coalition size distribution.
"""

import os
import sys
import csv
import time

EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(EXPERIMENT_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, 'src'))

from config import L_N2, tau_from_rho, PATTERN_RHO
from generators import generate_customers, generate_arrivals
from src.policies import select_next_nn
from src.policy_simulator import run_with_policy
from src.tsp_scaleup import scaled_tsp
from src.core_lp_restricted import check_core_restricted

DEPOT = (0.0, 0.0)

TARGETS = [
    # Seed 123: Phase 2.5 showed Thm11 fires=False at n=20,30 (potential intermediate)
    ('A', 20, 123),
    ('A', 30, 123),
    ('A', 50, 123),
    # Control: Thm11 fires cases -> should be Core empty (LP correctness sanity check)
    ('A', 20, 7),
    ('A', 30, 42),
]

NUM_SAMPLES = 10000


def main():
    out_csv = os.path.join(EXPERIMENT_DIR, 'logs', 'seed123_core_check.csv')
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    fieldnames = ['n', 'pattern', 'seed', 'L', 'rho', 'tau',
                  'C_N_online', 'c_star_N', 'r',
                  'num_sampled', 'num_in_lp',
                  'core_nonempty_restricted', 'eps_star',
                  'violating_sizes', 'elapsed_sec', 'note']

    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for pattern, n, seed in TARGETS:
            print(f"\n=== {pattern}, n={n}, seed={seed} ===")
            t0 = time.time()

            L = L_N2(n)
            rho = PATTERN_RHO[pattern]
            tau = tau_from_rho(rho)

            positions = generate_customers(n, seed, L=L)
            arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)

            sim = run_with_policy(positions, arrivals, select_next_nn)
            C_N_online = sim['C_N']
            service_times = sim['serve_times']

            c_star_N, _ = scaled_tsp(DEPOT, sorted(positions.keys()),
                                     positions, arrivals)
            r = C_N_online / c_star_N

            print(f"  L={L:.4f}, rho={rho}, tau={tau:.4f}")
            print(f"  C_online={C_N_online:.4f}, c*(N)={c_star_N:.4f}, r={r:.4f}")

            try:
                lp = check_core_restricted(
                    n, positions, arrivals, service_times,
                    C_N_online, num_samples=NUM_SAMPLES, seed=seed
                )
                print(f"  LP: {lp['num_feasible_in_lp']} constraints")
                print(f"  core_nonempty_restricted: {lp['core_nonempty']}")
                print(f"  eps*: {lp['eps_star']}")
                print(f"  violating sizes: {lp['violating_sizes']}")

                row = {
                    'n': n, 'pattern': pattern, 'seed': seed,
                    'L': round(L, 4), 'rho': rho, 'tau': round(tau, 4),
                    'C_N_online': round(C_N_online, 4),
                    'c_star_N': round(c_star_N, 4),
                    'r': round(r, 4),
                    'num_sampled': lp['num_coalitions_sampled'],
                    'num_in_lp': lp['num_feasible_in_lp'],
                    'core_nonempty_restricted': lp['core_nonempty'],
                    'eps_star': round(lp['eps_star'], 6)
                                if lp['eps_star'] is not None else None,
                    'violating_sizes': str(lp['violating_sizes']),
                    'elapsed_sec': round(time.time() - t0, 1),
                    'note': lp['note'],
                }
            except Exception as e:
                import traceback
                traceback.print_exc()
                row = {
                    'n': n, 'pattern': pattern, 'seed': seed,
                    'L': round(L, 4), 'rho': rho, 'tau': round(tau, 4),
                    'note': f'ERROR: {type(e).__name__}: {e}',
                    'elapsed_sec': round(time.time() - t0, 1),
                }

            writer.writerow(row)
            f.flush()
            print(f"  elapsed: {row['elapsed_sec']}s")

    print(f"\nDone. Output: {out_csv}")


if __name__ == '__main__':
    main()

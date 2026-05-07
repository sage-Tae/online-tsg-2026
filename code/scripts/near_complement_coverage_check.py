"""
Read-only analysis script for the v2.1.12 → v2.2.0/v2.1.13 phase-2 session.

For each of the 10 observed near-complement NN main-grid cases, rebuild the
instance deterministically from the main experiment generators, run the NN
simulator to obtain arrivals/serve-times/realized cost, enumerate the
collection B_{n-1} ∪ B_{n-2} restricted to F (feasibility checked directly
from the paper Def. 2 inequality max a_i < min s_i), solve the Bondareva–
Shapley balancing LP

    find  λ_S ≥ 0  for  S ∈ (B_{n-1} ∪ B_{n-2}) ∩ F
    s.t.  Σ_{S ∋ i} λ_S = 1  for every i ∈ N
    obj   minimize  Σ_S λ_S · c(S)

and report whether the resulting threshold  r^(♦) = (Σ_S λ_S c(S)) / c*(N)
is strictly less than the realized online ratio r.

This version avoids the full 2^n subset enumeration inside
`run_with_policy`/`reconstruct_F`: we invoke the low-level online event loop
to obtain (arrivals, serve_times, C_N_online) only, then compute c(S) only
for S ∈ (B_{n-1} ∪ B_{n-2}) ∩ F and for c*(N) itself (|B_{n-1}| + |B_{n-2}|
+ 1 + n TSP calls per instance).

Inputs (read-only):
  code/experiments/logs/policy_comparison_v2_full.csv
  code/src/generators.py, config.py, policies.py, tsp.py (distances + HK).

Outputs:
  stdout summary + code/results/near_complement_coverage_check.csv.
"""

import os
import sys
import csv
import time
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(CODE_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, 'src'))

from generators import generate_customers, generate_arrivals  # noqa: E402
from src.policies import make_policies  # noqa: E402
from src.tsp import tsp_cost, dist  # noqa: E402


NEAR_COMPLEMENT_CASES = [
    (10, 'A',        123),
    (10, 'B_heavy',  256),
    (10, 'C',        123),
    (15, 'A',         42),
    (15, 'A',         99),
    (15, 'A',        123),
    (15, 'B_heavy',    7),
    (15, 'C',         42),
    (15, 'C',         99),
    (15, 'C',        123),
]


def run_nn_lightweight(positions, arrival_times, depot=(0.0, 0.0),
                       speed=1.0, policy_fn=None):
    """Run the online TSG with NN dispatch and return (serve_times, C_N, k).

    Re-implements the core event loop of src.policy_simulator.run_with_policy
    WITHOUT the post-hoc reconstruct_F + compute_coalition_costs step, so
    we avoid 2^n enumeration for n=15 k=n instances.
    """
    all_ids = sorted(positions.keys())
    n = len(all_ids)
    arrivals = sorted(all_ids, key=lambda i: arrival_times[i])

    U_t = set()
    V_t = set()
    serve_times = {}
    k_max = 0
    vehicle_pos = depot
    current_time = 0.0
    total_travel = 0.0
    arrival_idx = 0

    if policy_fn is None:
        policy_fn = make_policies()['nearest_neighbor']

    while len(V_t) < n:
        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= current_time + 1e-9:
                U_t.add(cid)
                arrival_idx += 1
            else:
                break

        if not U_t:
            if arrival_idx < len(arrivals):
                current_time = arrival_times[arrivals[arrival_idx]]
                continue
            else:
                break

        best_id = policy_fn(vehicle_pos, U_t, positions, depot,
                            arrival_times, current_time, speed)
        best_d = dist(vehicle_pos, positions[best_id])
        travel_time = best_d / speed
        arrival_at_cust = current_time + travel_time
        serve_time = max(arrival_at_cust, arrival_times[best_id])

        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= serve_time + 1e-9:
                if cid not in V_t:
                    U_t.add(cid)
                arrival_idx += 1
            else:
                break
        if len(U_t) > k_max:
            k_max = len(U_t)

        total_travel += best_d
        current_time = serve_time
        vehicle_pos = positions[best_id]
        U_t.remove(best_id)
        V_t.add(best_id)
        serve_times[best_id] = serve_time

    total_travel += dist(vehicle_pos, depot)
    return {
        'serve_times': serve_times,
        'C_N': total_travel,
        'k': k_max,
        'players': all_ids,
    }


def feasible(S, arrivals, serve_times, tol=1e-9):
    """S ∈ F  iff  max_{i∈S} a_i < min_{i∈S} s_i  (paper Def. 2)."""
    if not S:
        return False
    max_a = max(arrivals[i] for i in S)
    min_s = min(serve_times[i] for i in S)
    return max_a < min_s - tol


def enumerate_collection_restricted_to_F(players, arrivals, serve_times):
    """Return the list of S in B_{n-1} ∪ B_{n-2} that are in F."""
    collection = []
    for i in players:
        S = frozenset(p for p in players if p != i)
        if feasible(S, arrivals, serve_times):
            collection.append(S)
    for i, j in combinations(players, 2):
        S = frozenset(p for p in players if p != i and p != j)
        if feasible(S, arrivals, serve_times):
            collection.append(S)
    return collection


def compute_costs_on_collection(collection, positions, arrivals, depot=(0, 0)):
    """For each S in collection, compute c(S) via Held–Karp (tsp_cost)."""
    costs = {}
    for S in collection:
        c, _ = tsp_cost(depot, list(S), positions, arrivals)
        costs[S] = c
    return costs


def solve_balancing_lp(collection, players, coalition_costs):
    from scipy.optimize import linprog
    import numpy as np

    if not collection:
        return {'feasible': False, 'opt_value': None, 'weights': None,
                'reason': 'collection is empty'}

    m = len(collection)
    n_players = len(players)
    player_idx = {p: k for k, p in enumerate(players)}

    c = np.array([coalition_costs[S] for S in collection], dtype=float)
    A_eq = np.zeros((n_players, m), dtype=float)
    for k, S in enumerate(collection):
        for p in S:
            A_eq[player_idx[p], k] = 1.0
    b_eq = np.ones(n_players, dtype=float)
    bounds = [(0.0, None)] * m

    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    if not res.success:
        return {'feasible': False, 'opt_value': None, 'weights': None,
                'reason': res.message}
    weights = {S: float(w) for S, w in zip(collection, res.x)}
    return {'feasible': True, 'opt_value': float(res.fun), 'weights': weights,
            'reason': None}


def check_one_case(n, pattern, seed):
    t0 = time.time()
    positions = generate_customers(n, seed)
    arrivals = generate_arrivals(n, pattern, positions, seed)

    sim = run_nn_lightweight(positions, arrivals)
    players = sim['players']
    serve_times = sim['serve_times']
    C_N_online = sim['C_N']

    c_star_N, _ = tsp_cost((0, 0), players, positions, arrivals)
    r = C_N_online / c_star_N if c_star_N > 0 else float('nan')

    collection = enumerate_collection_restricted_to_F(
        players, arrivals, serve_times)
    n_Bn1 = sum(1 for S in collection if len(S) == n - 1)
    n_Bn2 = sum(1 for S in collection if len(S) == n - 2)

    coalition_costs = compute_costs_on_collection(collection, positions, arrivals)

    lp = solve_balancing_lp(collection, players, coalition_costs)

    elapsed = time.time() - t0
    return {
        'n': n,
        'pattern': pattern,
        'seed': seed,
        'r': round(r, 6),
        'c_star_N': round(c_star_N, 6),
        'C_N_online': round(C_N_online, 6),
        'B_n1_in_F': n_Bn1,
        'B_n2_in_F': n_Bn2,
        'lp_feasible': lp['feasible'],
        'sum_lambda_c': round(lp['opt_value'], 6) if lp['opt_value'] is not None else None,
        'r_diamond': round(lp['opt_value'] / c_star_N, 6) if lp['opt_value'] is not None else None,
        'fires': (lp['opt_value'] is not None
                  and r > lp['opt_value'] / c_star_N + 1e-9),
        'lp_reason': lp.get('reason'),
        'elapsed_s': round(elapsed, 2),
    }


def main():
    print(f"{'n':>3}  {'pattern':<9}  {'seed':>4}  "
          f"{'r':>8}  {'r_diamond':>10}  {'fires':>5}  "
          f"{'|Bn1∩F|':>7}  {'|Bn2∩F|':>7}  {'t(s)':>5}")
    print("-" * 82)

    reports = []
    fires_count = 0
    for (n, pattern, seed) in NEAR_COMPLEMENT_CASES:
        sys.stdout.flush()
        try:
            rep = check_one_case(n, pattern, seed)
        except Exception as e:
            rep = {
                'n': n, 'pattern': pattern, 'seed': seed,
                'r': None, 'c_star_N': None, 'C_N_online': None,
                'B_n1_in_F': None, 'B_n2_in_F': None,
                'lp_feasible': False, 'sum_lambda_c': None,
                'r_diamond': None, 'fires': False,
                'lp_reason': f'exception: {e}', 'elapsed_s': None,
            }
        reports.append(rep)
        rd = rep['r_diamond']
        rd_str = f"{rd:10.6f}" if rd is not None else "    —     "
        tstr = f"{rep['elapsed_s']:5.1f}" if rep['elapsed_s'] is not None else "  —  "
        print(f"{rep['n']:>3}  {rep['pattern']:<9}  {rep['seed']:>4}  "
              f"{rep['r']:>8.4f}  {rd_str}  "
              f"{'YES' if rep['fires'] else 'no ':>5}  "
              f"{rep['B_n1_in_F']:>7}  {rep['B_n2_in_F']:>7}  "
              f"{tstr}")
        sys.stdout.flush()
        if rep['fires']:
            fires_count += 1

    print("-" * 82)
    print(f"Coverage: {fires_count} / {len(NEAR_COMPLEMENT_CASES)} cases fire "
          f"(r > r^♦).")

    results_dir = os.path.join(CODE_DIR, 'results')
    os.makedirs(results_dir, exist_ok=True)
    out_path = os.path.join(results_dir, 'near_complement_coverage_check.csv')
    fields = ['n', 'pattern', 'seed', 'r', 'c_star_N', 'C_N_online',
              'B_n1_in_F', 'B_n2_in_F', 'lp_feasible',
              'sum_lambda_c', 'r_diamond', 'fires', 'lp_reason', 'elapsed_s']
    with open(out_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rep in reports:
            w.writerow({k: rep.get(k) for k in fields})
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()

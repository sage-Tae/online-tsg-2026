"""
Phase 2 task 1 (B_{n-3} closure attempt).

Generalizes near_complement_coverage_check.py from the
B_{n-1} ∪ B_{n-2} support to B_{n-1} ∪ B_{n-2} ∪ B_{n-3}, then re-solves
the Bondareva-Shapley balancing LP

    find  λ_S ≥ 0  for  S ∈ (B_{n-1} ∪ B_{n-2} ∪ B_{n-3}) ∩ F
    s.t.  Σ_{S ∋ i} λ_S = 1  for every i ∈ N
    obj   minimize  Σ_S λ_S · c(S),

reporting r^(♦,3) = opt / c*(N) for each of the 10 NN main-grid
near-complement cases. The seed-42 (n=15, A) instance is the one
that fails the strict inequality at k=2 by ≈2×10⁻³; this script
records whether the k=3 enlargement closes that residual.

Read-only against the v2.4.10 archive, except for the new output CSV
at code/results/near_complement_coverage_check_k3.csv.

Output columns (per Phase 2 spec):
    n, pattern, seed, r, r_diamond_k2, r_diamond_k3,
    margin_k2, margin_k3, fires_k3,
    plus diagnostics (B_{n-3} count, LP status, runtime).
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
    """Reproduces the event loop of the existing k=2 script verbatim."""
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
    if not S:
        return False
    max_a = max(arrivals[i] for i in S)
    min_s = min(serve_times[i] for i in S)
    return max_a < min_s - tol


def enumerate_collection_k(players, arrivals, serve_times, max_drop):
    """B_{n-1} ∪ ... ∪ B_{n-max_drop} restricted to F.

    max_drop=2 reproduces the existing k=2 script; max_drop=3 adds B_{n-3}.
    """
    collection = []
    n = len(players)
    for d in range(1, max_drop + 1):
        for drop in combinations(players, d):
            drop_set = set(drop)
            S = frozenset(p for p in players if p not in drop_set)
            if feasible(S, arrivals, serve_times):
                collection.append(S)
    return collection


def compute_costs_on_collection(collection, positions, arrivals, depot=(0, 0)):
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


def lp_threshold(collection, players, costs, c_star_N):
    if not collection:
        return None, 'collection empty'
    lp = solve_balancing_lp(collection, players, costs)
    if not lp['feasible']:
        return None, lp['reason']
    return lp['opt_value'] / c_star_N, None


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

    coll_k2 = enumerate_collection_k(players, arrivals, serve_times, max_drop=2)
    coll_k3 = enumerate_collection_k(players, arrivals, serve_times, max_drop=3)
    n_Bn1 = sum(1 for S in coll_k2 if len(S) == n - 1)
    n_Bn2 = sum(1 for S in coll_k2 if len(S) == n - 2)
    n_Bn3 = sum(1 for S in coll_k3 if len(S) == n - 3)

    costs_k3 = compute_costs_on_collection(coll_k3, positions, arrivals)
    costs_k2 = {S: costs_k3[S] for S in coll_k2}

    rd_k2, reason_k2 = lp_threshold(coll_k2, players, costs_k2, c_star_N)
    rd_k3, reason_k3 = lp_threshold(coll_k3, players, costs_k3, c_star_N)

    margin_k2 = (r - rd_k2) if (rd_k2 is not None) else None
    margin_k3 = (r - rd_k3) if (rd_k3 is not None) else None
    fires_k2 = (rd_k2 is not None and r > rd_k2 + 1e-9)
    fires_k3 = (rd_k3 is not None and r > rd_k3 + 1e-9)

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
        'B_n3_in_F': n_Bn3,
        'r_diamond_k2': round(rd_k2, 6) if rd_k2 is not None else None,
        'r_diamond_k3': round(rd_k3, 6) if rd_k3 is not None else None,
        'margin_k2': round(margin_k2, 6) if margin_k2 is not None else None,
        'margin_k3': round(margin_k3, 6) if margin_k3 is not None else None,
        'fires_k2': fires_k2,
        'fires_k3': fires_k3,
        'lp_reason_k2': reason_k2,
        'lp_reason_k3': reason_k3,
        'elapsed_s': round(elapsed, 2),
    }


def main():
    print(f"{'n':>3}  {'pattern':<9}  {'seed':>4}  "
          f"{'r':>8}  {'rd_k2':>9}  {'rd_k3':>9}  "
          f"{'mar_k2':>9}  {'mar_k3':>9}  {'fires_k3':>8}  "
          f"{'|Bn3∩F|':>7}  {'t(s)':>6}")
    print("-" * 110)

    reports = []
    fires_k2 = 0
    fires_k3 = 0
    for (n, pattern, seed) in NEAR_COMPLEMENT_CASES:
        sys.stdout.flush()
        try:
            rep = check_one_case(n, pattern, seed)
        except Exception as e:
            rep = {
                'n': n, 'pattern': pattern, 'seed': seed,
                'r': None, 'c_star_N': None, 'C_N_online': None,
                'B_n1_in_F': None, 'B_n2_in_F': None, 'B_n3_in_F': None,
                'r_diamond_k2': None, 'r_diamond_k3': None,
                'margin_k2': None, 'margin_k3': None,
                'fires_k2': False, 'fires_k3': False,
                'lp_reason_k2': f'exception: {e}',
                'lp_reason_k3': f'exception: {e}',
                'elapsed_s': None,
            }
        reports.append(rep)

        def fmt(v, w=9, d=6):
            return f"{v:>{w}.{d}f}" if v is not None else " " * w

        tstr = f"{rep['elapsed_s']:6.1f}" if rep['elapsed_s'] is not None else "  -   "
        bn3 = rep['B_n3_in_F'] if rep['B_n3_in_F'] is not None else 0
        print(f"{rep['n']:>3}  {rep['pattern']:<9}  {rep['seed']:>4}  "
              f"{rep['r']:>8.4f}  {fmt(rep['r_diamond_k2'])}  "
              f"{fmt(rep['r_diamond_k3'])}  "
              f"{fmt(rep['margin_k2'])}  {fmt(rep['margin_k3'])}  "
              f"{('YES' if rep['fires_k3'] else 'no '):>8}  "
              f"{bn3:>7}  {tstr}")
        sys.stdout.flush()
        if rep['fires_k2']:
            fires_k2 += 1
        if rep['fires_k3']:
            fires_k3 += 1

    print("-" * 110)
    total = len(NEAR_COMPLEMENT_CASES)
    print(f"Coverage k=2: {fires_k2} / {total} cases fire (existing).")
    print(f"Coverage k=3: {fires_k3} / {total} cases fire (with B_{{n-3}}).")
    if fires_k3 > fires_k2:
        gained = fires_k3 - fires_k2
        print(f">>> {gained} additional case(s) closed by B_{{n-3}} enlargement.")

    # Spotlight seed 42
    s42 = next((r for r in reports if r['n'] == 15 and r['pattern'] == 'A'
                and r['seed'] == 42), None)
    if s42:
        print()
        print("seed-42 (n=15, A) spotlight:")
        print(f"  r           = {s42['r']}")
        print(f"  rd_k2       = {s42['r_diamond_k2']}  (margin {s42['margin_k2']})")
        print(f"  rd_k3       = {s42['r_diamond_k3']}  (margin {s42['margin_k3']})")
        print(f"  fires_k2    = {s42['fires_k2']}")
        print(f"  fires_k3    = {s42['fires_k3']}")

    results_dir = os.path.join(CODE_DIR, 'results')
    os.makedirs(results_dir, exist_ok=True)
    out_path = os.path.join(results_dir, 'near_complement_coverage_check_k3.csv')
    fields = ['n', 'pattern', 'seed', 'r', 'c_star_N', 'C_N_online',
              'B_n1_in_F', 'B_n2_in_F', 'B_n3_in_F',
              'r_diamond_k2', 'r_diamond_k3',
              'margin_k2', 'margin_k3',
              'fires_k2', 'fires_k3',
              'lp_reason_k2', 'lp_reason_k3', 'elapsed_s']
    with open(out_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rep in reports:
            w.writerow({k: rep.get(k) for k in fields})
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()

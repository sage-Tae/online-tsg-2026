"""Smoke tests for src.feasibility.reconstruct_F and the corrected
simulator pipeline (Phase 4 post-review fix).
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

from src.feasibility import reconstruct_F
from src.policies import select_next_nn
from src.policy_simulator import run_with_policy

from config import L_N2, tau_from_rho, PATTERN_RHO
from generators import generate_customers, generate_arrivals


def _build(n, pattern, seed):
    L = L_N2(n)
    rho = PATTERN_RHO[pattern]
    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)
    return positions, arrivals


def test_pattern_A_full_F():
    """Pattern A (simultaneous arrivals) has a_i = 0 for all i, and NN
    serves in strictly positive order, so every subset is feasible
    (max_a = 0 < min_s for any subset of size >= 1).  |F| = 2^n - 1.
    """
    n, pattern, seed = 10, 'A', 42
    positions, arrivals = _build(n, pattern, seed)
    sim = run_with_policy(positions, arrivals, select_next_nn)
    F_reco = reconstruct_F(n, arrivals, sim['serve_times'])
    assert len(F_reco) == 2**n - 1, \
        f"Pattern A n=10 seed=42: |F|={len(F_reco)} != {2**n-1}"
    # Every complement N\{i} must be feasible
    players = sorted(positions.keys())
    complements = [frozenset(p for p in players if p != i) for i in players]
    assert all(c in F_reco for c in complements), \
        "Pattern A: every complement should be feasible"
    print(f"test_pattern_A_full_F PASS  |F|={len(F_reco)}")


def test_pattern_B_heavy_complements():
    """Pattern B_heavy (rho=4) has tight sequential arrivals. Under NN
    the queue fills quickly, so nearly every complement coalition ought
    to be feasible at n=10 seed=42 (the heavy-regime signature).
    Stricter claim: count feasible complements at this cell.
    """
    n, pattern, seed = 10, 'B_heavy', 42
    positions, arrivals = _build(n, pattern, seed)
    sim = run_with_policy(positions, arrivals, select_next_nn)
    F_reco = reconstruct_F(n, arrivals, sim['serve_times'])

    players = sorted(positions.keys())
    complements_feasible = [
        i for i in players
        if frozenset(p for p in players if p != i) in F_reco
    ]
    # Heavy regime: expect many complements feasible
    assert len(complements_feasible) >= 5, \
        f"B_heavy n=10 seed=42: only {len(complements_feasible)}/10 " \
        f"complements feasible, expected >= 5"
    # Full 2^n - 1 should NOT hold in general for B_heavy (sparse gap)
    # but for seed=42 the pattern is dense enough that F is substantial
    assert len(F_reco) > 2**n / 4, \
        f"B_heavy n=10 seed=42: |F|={len(F_reco)} surprisingly small"
    print(f"test_pattern_B_heavy_complements PASS  "
          f"|F|={len(F_reco)}, feasible complements={len(complements_feasible)}/10")


def test_C_N_is_travel_distance():
    """C_N returned by run_with_policy must be the total travel distance,
    not elapsed time. Sanity: for Pattern B_heavy n=5 seed=7 in N2,
    travel distance should be lower-bounded by the depot's farthest
    customer's round-trip (2 * max d(0, x_i)).
    """
    import math

    n, pattern, seed = 5, 'B_heavy', 7
    positions, arrivals = _build(n, pattern, seed)
    sim = run_with_policy(positions, arrivals, select_next_nn)
    C_N = sim['C_N']
    depot = (0.0, 0.0)
    max_ind = max(math.hypot(positions[i][0] - depot[0],
                             positions[i][1] - depot[1])
                  for i in positions)
    # Return visit of the farthest customer alone is 2 * max_ind
    assert C_N >= 2 * max_ind - 1e-9, \
        f"C_N={C_N} is below the trivial 2*max_ind={2*max_ind}; " \
        f"likely elapsed-time bug"
    # And elapsed time would generally be >> travel distance for B_heavy
    # at this scale, so if C_N <= elapsed_bound we're likely OK.
    # Weak upper bound: diameter of queue times n.
    print(f"test_C_N_is_travel_distance PASS  "
          f"C_N={C_N:.4f}, 2*max_ind={2*max_ind:.4f}")


if __name__ == '__main__':
    test_pattern_A_full_F()
    test_pattern_B_heavy_complements()
    test_C_N_is_travel_distance()
    print("\nAll feasibility tests passed.")

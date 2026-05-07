"""
Feasibility family F reconstruction, aligned with paper Definition 2:

    S in F  iff  max_{i in S} a_i < min_{i in S} s_i

i.e. coalition S is feasible iff its members share a nonempty common
waiting window CW(S) = intersection of [a_i, s_i).

The previous simulator implementations enumerated subsets of U_t at
dispatch-iteration entry only, which systematically missed coalitions
that materialize due to arrivals during vehicle travel.  This module
performs a post-hoc enumeration from the final (arrivals, serve_times)
pair, giving the definition-compliant F.
"""

import sys
from itertools import combinations

from src.tsp import tsp_cost


def reconstruct_F(n, arrivals, serve_times, tol=1e-9):
    """Return the set of feasible coalitions per paper Definition 2.

    Parameters
    ----------
    n : int
        Number of customers.
    arrivals : dict[int, float]
        a_i for each customer.
    serve_times : dict[int, float]
        s_i for each customer.
    tol : float
        Strict-inequality tolerance (max_a must be strictly less than
        min_s by at least ``tol``).

    Returns
    -------
    set[frozenset]
        Every feasible coalition including singletons and (when
        applicable) the grand coalition.  For ``n > 15`` the full
        enumeration is skipped (2^n > ~33k) and an empty set is
        returned with a warning; callers should fall back to the
        on-the-fly ``coalition_costs`` produced by the simulator.
    """
    if n > 15:
        print(f"  WARNING: reconstruct_F skipped for n={n} > 15 "
              f"(would enumerate 2^n subsets)", file=sys.stderr)
        return set()

    players = sorted(arrivals.keys())
    if len(players) != n:
        raise ValueError(f"arrivals has {len(players)} entries, expected n={n}")

    F = set()
    # Include singletons unconditionally
    for i in players:
        F.add(frozenset([i]))

    # Intermediate sizes
    for size in range(2, n + 1):
        for subset in combinations(players, size):
            max_a = max(arrivals[i] for i in subset)
            min_s = min(serve_times[i] for i in subset)
            if max_a < min_s - tol:
                F.add(frozenset(subset))

    return F


def compute_coalition_costs(F, positions, arrivals, depot=(0.0, 0.0),
                            speed=1.0, cache=None):
    """Compute c(S) for every S in F, using tsp_cost.

    Parameters
    ----------
    F : iterable[frozenset]
    positions : dict[int, tuple]
    arrivals : dict[int, float]
    depot : tuple
    speed : float
    cache : dict[frozenset, float], optional
        Shared cross-instance cache for TSP results.  Mutated in place.

    Returns
    -------
    dict[frozenset, float]
        Mapping S -> c(S).  The cache is updated with any new entries.
    """
    if cache is None:
        cache = {}
    costs = {}
    for S in F:
        if S in cache:
            costs[S] = cache[S]
            continue
        if len(S) == 0:
            costs[S] = 0.0
            cache[S] = 0.0
            continue
        cost, _ = tsp_cost(depot, list(S), positions, arrivals, speed)
        costs[S] = cost
        cache[S] = cost
    return costs

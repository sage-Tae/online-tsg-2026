"""LKH-based TSP for scale-up (n > 15). Returns shortest Hamiltonian
cycle length (pure distance) to match the paper's c(S) definition.
"""

import elkai
from src.tsp import dist, exact_tsp


def _integer_dm(depot, customers, positions, scale=10000):
    pts = [depot] + [positions[c] for c in customers]
    m = len(pts)
    dm = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            d = int(round(dist(pts[i], pts[j]) * scale))
            dm[i][j] = d
            dm[j][i] = d
    return pts, dm


def lkh_tsp(depot, customers, positions, early_times=None, speed=1.0,
             scale=10000):
    """Shortest-distance TSP via LKH (elkai). Pure distance; earlyTime
    and speed are accepted for API symmetry but ignored."""
    if not customers:
        return 0.0, []
    if len(customers) == 1:
        cid = customers[0]
        return 2 * dist(depot, positions[cid]), [cid]

    pts, dm = _integer_dm(depot, customers, positions, scale)
    tour = elkai.DistanceMatrix(dm).solve_tsp()
    if tour[0] != 0:
        i0 = tour.index(0)
        tour = tour[i0:] + tour[1:i0 + 1]
    order_ids = [customers[k - 1] for k in tour[1:-1]]
    # compute actual float distance of the returned closed tour
    total = 0.0
    cur = depot
    for cid in order_ids:
        total += dist(cur, positions[cid])
        cur = positions[cid]
    total += dist(cur, depot)
    return total, order_ids


def scaled_tsp(depot, customers, positions, early_times=None, speed=1.0,
               exact_threshold=20):
    """Exact Held-Karp for n <= exact_threshold, LKH fallback otherwise."""
    if len(customers) <= exact_threshold:
        return exact_tsp(depot, customers, positions, early_times, speed)
    return lkh_tsp(depot, customers, positions, early_times, speed)

"""
TSP solver module for Online TSG experiment.

Two flavors:
- `exact_tsp`, `nn_tsp`, `tsp_cost`: pure-distance Hamiltonian cycle
  cost on the depot + customers set. This matches the paper's c(S)
  definition (Section 3.2, Table 1), which is time-independent.
- `exact_tsp_time_aware`, `nn_tsp_time_aware`: legacy total-completion-
  time variants that include earlyTime waits. Retained for the online
  simulator only (C(N)_online accumulation) and for reproducibility of
  the older time-aware experiments.
"""

import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# ─────────────────────────────────────────────────────────────
# Pure-distance (paper-consistent) Held-Karp and nearest-neighbor.
# ─────────────────────────────────────────────────────────────

def exact_tsp(start, customers, positions, early_times=None, speed=1.0):
    """Shortest Hamiltonian cycle (depot->...->depot) length.

    Pure distance; earlyTime / speed are accepted for API symmetry but
    have no effect. Time-aware variant lives in `exact_tsp_time_aware`.
    """
    if not customers:
        return 0.0, []

    n = len(customers)
    if n == 1:
        cid = customers[0]
        return 2 * dist(start, positions[cid]), [cid]

    idx_to_id = {i: customers[i] for i in range(n)}

    # 0=depot, 1..n=customers
    dm = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        dm[0][i + 1] = dist(start, positions[idx_to_id[i]])
        dm[i + 1][0] = dm[0][i + 1]
        for j in range(i + 1, n):
            dd = dist(positions[idx_to_id[i]], positions[idx_to_id[j]])
            dm[i + 1][j + 1] = dd
            dm[j + 1][i + 1] = dd

    INF = float('inf')
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    for i in range(n):
        dp[1 << i][i] = dm[0][i + 1]

    for mask in range(1, size):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            v = dp[mask][last]
            if v == INF:
                continue
            rem = (~mask) & (size - 1)
            while rem:
                nxt = (rem & -rem).bit_length() - 1
                rem &= rem - 1
                new_mask = mask | (1 << nxt)
                cand = v + dm[last + 1][nxt + 1]
                if cand < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cand
                    parent[new_mask][nxt] = last

    full = size - 1
    best_cost = INF
    best_last = -1
    for i in range(n):
        c = dp[full][i] + dm[i + 1][0]
        if c < best_cost:
            best_cost = c
            best_last = i

    order = []
    mask = full
    last = best_last
    while last != -1:
        order.append(idx_to_id[last])
        prev = parent[mask][last]
        mask ^= (1 << last)
        last = prev
    order.reverse()
    return best_cost, order


def nn_tsp(start, customers, positions, early_times=None, speed=1.0):
    """Nearest-neighbor tour length (pure distance)."""
    if not customers:
        return 0.0, []
    remaining = list(customers)
    order = []
    cur = start
    total = 0.0
    while remaining:
        best = min(remaining, key=lambda c: dist(cur, positions[c]))
        total += dist(cur, positions[best])
        cur = positions[best]
        order.append(best)
        remaining.remove(best)
    total += dist(cur, start)
    return total, order


def tsp_cost(start, customers, positions, early_times=None, speed=1.0):
    """Pure-distance TSP. Exact Held--Karp for n<=20, LKH fallback otherwise.
    For n in (15, 20] we still run Held--Karp — ~1s per call at n=20 is
    acceptable for the infrequent grand/complement lookups in scale-up."""
    n = len(customers)
    if n <= 20:
        return exact_tsp(start, customers, positions, early_times, speed)
    from src.tsp_scaleup import lkh_tsp
    return lkh_tsp(start, customers, positions, early_times, speed)


# ─────────────────────────────────────────────────────────────
# Legacy time-aware variants (for online dispatch / backward compat).
# ─────────────────────────────────────────────────────────────

def _tour_time(start, order, positions, early_times, speed=1.0):
    current_pos = start
    current_time = 0.0
    for cid in order:
        d = dist(current_pos, positions[cid])
        travel_time = d / speed
        arrival_at_cust = current_time + travel_time
        serve_time = max(arrival_at_cust, early_times.get(cid, 0.0))
        current_time = serve_time
        current_pos = positions[cid]
    current_time += dist(current_pos, start) / speed
    return current_time


def exact_tsp_time_aware(start, customers, positions, early_times=None, speed=1.0):
    """Minimum-completion-time Held-Karp with earlyTime waits."""
    if early_times is None:
        early_times = {}
    if not customers:
        return 0.0, []

    n = len(customers)
    if n == 1:
        cid = customers[0]
        d = dist(start, positions[cid])
        arrival = d / speed
        serve = max(arrival, early_times.get(cid, 0.0))
        return_time = serve + d / speed
        return return_time, [cid]

    idx_to_id = {i: customers[i] for i in range(n)}

    dm = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        dm[0][i + 1] = dist(start, positions[idx_to_id[i]])
        dm[i + 1][0] = dm[0][i + 1]
        for j in range(i + 1, n):
            dd = dist(positions[idx_to_id[i]], positions[idx_to_id[j]])
            dm[i + 1][j + 1] = dd
            dm[j + 1][i + 1] = dd

    et = [early_times.get(idx_to_id[i], 0.0) for i in range(n)]
    full_mask = (1 << n) - 1
    INF = float('inf')

    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    for i in range(n):
        travel = dm[0][i + 1] / speed
        dp[1 << i][i] = max(travel, et[i])

    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                travel = dm[last + 1][nxt + 1] / speed
                arrival = dp[mask][last] + travel
                serve_time = max(arrival, et[nxt])
                if serve_time < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = serve_time
                    parent[new_mask][nxt] = last

    best_time = INF
    best_last = -1
    for i in range(n):
        return_time = dp[full_mask][i] + dm[i + 1][0] / speed
        if return_time < best_time:
            best_time = return_time
            best_last = i

    order = []
    mask = full_mask
    last = best_last
    while last != -1:
        order.append(idx_to_id[last])
        prev = parent[mask][last]
        mask ^= (1 << last)
        last = prev
    order.reverse()
    return best_time, order


def nn_tsp_time_aware(start, customers, positions, early_times=None, speed=1.0):
    if early_times is None:
        early_times = {}
    if not customers:
        return 0.0, []
    remaining = list(customers)
    order = []
    current_pos = start
    current_time = 0.0
    while remaining:
        best_id = min(remaining, key=lambda c: dist(current_pos, positions[c]))
        d = dist(current_pos, positions[best_id])
        travel_time = d / speed
        arrival = current_time + travel_time
        serve_time = max(arrival, early_times.get(best_id, 0.0))
        current_time = serve_time
        current_pos = positions[best_id]
        order.append(best_id)
        remaining.remove(best_id)
    current_time += dist(current_pos, start) / speed
    return current_time, order

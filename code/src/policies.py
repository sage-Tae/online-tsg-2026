"""Dispatch policies for Online TSG.

Each `select_next_*` picks which customer from U_t (waiting queue) the
vehicle should visit next, given its current position. All policies
share the same signature so they are drop-in for the simulator.
"""

from src.tsp import dist


def select_next_nn(vehicle_pos, U_t, positions, depot, early_times, current_time, speed):
    """Nearest-neighbor: closest customer from current position."""
    return min(U_t, key=lambda c: dist(vehicle_pos, positions[c]))


def select_next_cheapest_insertion(vehicle_pos, U_t, positions, depot,
                                    early_times, current_time, speed):
    """Cheapest-insertion online heuristic.

    Build a tour from vehicle_pos through all of U_t back to depot by
    inserting customers one at a time at the cheapest position; return
    the first customer in that tour. Re-planned at every dispatch event.
    """
    U_list = list(U_t)
    if len(U_list) == 1:
        return U_list[0]

    # tour is list of (id, pos); None id for vehicle anchor and depot
    tour = [(None, vehicle_pos), (None, depot)]
    remaining = list(U_list)
    while remaining:
        best_c, best_i, best_delta = None, -1, float('inf')
        for c in remaining:
            cpos = positions[c]
            for i in range(len(tour) - 1):
                a = tour[i][1]
                b = tour[i + 1][1]
                delta = dist(a, cpos) + dist(cpos, b) - dist(a, b)
                if delta < best_delta:
                    best_delta = delta
                    best_c = c
                    best_i = i + 1
        tour.insert(best_i, (best_c, positions[best_c]))
        remaining.remove(best_c)

    for i in range(1, len(tour)):
        if tour[i][0] is not None:
            return tour[i][0]
    raise RuntimeError("cheapest_insertion produced empty tour")


def _held_karp_path(vehicle_pos, U_list, positions, depot, early_times,
                     current_time, speed):
    """Shortest Hamiltonian path from vehicle_pos through U_list to depot,
    with earlyTime waiting. Returns ordered list of customer ids.
    """
    n = len(U_list)
    INF = float('inf')
    idx_to_id = {i: U_list[i] for i in range(n)}

    pts = [vehicle_pos] + [positions[cid] for cid in U_list] + [depot]
    dm = [[dist(pts[i], pts[j]) / speed for j in range(n + 2)]
          for i in range(n + 2)]
    et = [0.0] + [early_times.get(cid, 0.0) for cid in U_list] + [0.0]

    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    for i in range(n):
        travel = dm[0][i + 1]
        arr = current_time + travel
        dp[1 << i][i] = max(arr, et[i + 1])

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
                arr = v + dm[last + 1][nxt + 1]
                serve = max(arr, et[nxt + 1])
                if serve < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = serve
                    parent[new_mask][nxt] = last

    full = size - 1
    best_time = INF
    best_last = -1
    for last in range(n):
        v = dp[full][last]
        if v == INF:
            continue
        ret = v + dm[last + 1][n + 1]
        if ret < best_time:
            best_time = ret
            best_last = last

    order = []
    mask = full
    last = best_last
    while last != -1:
        order.append(last)
        prev = parent[mask][last]
        mask ^= (1 << last)
        last = prev
    order.reverse()
    return [idx_to_id[i] for i in order]


class BatchReoptimizePolicy:
    """Stateful policy: caches optimal tour, re-plans only when U_t
    changes by more than one served removal (i.e. a new arrival)."""

    def __init__(self):
        self.plan = []          # remaining customers in planned order
        self.prev_U_t = None    # frozenset of last-seen U_t

    def __call__(self, vehicle_pos, U_t, positions, depot, early_times,
                 current_time, speed):
        U_frozen = frozenset(U_t)
        need_replan = True
        if self.prev_U_t is not None and self.plan:
            # If current U_t equals prev_U_t minus exactly the first plan
            # element (== last served), keep the existing plan.
            expected = self.prev_U_t - {self.plan[0]}
            if U_frozen == expected:
                self.plan = self.plan[1:]
                need_replan = False
        if need_replan:
            if len(U_frozen) == 1:
                self.plan = [next(iter(U_frozen))]
            else:
                self.plan = _held_karp_path(vehicle_pos, list(U_frozen),
                                             positions, depot, early_times,
                                             current_time, speed)
        self.prev_U_t = U_frozen
        return self.plan[0]


def make_policies():
    """Factory returning a fresh dict of policies (stateful ones get fresh state)."""
    return {
        'nearest_neighbor': select_next_nn,
        'cheapest_insertion': select_next_cheapest_insertion,
        'batch_reoptimize': BatchReoptimizePolicy(),
    }


# Backward-compat module-level dict (re-created per import; callers should
# prefer make_policies() when running many instances).
POLICIES = make_policies()

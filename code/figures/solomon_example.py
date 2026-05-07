"""Compute numerical Example values for Solomon C101 first 5 customers."""
import numpy as np
from itertools import permutations

# Solomon C101 first 5 customers + depot
depot = (35.0, 35.0)
customers = {
    1: (45.0, 68.0),
    2: (45.0, 70.0),
    3: (42.0, 66.0),
    4: (42.0, 68.0),
    5: (40.0, 69.0),
}
ready = {1: 912, 2: 825, 3: 65, 4: 727, 5: 15}

def dist(a, b):
    return np.hypot(a[0]-b[0], a[1]-b[1])

# Build distance matrix
nodes = {0: depot, **customers}
def d(i, j):
    return dist(nodes[i], nodes[j])

def tsp(S):
    """Optimal TSP on S + depot, cycle starting/ending at 0."""
    S = list(S)
    if len(S) == 0:
        return 0.0
    if len(S) == 1:
        return 2 * d(0, S[0])
    best = float('inf')
    for perm in permutations(S):
        cost = d(0, perm[0])
        for a, b in zip(perm, perm[1:]):
            cost += d(a, b)
        cost += d(perm[-1], 0)
        if cost < best:
            best = cost
    return best

# All non-empty coalitions
from itertools import chain, combinations
def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

N = [1,2,3,4,5]
print("=== TSP costs c(S) ===")
tsp_cost = {}
for S in powerset(N):
    c = tsp(S)
    tsp_cost[tuple(sorted(S))] = c

# Singletons
for i in N:
    print(f"  c({{{i}}}) = {tsp_cost[(i,)]:.3f}")

c_N = tsp_cost[tuple(N)]
print(f"\n  c*(N) = c({{1,...,5}}) = {c_N:.3f}")

# N\{i}
print("\n=== c(N\\{i}) ===")
for i in N:
    S = tuple(sorted(set(N) - {i}))
    print(f"  c(N\\{{{i}}}) = {tsp_cost[S]:.3f}")

# delta_i
print("\n=== delta_i = c({i}) + c(N\\{i}) - c*(N) ===")
deltas = {}
for i in N:
    S = tuple(sorted(set(N) - {i}))
    delta = tsp_cost[(i,)] + tsp_cost[S] - c_N
    deltas[i] = delta
    print(f"  delta_{i} = {delta:.3f}")

print(f"\n  min_i delta_i = {min(deltas.values()):.3f}  (at i={min(deltas, key=deltas.get)})")
print(f"  r** = 1 + min_i delta_i / c*(N) = {1 + min(deltas.values())/c_N:.4f}")

# Online NN policy: leave depot at t=0, for each event pick nearest available
# Serve customers as they become reachable; wait if not yet ready
# NN priority: at each decision, go to nearest unserved whose ready time allows

def simulate_online_nn():
    """NN policy: always go to nearest customer who has already arrived; if none, wait."""
    current = 0
    t = 0.0
    total_cost = 0.0
    remaining = set(N)
    service = {}
    while remaining:
        # Available: those with ready <= t OR will be next
        # At this moment, pick the customer that is reachable earliest and closest
        # Simple NN: pick the next customer that minimizes (max(t + travel, ready))
        best = None
        best_arr = float('inf')
        for j in remaining:
            travel = d(current, j)
            arr = max(t + travel, ready[j])
            # tie-break by distance
            if arr < best_arr or (arr == best_arr and travel < d(current, best if best else list(remaining)[0])):
                best = j
                best_arr = arr
        # go to best
        travel = d(current, best)
        t = max(t + travel, ready[best])
        total_cost += travel
        service[best] = t
        current = best
        remaining.remove(best)
    # return to depot
    total_cost += d(current, 0)
    return total_cost, service

C_online, service = simulate_online_nn()
print(f"\n=== Online tour ===")
print(f"  C(N)_online = {C_online:.3f}")
print(f"  r = C_online / c* = {C_online/c_N:.4f}")
for i in N:
    print(f"  service_{i} = {service[i]:.3f}")

# Determine F
print("\n=== Feasibility of key coalitions ===")
a = ready
s = service

def CW(S):
    lo = max(a[i] for i in S)
    hi = min(s[i] for i in S)
    return (lo, hi) if lo < hi else None

# Check all non-singleton coalitions
feasible = []
for S in powerset(N):
    if len(S) == 0:
        continue
    S_sorted = tuple(sorted(S))
    cw = CW(S)
    if cw is not None:
        feasible.append(S_sorted)
print(f"  |F| = {len(feasible)}")
for S in feasible:
    cw = CW(S)
    print(f"   {set(S)}: CW = [{cw[0]:.2f}, {cw[1]:.2f})")

print(f"\n  All coalitions considered: {2**5 - 1} = 31")
print(f"  |F|/(2^n-1) = {len(feasible)/31:.3f}")

# Pattern diagnostic
print("\n=== Sequentiality check ===")
order = sorted(N, key=lambda i: a[i])
print(f"  Customer arrival order: {order}")
print(f"  Sequentiality s_j <= a_{{next}}?")
for i in range(len(order)-1):
    j, jnext = order[i], order[i+1]
    print(f"    s_{j}={s[j]:.2f} <= a_{jnext}={a[jnext]} : {s[j] <= a[jnext]}")

# Since only singletons are feasible, Temporal Nucleolus minimizes
# max_i (c({i}) - x_i)  subject to sum x_i = c(N)
# Optimal: x_i = c({i}) - (sum c({i}) - c(N))/n
sum_singletons = sum(tsp_cost[(i,)] for i in N)
# [tsg-agent T3/E1] Paper uses C_online as efficiency budget (Def 4)
slack = (sum_singletons - C_online) / len(N)
tnu = {i: tsp_cost[(i,)] - slack for i in N}
print(f"\n=== Temporal Nucleolus (singletons-only F) ===")
print(f"  Uniform slack per player: (sum c({{i}}) - c(N)) / n = {slack:.3f}")
for i in N:
    print(f"  x_{i} = c({{{i}}}) - slack = {tnu[i]:.3f}")
print(f"  Sum x_i = {sum(tnu.values()):.3f} (should equal C_online = {C_online:.3f})")

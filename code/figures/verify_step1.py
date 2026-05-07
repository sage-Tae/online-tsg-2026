import numpy as np
from itertools import permutations

depot = np.array([35.0, 35.0])
pos = {
    1: np.array([45.0, 68.0]),
    2: np.array([45.0, 70.0]),
    3: np.array([42.0, 66.0]),
    4: np.array([42.0, 68.0]),
    5: np.array([40.0, 69.0])
}
ready = {1: 912, 2: 825, 3: 65, 4: 727, 5: 15}
due   = {1: 967, 2: 870, 3: 146, 4: 782, 5: 67}
speed = 1.0

def dist(a, b):
    return float(np.linalg.norm(a - b))

print("=== c({i}) ===")
c_single = {}
for i in range(1, 6):
    c_single[i] = 2 * dist(depot, pos[i])
    print(f"c({{{i}}}) = {c_single[i]:.3f}")

print("\n=== Online NN Tour ===")
current_pos = depot.copy()
t = 0.0
unserved = list(range(1, 6))
route = []
total_travel = 0.0

while unserved:
    arrived = [i for i in unserved if ready[i] <= t]
    if not arrived:
        next_arrive_time = min(ready[i] for i in unserved)
        next_customer = min(
            [i for i in unserved if ready[i] == next_arrive_time],
            key=lambda i: dist(current_pos, pos[i])
        )
        travel_time = dist(current_pos, pos[next_customer])
        arrive_at_customer = t + travel_time
        if arrive_at_customer <= ready[next_customer]:
            t = arrive_at_customer
            continue
        else:
            t = next_arrive_time
            continue
    nn = min(arrived, key=lambda i: dist(current_pos, pos[i]))
    travel = dist(current_pos, pos[nn])
    t_arrive = t + travel
    serve_t = max(t_arrive, float(ready[nn]))
    total_travel += travel
    route.append({'customer': nn, 'serve_time': serve_t, 'travel': travel})
    current_pos = pos[nn].copy()
    t = serve_t
    unserved.remove(nn)

return_dist = dist(current_pos, depot)
total_travel += return_dist

print(f"Visit order: {[r['customer'] for r in route]}")
for r in route:
    print(f"  Customer {r['customer']}: serve_time = {r['serve_time']:.4f}")
print(f"C(N)_online (travel only) = {total_travel:.3f}")

serve_times = {r['customer']: r['serve_time'] for r in route}

print("\n=== Fully Sequential Check ===")
visit_order = [r['customer'] for r in route]
is_sequential = True
for k in range(len(visit_order) - 1):
    cur, nxt = visit_order[k], visit_order[k+1]
    ok = serve_times[cur] <= ready[nxt]
    print(f"  s_{cur}={serve_times[cur]:.3f} <= a_{nxt}={ready[nxt]}: {ok}")
    if not ok:
        is_sequential = False
print(f"Fully sequential: {is_sequential}")

print("\n=== c*(N) Exact TSP ===")
customers = list(range(1, 6))
best_cost = float('inf')
for perm in permutations(customers):
    cost = dist(depot, pos[perm[0]])
    for j in range(len(perm)-1):
        cost += dist(pos[perm[j]], pos[perm[j+1]])
    cost += dist(pos[perm[-1]], depot)
    if cost < best_cost:
        best_cost = cost
        best_perm = perm
print(f"c*(N) = {best_cost:.3f}, order = {best_perm}")
print(f"\nr = {total_travel/best_cost:.4f}")

print("\n=== delta_i ===")
deltas = {}
for i in customers:
    rest = [j for j in customers if j != i]
    c_rest = float('inf')
    for perm in permutations(rest):
        cost = dist(depot, pos[perm[0]])
        for j in range(len(perm)-1):
            cost += dist(pos[perm[j]], pos[perm[j+1]])
        cost += dist(pos[perm[-1]], depot)
        if cost < c_rest:
            c_rest = cost
    delta = c_single[i] + c_rest - best_cost
    deltas[i] = delta
    print(f"  delta_{i} = {delta:.3f}, c(N\\{{{i}}}) = {c_rest:.3f}")

min_delta = min(deltas.values())
r_star_star = 1 + min_delta / best_cost
print(f"\nr** = {r_star_star:.4f}")

print("\n=== Temporal Nucleolus (F = singletons) ===")
sum_c_single = sum(c_single[i] for i in customers)
n = 5
epsilon = (sum_c_single - total_travel) / n
print(f"Sum c({{i}}) = {sum_c_single:.3f}")
print(f"C(N)_online = {total_travel:.3f}")
print(f"epsilon = {epsilon:.4f}")
for i in customers:
    xi = c_single[i] - epsilon
    print(f"  x_{i} = {xi:.4f}")
print(f"Sum x_i = {sum(c_single[i]-epsilon for i in customers):.4f}")

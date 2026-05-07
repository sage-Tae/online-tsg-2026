"""Online TSG simulator parameterized by dispatch policy.

Event semantics match the paper's Online TSG (Section 3):
  - Customer i arrives at time a_i and enters the waiting queue U_t.
  - The vehicle, following the dispatch policy, picks the next served
    customer from U_t; its serve time s_i is the instant that customer
    is reached.
  - The total online cost C(N)_online returned here is the *total
    travel distance* of the realized tour (from depot through all
    customers and back), matching paper Section 3.2 and Table 1.

Feasible coalitions F are reconstructed post-hoc from the realized
(arrivals, serve_times) pair using the paper Definition 2
(src.feasibility.reconstruct_F), so dispatch-iteration miss effects
that previously truncated F are eliminated.
"""

import sys

from src.tsp import dist
from src.feasibility import reconstruct_F, compute_coalition_costs


def run_with_policy(positions, arrival_times, policy_fn,
                    depot=(0, 0), speed=1.0, coalition_cache=None):
    """Run the online TSG with the given dispatch policy.

    Returns dict with:
      C_N            : total travel distance of the realized tour
      coalition_costs: {S: c(S)} for every S in F per Definition 2
      route, events, serve_times
      k              : max_t |U_t|  (peak waiting-queue size)
      players        : sorted list of customer ids
    """
    all_ids = sorted(positions.keys())
    n = len(all_ids)
    arrivals = sorted(all_ids, key=lambda i: arrival_times[i])

    if coalition_cache is None:
        coalition_cache = {}

    U_t = set()
    V_t = set()
    events = []
    route = []
    serve_times = {}
    k_max = 0

    vehicle_pos = depot
    current_time = 0.0
    total_travel = 0.0
    arrival_idx = 0

    while len(V_t) < n:
        # arrivals up to current_time
        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= current_time + 1e-9:
                U_t.add(cid)
                events.append({'type': 'ARRIVE', 'time': arrival_times[cid],
                               'customer': cid, 'vehicle_pos': vehicle_pos})
                arrival_idx += 1
            else:
                break

        if not U_t:
            if arrival_idx < len(arrivals):
                current_time = arrival_times[arrivals[arrival_idx]]
                continue
            else:
                break

        # delegate to policy
        best_id = policy_fn(vehicle_pos, U_t, positions, depot,
                            arrival_times, current_time, speed)

        best_d = dist(vehicle_pos, positions[best_id])
        travel_time = best_d / speed
        arrival_at_cust = current_time + travel_time
        serve_time = max(arrival_at_cust, arrival_times[best_id])

        # Sweep in arrivals up to serve_time (for peak-queue measurement)
        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= serve_time + 1e-9:
                if cid not in V_t:
                    U_t.add(cid)
                events.append({'type': 'ARRIVE', 'time': arrival_times[cid],
                               'customer': cid, 'vehicle_pos': vehicle_pos})
                arrival_idx += 1
            else:
                break
        if len(U_t) > k_max:
            k_max = len(U_t)

        # Accumulate travel distance (not elapsed time)
        total_travel += best_d
        current_time = serve_time
        vehicle_pos = positions[best_id]

        U_t.remove(best_id)
        V_t.add(best_id)
        route.append((best_id, serve_time))
        serve_times[best_id] = serve_time
        events.append({'type': 'SERVE', 'time': serve_time,
                       'customer': best_id, 'vehicle_pos': vehicle_pos})

    # Return-to-depot leg
    return_leg = dist(vehicle_pos, depot)
    total_travel += return_leg

    # Reconstruct F per paper Definition 2 and compute c(S) for S in F.
    # We additionally compute c(N) unconditionally because it is needed to
    # form the competitive ratio r = C_N_online / c*(N), independent of
    # whether N is feasible per Definition 2.
    if n <= 15:
        from src.tsp import tsp_cost
        F = reconstruct_F(n, arrival_times, serve_times)
        coalition_costs = compute_coalition_costs(
            F, positions, arrival_times, depot=depot, speed=speed,
            cache=coalition_cache,
        )
        grand = frozenset(all_ids)
        if grand not in coalition_costs:
            if grand in coalition_cache:
                coalition_costs[grand] = coalition_cache[grand]
            else:
                cost, _ = tsp_cost(depot, all_ids, positions, arrival_times, speed)
                coalition_costs[grand] = cost
                coalition_cache[grand] = cost
    else:
        # Fallback: n too large for full 2^n enumeration.
        # We retain singletons + the grand coalition only; experiments
        # at n > 15 use the restricted-LP path (Appendix C) or the
        # scaleup runner, both of which reconstruct F themselves.
        coalition_costs = {}
        from src.tsp import tsp_cost
        for cid in all_ids:
            fs = frozenset([cid])
            if fs in coalition_cache:
                coalition_costs[fs] = coalition_cache[fs]
            else:
                cost, _ = tsp_cost(depot, [cid], positions, arrival_times, speed)
                coalition_costs[fs] = cost
                coalition_cache[fs] = cost
        grand = frozenset(all_ids)
        if grand in coalition_cache:
            coalition_costs[grand] = coalition_cache[grand]
        else:
            cost, _ = tsp_cost(depot, all_ids, positions, arrival_times, speed)
            coalition_costs[grand] = cost
            coalition_cache[grand] = cost
        print(f"  WARNING: n={n} > 15, coalition_costs truncated to "
              f"singletons+N; use scaleup path for full analysis",
              file=sys.stderr)

    return {
        'events': events,
        'route': route,
        'serve_times': serve_times,
        'coalition_costs': coalition_costs,
        'C_N': total_travel,   # total travel distance (paper definition)
        'players': all_ids,
        'k': k_max,
    }

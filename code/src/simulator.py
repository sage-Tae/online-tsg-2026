"""Online TSG Simulator (nearest-neighbor dispatch).

C(N)_online is the total travel distance of the realized tour
(depot -> customers -> depot), matching paper Section 3.2 and Table 1.
Feasible coalitions F are reconstructed post-hoc from the realized
(arrivals, serve_times) pair per paper Definition 2.
"""

from src.tsp import dist
from src.feasibility import reconstruct_F, compute_coalition_costs


class OnlineTSGSimulator:
    def __init__(self, customers, arrival_times, speed=1.0, depot=(0, 0)):
        self.customers = customers
        self.arrival_times = arrival_times
        self.speed = speed
        self.depot = depot
        self.positions = dict(customers)

    def run(self):
        depot = self.depot
        positions = self.positions
        early_times = self.arrival_times
        all_ids = sorted(self.customers.keys())
        n = len(all_ids)

        arrivals = sorted(all_ids, key=lambda i: early_times[i])

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
            # Process arrivals up to current_time
            while arrival_idx < len(arrivals):
                cid = arrivals[arrival_idx]
                if early_times[cid] <= current_time + 1e-9:
                    U_t.add(cid)
                    events.append({
                        'type': 'ARRIVE', 'time': early_times[cid],
                        'customer': cid, 'vehicle_pos': vehicle_pos
                    })
                    arrival_idx += 1
                else:
                    break

            if not U_t:
                if arrival_idx < len(arrivals):
                    current_time = early_times[arrivals[arrival_idx]]
                    continue
                else:
                    break

            # NN: serve nearest unserved
            best_id = None
            best_d = float('inf')
            for cid in U_t:
                d = dist(vehicle_pos, positions[cid])
                if d < best_d:
                    best_d = d
                    best_id = cid

            travel_time = best_d / self.speed
            arrival_time_at_cust = current_time + travel_time
            serve_time = max(arrival_time_at_cust, early_times[best_id])

            # Sweep arrivals up to serve_time (peak-queue measurement)
            while arrival_idx < len(arrivals):
                cid = arrivals[arrival_idx]
                if early_times[cid] <= serve_time + 1e-9:
                    if cid not in V_t:
                        U_t.add(cid)
                    events.append({
                        'type': 'ARRIVE', 'time': early_times[cid],
                        'customer': cid, 'vehicle_pos': vehicle_pos
                    })
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
            route.append((best_id, serve_time))
            serve_times[best_id] = serve_time
            events.append({
                'type': 'SERVE', 'time': serve_time,
                'customer': best_id, 'vehicle_pos': vehicle_pos
            })

        # Return-to-depot leg
        return_leg = dist(vehicle_pos, depot)
        total_travel += return_leg

        # Reconstruct F per paper Definition 2 and compute c(S).
        # c(N) is added unconditionally since r = C_N_online / c*(N)
        # needs it regardless of whether N is feasible.
        from src.tsp import tsp_cost
        F = reconstruct_F(n, early_times, serve_times)
        coalition_costs = compute_coalition_costs(
            F, positions, early_times, depot=depot, speed=self.speed,
        )
        grand = frozenset(all_ids)
        if grand not in coalition_costs:
            cost, _ = tsp_cost(depot, all_ids, positions, early_times, self.speed)
            coalition_costs[grand] = cost

        return {
            'events': events,
            'route': route,
            'serve_times': serve_times,
            'coalition_costs': coalition_costs,
            'C_N': total_travel,   # total travel distance (paper definition)
            'players': all_ids,
            'k': k_max,
        }

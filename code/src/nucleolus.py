"""Temporal + Static Nucleolus computation using PuLP.

Implementation note (degeneracy). This implementation fixes ALL tight
constraints at each stage's optimum (simplified Kopelowitz). It is
sufficient for Core existence judgment via the first-stage epsilon
(returned as ``core_epsilon``), but does not guarantee uniqueness of
the returned nucleolus coordinates under primal degeneracy. A rank-
aware procedure following Kopelowitz (1967) and Guajardo-Jornsten
(2015), which fixes only linearly independent tight constraints, can
be layered on top without affecting the Core stability results
reported in the paper.
"""

import pulp
from src.tsp import tsp_cost


def compute_nucleolus(coalition_costs, C_N, players):
    """
    Sequential LP로 nucleolus 계산 (Guajardo 2015 방식).
    return: ({player: allocation}, epsilon_star, core_epsilon)
      - epsilon_star: 최종 nucleolus epsilon (lexicographic)
      - core_epsilon: 첫 번째 iteration epsilon (Core 판정용, >0이면 Core 비어있음)
    """
    n = len(players)

    coalitions = []
    costs = []
    for S, cS in coalition_costs.items():
        if len(S) == 0 or len(S) == n:
            continue
        coalitions.append(S)
        costs.append(cS)

    if not coalitions:
        return {p: C_N / n for p in players}, 0.0, 0.0

    fixed_coalitions = set()
    epsilon_star = None
    core_epsilon = None
    allocation = {p: C_N / n for p in players}

    for iteration in range(n + 1):
        prob = pulp.LpProblem(f"nucleolus_iter_{iteration}", pulp.LpMinimize)

        y = {p: pulp.LpVariable(f"y_{p}", cat='Continuous') for p in players}
        eps = pulp.LpVariable("epsilon", cat='Continuous')

        prob += eps
        prob += pulp.lpSum([y[p] for p in players]) == C_N

        # Note: no y[p] >= 0 constraint -- Definition 3 of the paper does
        # not require nonnegativity.  Cost allocations may be negative if
        # some customer's removal would shortcut the grand tour, in which
        # case the remaining customers effectively pay for the carried
        # coalition's detour (Potters et al. 1992).

        for idx, S in enumerate(coalitions):
            lhs = pulp.lpSum([y[p] for p in S])
            if idx in fixed_coalitions:
                prob += lhs - costs[idx] <= epsilon_star
            else:
                prob += lhs - costs[idx] <= eps

        prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=30))

        if prob.status != pulp.constants.LpStatusOptimal:
            break

        epsilon_star = pulp.value(eps)
        allocation = {p: pulp.value(y[p]) for p in players}

        # 첫 번째 iteration의 epsilon = Core 판정용 (최대 excess)
        if core_epsilon is None:
            core_epsilon = epsilon_star

        new_fixed = False
        for idx, S in enumerate(coalitions):
            if idx in fixed_coalitions:
                continue
            excess = sum(allocation[p] for p in S) - costs[idx]
            if abs(excess - epsilon_star) < 1e-6:
                fixed_coalitions.add(idx)
                new_fixed = True

        if not new_fixed:
            break

    return allocation, epsilon_star, core_epsilon


def temporal_nucleolus(coalition_costs, C_N, players):
    alloc, eps_star, core_eps = compute_nucleolus(coalition_costs, C_N, players)
    return alloc, core_eps  # Core 판정용 epsilon 반환


def static_nucleolus(customers, positions, arrival_times, depot=(0, 0)):
    from itertools import combinations

    players = sorted(customers.keys()) if isinstance(customers, dict) else sorted(customers)
    n = len(players)

    if n > 12:
        return None, None, None

    coalition_costs = {}
    for size in range(1, n + 1):
        for subset in combinations(players, size):
            fs = frozenset(subset)
            cost, _ = tsp_cost(depot, list(subset), positions, arrival_times)
            coalition_costs[fs] = cost

    grand = frozenset(players)
    C_N_static = coalition_costs[grand]

    alloc, eps_star, core_eps = compute_nucleolus(coalition_costs, C_N_static, players)

    return alloc, core_eps, C_N_static

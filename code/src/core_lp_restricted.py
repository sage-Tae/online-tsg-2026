"""
Restricted Core LP check for large n where full 2^n coalition enumeration
is infeasible.

Strategy:
  1. Always include all singletons {i} and all complements N\{i}.
  2. Randomly sample additional coalitions of intermediate sizes.
  3. Keep only those feasible: max_{j in S} a_j < min_{j in S} s_j.
  4. Solve LP: find x with sum x_i = C_online and x(S) <= c(S) for sampled S.
  5. Infeasible LP => Core is empty (certified).
  6. Feasible LP => "no violation found in sample" (Core may still be empty
     via coalitions we did not sample; this test is a one-sided certificate).
"""

import random

import pulp

from src.tsp_scaleup import scaled_tsp

DEPOT = (0.0, 0.0)


def _feasible_coalition(S, arrivals, service_times):
    """S is feasible iff there exists a time window with S subset U_t."""
    if len(S) == 0:
        return False
    return max(arrivals[i] for i in S) < min(service_times[i] for i in S) - 1e-9


def sample_feasible_coalitions(n, arrivals, service_times, num_samples, seed=0):
    """Sample coalitions; always include singletons + complements + grand.

    Returns a set of frozensets.
    """
    rng = random.Random(seed)
    players = list(range(1, n + 1))
    full = frozenset(players)

    coalitions = set()

    # Singletons
    for i in players:
        S = frozenset([i])
        if _feasible_coalition(S, arrivals, service_times):
            coalitions.add(S)
    # Complements N\{i}
    for i in players:
        S = frozenset(full - {i})
        if _feasible_coalition(S, arrivals, service_times):
            coalitions.add(S)
    # Grand coalition
    if _feasible_coalition(full, arrivals, service_times):
        coalitions.add(full)

    # Random intermediate sizes
    attempts = 0
    max_attempts = num_samples * 20
    while len(coalitions) < num_samples and attempts < max_attempts:
        size = rng.randint(2, n - 1)
        members = rng.sample(players, size)
        S = frozenset(members)
        if S not in coalitions and _feasible_coalition(S, arrivals, service_times):
            coalitions.add(S)
        attempts += 1

    return coalitions


def check_core_restricted(n, positions, arrivals, service_times,
                          C_N_online, num_samples=10000, seed=0, verbose=True):
    """Restricted Core emptiness certificate.

    Returns dict with:
        core_nonempty: True/False (True means feasible in sample, NOT full proof)
        num_coalitions_sampled: int
        num_feasible_in_lp: int
        violating_sizes: sorted list[int] of coalition sizes that bind (if infeasible)
        coalition_cache: dict[frozenset -> cost]
    """
    if verbose:
        print(f"  Sampling up to {num_samples} feasible coalitions from 2^{n}...")

    sampled = sample_feasible_coalitions(
        n, arrivals, service_times, num_samples, seed=seed
    )
    if verbose:
        print(f"  Sampled {len(sampled)} feasible coalitions.")

    # Compute c(S) for each via scaled_tsp (Held-Karp or LKH)
    cache = {}
    for S in sampled:
        if S in cache:
            continue
        cost, _ = scaled_tsp(DEPOT, list(S), positions, arrivals)
        cache[S] = cost

    players = list(range(1, n + 1))
    full = frozenset(players)

    if full not in cache:
        cost, _ = scaled_tsp(DEPOT, list(full), positions, arrivals)
        cache[full] = cost

    # LP: minimize epsilon s.t. sum x = C_online, x(S) - c(S) <= epsilon for S in sample
    prob = pulp.LpProblem("core_restricted", pulp.LpMinimize)
    y = {p: pulp.LpVariable(f"y_{p}", cat='Continuous') for p in players}
    eps = pulp.LpVariable("eps", cat='Continuous')
    prob += eps
    prob += pulp.lpSum(y[p] for p in players) == C_N_online

    constraint_coalitions = []
    for S in sampled:
        if len(S) == 0 or S == full:
            continue
        lhs = pulp.lpSum(y[p] for p in S)
        prob += lhs - cache[S] <= eps
        constraint_coalitions.append(S)

    if verbose:
        print(f"  LP: {n} vars, {len(constraint_coalitions)} constraints")

    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=300))
    if status != pulp.constants.LpStatusOptimal:
        return {
            'core_nonempty': None,
            'eps_star': None,
            'num_coalitions_sampled': len(sampled),
            'num_feasible_in_lp': len(constraint_coalitions),
            'violating_sizes': [],
            'note': f'lp_status={pulp.LpStatus[status]}',
        }
    eps_star = pulp.value(eps)
    core_nonempty = eps_star <= 1e-6

    # Identify binding / violating coalitions (those with x(S) - c(S) close to eps_star)
    violating_sizes = []
    if not core_nonempty:
        y_val = {p: pulp.value(y[p]) for p in players}
        for S in constraint_coalitions:
            lhs = sum(y_val[p] for p in S)
            slack = cache[S] + eps_star - lhs
            if abs(slack) < 1e-4:  # binding
                violating_sizes.append(len(S))
        violating_sizes = sorted(set(violating_sizes))

    return {
        'core_nonempty': core_nonempty,
        'eps_star': eps_star,
        'num_coalitions_sampled': len(sampled),
        'num_feasible_in_lp': len(constraint_coalitions),
        'violating_sizes': violating_sizes,
        'coalition_cache': cache,
        'note': 'Optimal',
    }

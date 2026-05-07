"""Experiment metrics computation."""


def compute_metrics(sim_result, temporal_result, static_result):
    """
    sim_result: simulator output dict
    temporal_result: (allocation, epsilon)
    static_result: (allocation, epsilon, C_N_static) or (None, None, None)
    """
    players = sim_result['players']
    coalition_costs = sim_result['coalition_costs']
    C_N_online = sim_result['C_N']

    temporal_alloc, temporal_epsilon = temporal_result

    # Individual costs
    sum_individual = sum(coalition_costs.get(frozenset([p]), 0) for p in players)

    # Static results
    if static_result[0] is not None:
        static_alloc, static_epsilon, C_N_static = static_result
    else:
        static_alloc, static_epsilon, C_N_static = None, None, None

    # Competitive ratio
    if C_N_static is not None and C_N_static > 1e-9:
        r = C_N_online / C_N_static
        r_star = sum_individual / C_N_static
    else:
        r = None
        r_star = None

    # r vs r*
    if r is not None and r_star is not None:
        if r < r_star - 1e-9:
            r_vs_rstar = 'r<r*'
        elif r > r_star + 1e-9:
            r_vs_rstar = 'r>r*'
        else:
            r_vs_rstar = 'r=r*'
    else:
        r_vs_rstar = None

    # Core judgment
    temporal_core = temporal_epsilon is not None and temporal_epsilon <= 1e-6
    static_core = static_epsilon is not None and static_epsilon <= 1e-6

    # Theorem predictions
    theorem2_predicts_no_core = C_N_online > sum_individual + 1e-9
    theorem4_predicts_safe = r is not None and r_star is not None and r <= r_star + 1e-9

    n = len(players)
    n_feasible = len(coalition_costs)
    n_static = 2**n - 1

    return {
        'C_N_online': round(C_N_online, 4),
        'C_N_static': round(C_N_static, 4) if C_N_static is not None else None,
        'r': round(r, 4) if r is not None else None,
        'sum_individual': round(sum_individual, 4),
        'r_star': round(r_star, 4) if r_star is not None else None,
        'r_vs_rstar': r_vs_rstar,
        'temporal_epsilon': round(temporal_epsilon, 6) if temporal_epsilon is not None else None,
        'static_epsilon': round(static_epsilon, 6) if static_epsilon is not None else None,
        'temporal_core': temporal_core,
        'static_core': static_core,
        'theorem2_predicts_no_core': theorem2_predicts_no_core,
        'theorem4_predicts_safe': theorem4_predicts_safe,
        'n_feasible_coalitions': n_feasible,
        'n_static_coalitions': n_static,
        'coalition_reduction_ratio': round(n_feasible / n_static, 4) if n_static > 0 else None,
    }

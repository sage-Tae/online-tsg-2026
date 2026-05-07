"""
Sensitivity experiment (Phase 2.5, Appendix B).

Empirical verification of scale invariance:
Joint rescaling (L, tau) -> (alpha*L, alpha*tau) with fixed speed.
All dimensionless observables (r, r**, k, core status) should be invariant.

Grid: alpha in {0.5, 1.0, 2.0, 5.0} x n in {10, 20} x patterns {B_heavy, B_medium, C}
       x seed = 42  =>  24 instances.

Output: logs/sensitivity_v2.csv
"""

import os
import sys
import signal
import time
import traceback
from contextlib import contextmanager
from itertools import product

import pandas as pd
import pulp

EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(EXPERIMENT_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, 'src'))

from config import (
    SENSITIVITY_ALPHAS, SENSITIVITY_N_VALUES, SENSITIVITY_PATTERNS,
    SENSITIVITY_SEED,
    PATTERN_RHO, L_N2, tau_from_rho,
)
from generators import generate_scaled_instance

from src.policies import select_next_nn
from src.policy_simulator import run_with_policy
from src.tsp_scaleup import scaled_tsp

DEPOT = (0.0, 0.0)
LOG_DIR = os.path.join(EXPERIMENT_DIR, 'logs')
OUT_PATH = os.path.join(LOG_DIR, 'sensitivity_v2.csv')

CORE_LP_TIMEOUT = 300


class TimeoutError_(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def handler(signum, frame):
        raise TimeoutError_("Timed out")
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _cost_of(subset, positions, arrivals, cache):
    fs = frozenset(subset)
    if fs in cache:
        return cache[fs]
    cost, _ = scaled_tsp(DEPOT, list(subset), positions, arrivals)
    cache[fs] = cost
    return cost


def check_core_lp(coalition_costs, C_N, players, timeout=CORE_LP_TIMEOUT):
    n = len(players)
    coalitions = [S for S in coalition_costs if 0 < len(S) < n]
    prob = pulp.LpProblem("core_check", pulp.LpMinimize)
    y = {p: pulp.LpVariable(f"y_{p}", cat='Continuous') for p in players}
    eps = pulp.LpVariable("eps", cat='Continuous')
    prob += eps
    prob += pulp.lpSum(y[p] for p in players) == C_N
    for S in coalitions:
        lhs = pulp.lpSum(y[p] for p in S)
        prob += lhs - coalition_costs[S] <= eps
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=timeout))
    if status != pulp.constants.LpStatusOptimal:
        return None, None, pulp.LpStatus[status]
    eps_star = pulp.value(eps)
    return (eps_star <= 1e-6), eps_star, 'Optimal'


def run_instance(n, pattern, seed, alpha):
    positions, arrivals, meta = generate_scaled_instance(n, pattern, seed, alpha=alpha)
    players = sorted(positions.keys())

    sim = run_with_policy(positions, arrivals, select_next_nn)
    C_N = sim['C_N']
    F = set(sim['coalition_costs'].keys())
    k = sim['k']
    serve_times = sim['serve_times']
    cost_cache = dict(sim['coalition_costs'])

    c_star_N = _cost_of(tuple(players), positions, arrivals, cost_cache)
    r = C_N / c_star_N if c_star_N > 1e-9 else None

    # Lemma 9 applicability
    deltas_feasible = []
    for i in players:
        a_others = [arrivals[j] for j in players if j != i]
        s_others = [serve_times[j] for j in players if j != i]
        if max(a_others) < min(s_others) - 1e-9:
            comp = frozenset(p for p in players if p != i)
            c_comp = _cost_of(tuple(sorted(comp)), positions, arrivals, cost_cache)
            c_i = _cost_of((i,), positions, arrivals, cost_cache)
            deltas_feasible.append(c_i + c_comp - c_star_N)
            F.add(comp)

    thm11_applicable = len(deltas_feasible) > 0
    if thm11_applicable:
        r_ss = 1.0 + min(deltas_feasible) / c_star_N
        thm11_fires = r > r_ss + 1e-9
    else:
        r_ss = None
        thm11_fires = False

    # Core LP
    note = ''
    core_nonempty = None
    core_eps = None
    if pattern == 'A' and n >= 30:
        note = f'core_lp_intractable'
    else:
        try:
            with time_limit(CORE_LP_TIMEOUT):
                core_nonempty, core_eps, status = check_core_lp(
                    {S: cost_cache[S] for S in F}, C_N, players)
                if status != 'Optimal':
                    note = f'lp_status={status}'
        except TimeoutError_:
            note = 'core_lp_timeout'
        except Exception as e:
            note = f'core_lp_error={type(e).__name__}'

    return {
        'n': n, 'pattern': pattern, 'seed': seed, 'alpha': alpha,
        'L': round(meta['L'], 4),
        'rho': meta['rho'],
        'tau': round(meta['tau'], 4),
        'c_star_N': round(c_star_N, 4),
        'C_N_online': round(C_N, 4),
        'r': round(r, 6) if r is not None else None,
        'r_star_star': round(r_ss, 6) if r_ss is not None else None,
        'k': k,
        'n_feasible': len(F),
        'core_nonempty': core_nonempty,
        'core_epsilon': round(core_eps, 6) if core_eps is not None else None,
        'theorem11_applicable': thm11_applicable,
        'theorem11_fires': thm11_fires,
        'note': note,
    }


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    results = []
    configs = list(product(SENSITIVITY_N_VALUES, SENSITIVITY_PATTERNS, SENSITIVITY_ALPHAS))
    total = len(configs)
    print(f"Running {total} sensitivity instances (seed={SENSITIVITY_SEED})")

    t0 = time.time()
    for idx, (n, pattern, alpha) in enumerate(configs, 1):
        try:
            m = run_instance(n, pattern, SENSITIVITY_SEED, alpha)
        except Exception as e:
            traceback.print_exc()
            m = {'n': n, 'pattern': pattern, 'seed': SENSITIVITY_SEED,
                 'alpha': alpha, 'note': f'fatal_error={type(e).__name__}'}
        results.append(m)
        pd.DataFrame(results).to_csv(OUT_PATH, index=False)
        elapsed = time.time() - t0
        print(f"  [{idx}/{total}] n={n} pat={pattern} α={alpha} "
              f"r={m.get('r','?')} r**={m.get('r_star_star','?')} "
              f"k={m.get('k','?')} elapsed={elapsed:.1f}s")

    print(f"\nWrote {len(results)} rows to {OUT_PATH}  ({time.time()-t0:.1f}s)")


if __name__ == '__main__':
    main()

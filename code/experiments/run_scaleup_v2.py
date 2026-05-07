"""
Scale-up experiment runner (Phase 2.5).

Extends run_main.py to n in {20, 30, 50} for patterns
{A, B_medium, C} under NN policy only.

Uses new N2 normalization + rho-based patterns (phase1_design.md §3.2),
but preserves the solid legacy logic from run_scaleup.py:
- scaled_tsp() auto-switch between Held-Karp (n<=20) and LKH (n>20)
- Core LP check with 300s timeout
- Lemma-9 bypass of simulator F truncation (|U_t|>15)
- Incremental CSV persistence

Output: logs/scaleup_v2.csv
"""

import os
import sys
import signal
import time
import traceback
from contextlib import contextmanager

import pandas as pd
import pulp

EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(EXPERIMENT_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, 'src'))

from config import (
    SCALEUP_N_VALUES, SCALEUP_PATTERNS,
    DEFAULT_SEEDS,
    PATTERN_RHO, L_N2, tau_from_rho,
)
from generators import generate_customers, generate_arrivals

from src.policies import select_next_nn
from src.policy_simulator import run_with_policy
from src.tsp_scaleup import scaled_tsp

DEPOT = (0.0, 0.0)
LOG_DIR = os.path.join(EXPERIMENT_DIR, 'logs')
OUT_PATH = os.path.join(LOG_DIR, 'scaleup_v2.csv')

CORE_LP_TIMEOUT = 300  # seconds


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
    """Solve nucleolus first-stage LP; Core nonempty iff epsilon* <= 0."""
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


def run_instance(n, pattern, seed):
    L = L_N2(n)
    rho = PATTERN_RHO[pattern]
    tau = tau_from_rho(rho)

    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho)
    players = sorted(positions.keys())

    sim = run_with_policy(positions, arrivals, select_next_nn)
    C_N = sim['C_N']
    F = set(sim['coalition_costs'].keys())
    k = sim['k']
    serve_times = sim['serve_times']
    cost_cache = dict(sim['coalition_costs'])

    c_star_N = _cost_of(tuple(players), positions, arrivals, cost_cache)
    c_star_source = 'held_karp' if n <= 20 else 'lkh'
    r = C_N / c_star_N if c_star_N > 1e-9 else None

    # Lemma 9: applicability directly from arrival/service windows
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

    n_feasible = len(F)

    # Core LP
    note = ''
    core_nonempty = None
    core_eps = None
    t_lp0 = time.time()

    if pattern == 'A' and n >= 30:
        core_nonempty = None
        note = f'core_lp_intractable (|F|=2^{n}-1)'
        runtime_core_lp = 0.0
    else:
        try:
            with time_limit(CORE_LP_TIMEOUT):
                core_nonempty, core_eps, status = check_core_lp(
                    {S: cost_cache[S] for S in F}, C_N, players,
                    timeout=CORE_LP_TIMEOUT)
                if status != 'Optimal':
                    note = f'lp_status={status}'
        except TimeoutError_:
            note = 'core_lp_timeout'
            core_nonempty = None
        except Exception as e:
            note = f'core_lp_error={type(e).__name__}:{str(e)[:40]}'
            core_nonempty = None
        runtime_core_lp = time.time() - t_lp0

    return {
        'n': n, 'pattern': pattern, 'seed': seed,
        'L': round(L, 4), 'rho': rho, 'tau': round(tau, 4),
        'c_star_N': round(c_star_N, 4),
        'c_star_source': c_star_source,
        'C_N_online': round(C_N, 4),
        'r': round(r, 4) if r is not None else None,
        'n_feasible': n_feasible,
        'k': k,
        'core_nonempty': core_nonempty,
        'core_epsilon': round(core_eps, 6) if core_eps is not None else None,
        'r_star_star': round(r_ss, 4) if r_ss is not None else None,
        'theorem11_applicable': thm11_applicable,
        'theorem11_fires': thm11_fires,
        'runtime_core_lp_sec': round(runtime_core_lp, 2),
        'note': note,
    }


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    results = []
    total = len(SCALEUP_N_VALUES) * len(SCALEUP_PATTERNS) * len(DEFAULT_SEEDS)
    count = 0
    t0 = time.time()
    last_pct = -1

    for n in SCALEUP_N_VALUES:
        for pat in SCALEUP_PATTERNS:
            for seed in DEFAULT_SEEDS:
                count += 1
                try:
                    m = run_instance(n, pat, seed)
                except Exception as e:
                    traceback.print_exc()
                    m = {'n': n, 'pattern': pat, 'seed': seed,
                         'note': f'fatal_error={type(e).__name__}'}
                results.append(m)

                pd.DataFrame(results).to_csv(OUT_PATH, index=False)

                pct = int(100 * count / total)
                if pct // 10 > last_pct // 10:
                    elapsed = time.time() - t0
                    rate = count / elapsed if elapsed else 0
                    eta = (total - count) / rate if rate > 0 else 0
                    print(f"  [{count}/{total}] {pct}%  "
                          f"elapsed={elapsed:6.1f}s  eta={eta:6.1f}s  "
                          f"last={n}_{pat}_{seed}", flush=True)
                    last_pct = pct

    print(f"\nWrote {len(results)} rows to {OUT_PATH}")
    df = pd.DataFrame(results)
    print("\n=== Scale-up summary ===")
    for pat in SCALEUP_PATTERNS:
        for n in SCALEUP_N_VALUES:
            sub = df[(df.pattern == pat) & (df.n == n)]
            if sub.empty:
                continue
            nonempty = sub['core_nonempty'].apply(lambda v: v is True).sum()
            intract = sub['note'].str.contains('intractable', na=False).sum()
            to = sub['note'].str.contains('timeout', na=False).sum()
            r_mean = sub['r'].mean()
            r_ss_mean = sub['r_star_star'].mean()
            k_mean = sub['k'].mean()
            print(f"  {pat:>10s} n={n}: core_ok={nonempty}/{len(sub)}, "
                  f"intract={intract}, timeout={to}, "
                  f"r={r_mean:.3f}, r**={r_ss_mean:.3f}, k={k_mean:.1f}")


if __name__ == '__main__':
    main()

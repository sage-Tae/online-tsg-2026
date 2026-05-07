"""
Theorem 5, Lemma 5.1/5.2, Corollary 5.2 수치 검증.
results/summary.csv의 모든 인스턴스를 재시뮬레이션하여 검증.
"""

import sys, os, traceback, multiprocessing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from itertools import combinations

from src.simulator import OnlineTSGSimulator
from src.tsp import tsp_cost, exact_tsp, nn_tsp, dist
from src.nucleolus import temporal_nucleolus
from experiments.run_all import generate_customers, generate_arrival_times

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')


# ─── Helper functions ───

def all_subsets(items):
    """모든 비빈 부분집합 생성."""
    for size in range(1, len(items) + 1):
        for subset in combinations(items, size):
            yield subset


def compute_CW(S, arrival_times, serve_times):
    """CW(S) = ∩_{i∈S} [arrival_time_i, serve_time_i). None if empty."""
    start = max(arrival_times[i] for i in S)
    end = min(serve_times[i] for i in S)
    if start < end - 1e-9:
        return (start, end)
    return None


def verify_lemma51(F, arrival_times, serve_times, all_customers):
    """Lemma 5.1: CW(S)≠∅ ↔ S∈F. 일치율 반환."""
    total = 0
    match = 0
    for S in all_subsets(all_customers):
        fs = frozenset(S)
        cw = compute_CW(S, arrival_times, serve_times)
        cw_nonempty = (cw is not None)
        s_in_F = fs in F
        total += 1
        if cw_nonempty == s_in_F:
            match += 1
    return match / total if total > 0 else 1.0


def verify_lemma52(serve_times, arrival_times, route_order):
    """Lemma 5.2: 완전 순차 도착 확인 + N\\{i} ∉ F 확인."""
    is_fully_sequential = True
    for k in range(len(route_order) - 1):
        cur = route_order[k]
        nxt = route_order[k + 1]
        if serve_times[cur] >= arrival_times[nxt] - 1e-9:
            is_fully_sequential = False
            break
    return is_fully_sequential


def compute_deltas(players, positions, arrival_times, depot=(0, 0)):
    """δ_i = c({i}) + c(N\\{i}) - c*(N) for all i."""
    n = len(players)
    c_star_N, _ = tsp_cost(depot, players, positions, arrival_times)

    deltas = {}
    for i in players:
        c_i, _ = tsp_cost(depot, [i], positions, arrival_times)
        N_minus_i = [j for j in players if j != i]
        c_Ni, _ = tsp_cost(depot, N_minus_i, positions, arrival_times)
        deltas[i] = c_i + c_Ni - c_star_N

    return deltas, c_star_N


def verify_theorem5(C_N_online, c_star_N, deltas, temporal_core, F, players):
    """Theorem 5: N\\{i*} ∈ F AND C(N) > c*(N) + min_i δ_i → Core = ∅.
    전제조건: argmin δ_i에 대해 N\\{i*}가 feasible이어야 함."""
    # δ_i가 가장 작은 i* 찾되, N\{i*} ∈ F인 것만
    eligible = {}
    for i, d in deltas.items():
        N_minus_i = frozenset(j for j in players if j != i)
        if N_minus_i in F:
            eligible[i] = d

    if eligible:
        i_star = min(eligible, key=eligible.get)
        min_delta = eligible[i_star]
    else:
        # N\{i} ∉ F for all i → Theorem 5 적용 불가
        min_delta = min(deltas.values())
        return {
            'min_delta': min_delta,
            'r_double_star': 1 + min_delta / c_star_N if c_star_N > 1e-9 else None,
            'threshold': c_star_N + min_delta,
            'predicted_empty': False,  # 적용 불가
            'actual_empty': not temporal_core,
            'theorem5_correct': True,  # vacuously true
            'theorem5_applicable': False,
        }

    r_double_star = 1 + min_delta / c_star_N if c_star_N > 1e-9 else None
    threshold = c_star_N + min_delta

    predicted_empty = (C_N_online > threshold + 1e-9)
    actual_empty = (not temporal_core)

    if predicted_empty:
        correct = actual_empty
    else:
        correct = True

    return {
        'min_delta': min_delta,
        'r_double_star': r_double_star,
        'threshold': threshold,
        'predicted_empty': predicted_empty,
        'actual_empty': actual_empty,
        'theorem5_correct': correct,
        'theorem5_applicable': True,
    }


def verify_corollary52(k, n, temporal_core):
    """Corollary 5.2: k < n-1 → Core 안전."""
    safe_predicted = (k < n - 1)
    actual_safe = temporal_core

    if safe_predicted:
        correct = actual_safe
    else:
        correct = True

    return {
        'k': k,
        'cor52_safe_predicted': safe_predicted,
        'cor52_actual_safe': actual_safe,
        'cor52_correct': correct
    }


# ─── Single instance validation ───

def validate_single(n, pattern, seed):
    """단일 인스턴스 전체 검증."""
    positions = generate_customers(n, seed)
    arrival_times = generate_arrival_times(n, pattern, positions, seed)
    depot = (0, 0)
    players = sorted(positions.keys())

    # Simulate
    sim = OnlineTSGSimulator(positions, arrival_times, depot=depot)
    result = sim.run()
    C_N_online = result['C_N']
    coalition_costs = result['coalition_costs']

    # serve_times from route
    serve_times = {}
    for cid, stime in result['route']:
        serve_times[cid] = stime

    # F = set of feasible coalitions (from simulator)
    F = set(coalition_costs.keys())

    # route order
    route_order = [cid for cid, _ in result['route']]

    # k = max |U_t|
    k = 0
    U_t = set()
    V_t = set()
    arrivals_sorted = sorted(players, key=lambda i: arrival_times[i])
    arr_idx = 0
    for cid, stime in result['route']:
        # process arrivals up to serve_time
        while arr_idx < len(arrivals_sorted):
            aid = arrivals_sorted[arr_idx]
            if arrival_times[aid] <= stime + 1e-9:
                if aid not in V_t:
                    U_t.add(aid)
                arr_idx += 1
            else:
                break
        k = max(k, len(U_t))
        U_t.discard(cid)
        V_t.add(cid)

    # Temporal nucleolus
    t_alloc, t_eps = temporal_nucleolus(coalition_costs, C_N_online, players)
    temporal_core = (t_eps is not None and t_eps <= 1e-6)

    # ─── Lemma 5.1 ───
    if n <= 12:
        lemma51_rate = verify_lemma51(F, arrival_times, serve_times, players)
    else:
        lemma51_rate = None  # 2^15 too many

    # ─── Lemma 5.2 ───
    is_sequential = verify_lemma52(serve_times, arrival_times, route_order)
    # check N\{i} ∉ F for all i
    N_i_not_in_F = True
    for i in players:
        N_minus_i = frozenset(j for j in players if j != i)
        if N_minus_i in F:
            N_i_not_in_F = False
            break

    # ─── Theorem 5 ───
    deltas, c_star_N = compute_deltas(players, positions, arrival_times, depot)
    t5 = verify_theorem5(C_N_online, c_star_N, deltas, temporal_core, F, players)

    # ─── Corollary 5.2 ───
    c52 = verify_corollary52(k, n, temporal_core)

    r = C_N_online / c_star_N if c_star_N > 1e-9 else None

    return {
        'n': n, 'pattern': pattern, 'seed': seed,
        'C_N_online': round(C_N_online, 4),
        'c_star_N': round(c_star_N, 4),
        'r': round(r, 4) if r else None,
        'temporal_core': temporal_core,
        'temporal_epsilon': round(t_eps, 6) if t_eps is not None else None,
        'lemma51_match_rate': round(lemma51_rate, 6) if lemma51_rate is not None else None,
        'lemma52_is_sequential': is_sequential,
        'lemma52_N_i_not_in_F': N_i_not_in_F,
        'min_delta': round(t5['min_delta'], 6),
        'r_double_star': round(t5['r_double_star'], 6) if t5['r_double_star'] else None,
        'theorem5_applicable': t5.get('theorem5_applicable', True),
        'theorem5_predicted_empty': t5['predicted_empty'],
        'theorem5_actual_empty': t5['actual_empty'],
        'theorem5_correct': t5['theorem5_correct'],
        'k': c52['k'],
        'cor52_safe_predicted': c52['cor52_safe_predicted'],
        'cor52_actual_safe': c52['cor52_actual_safe'],
        'cor52_correct': c52['cor52_correct'],
    }


def _worker(args):
    return validate_single(*args)


# ─── Main ───

def main():
    df_summary = pd.read_csv(os.path.join(RESULTS_DIR, 'summary.csv'))
    instances = list(zip(df_summary['n'], df_summary['pattern'], df_summary['seed']))

    results = []
    errors = []
    total = len(instances)

    print(f"=== Theory Validation ===")
    print(f"Total instances: {total}")
    print(f"{'n':>3} {'pat':>3} {'seed':>4} {'L51':>6} {'L52seq':>6} {'L52NiF':>6} "
          f"{'minδ':>8} {'r**':>7} {'T5pred':>6} {'T5act':>6} {'T5ok':>4} "
          f"{'k':>3} {'C52p':>4} {'C52ok':>5}")
    print("-" * 95)

    for idx, (n, pattern, seed) in enumerate(instances):
        try:
            pool = multiprocessing.Pool(1)
            async_result = pool.apply_async(_worker, ((n, pattern, seed),))
            m = async_result.get(timeout=120)
            pool.terminate()
            pool.join()

            results.append(m)

            l51 = f"{m['lemma51_match_rate']:.3f}" if m['lemma51_match_rate'] is not None else "skip"
            l52s = str(m['lemma52_is_sequential'])[:5]
            l52n = str(m['lemma52_N_i_not_in_F'])[:5]
            md = f"{m['min_delta']:.4f}"
            rds = f"{m['r_double_star']:.4f}" if m['r_double_star'] else "N/A"
            t5p = str(m['theorem5_predicted_empty'])[:5]
            t5a = str(m['theorem5_actual_empty'])[:5]
            t5ok = "✓" if m['theorem5_correct'] else "✗"
            kk = str(m['k'])
            c52p = str(m['cor52_safe_predicted'])[:4]
            c52ok = "✓" if m['cor52_correct'] else "✗"

            print(f"{n:>3} {pattern:>3} {seed:>4} {l51:>6} {l52s:>6} {l52n:>6} "
                  f"{md:>8} {rds:>7} {t5p:>6} {t5a:>6} {t5ok:>4} "
                  f"{kk:>3} {c52p:>4} {c52ok:>5}  [{idx+1}/{total}]")

        except Exception as e:
            try:
                pool.terminate()
                pool.join()
            except:
                pass
            err_msg = f"[{n}_{pattern}_{seed}] {str(e)}"
            errors.append(err_msg)
            print(f"{n:>3} {pattern:>3} {seed:>4}  ERROR: {str(e)[:50]}  [{idx+1}/{total}]")

    # Save
    if results:
        df_out = pd.DataFrame(results)
        out_path = os.path.join(RESULTS_DIR, 'theorem5_validation.csv')
        df_out.to_csv(out_path, index=False)
        print(f"\n=== Saved to {out_path} ===")
        print(f"Total: {len(results)} completed, {len(errors)} errors")

    if errors:
        err_path = os.path.join(RESULTS_DIR, 'validation_errors.log')
        with open(err_path, 'w') as f:
            for e in errors:
                f.write(e + "\n")
        print(f"Errors logged to {err_path}")

    # ─── Step 3: 결과 요약 ───
    if results:
        df = pd.DataFrame(results)
        print("\n" + "=" * 60)
        print("Theory Validation Results")
        print("=" * 60)

        # Lemma 5.1
        l51 = df.dropna(subset=['lemma51_match_rate'])
        if len(l51) > 0:
            print(f"\nLemma 5.1 (CW(S)≠∅ ↔ S∈F):")
            print(f"  평균 일치율: {l51['lemma51_match_rate'].mean():.4%}")
            print(f"  완벽 일치: {(l51['lemma51_match_rate'] >= 1.0 - 1e-6).sum()}/{len(l51)}")
            if (l51['lemma51_match_rate'] < 1.0 - 1e-6).any():
                bad = l51[l51['lemma51_match_rate'] < 1.0 - 1e-6]
                print(f"  불일치 인스턴스:")
                for _, row in bad.iterrows():
                    print(f"    n={row['n']} pat={row['pattern']} seed={row['seed']}: {row['lemma51_match_rate']:.6f}")

        # Lemma 5.2
        print(f"\nLemma 5.2 (완전 순차 → N\\{{i}} ∉ F):")
        seq = df[df['lemma52_is_sequential'] == True]
        print(f"  완전 순차 인스턴스 수: {len(seq)}/{len(df)}")
        if len(seq) > 0:
            l52_ok = seq['lemma52_N_i_not_in_F'].mean()
            print(f"  N\\{{i}} ∉ F 검증 정확도: {l52_ok:.1%}")
            if l52_ok < 1.0:
                bad = seq[seq['lemma52_N_i_not_in_F'] == False]
                print(f"  반례: {len(bad)}건")

        # Theorem 5
        print(f"\nTheorem 5 (N\\{{i*}}∈F AND C(N) > c*(N) + min δ_i → Core = ∅):")
        t5_appl = df[df.get('theorem5_applicable', True) == True] if 'theorem5_applicable' in df.columns else df
        t5_pred = df[df['theorem5_predicted_empty'] == True]
        t5_not_appl = len(df) - len(t5_appl) if 'theorem5_applicable' in df.columns else 0
        print(f"  적용 가능 인스턴스: {len(t5_appl)}/{len(df)} (N\\{{i*}}∉F: {t5_not_appl})")
        print(f"  Core 소멸 예측 수: {len(t5_pred)}/{len(df)}")
        print(f"  충분조건 정확도: {df['theorem5_correct'].mean():.1%}")
        if len(t5_pred) > 0:
            t5_acc = t5_pred['theorem5_actual_empty'].mean()
            print(f"  예측=Empty 중 실제=Empty: {t5_acc:.1%} ({int(t5_pred['theorem5_actual_empty'].sum())}/{len(t5_pred)})")

        # Theorem 5 vs Theorem 4
        r_star_vals = pd.read_csv(os.path.join(RESULTS_DIR, 'summary.csv'))['r_star']
        rds = df['r_double_star'].dropna()
        if len(rds) > 0:
            print(f"\n  r** 통계:")
            print(f"    평균 r**: {rds.mean():.4f}")
            print(f"    평균 r* (Theorem 2): {r_star_vals.dropna().mean():.4f}")
            print(f"    r** << r* 확인: r**/r* = {rds.mean()/r_star_vals.dropna().mean():.4f}")

        # By pattern
        print(f"\n  패턴별 Theorem 5 예측:")
        for pat, grp in df.groupby('pattern'):
            pred = grp['theorem5_predicted_empty'].sum()
            act = grp['theorem5_actual_empty'].sum()
            print(f"    {pat}: predicted={int(pred)}, actual_empty={int(act)}, total={len(grp)}")

        # Corollary 5.2
        print(f"\nCorollary 5.2 (k < n-1 → Core 안전):")
        c52_pred = df[df['cor52_safe_predicted'] == True]
        print(f"  k < n-1 인스턴스: {len(c52_pred)}/{len(df)}")
        print(f"  충분조건 정확도: {df['cor52_correct'].mean():.1%}")
        if len(c52_pred) > 0:
            c52_acc = c52_pred['cor52_actual_safe'].mean()
            print(f"  예측=Safe 중 실제=Safe: {c52_acc:.1%} ({int(c52_pred['cor52_actual_safe'].sum())}/{len(c52_pred)})")

        # k distribution
        print(f"\n  패턴별 k 통계:")
        for pat, grp in df.groupby('pattern'):
            print(f"    {pat}: k_mean={grp['k'].mean():.1f}, k_max={grp['k'].max()}, k<n-1 비율={((grp['k'] < grp['n']-1)).mean():.1%}")


if __name__ == '__main__':
    main()

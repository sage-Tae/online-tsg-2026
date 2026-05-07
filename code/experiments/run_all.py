"""전체 실험 자동 실행 스크립트."""

import sys
import os
import traceback
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulator import OnlineTSGSimulator
from src.nucleolus import temporal_nucleolus, static_nucleolus
from src.metrics import compute_metrics
from src.tsp import dist

# ─── 실험 파라미터 ───
SIZES = [5, 7, 10, 12, 15]
SEEDS = [42, 123, 7, 99, 256]
PATTERNS = ['A', 'B1', 'B2', 'B5', 'C', 'D', 'E']
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
RAW_DIR = os.path.join(RESULTS_DIR, 'raw')
ERROR_LOG = os.path.join(RESULTS_DIR, 'errors.log')


def generate_customers(n, seed):
    """랜덤 고객 위치 생성."""
    rng = np.random.RandomState(seed)
    positions = {}
    for i in range(1, n + 1):
        positions[i] = (rng.uniform(0, 10), rng.uniform(0, 10))
    return positions


def generate_arrival_times(n, pattern, positions, seed):
    """도착 패턴별 arrival_times 생성."""
    rng = np.random.RandomState(seed + 1000)
    ids = list(range(1, n + 1))

    if pattern == 'A':
        # 동시 도착
        return {i: 0.0 for i in ids}

    elif pattern.startswith('B'):
        # 순차 도착
        interval = float(pattern[1:])
        return {i: (i - 1) * interval for i in ids}

    elif pattern == 'C':
        # 클러스터 도착 (각도 interleave + 짧은 gap → temporal overlap)
        # 핵심: gap이 짧아야 cross-cluster coalition이 feasible해지고,
        # 각도 interleave로 NN이 zigzag하여 C(N)_online 증가 → Core 소멸
        import math
        depot = (0, 0)
        angles = [(i, math.atan2(positions[i][1] - depot[1],
                                  positions[i][0] - depot[0])) for i in ids]
        angles.sort(key=lambda x: x[1])
        times = {}
        for rank, (cid, _) in enumerate(angles):
            cluster = rank % 2  # 각도 교대 → 공간 interleave
            # gap=2: 짧은 간격 → cluster1 서비스 중 cluster2 도착 → overlap
            times[cid] = cluster * 2.0 + rng.uniform(0, 0.3)
        return times

    elif pattern == 'D':
        # 역순 도착: 각도 교대 zigzag + 적당한 간격
        # 0°, 180°, 60°, 240°, 120°, 300° 순서로 도착 → NN이 반대편 왕복
        import math
        depot = (0, 0)
        angles = [(i, math.atan2(positions[i][1] - depot[1],
                                  positions[i][0] - depot[0])) for i in ids]
        angles.sort(key=lambda x: x[1])
        # zigzag 순서: 0번째, 마지막, 1번째, 마지막-1, ...
        zigzag_order = []
        lo, hi = 0, len(angles) - 1
        while lo <= hi:
            zigzag_order.append(angles[lo])
            if lo != hi:
                zigzag_order.append(angles[hi])
            lo += 1
            hi -= 1
        times = {}
        for rank, (cid, _) in enumerate(zigzag_order):
            times[cid] = rank * 3.0  # 3.0 간격: 이전 고객 서비스 중 다음 도착
        return times

    elif pattern == 'E':
        # 랜덤 도착
        return {i: rng.uniform(0, n * 2) for i in ids}

    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def run_single(n, pattern, seed):
    """단일 인스턴스 실행."""
    positions = generate_customers(n, seed)
    arrival_times = generate_arrival_times(n, pattern, positions, seed)

    # Simulate
    sim = OnlineTSGSimulator(positions, arrival_times)
    sim_result = sim.run()

    # Temporal nucleolus - C(N) = Online 실제 비용 (NN 경로)
    C_N_online = sim_result['C_N']
    t_alloc, t_eps = temporal_nucleolus(
        sim_result['coalition_costs'], C_N_online, sim_result['players']
    )

    # Static nucleolus (skip if n > 8 — LP too slow for 2^n coalitions)
    if n <= 8:
        s_alloc, s_eps, C_N_static = static_nucleolus(
            positions, positions, arrival_times
        )
        static_result = (s_alloc, s_eps, C_N_static)
    else:
        static_result = (None, None, None)

    # Metrics
    metrics = compute_metrics(sim_result, (t_alloc, t_eps), static_result)
    metrics['n'] = n
    metrics['pattern'] = pattern
    metrics['seed'] = seed

    return metrics


def _run_worker(args):
    """multiprocessing worker."""
    n, pattern, seed = args
    return run_single(n, pattern, seed)


def run_single_with_timeout(n, pattern, seed, timeout=60):
    """multiprocessing으로 격리 실행 → CBC hang 방지."""
    import multiprocessing
    pool = multiprocessing.Pool(1)
    try:
        result = pool.apply_async(_run_worker, ((n, pattern, seed),))
        return result.get(timeout=timeout)
    except multiprocessing.TimeoutError:
        pool.terminate()
        raise TimeoutError(f"Timeout after {timeout}s")
    finally:
        pool.terminate()
        pool.join()


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    results = []
    errors = []
    total = len(SIZES) * len(PATTERNS) * len(SEEDS)
    count = 0

    print(f"=== Online TSG Experiment ===")
    print(f"Total instances: {total}")
    print(f"{'n':>3}  {'pat':>3}  {'seed':>4}  {'r':>7}  {'r*':>7}  {'r<r*':>5}  {'T_eps':>10}  {'S_eps':>10}  {'T_core':>6}  {'S_core':>6}  {'Thm2':>5}  {'Thm4':>5}")
    print("-" * 90)

    for n in SIZES:
        for pattern in PATTERNS:
            for seed in SEEDS:
                count += 1
                try:
                    m = run_single_with_timeout(n, pattern, seed, timeout=120)
                    results.append(m)

                    # Print row
                    r_str = f"{m['r']:.3f}" if m['r'] is not None else "N/A"
                    rs_str = f"{m['r_star']:.3f}" if m['r_star'] is not None else "N/A"
                    rvs = m['r_vs_rstar'] if m['r_vs_rstar'] else "N/A"
                    te = f"{m['temporal_epsilon']:.6f}" if m['temporal_epsilon'] is not None else "N/A"
                    se = f"{m['static_epsilon']:.6f}" if m['static_epsilon'] is not None else "N/A"
                    tc = str(m['temporal_core'])
                    sc = str(m['static_core'])
                    t2 = str(m['theorem2_predicts_no_core'])
                    t4 = str(m['theorem4_predicts_safe'])

                    print(f"{n:>3}  {pattern:>3}  {seed:>4}  {r_str:>7}  {rs_str:>7}  {rvs:>5}  {te:>10}  {se:>10}  {tc:>6}  {sc:>6}  {t2:>5}  {t4:>5}  [{count}/{total}]")

                    # Save per-instance
                    pd.DataFrame([m]).to_csv(
                        os.path.join(RAW_DIR, f"{n}_{pattern}_{seed}.csv"), index=False
                    )

                except Exception as e:
                    err_msg = f"[{n}_{pattern}_{seed}] {str(e)}\n{traceback.format_exc()}"
                    errors.append(err_msg)
                    print(f"{n:>3}  {pattern:>3}  {seed:>4}  ERROR: {str(e)[:50]}  [{count}/{total}]")

    # Save summary
    if results:
        df = pd.DataFrame(results)
        summary_path = os.path.join(RESULTS_DIR, 'summary.csv')
        df.to_csv(summary_path, index=False)
        print(f"\n=== Summary saved to {summary_path} ===")
        print(f"Total: {len(results)} completed, {len(errors)} errors")

    # Save errors
    if errors:
        with open(ERROR_LOG, 'w') as f:
            for e in errors:
                f.write(e + "\n---\n")
        print(f"Errors logged to {ERROR_LOG}")

    # ─── 검증 ───
    if results:
        df = pd.DataFrame(results)
        print("\n" + "=" * 60)
        print("=== THEOREM VERIFICATION ===")
        print("=" * 60)

        print(f"\nTotal instances: {len(df)}")

        # Theorem 1: 동시 도착 → F = 2^N (game structure 동일)
        # C(N)_online = C*(N)인 경우에만 Temporal = Static 완전 동치
        t1 = df[df.pattern == 'A']
        t1_valid = t1.dropna(subset=['coalition_reduction_ratio'])
        if len(t1_valid) > 0:
            f_match = (abs(t1_valid['coalition_reduction_ratio'] - 1.0) < 1e-4).mean()
            print(f"\nTheorem 1 (A pattern: F=2^N): {f_match*100:.1f}% ({len(t1_valid)} instances)")
            # r≈1인 경우 epsilon도 일치해야 함
            t1_r1 = t1_valid.dropna(subset=['r', 'temporal_epsilon', 'static_epsilon'])
            t1_r1 = t1_r1[abs(t1_r1['r'] - 1.0) < 0.01]
            if len(t1_r1) > 0:
                eps_match = (abs(t1_r1['temporal_epsilon'] - t1_r1['static_epsilon']) < 1e-3).mean()
                print(f"  Theorem 1+ (A & r≈1 → T_eps≈S_eps): {eps_match*100:.1f}% ({len(t1_r1)} instances)")
        else:
            print("\nTheorem 1: No valid instances")

        # Theorem 2: C_N > sum_individual → Core 소멸
        t2 = df[df.theorem2_predicts_no_core == True]
        if len(t2) > 0:
            accuracy = (~t2['temporal_core']).mean()
            print(f"Theorem 2 (Core 소멸 예측 정확도): {accuracy*100:.1f}% ({len(t2)} instances)")
        else:
            print("Theorem 2: No instances with C_N > sum_individual")

        # Theorem 3: r==1 → static core → temporal core
        t3 = df.dropna(subset=['r'])
        t3_r1 = t3[abs(t3['r'] - 1.0) < 1e-4]
        if len(t3_r1) > 0:
            t3_check = t3_r1[t3_r1['static_core'] == True]
            if len(t3_check) > 0:
                accuracy = t3_check['temporal_core'].mean()
                print(f"Theorem 3 (r=1, static→temporal): {accuracy*100:.1f}% ({len(t3_check)} instances)")
            else:
                print(f"Theorem 3: {len(t3_r1)} instances with r≈1 but none have static core")
        else:
            print("Theorem 3: No instances with r≈1")

        # Theorem 4: r <= r* → safe
        t4 = df[df.theorem4_predicts_safe == True]
        if len(t4) > 0:
            accuracy = t4['temporal_core'].mean()
            print(f"Theorem 4 (r≤r* → Core safe): {accuracy*100:.1f}% ({len(t4)} instances)")
        else:
            print("Theorem 4: No instances with r ≤ r*")

        # 패턴별 Core 존재율
        print(f"\nCore existence rate by pattern:")
        core_rate = df.groupby('pattern')['temporal_core'].mean()
        for pat, rate in core_rate.items():
            cnt = len(df[df.pattern == pat])
            print(f"  {pat}: {rate*100:.1f}% ({cnt} instances)")

        # Coalition reduction
        cr = df.dropna(subset=['coalition_reduction_ratio'])
        if len(cr) > 0:
            print(f"\nCoalition reduction (mean): {cr['coalition_reduction_ratio'].mean():.4f}")
            print(f"  By pattern:")
            for pat, grp in cr.groupby('pattern'):
                print(f"    {pat}: {grp['coalition_reduction_ratio'].mean():.4f}")


if __name__ == '__main__':
    main()

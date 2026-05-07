# Phase 2 — Summary (Task 1: B_{n-3} closure attempt)

Branch: `phase2-experiments`
Working code repo: `../TSG_agent/` (extracted from
`TSG_agent_submission_v2_4_10_20260426.zip`).

## What ran

`code/scripts/near_complement_coverage_check_k3.py` on the 10 NN
near-complement instances. For each instance, the Bondareva–Shapley
balancing LP was solved both at $k=2$ (existing support
$B_{n-1}\cup B_{n-2}$) and at $k=3$ (extended support
$B_{n-1}\cup B_{n-2}\cup B_{n-3}$). The full $k=3$ LP for $n=15$
solves over $15+\binom{15}{2}+\binom{15}{3}=15+105+455=575$
non-negative variables and 15 equality constraints; per-instance
runtime $\approx 25$ s.

## Console transcript

```
  n  pattern    seed         r      rd_k2      rd_k3     mar_k2     mar_k3  fires_k3  |Bn3∩F|    t(s)
--------------------------------------------------------------------------------------------------------------
 10  A           123    1.0529   1.048969   1.048969   0.003928   0.003928       YES      120     1.3
 10  B_heavy     256    1.1261   1.047974   1.047974   0.078150   0.078150       YES      120     0.1
 10  C           123    1.1238   1.048969   1.048969   0.074842   0.074842       YES      120     0.1
 15  A            42    1.0475   1.049458   1.047878  -0.001924  -0.000345       no       455    25.0
 15  A            99    1.0507   1.040182   1.040182   0.010509   0.010509       YES      455    25.5
 15  A           123    1.0749   1.041439   1.040072   0.033422   0.034789       YES      455    25.5
 15  B_heavy       7    1.1849   1.042080   1.042080   0.142814   0.142814       YES      455    25.5
 15  C            42    1.0680   1.049458   1.047878   0.018572   0.020151       YES      455    25.5
 15  C            99    1.1476   1.040182   1.040182   0.107394   0.107394       YES      455    25.3
 15  C           123    1.1406   1.041439   1.040072   0.099114   0.100481       YES      455    25.0
--------------------------------------------------------------------------------------------------------------
Coverage k=2: 9 / 10 cases fire (existing).
Coverage k=3: 9 / 10 cases fire (with B_{n-3}).
```

## Sanity checks vs v2.7.0

- `near_complement_coverage_check_k3.csv` reproduces the v2.7.0
  $k=2$ column verbatim against
  `code/results/near_complement_coverage_check.csv` (the existing
  archive output) — including the seed-42 negative margin $-1.92\times
  10^{-3}$ that motivated this Phase 2 task.
- `c^*(N)$ values match between the new run and the existing CSV
  (e.g. $n=10$ A 123: $c^*=9.949941$; $n=15$ A 42: $c^*=14.088287$).

## Branch outcome

**Branch B** (residual not closed): see `phase2_branch_outcome.md`.

## Files added/modified in this phase

```
TSG_ejor_resubmission_v2_7_0/
├── paper/supplementary_ejor.tex     (single paragraph rewrite in §S4)
├── paper/supplementary_ejor.pdf     (rebuilt; still 13 pages)
├── paper/main_ejor.pdf              (rebuilt without changes; still 30 pages)
├── Phase2_summary.md                (this file)
└── phase2_branch_outcome.md

../TSG_agent/code/
├── scripts/near_complement_coverage_check_k3.py        (new, ~280 lines)
└── results/near_complement_coverage_check_k3.csv        (new, 10 rows)
```

## Deferred

- Phase 2 task 3 (Pattern E n=25 expansion). The archive already
  reproduces v2.7.0's 5-seed Pattern E numbers exactly, so the 25-seed
  expansion is a separate scope and will be run when you give the go.

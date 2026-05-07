# Phase 2 Task 1 — Branch Outcome

## Branch: B (residual NOT closed)

The seed-42 (n=15, Pattern A) instance still fails the strict
inequality $r > r^{(\diamond)}_{\min}$ after the $B_{n-3}$ enlargement,
though the negative margin is tightened ~5.6×.

## Numerical result

| Quantity | k=2 (existing) | k=3 (this work) |
|---|---|---|
| $r^{(\diamond)}_{\min}$ on (n=15, A, seed 42) | 1.049458 | **1.047878** |
| Realized $r$ | 1.047533 | 1.047533 |
| Margin $r - r^{(\diamond)}_{\min}$ | $-1.92\times 10^{-3}$ | $-3.45\times 10^{-4}$ |
| Fires at this case | **No** | **No** |
| Coverage on the 10 near-complement cases | 9 / 10 | **9 / 10** (unchanged) |

The other 9 cases either keep the same $r^{(\diamond)}_{\min}$ value
under the enlargement or become marginally tighter; in no case does
the fires/no-fires classification flip in either direction.

## Implication

- The conjecture stated in supplementary §S4 — that every near-
  complement instance failing $B_{n-1}\cup B_{n-2}$ by less than
  $O(n^{-1/2})$ is closed by $B_{n-1}\cup B_{n-2}\cup B_{n-3}$ — is
  **falsified** for the seed-42 case. The single-step enlargement
  reduces the gap by a factor of ~5.6 but does not close it.
- The seed-42 residual remains uncovered analytically. The first-stage
  Core LP on the full $\mathcal{F}$ still certifies emptiness (the
  observation was always: "Core empty, but no closed-form threshold
  fires on it"), so Core stability claims are unaffected; the open
  problem is purely about analytic certification.

## Paper updates (Branch B)

Per the user's branch-B protocol:

- **No body changes.** All "66 of 67" / "1 near-complement residual"
  language preserved verbatim.
- **§S4 only:** the "Refined open problem" paragraph now reports
  the negative result — what was tested, what closed, what didn't,
  and what remains open ($B_{n-4}$, covering inequality, non-balancing
  certificates).
- Page budgets unchanged: main 30 / supplementary 13.

## Reference artifacts

- Script: `code/scripts/near_complement_coverage_check_k3.py`
- CSV: `code/results/near_complement_coverage_check_k3.csv` (10 rows;
  one per near-complement case, with k=2 and k=3 columns side-by-side)
- Run log: console transcript pasted into `Phase2_summary.md`.

## What is *not* in this commit

- Pattern E n=25 expansion (Phase 2 task 3) — deferred.
- Any change to v2.7.0's headline counts (37 + 11 + 9 + 1 + 9 = 67) or
  to highlights / cover letter / abstract.

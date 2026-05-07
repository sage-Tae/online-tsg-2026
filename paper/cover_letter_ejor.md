# Cover Letter

**To:** Editor-in-Chief\
**Journal:** European Journal of Operational Research\
**Date:** 2026-05-07\
**Re:** New submission — *Online Traveling Salesman Games: Core Fragility and the Temporal Nucleolus under Dynamic Arrivals*

**Authors:**

- Seyun Jeong (Korea Institute of Industrial Technology, Cheonan, Republic of Korea) — jeongsseyyun@kitech.re.kr
- Hyunchul Tae (Korea Institute of Industrial Technology, Cheonan, Republic of Korea) — *corresponding author, sage@kitech.re.kr*

---

Dear Editor,

We submit the enclosed manuscript for consideration as a new
research article in *EJOR*. The paper extends the cooperative
Traveling Salesman Game of Potters, Curiel, and Tijs (1992) to an
online setting in which customers arrive over time, couples the
cooperative-game stability question to the realized dispatch
dynamics, and provides both analytic and computational results.

The topic sits squarely at the intersection of routing and
cooperative game theory, a combination with strong *EJOR* lineage:
the basic Vehicle Routing Game nucleolus is from Göthe-Lundgren,
Jörnsten, and Värbrand (1996, *Mathematical Programming*); the
heterogeneous-fleet extension and the time-window VRG nucleolus
appeared respectively in *Transportation Science* (Engevall et al.
2004) and *Applied Mathematical Modelling* (Tae, Kim, and Park 2020);
the cooperative-TSP rolling-horizon Shapley/Core variants are from
Kimms and Kozeletskyi (2016a, *EJOR*; 2016b, *EURO J. Transp. Logist.*);
and the most recent collaborative-routing cost-allocation paper
(Lyu, Lalla-Ruiz, and Schulte, 2025, *EJOR*) provides the most
direct methodological precedent — row-generation over a static
coalition family, replaced here by a sequential-LP cascade over a
*time-induced* family.

## Core contribution

We introduce the *Online Traveling Salesman Game* $(N, c, \mathcal{F})$,
a cooperative game in which the family $\mathcal{F}$ of feasibility-
admissible coalitions is endogenously induced by the realized
arrival–service process rather than specified exogenously as in
Myerson-style graph-restricted or antimatroid-restricted games. On
this family we define the *Temporal Nucleolus* as the lexicographic
minimizer of excess and compute it by a sequential linear program
over $\mathcal{F}$.

The paper's theoretical contribution is a general partition-pair
certificate (Theorem 14, formerly Proposition 14) for Temporal Core
emptiness, with three a priori computable specializations: the
single-complement threshold $r^{**}$ (Corollary 9, formerly Theorem 9),
the balanced-complement threshold $r^{***}$ (Corollary 10, formerly
Proposition 10), and the balanced-near-complement threshold
$r^{(\diamond)}$ on the mixed collection $B_{n-1}\cup B_{n-2}$
(Corollary 13, formerly Proposition 13). The general theorem
additionally fires on non-singleton partition pairs at $k<n-1$, where
the three specializations are vacuous. A structural obstruction
(Corollary 19): a bounded peak queue $k < n-1$ simultaneously blocks
the three computable specializations but not the partition-pair
mechanism via non-singleton splits. Together the four analytic
thresholds certify 66 of the 67 observed empty Cores in our
175-instance grid (the remaining one near-complement case eludes the
closed-form thresholds by $\approx 2\times 10^{-3}$), with no false
positives across 525 policy-instance pairs (three dispatch policies).
An asymptotic refinement (Theorem 16) ties $r^{**}\to 1$ to the
classical Beardwood–Halton–Hammersley $\sqrt{n}$ scaling of the
Euclidean TSP, and a scale-up to $n=50$ confirms the asymptotic decay.

## Scope and methodological choice

The paper is scoped to a single-vehicle routing game. This is a
deliberate methodological choice — the single-tour setting isolates
the temporal coalition-feasibility structure of $\mathcal{F}$ from
fleet-assignment confounds, and the complement-based arguments rely on
the single-vehicle insertion identity. A multi-vehicle *Online Vehicle Routing Game* extending this framework with capacity constraints is identified as future work in Section 7.

The manuscript has not been published elsewhere and is not under consideration at any other journal.

## Reproducibility

All code, random seeds, and raw CSV results are at
<https://github.com/sage-Tae/online-tsg-2026>. The repository ships
version tags for each iteration in the revision history.
`REPRODUCIBILITY.md` documents the environment, the full 175-instance
main study (Table 4 of the manuscript), the 45-instance scale-up to
$n=50$, and the partition-pair-dual analysis script
`code/scripts/intermediate_dual_analysis.py` used to extract the 9
partition-pair certificates of Supplementary §S9.

## Declarations

- Declaration of interest: The authors declare no competing financial interests or personal relationships that could have influenced this work.
- The work reported has not been published elsewhere, and is not under consideration at any other journal.
- All authors have read and approved this submission.
- We disclose that Claude (Anthropic) was used to assist with language editing and analysis during manuscript preparation, as declared in the manuscript.
- This work was supported by the Korea Institute of Industrial Technology (Grant No. EH-26-0002).

We thank the editorial office in advance for handling this
manuscript and look forward to the reviewers' feedback.

Sincerely,

**Hyunchul Tae**, on behalf of the authors
Korea Institute of Industrial Technology
sage@kitech.re.kr
ORCID: 0000-0002-2277-0722

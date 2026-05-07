# Reproducibility Guide — Online TSG (v2.4.5)

This document describes how to reproduce the empirical results in the paper *"Online Traveling Salesman Games: Core Fragility and the Temporal Nucleolus under Dynamic Arrivals"* (TRSC submission, v2.4.5).

## Submission Identity

- **Version**: v2.4.5 (TRSC re-review pre-submission repair; supersedes the EJOR-track v2.0–v2.2.x and the TRSC-track v2.4.0–v2.4.4)
- **Pages**: `paper/main_trsc.pdf` 35 pages (TRSC manuscript cap), `paper/supplementary_trsc.pdf` 13 pages (≤ 15 cap)
- **Files in submission ZIP**: `paper/main_trsc.pdf`, `paper/supplementary_trsc.pdf` (no separate Highlights file under TRSC convention)
- **Experimental instances**: 596 total
  - Main study: 525 (5 sizes × 7 patterns × 5 seeds × 3 policies)
  - Scale-up: 45 (3 sizes × 3 patterns × 5 seeds × NN)
  - Scale invariance: 24 (sensitivity study, Supplementary Materials §S2)
  - Restricted Core LP certification: 2 seed-123 near-complement cases (Supplementary Materials §S3) under the corrected feasibility family $\F$
  - Partition-pair certification (Proposition 14): 9 intermediate-coalition cases (Supplementary Materials §S8)

## Transportation Science Submission Layout

The paper is submitted in two files per the TRSC manuscript-plus-e-companion convention:

- `paper/main_trsc.pdf` (35 pages) — Manuscript slot.
- `paper/supplementary_trsc.pdf` (13 pages) — E-Companion slot. Contains:
  - §S1 Per-pattern Core-existence breakdown
  - §S2 Scale invariance empirical verification
  - §S3 Restricted Core LP methodology + 10 near-complement / 9 intermediate-coalition case tables + Temporal Nucleolus cascade implementation note
  - §S4 Balanced-near-complement coverage audit (Proposition 13)
  - §S5 Dispatch-policy robustness (NN / CI / BR over 525 policy-instance pairs)
  - §S6 Solomon C101 illustrative example + simultaneous-arrivals reduction
  - §S7 Inheritance of static Core stability
  - §S8 Partition-pair certification of 9 intermediate cases (Proposition 14)
  - §S9 Threshold-distribution histograms

Both files share `references.bib`. The main manuscript references supplementary sections via the `xr` package (`\externaldocument{supplementary_trsc}` and the symmetric declaration in supp). Earlier EJOR-era files (`paper/main.tex`, `paper/supplementary.tex`, `paper/highlights.tex`, `paper/main.pdf`, `paper/supplementary.pdf`, `paper/highlights.pdf`) are retained in the repository for archival reproducibility but are **not** part of the TRSC submission.

## Environment Setup

### Required
- Python 3.9 or later
- LaTeX distribution (TeX Live / MacTeX / MiKTeX) — for compiling the paper

### Python Dependencies

Install via pip:

```bash
pip install -r code/requirements.txt
```

Required packages:
- `numpy`, `scipy`, `pandas`, `matplotlib` (standard scientific stack)
- `pulp>=2.7` (Core LP solver, used in the Supplementary Materials §S3 restricted LP)
- `elkai>=1.2` (LKH TSP solver for n > 15)

## Seeds

All experiments use the seed set `{7, 42, 99, 123, 256}`, declared in `code/src/config.py`. Re-running with the same seeds produces bit-identical numerical results for every aggregate statistic reported in the paper.

## Reproducing Experiments

### 1. Main study (525 policy-instance pairs)

```bash
cd code/experiments
python3 run_main.py --output logs/policy_comparison_v2_full.csv
```

- **Runtime**: ~13 minutes on a laptop.
- **Output CSV columns** (18): n, pattern, seed, policy, L, rho, tau, C_N_online, c_star_N, r, r_star, r_ss, n_feasible, k, core_nonempty, core_epsilon, theorem11_applicable, theorem11_fires.
- **Source for**: Tables 5-7, Section 6.4 strata, all figures (after Step 1.5 augment below).

### 1.5. Augment summary CSV with `r_sss` and `empty_mechanism` columns

`run_main.py` produces 18 columns. Figure regeneration, the 4-mechanism taxonomy, and the Table 6 `r***` column all require two additional columns: `r_sss` (balanced-complement threshold, Proposition 12) and `empty_mechanism` (4-way classification: single / balanced / near / intermediate / core_nonempty). These are computed by a post-processing script that reads and overwrites the same CSV in place:

```bash
cd code
python3 scripts/augment_summary.py
```

- **Input / output**: `code/experiments/logs/policy_comparison_v2_full.csv` (read and overwritten; the script hard-codes this path).
- **Runtime**: ~15 minutes (reruns the simulator for each of 525 rows to recover `coalition_costs` needed for the binding-size classification).
- **Output columns after Step 1.5** (20 total): the original 18 plus `r_sss` and `empty_mechanism`.
- **Required by**: `make_figures_v3.py` (Step 5) and the Supplementary Materials §S3 restricted-LP analysis in `scripts/residual_binding_analysis.py`. Must be run before those downstream steps; idempotent on re-runs.

### 2. Scale-up study (45 instances)

```bash
cd code/experiments
python3 run_scaleup_v2.py
```

- **Runtime**: ~110 minutes (LKH for n ∈ {30, 50}).
- **Output**: `logs/scaleup_v2.csv` covering n ∈ {20, 30, 50} × {A, B_medium, C} × 5 seeds under NN dispatch.
- **Source for**: Table 8 and Section 6.8 findings.

### 3. Scale invariance (24 instances, Supplementary Materials §S2)

```bash
cd code/experiments
python3 run_sensitivity_v2.py
```

- **Runtime**: ~55 minutes.
- **Output**: `logs/sensitivity_v2.csv` with α ∈ {0.5, 1.0, 2.0, 5.0} variants across 6 (n, pattern) configurations.
- **Expected result**: bit-identical r, r**, k within each (n, pattern) group across α.
- **Source for**: Supplementary Materials §S2, Table S1.

### 4. Restricted Core LP certification (2 instances, Supplementary Materials §S3)

```bash
cd code/experiments
python3 run_seed123_check.py
```

- **Runtime**: ~5 hours total for the 2 shipped rows (n=20 seed 123 Pattern A ≈ 1 h, n=30 seed 123 Pattern A ≈ 4 h; both dominated by LKH calls on ~10,000 sampled coalitions each). Requires augmented summary CSV from Step 1.5 for cross-checks.
- **Output**: `logs/seed123_core_check.csv` (2 rows: n=20 and n=30 seed 123 under Pattern A — exactly the Supplementary Materials §S3 Table). TARGETS in the script match this scope.
- **Source for**: Supplementary Materials §S3 "Scale-up certification" 2-row table. The n=50 seed 123 case is analytically covered by Theorem 11 firing directly (Finding 4) and does not require restricted-LP treatment in v2.2.5.
- **Legacy scope**: the v2.1.4-and-earlier 5-entry TARGETS list (adding n=50 seed 123 and two control rows for Theorem-11-fires sanity checks) is preserved at `code/scripts/legacy/run_seed123_check_extended.py`.

### 5. Figures regeneration

```bash
cd code/figures
python3 make_figures_v3.py
```

- **Runtime**: ~10 seconds.
- **Output**: 5 PDF figures in `code/figures/` (`fig2_r_vs_rstar`, `fig3_core_vs_k`, `fig3_core_vs_n`, `fig4_coalition_reduction`, `fig5_rstar_vs_rss`).
- **Input**: `policy_comparison_v2_full.csv` **after Step 1.5 augment** (requires the `r_sss` and `empty_mechanism` columns; running this step on the 18-column raw output will fail).

## Design Framework (N2 Convention)

Customers are sampled uniformly in [0, L]² with **L = √n** (Steele 1997 convention, fixing customer density at 1 per unit area). Vehicle speed is normalized to 1. See Section 6.1 of the paper and `code/src/config.py`.

### Arrival Patterns (ρ-based)

| Pattern | ρ | Interval τ | Structure |
|---------|---|-----------|-----------|
| A | ∞ | 0 | Simultaneous |
| B_heavy | 4.0 | 0.178 | Sequential uniform |
| B_medium | 2.0 | 0.356 | Sequential uniform |
| B_light | 0.5 | 1.425 | Sequential uniform |
| C | 2.0 | 0.356 | Clustered interleave |
| D | 1.0 | 0.712 | Reverse zig-zag |
| E | 1.0 | 0.712 | Poisson random |

where ρ = (L/v)/τ is the dimensionless load parameter and τ = β_BHH / ρ with β_BHH ≈ 0.7124 the Beardwood–Halton–Hammersley constant.

### Scale Invariance

All observables (r, r**, k, Core status) are invariant under the joint rescaling (L, v, τ) → (αL, αv, ατ) for any α > 0. Empirical verification: `r` relative standard deviation = 0.00e+00 across α ∈ {0.5, 1.0, 2.0, 5.0} for all 6 tested configurations (Supplementary Materials §S2, `sensitivity_v2.csv`).

### Near-complement Mechanism

For Pattern A at seed = 123 (n ∈ {20, 30}), Theorem 11 is vacuous (r ≤ r**) yet the Core is empty. Certification via a restricted Core LP over 10,000 sampled coalitions shows binding constraints at sizes both (n-1) and (n-2) simultaneously. See `code/src/core_lp_restricted.py`, `code/experiments/run_seed123_check.py`, and Supplementary Materials §S3.

## Key Source Modules

| File | Role |
|---|---|
| `code/src/config.py` | Design constants (N2, ρ map, seeds, patterns) |
| `code/src/generators.py` | Position and arrival-time generators |
| `code/src/simulator.py` | Online TSG simulator (legacy paths) |
| `code/src/policies.py` | Dispatch policies (NN, cheapest-insertion, batch-reopt) |
| `code/src/policy_simulator.py` | Policy-aware simulator (used by v2 runners) |
| `code/src/nucleolus.py` | Temporal Nucleolus sequential LP |
| `code/src/metrics.py` | Competitive ratio and auxiliary metrics |
| `code/src/tsp.py` | Held–Karp exact TSP for small n |
| `code/src/tsp_scaleup.py` | LKH wrapper (via `elkai`) for large n |
| `code/src/core_lp_restricted.py` | Restricted Core LP (Supplementary Materials §S3) |

## Data Files (v2.2.5)

All in `code/experiments/logs/`:

| File | Rows | Description |
|---|---|---|
| `policy_comparison_v2_full.csv` | 525 | Main study |
| `scaleup_v2.csv` | 45 | Scale-up study |
| `sensitivity_v2.csv` | 24 | Scale invariance verification (Supplementary Materials §S2) |
| `seed123_core_check.csv` | 2 | Near-complement certification (Supplementary Materials §S3; n=20 and n=30 seed 123 under Pattern A — legacy 5-row version at `logs/legacy/seed123_core_check_extended.csv`) |
| `run_main_v2_full.log` | — | Execution log of main study |

Legacy CSVs (`policy_comparison.csv`, `scaleup.csv`, etc.) correspond to the v1.2 submission and are retained for historical reference; they are **not** the basis for v2.2.5's reported numbers.

## Compiling the Paper

Two PDFs must be built: `main_trsc.pdf` (the 35-page manuscript) and `supplementary_trsc.pdf` (the 13-page E-Companion).

```bash
cd paper

# Main manuscript
pdflatex -interaction=nonstopmode main_trsc.tex
bibtex main_trsc
pdflatex -interaction=nonstopmode main_trsc.tex
pdflatex -interaction=nonstopmode main_trsc.tex
pdflatex -interaction=nonstopmode supplementary_trsc.tex

# E-Companion (xr cross-doc requires interleaved second pass)
pdflatex -interaction=nonstopmode supplementary_trsc.tex
bibtex supplementary_trsc
pdflatex -interaction=nonstopmode supplementary_trsc.tex
pdflatex -interaction=nonstopmode main_trsc.tex
pdflatex -interaction=nonstopmode supplementary_trsc.tex
```

Expected output: `paper/main_trsc.pdf` (35 pages) and `paper/supplementary_trsc.pdf` (13 pages), each with 0 errors and 0 undefined references or citations. The xr cross-document references resolve after interleaved main/supp builds.

Required TeX packages: `natbib`, `mathtools`, `multirow`, `enumitem`, `authblk`, `setspace`, `caption`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`, `hyperref`, `xcolor`, `geometry`.

## TRSC Submission

Upload to the INFORMS Editorial system in the following slots:

- **Manuscript**: `paper/main_trsc.pdf` (35 pages; under TRSC's 35-page cap).
- **E-Companion**: `paper/supplementary_trsc.pdf` (13 pages; under TRSC's 15-page cap).
- **Cover letter**: `paper/cover_letter_trsc.pdf`.
- **Source files** (if requested): `paper/main_trsc.tex`, `paper/supplementary_trsc.tex`, `paper/references.bib`, and `code/figures/*.pdf`.

## Submission Verification

Two helper scripts at the repository root guard against regressions between iterations:

```bash
# Clean-room rebuild test: extract ZIP to a tmp dir and verify main_trsc.pdf
# (≤35 pages) and supplementary_trsc.pdf (≤15 pages) all compile with 0
# errors / 0 undef refs / 0 undef cites.
bash scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_11_20260419.zip

# Documentation consistency check: grep-based stale-label sweep over
# README.md and REPRODUCIBILITY.md (version labels outside historical
# context, page counts, seed123 row counts, orphan top-level figures/,
# legacy metric values). Every category must report "(none)".
bash scripts/verify_doc_consistency.sh
```

Both are expected to pass on a clean `v2.2.5` checkout. Use them on every future iteration before tagging a new version.

## Proposition 14 (general partition-pair certificate) reproduction

The new Proposition 14 (introduced in v2_4_3) certifies all 9 NN main-grid intermediate-coalition cases of Observation 15 via dual support of the first-stage Core LP. Reproduction:

```bash
cd code/scripts
python3 intermediate_dual_analysis.py
# Outputs:
#   code/results/intermediate_dual_analysis.json
#   code/results/partition_pair_threshold.json
```

Validates: each of 9 cases admits a feasible partition pair $(S, N\setminus S)$ with both halves in $\F$ such that $r > r^{(P)}_S = [c(S)+c(N\setminus S)]/c^{\ast}(N)$, certifying Core emptiness analytically via Bondareva–Shapley with weights $\lambda_S = \lambda_{N\setminus S} = 1$. Margins (across all 9 cases) range from 0.008 to 0.152.

Reference output (Supplementary §S8 Table):

| n  | pattern   | seed | \|S\| | \|N\\S\| | r     | r^(P)_S | margin   |
|----|-----------|------|-------|----------|-------|---------|----------|
|  7 | B_medium  | 256  | 2     | 5        | 1.436 | 1.428   | +0.008   |
| 10 | B_medium  | 123  | 5     | 5        | 1.423 | 1.384   | +0.039   |
| 10 | B_medium  | 256  | 8     | 2        | 1.358 | 1.313   | +0.045   |
| 10 | E         |  42  | 3     | 7        | 1.495 | 1.484   | +0.012   |
| 12 | B_medium  |  99  | 9     | 3        | 1.395 | 1.284   | +0.111   |
| 12 | B_medium  | 123  | 3     | 9        | 1.487 | 1.354   | +0.133   |
| 12 | B_medium  | 256  | 10    | 2        | 1.423 | 1.271   | +0.152   |
| 12 | E         |  42  | 4     | 8        | 1.610 | 1.561   | +0.049   |
| 15 | B_medium  | 256  | 12    | 3        | 1.326 | 1.300   | +0.026   |

## Version History

- **v2.4.5** (current): TRSC re-review pre-submission repair. Eight categories of edits: (1) 18 supp hardcoded old theorem numbers replaced by `\ref{}` cross-doc to main labels; (2) Table 5 caption "strictly generalises" → "contains ... on the common applicability domain", "recovers Proposition 12" → `\ref{prop:bondareva-complement}`; (3) Abstract compressed 290→280 words and last sentence softened from "operational implication is direct" to "In our synthetic single-vehicle experiments"; (4) Definition 2 "Ex-post, policy-induced character of $\F$" paragraph inserted; (5) Proposition 14 framing tone-down ("four complementary sufficient conditions" → "three complement-family + one unifying partition-pair certificate"; certificate-not-bound clarification; §6.3 dual-support sentence; §7 first paragraph "general partition-pair threshold" → "unifying partition-pair certificate"); (6) Table 7 caption + §7(ii) "certified a priori" replaced by explicit minimum margin 0.0159 with LKH calibration error 0.000% against Held–Karp at $n=15$; (7) "Solver and calibration follows" → "follow", supp title aligned with main title, `code/scripts/intermediate_dual_analysis.py` comments updated; (8) `README.md` and `REPRODUCIBILITY.md` rewritten from EJOR / `main.pdf` basis to TRSC / `main_trsc.pdf` basis. main_trsc.pdf 35 / 35 pages, supplementary_trsc.pdf 13 / 15 pages, 0 ATTENTION boxes, 0 undefined references, 0 cross-doc `??` markers; multiply-defined citation warning of 4 keys is a benign xr/natbib interaction (not a real bib duplication; verified by single `@article` per key in `references.bib`). EJOR-bound 20 files unchanged. No theorem statement, proof, numerical result (37+11+9+1+9 = 67 empty Cores; 9/10 Prop 13 fires; 0 false positives; 525 policy-instance pairs; r̄** = 1.223; r̄*** = 1.096; 3.56× / 3.97× sharpness; 9 partition-pair certificates), figure, or CSV modified.
- **v2.4.4**: Narrative-consistency cleanup after Proposition 14 (4 sites updated to "4 thresholds, 66 of 67"); main 35p / supp 13p preserved.
- **v2.4.3**: R1 Phases C and D — new Proposition 14 (general partition-pair certificate) certifies all 9 intermediate cases; §7 Operational trade-offs paragraph (C2); §7 Limitation (v) Policy-dependence of $\F$ (C4); Limitation (iv) reframed; new analysis script `code/scripts/intermediate_dual_analysis.py`.
- **v2.4.2**: Main → supp demotion (Example 4 / Reduction prop / Inheritance prop / sharpness fig moved to new supp §S6/§S7/§S8); xr cross-doc wired; main 35→33p (saved 2p budget for Phase C/D).
- **v2.4.1**: R1 Phase B (statistical reporting) — Wilson 95% CIs in Table 7; (ρ, structure) factorial rationale in §6.1; Finding 3(b) "Detection-limit warning (n=50 specifically)"; log-log regression slope –0.54, R²=0.99 in §6.8.
- **v2.4.0**: R1 Phase A (critical fixes) — M1–M8 typographic / mathematical / wording fixes (encoding artifact `k<n-1`, singleton-summation, Definition 3 wording, "for sequential arrival regimes", $\rho=L/\tau$ note, abstract caveat).

### Earlier EJOR-track revisions (archived)

- **v1.2** (initial submission): 23 pages, 625 instances, L = 10 coordinate convention.
- **v2.0** (intermediate major revision): 29 pages, 599 instances, N2 convention (L = √n, Steele 1997), near-complement mechanism (Remark + Appendix C), scale invariance verification (Appendix B), pattern re-parameterization to ρ-based taxonomy.
- **v2.1.0** (intermediate; responded to 5 fundamental critiques): 30 pages, §2.5 Restricted Cooperation Games added, Definition 3 proper-subset constraints, over-claim tone-downs, Nucleolus algorithmic details.
- **v2.1.2** (intermediate; post-F-generation fix): 34 pages, corrected feasibility family F via post-hoc reconstruction per paper Definition 2, Proposition 12 (balanced-complement threshold), Observation 15 (intermediate-coalition mechanism), 4-mechanism taxonomy.
- **v2.1.3** (intermediate): 34 pages. Sync fixes: Conclusion and README numerics aligned to v2.1.2 data, Figure 1 caption corrected (broken "Fig None" reference fixed, four-mechanism decomposition explicit), Nucleolus §4.2 algorithmic-details tone-downed to two-tier scope (first-stage LP for Core judgment; simplified cascade for Nucleolus point under non-degeneracy), B_medium nonemptiness claim at n>15 restricted-LP-caveated.
- **v2.1.4** (intermediate): 35 pages. Reproducibility polish: Step 1.5 `augment_summary.py` documented; seed123 CSV aligned with Appendix C (2 rows; 3 legacy rows retained untracked); §6.8 Summary tone-down.
- **v2.1.5** (intermediate): 35 pages. Scale-up near-complement scope aligned across paper/script/CSV. Finding 4 rewritten as a two-tier pattern (restricted LP at n=20, 30; Theorem 11 fires directly at n=50), consistent with Theorem 14's $O(n^{-1/2})$ tightening. `run_seed123_check.py` TARGETS reduced from 5 to 2 to match Appendix C (legacy 5-entry version retained at `code/scripts/legacy/run_seed123_check_extended.py`).
- **v2.1.6** (intermediate): 35 pages. Submission-ZIP rebuildability fix. `paper/main.tex` `\graphicspath` extended from `{../figures/}` to `{../figures/}{../code/figures/}` so that a clean-room extraction of the submission ZIP — which ships `paper/` and `code/figures/` but not a top-level `figures/` symlink — compiles without `! LaTeX Error: File ... not found`. `REPRODUCIBILITY.md` Data-Files table `seed123_core_check.csv` row corrected from `5` to `2` to match Appendix C and the shipped CSV. `scripts/verify_zip_rebuild.sh` added as an automated clean-room rebuild check (extract ZIP to tmp → 3-pass LaTeX → verify 35 pages). No theoretical, experimental, or figure changes.
- **v2.1.7** (intermediate): 35 pages. Documentation semantic-sweep consistency pass. `REPRODUCIBILITY.md` §4 heading "Restricted Core LP certification (5 instances, Appendix C)" corrected to "(2 instances, Appendix C)" — the last residual `5 instances` label from the v2.1.2 scope, which had survived prior line-local fixes because it lived in a section heading rather than body text. `README.md` header current-version label bumped to v2.1.7, version history appended, and `Reproducibility tags` section updated so that the `(current, major revision)` marker follows the active tag rather than `v2.1.2`. Both files given an end-to-end semantic review rather than a pattern-local edit. `scripts/verify_doc_consistency.sh` added: automated stale-label grep check (version labels / page counts / seed123 row counts / orphan top-level `figures/` / stale metrics) so that future iterations fail loudly at the same class of issue. No theoretical, experimental, figure, CSV, or paper-source changes.
- **v2.1.8** (intermediate): main manuscript 30 pages (EJOR-compliant), Supplementary Materials 6 pages. EJOR 30-page compliance split: the three appendices (per-pattern Core-existence, scale-invariance verification, restricted Core LP methodology + classification tables) are moved out of `main.tex` into a new `paper/supplementary.tex` (sections §S1, §S2, §S3). Main-body references rewritten as `Supplementary Materials §S1–§S3` and `Supplementary Figure/Table S*`. §6.8 gains a one-paragraph self-contained summary of the restricted-LP methodology so the main manuscript does not depend on the supplement to explain its scale-up certifications. §2 Related Work consolidated from five subsections to three (Static+Dynamic merged; Online+Nucleolus merged; Restricted Cooperation kept) and bibliography `\bibsep` compressed so the references fit on page 30. `scripts/verify_zip_rebuild.sh` extended to build and validate both `main.pdf` (≤30 pages hard cap) and `supplementary.pdf`. Theorem/Proposition/Corollary/Remark/Observation statements and proofs are unchanged; experimental CSVs and figure PDFs are unchanged bit-for-bit.
- **v2.1.9** (intermediate): main manuscript 30 pages, Supplementary Materials 6 pages. EJOR desk-check compliance pass. Abstract rewritten (formula-free, theorem-reference-free, all abbreviations defined on first use, 238 words — within the 50–250 EJOR band). Keywords trimmed from 7 to 5, one of them from the EJOR official list (Routing). `code/figures/make_figures_v3.py` Figure 2 caption text corrected from "see Appendix C" to "see Supplementary Materials S3" (the last Appendix-era reference lingering in a figure PDF); Figure 2 regenerated. `REPRODUCIBILITY.md` Data-Files table pruned of four unshipped-log rows (only the main-study execution log is shipped) and the Design-Documents section removed (three internal working files were being listed but are not in the submission ZIP). Theorem statements, CSV data, and Python source unchanged.
- **v2.1.10** (intermediate): main manuscript 30 pages, Supplementary Materials 6 pages, Highlights 1 page. EJOR Highlights desk-check compliance + package polish. Highlights moved from an in-manuscript `\section*{Highlights}` block into a new standalone `paper/highlights.tex` / `paper/highlights.pdf`, with a plain-text `paper/highlights.txt` for Editorial-Manager paste-in; five bullets, each ≤ 85 characters, formula-free and with no undefined abbreviations. The old in-manuscript Highlights (which contained four math-mode bullets and two undefined abbreviations) is removed from `main.tex` — the document now starts at the Abstract. Active-text "Appendix B" / "Appendix C" references in `REPRODUCIBILITY.md` are replaced by "Supplementary Materials §S2" / "§S3" (historical-block refs in Version History are kept). README.md repository-tree updated to drop `phase1_design.md` and `phase3_narrative.md` (both internal working files, not shipped), and the paper title plus BibTeX `title` in the Citation block are synced to the current paper title. `scripts/verify_zip_rebuild.sh` extended to build and validate a third PDF (`highlights.pdf`) alongside the main and supplementary. No theoretical, experimental, CSV, or figure-data changes.
- **v2.1.11** (intermediate): main manuscript 30 pages, Supplementary Materials 7 pages, Highlights 1 page. Response-to-weaknesses revision. (T1.1) Static-reduction "Theorem 6" downgraded to Proposition 6, static-Core-inheritance "Theorem 18" downgraded to Proposition 18; labels `thm:static-equiv` and `thm:core-inheritance` preserved for cross-reference compatibility. (T1.3) Example 4 (Solomon C101) cleaned of the illustrative "≈1.81" numerical value, since $r^{\ast\ast}$ is undefined there (empty-minimum convention). (T1.4) §6.8 Finding 3 and §7(ii) rewritten with an explicit split between (a) the analytic structural claim that Corollary 19 ($\bar k<n-1$) blocks both complement-based mechanisms and (b) a one-sided empirical observation (no intermediate-coalition violation detected in the sampled restricted LP), together with a detection-limit caveat quantifying per-draw miss probability at $n=20,30,50$. (T1.5) Five new citations in §2: Klijn & Slikker (2005), Platz & Hamers (2015), Özener & Ergun (2008), Drechsel & Kimms (2010), Özener, Ergun & Savelsbergh (2013). (T1.6) Theorem 16's "uniformly over arrival patterns" clause explicitly scoped to the subclass where $\{i: N\setminus\{i\}\in\mathcal{F}\}$ is non-empty. (T1.7) Remark 17's depot-position constant made explicit: universal constant in $[1,4]$ between corner (sector angle $\pi/2$) and interior (sector angle $2\pi$) placements, with $O(n^{-1})$ rate unchanged. (T2.1) Remark 14 kept as-is; the balanced-near-complement sufficient condition is documented as an open problem in Supplementary §S4 with the clean Bondareva--Shapley formulation. (T2.2) Detection-limit quantification integrated into §6.8 Finding 3 and caveat. (Tier 3) Online VRG added as a future-work paragraph in §7 noting that the single-vehicle insertion identity underlying $r^{\ast\ast}$ does not immediately generalize. Bibliography set to `\footnotesize` with reduced `\bibsep` so main fits within the 30-page cap. No CSVs, figures (except Fig. 2 regenerated for audit), or `src/` files touched.
- **v2.1.12** (intermediate): main manuscript 30 pages, Supplementary Materials 7 pages, Highlights 1 page. Reference-accuracy patch against `docs/v2_1_11_verification_report.md` items V2.1 and V2.4 (both FAIL). **P1:** The Klijn & Slikker (2005) "Sequencing games with non-linear cost functions" reference added in v2.1.11 is a hallucinated entry — DBLP's TOC for *Mathematical Methods of Operations Research* vol 62 issue 1 (Sept 2005) contains no paper by these authors with that title; Klijn and Slikker have no joint 2005 publication. The bib entry is deleted from `paper/references.bib` and the single citing sentence in §2.2 is removed; no substitute citation is added. Adjusted §2 citation count: five new refs in v2.1.11 → four retained. **P2:** The Drechsel & Kimms (2010) reference had the correct title/authors/year but the wrong venue. The real paper is in *International Journal of Production Economics*, vol 128, no 1, pp. 310–321, November 2010 (ScienceDirect pii S0925527310002689). The bib entry's `journal`, `volume`, `number`, and `pages` fields are corrected; the bib-key `drechsel2010computing`, authors, title, year, and the in-text `\citet{drechsel2010computing}` citation in §2.2 are unchanged. No theoretical, experimental, numerical, figure, CSV, or `src/` changes. Pages: main.pdf 30 (unchanged), supplementary.pdf 7 (unchanged), highlights.pdf 1 (unchanged).
- **v2.2.0** (intermediate): main manuscript 30 pages, Supplementary Materials 8 pages, Highlights 1 page. New theorem. The v2.1.11 Supplementary §S4 conjecture is promoted to **Proposition~15 (Balanced-near-complement threshold)** in main manuscript §5.1: under $\mathcal{F}\supseteq B_{n-1}\cup B_{n-2}$, if there exist non-negative weights $\{\lambda_S\}$ with $\sum_{S\ni i}\lambda_S = 1$ for every $i\in N$ such that $r > (\sum_S \lambda_S\,c(S))/c^{\ast}(N)$, then the Temporal Core is empty. Proof-sketch is inline in main.tex; the full proof lives in Supplementary §S4 together with the empirical coverage audit. The coverage audit (`code/scripts/near_complement_coverage_check.py`, output `code/results/near_complement_coverage_check.csv`) solves the sharpest-threshold balancing LP on each of the 10 observed NN near-complement main-grid cases; the proposition fires on 9/10, with a single residual ($n=15$, Pattern~A, seed 42) falling short by $\approx 2\times 10^{-3}$ and deferred to a refined open problem in §S4. Table~5 is extended to a five-row decomposition: 37 single + 11 balanced + 9 balanced-near + 1 near-complement-residual + 9 intermediate = 67 empty. Abstract, §1 (C2, C4), §5.1, §5.2 Corollary 19, §6.4, §6.8 Summary, and §7 Conclusion all updated to reference the three-threshold (instead of two-threshold) structure. Numbering shift inside §5: Observation 15 → 16, Theorem 16 → 17, Remark 17 → 18, Proposition 18 → 19, Corollary 19 → 20; main-text cross-references via `\ref{}` auto-update; three literal "Observation~15" strings in supplementary.tex corrected to "Observation~16". No CSVs touched. One new analysis script added under `code/scripts/` (read-only, does not modify `code/src/` or `code/experiments/`). Bibliography compressed to `\scriptsize` with `\bibsep = 0pt plus 0.1ex` to preserve the 30-page cap. Reproducibility: the coverage audit takes ~75 s on the 10 cases (dominated by Held–Karp at $n=15$).
- **v2.2.1** (intermediate): main manuscript 30 pages, Supplementary Materials 8 pages, Highlights 1 page. Documentation-consistency patch against the v2.2.0 verification report (`docs/v2_2_0_verification_report.md` items W3.c FAIL and W7 WARN). **P1:** Three `paper/main.tex` paragraphs still used the pre-v2.2.0 "both complement-based mechanisms" language after Proposition 15 was added — §6.4 "Analytic sharpness of Corollary 20" (line 546), §6.8 Finding 3(a) (line 719), and §7 Platform-design implication (line 741). Each is rewritten to list all three complement-based mechanisms that Corollary 20 blocks when $k<n-1$: Theorem 11 (single-complement), Proposition 12 (balanced-complement), and Proposition 15 (balanced-near-complement). The underlying logic is unchanged (Corollary 20's statement and proof already listed all three; only the prose in these three paragraphs was stale). **P2:** The phrase "near-miss" appeared once in `docs/v2_1_12_to_v2_2_0_response.md` and once in `docs/phase2_option1_log.md`; both replaced with the neutral "failing the strict inequality by approximately $2\times 10^{-3}$" to match the paper's own phrasing. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file.
- **v2.2.2** (intermediate): main manuscript 30 pages, Supplementary Materials 8 pages, Highlights 1 page. EJOR submission-polish patch — presentation only, no new results. **T1 (Abstract / Highlights / Intro consistency sweep):** `paper/highlights.tex` and `paper/highlights.txt` bullet 4 updated from "both complement-based mechanisms" to "all three complement-based mechanisms" (still ≤ 85 chars, formula-free). §1 Practical-implication parenthetical updated to list Proposition 15 alongside Theorem 11 and Proposition 12. Abstract and C2/C4 were already current from v2.2.0 and required no change. **T2 (defensive single-vehicle scope demarcation):** §7 "Broader directions" paragraph rewritten to frame the single-vehicle scope as a deliberate methodological choice isolating the temporal coalition-feasibility structure of $\mathcal{F}$ from fleet-assignment confounds, announcing an Online VRG companion manuscript. §1 Structure paragraph gained a one-sentence scope note upfront. **T3 (cover letter):** `paper/cover_letter.md` drafted for the EJOR submission portal (579 words, addressed to Prof. Słowiński; author-side placeholders for submission date / e-mail / ORCID). **Page budget:** one redundant "secondary point" sentence in §6.6 Sharpness trimmed to keep `main.pdf` at 30 pages. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file.
- **v2.2.3** (intermediate): main manuscript 30 pages (target; rebuild was deferred), Supplementary Materials 8 pages, Highlights 1 page. External-critique polish — literature additions + minor scope notes; no new results, no numerical changes. **P1 (Lyu, Lalla-Ruiz & Schulte 2025, *EJOR* 323(3):888–906):** bib entry `lyu2025collaborative` added; one sentence added to §2.1 framing their row-generation approach to the collaborative berth allocation problem as a static coalition family contrasted with our arrival-dynamics restriction. **P2 (Chen, Wang & Meng 2023, *TR-B* 173:119–141):** bib entry `chen2023cost` added; one short sentence added to §2.1 flagging their autonomous-truck-platooning cost-allocation study as a related dynamic-vehicle cooperative game application. **P3 (van Zon, Spliet & van den Heuvel 2021, *Transportation Science* 55(1):179–195):** bib entry `vanzon2021joint` added; one sentence added to §2.2 describing the Joint Network Vehicle Routing Game's row-generation algorithm as the closest static-coalition-family methodological precedent to our sequential-LP cascade over the time-induced $\mathcal{F}$. (The external critique's R3 originally cited "The effect of algorithm capabilities on cooperative games" as an Erasmus EI2021-02 working paper; the verification report replaced that with the correctly-titled published JNVRG paper.) **P4 (Theorem 17 scope note):** one sentence added after the proof of Theorem 17, noting that the uniform-i.i.d. hypothesis extends to general absolutely continuous distributions (including clustered patterns) via the Steele (1997) limiting-functional framework, with the hidden constant then density-dependent. **P5 (Goyal orthogonality):** the existing `\citet{goyal2025temporal}` sentence in §2.2 is expanded by one sentence making the orthogonality explicit — their worth $v(\pi)$ is sequence-indexed with the full power-set coalition structure, whereas ours is set-valued $c(S)$ on a time-restricted family $\mathcal{F}$. **P6 (abstract mild softening):** the abstract's final sentence changed from "short service windows plus informed dispatch preserve Core stability" to "short service windows plus informed dispatch substantially improve Core stability in our experiments" — matching the observational (not theoretical) scope of the claim. **Page-budget offsets:** one sentence in §5.3 Discussion ("In the language of queueing theory...") compressed from ~85 words to ~35 words; the last sentence of §6.6 Sharpness ("Note that $r^{\ast\ast\ast}$ averages across complements...") removed. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file.
- **v2.2.4** (intermediate): main manuscript **31 pages** (1 over the EJOR 30-page cap), Supplementary Materials 8 pages, Highlights 1 page. Reference-accuracy patch on top of v2.2.3 + first full PDF rebuild (pdflatex / bibtex / pdflatex / pdflatex for `main.tex` and `supplementary.tex`; two pdflatex passes for `highlights.tex`; TeX Live 2026). **P1 (van Zon first-author given-name correction):** `paper/references.bib` entry `vanzon2021joint` has `author = {van Zon, Mart{\'\i}n and ...}` corrected to `author = {van Zon, Mathijs and ...}`. The first author's given name is "Mathijs" per INFORMS DOI 10.1287/trsc.2020.1008 and the RePEc listing (`ideas.repec.org/p/ems/eureir/115273.html`); "Mart{\'\i}n" in v2.2.3 was a hallucination. Under `plainnat` the in-text citation is "van Zon et al. (2021)" regardless (given names are not printed), so no prose edit was needed. **P2 (PDF rebuild — main.pdf overflow flagged).** `supplementary.pdf` = 8 pages (on-spec), `highlights.pdf` = 1 page (on-spec), `main.pdf` = 31 pages (1 over cap). The v2.2.3 §5.3 / §6.6 trims were therefore insufficient rather than overkill and are retained as-is. The 1-page overflow is a structural artifact of v2.2.3's six prose additions net of the two trims (net ~+50 words in the v2.2.3 response document, in practice rendered as +1 page under TeX Live 2026's line-breaking). Further ~50-word trimming outside the protected regions (Proposition 15, its proof, §S4, Theorems, Table 5) is deferred to the author's judgement; this iteration is a minimal reference-accuracy patch only and does not perform additional prose trimming. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file. Restore locally via `git checkout v2.2.4`.
- **v2.2.5** (current): main manuscript **30 pages** (EJOR-compliant), Supplementary Materials 8 pages, Highlights 1 page. 1-page overflow fix on top of v2.2.4. Three localized minimal edits, applied in Tier 1 → Tier 2 → Tier 3 order and stopping at the first tier whose rebuild achieved the 30-page target. **Tier 1 (§2.1, Chen et al. 2023 removal):** the v2.2.3 P2 sentence "Related dynamic-vehicle cooperative game applications include cost allocation in autonomous truck platooning \citep{chen2023cost}." was removed from `paper/main.tex` and the `chen2023cost` entry was removed from `paper/references.bib`. Rebuild: 31 pages — insufficient. **Tier 2 (two small overfull-hbox tightenings):** §3.1 line 164 — the trailing clause ", since the online policy must commit to visits without seeing future arrivals" was removed (already stated earlier in the same paragraph as "because the online policy cannot anticipate future arrivals"), and §7(i) line 745 — "dispatch policies" → "policies" (the word "dispatch" is redundant in the Dispatch-policy limitation paragraph). Rebuild: still 31 pages. **Tier 3 (§2.2 Goyal orthogonality compression):** the v2.2.3 P5 expansion "The two frameworks are complementary: their worth $v(\pi)$ is a function of the realized arrival sequence $\pi$ while the coalition structure remains the full power set, whereas our Online TSG keeps the characteristic function $c(S)$ set-valued (matching the static TSG exactly) and restricts the coalition family to $\F$ induced by the arrival--service process." was compressed to "Their worth $v(\pi)$ depends on the arrival sequence while coalitions remain unrestricted; our $c(S)$ is set-valued but coalitions are restricted to $\mathcal{F}$, an orthogonal axis of temporality." (58 → 33 words). Rebuild: **30 pages — target achieved**. Lyu et al. 2025 and van Zon et al. 2021 citations retained. `supplementary.pdf` and `highlights.pdf` unchanged at 8 pages and 1 page respectively. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file. Restore locally via `git checkout v2.2.5`.

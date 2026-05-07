# Online Traveling Salesman Games

Code and data for the paper:

> **Online Traveling Salesman Games: Core Fragility and the Temporal Nucleolus under Dynamic Arrivals**
> Seyun Jeong and Hyunchul Tae (Korea Institute of Industrial Technology)
> Submitted to *Transportation Science* (INFORMS), 2026

**Current version: v2.7.0** (External-review compliance, 2026-05-07)

Version history (EJOR-track current; earlier TRSC-track entries below):
- v2.7.0 (current, external-review compliance): eight technical/correctness/formatting fixes from a pre-submission external review. No theorem/proposition number changes.
  - F1 (CRITICAL typo): Table 1 r*** definition corrected to match Proposition 10's proof — $\sum_i c(N\setminus\{i\}) / [(n-1)\,c^*(N)]$ (the previous $1+\sum\delta_i/[(n-1)c^*(N)]$ form is not equivalent in general; equivalence requires $r^*=1$).
  - F2 (definition consistency): §6.1 ρ redefined as $\beta_{\text{BHH}}/\tau$ (per-customer characteristic edge / inter-arrival), making $\tau = \beta_{\text{BHH}}/\rho$ self-consistent under the $L=\sqrt{n}$ convention. Previous "$\rho = L/\tau$" was inconsistent with the pattern generation rule.
  - F3 (claim precision): §6.6, §7(i), §7(v) "policy-independent" claims separated into geometric (policy-independent: $c(\{i\})$, $c(N\setminus\{i\})$, $c^*(N)$) vs F-dependent minima (policy-dependent: $r^{**}$, $r^{(P)}_{\min}$ applicability and values).
  - F4 (EJOR title-page): full postal address with postal code 31056 added to KITECH affiliation.
  - F5 (Elsevier highlights ≤85 chars): bullets 3 and 5 trimmed (was 86 chars each); all five now ≤83.
  - F6 (text precision): §4.3 duplicate "proper generalization" sentence removed; §5.3 "vacuously satisfied" → "hypothesis vacuous, theorem inapplicable"; §5.3 "near-complement violations remain possible at k<n-1" corrected — near-complement requires $B_{n-1}\subseteq\F$, hence is also blocked at k<n-1; only intermediate-coalition violations remain.
  - F7 (supplementary precision): §S3 parenthetical reworded — the previous "true restricted Core is a subset of the unrestricted Core" was confusing; replaced with the correct relaxation argument (sampled LP drops constraints, never adds them, so positive ε* on sample certifies emptiness on the full restricted set one-sidedly).
  - F8 (cover letter): TS desk-rejection paragraph removed; "companion manuscript in preparation" softened to "future work" in cover letter and at 3 sites in main_ejor.tex (§1 "Why single vehicle", §1 Structure paragraph, §7 Scope demarcation).
  - Page-budget offsets: §6.6 trailing F-dependence clause shortened, §7(iii) "(Suppl.~§S4)" parenthetical removed, to absorb the F2/F3 added precision and stay within the 30p cap.
  - Build outcome: `main_ejor.pdf` = **30 pages (EJOR cap met)**, `supplementary_ejor.pdf` = 13 pages, `cover_letter_ejor.pdf` ≤ 2 pages, all unresolved-ref-clean. Theorem 9, Theorem 16, Propositions 10, 13, 14, Observation 15, Corollaries 11, 19, and Remarks 5, 12, 17, 18 all preserved.
- v2.6.2 (submission-date alignment): all submission-facing dates set to 2026-05-07. No content changes.
  - `cover_letter_ejor.md`: Date `2026-05-02` → `2026-05-07`; `cover_letter_ejor.pdf` rebuilt via pandoc.
  - `main_ejor.tex` / `supplementary_ejor.tex`: `\date{\today}` hardcoded to `\date{May 7, 2026}` for build stability.
  - `Declaration_of_Interests.docx`: signing date `May 6, 2026` → `May 7, 2026` (2 occurrences, patched in-place via `word/document.xml`).
  - `main_ejor.pdf` and `supplementary_ejor.pdf` rebuilt; page counts unchanged (30p, 13p); page-1 date renders as `May 7, 2026`.
  - `REVISION_NOTES.md` and `docs/v2_5_0_to_v2_5_1_response.md` historical dates left unchanged (work-history records).
- v2.6.1 (EJOR-track minor revision): page trim 32→30p (EJOR cap met), no theorem/proposition/table changes. Substance preserved on the v2.6.0 C1–C6 paragraphs.
  - T0: Cover letter `Corollary 18` → `Corollary 19` (one-token fix); `cover_letter_ejor.pdf` regenerated via pandoc.
  - T1: §7 Limitations (i)–(iv) tightened to 1–2 sentences each (item v already short); ~12 source lines saved.
  - T2: §6.4 "Three patterns stand out" + "secondary observation" paragraphs collapsed into a single regime-level paragraph (per-pattern detail still in Table~6); ~10 source lines saved.
  - T3: §6.7 Finding 4 collapsed from 2 bullets + closing paragraph into one paragraph; the asymptotic-transition narrative absorbed into Suppl §S3 (one extra sentence on the Pattern A near-complement scale-up paragraph). Suppl page count unchanged at 13p.
  - T4: §6.3 five-way decomposition five bullets compressed to single paragraph; Table~4 unchanged.
  - T5: §6.7 "Intractability of Pattern A at n≥30" paragraph compressed from ~10 lines to 4 lines.
  - T6: §6.4 "Load parameter ρ alone does not determine" paragraph compressed (~3 lines saved).
  - Additional trims to hit 30p: Operational trade-offs (§7) tightened; Scope demarcation (§7) cross-references the new §1 "Why single vehicle" instead of restating; Findings 1 and 2 in §6.7 modestly trimmed; Detection-limit warning (§6.7) and Summary (§6.7) deduplicated; Table~3 hierarchy caption tightened; §5.1 Computability paragraph tightened.
  - Build outcome: `main_ejor.pdf` = **30 pages (EJOR cap met)**, `supplementary_ejor.pdf` = 13 pages, both unresolved-ref-clean. Theorem 9, Theorem 16, Propositions 10, 13, 14, Observation 15, Corollary 19, and the v2.6.0 numbering (Remark 17 = asymptotic-scope, Remark 18 = asymptotic-tighter) all preserved. No table or figure changed.
- v2.6.0 (EJOR-track major revision): six pre-submission critique points addressed (page-cap deferred; trimming in v2.6.1).
  - C0: Supplementary build repair — xr cross-references already wired in v2.5.0 preamble; verified ?? count 0 in `supplementary_ejor.pdf`.
  - C1: Theorem 16 applicability subclass paragraph (before statement) and post-statement Remark added; sequential-regime exclusion (Bmedium / Blight / D) made explicit at theorem level. Numbering shift inside §5: new Remark 17 inserted; old Remark 17 (`rem:asymptotic-tighter`) → 18, Corollary 18 (`cor:cor52`) → 19 (all via automatic `\ref{}`). Theorem 9, Theorem 16, and Proposition 14 numbers preserved.
  - C2: §5.1 Computability paragraph distinguishing a priori (r∗∗, r∗∗∗) from post-hoc (r^(⋄), r^(P)) thresholds; Table 1 (Notation) annotated with computability tags and a new r^(P)_min row.
  - C3: Table 7 footnote § strengthened with per-n joint-detection breakdown; §6.7 Summary paragraph reframes the n=50 sampled-LP companion as a placeholder; only Corollary 19 structural blocking carries asymptotic strength at n=50.
  - C4: §1 "Why single vehicle" paragraph added between Research-question and Contributions — multi-vehicle insertion-identity failure made explicit (cross-references the §7 Online VRG demarcation already in v2.5.0).
  - C5: New threshold hierarchy table at §5.1 head (`tab:threshold-hierarchy`, Table 3) summarizing the five mechanisms with hypothesis, computability, and sharpness columns.
  - C6: Pattern E footnote on intra-pattern stochasticity added in §6.1; sd values (0.169 for r, 0.139 for r∗∗) cross-referenced to Table 6 Pattern E row.
  - Build outcome: `main_ejor.pdf` = 32 pages (estimated 1–2p over the EJOR 30-page cap), `supplementary_ejor.pdf` = 13 pages, both unresolved-ref-clean. Trimming and supplementary-demotion deferred to v2.6.1. Cover letter (`paper/cover_letter_ejor.md`) is a v2.5.x artifact and references "Corollary 18" — needs a one-token update to "Corollary 19" before v2.6.x submission.

Earlier TRSC-track history (archived):
- v2.4.5 — TRSC re-review pre-submission repair: 18 supp hardcoded old theorem numbers replaced by `\ref{}`; Table 5 caption "strictly generalises" → "contains ... on the common applicability domain"; abstract compressed (290→280 words) and last sentence softened from "operational implication is direct" to "In our synthetic single-vehicle experiments"; new Definition 2 paragraph on ex-post / policy-induced character of $\F$; Proposition 14 framing tone-down ("four complementary sufficient conditions" → "three complement-family + one unifying partition-pair certificate"; certificate-not-bound clarification); Table 7 / §7(ii) "certified a priori" replaced by explicit LKH minimum margin 0.0159 with 0.000% calibration error against Held-Karp; "follows the methodology" → "follow"; supp title aligned with main title; intermediate_dual_analysis.py comments updated.
- v2.4.4 — narrative consistency cleanup after Proposition 14 (4 sites updated to "4 thresholds, 66 of 67"; main 35p / supp 13p preserved).
- v2.4.3 — R1 Phases C and D: new **Proposition 14 (general partition-pair Bondareva–Shapley certificate)** certifies all 9 intermediate-coalition cases; §7 Operational trade-offs paragraph (C2); §7 Limitation (v) Policy-dependence of $\F$ (C4); Limitation (iv) reframed; new analysis script `code/scripts/intermediate_dual_analysis.py`.
- v2.4.2 — main → supp demotion (Example 4 / Reduction prop / Inheritance prop / sharpness fig moved to new supp §S6/§S7/§S8); xr cross-doc wired; main 35→33p (saved 2p budget for Phase C/D).
- v2.4.1 — R1 Phase B (statistical reporting): Wilson 95% CIs in Table 7; (ρ, structure) factorial rationale in §6.1; Finding 3(b) "Detection-limit warning (n=50 specifically)"; log-log regression slope –0.54 / R²=0.99 in §6.8.
- v2.4.0 — R1 Phase A (critical fixes): M1–M8 typographic / mathematical / wording fixes (encoding artifact `k<n-1`, singleton-summation, Definition 3 wording, "for sequential arrival regimes", $\rho=L/\tau$ note, abstract caveat).

## Earlier EJOR-track revisions (archived)

- v2.0.x — initial submission (v2.0, v2.0.1, v2.0.2, v2.0.3)
- v2.1.0 — first-round review response (superseded; F-generation bug)
- v2.1.2 — F-generation fix + 4-mechanism taxonomy (Proposition 12, Observation 15)
- v2.1.3 — documentation sync (Conclusion, Figure 1 caption, README, Nucleolus scope, B_medium caveat)
- v2.1.4 — reproducibility polish (augment step, seed123 CSV alignment, §6.8 Summary tone-down, version labels)
- v2.1.5 — seed 123 scale-up alignment (Finding 4 two-tier pattern, `run_seed123_check.py` TARGETS 5 → 2, REPRODUCIBILITY labels)
- v2.1.6 — ZIP-rebuildability fix (`\graphicspath` extended for clean-room extraction, Data-Files table `seed123_core_check.csv` 5 → 2 rows, `scripts/verify_zip_rebuild.sh` added)
- v2.1.7 — documentation semantic-sweep consistency pass (REPRODUCIBILITY §4 heading `5 instances` → `2 instances`, README version/Reproducibility-tags/repo-tree synced, `scripts/verify_doc_consistency.sh` added)
- v2.1.8 — EJOR 30-page compliance split (Appendix A/B/C moved to a separate `paper/supplementary.pdf`; main manuscript trimmed to 30 pages; §2 Related Work consolidated; `scripts/verify_zip_rebuild.sh` extended to validate both PDFs)
- v2.1.9 — EJOR desk-check compliance (Abstract rewritten formula-free and theorem-reference-free at 238 words; Keywords trimmed 7 → 5 with one EJOR-list term; `make_figures_v3.py` Figure 2 caption's "see Appendix C" → "see Supplementary Materials S3" + Fig 2 regenerated; REPRODUCIBILITY Data-Files table pruned of unshipped logs / Design-Documents section)
- v2.1.10 — EJOR Highlights compliance + package polish (separate `paper/highlights.{tex,pdf,txt}` with 5 bullets each ≤ 85 chars, formula-free and abbreviation-free; in-manuscript `\section*{Highlights}` removed from `main.tex`; active `Appendix B/C` text in REPRODUCIBILITY replaced by `Supplementary Materials §S2/§S3`; README repo-tree and Citation block synced to current paper title; `verify_zip_rebuild.sh` extended to build highlights.pdf)
- v2.1.11 — response-to-weaknesses revision (T1.1 Thm 6 and Thm 18 downgraded to Propositions; T1.3 "≈1.81" removed from Example 4; T1.4 §6.8 Finding 3 and §7(ii) rewritten as structural vs empirical split with detection-limit caveat; T1.5 five new citations added in §2 — Klijn&Slikker, Platz&Hamers, Özener&Ergun, Drechsel&Kimms, Özener et al. 2013; T1.6 Theorem 16 "uniformly" clause clarified; T1.7 Remark 17 depot-position constant made explicit; T2.1 Remark 14 kept as-is, balancing open-problem formulation added in Supplementary §S4; T2.2 detection-limit quantification integrated into §6.8 Finding 3 and caveat; Tier 3 VRG future-work paragraph expanded in §7; no CSVs touched.)
- v2.1.12 — reference-accuracy patch (verification report V2 flagged two bib errors in v2.1.11: P1 removed the hallucinated Klijn & Slikker (2005) reference entirely — bib entry deleted and the single citing sentence in §2.2 dropped; P2 corrected the Drechsel & Kimms (2010) venue from `Computers & Industrial Engineering, 59(4):547–555` to `International Journal of Production Economics, 128(1):310–321` (same title, same authors, same year). No theoretical, experimental, numerical, figure, or CSV changes; only references.bib and one sentence in `paper/main.tex`.)
- v2.2.0 — balanced-near-complement proposition (new Proposition 15 in §5.1 promoting the v2.1.11 Supplementary §S4 conjecture. Statement: under $\mathcal{F}\supseteq B_{n-1}\cup B_{n-2}$, if there exist non-negative weights $\lambda_S$ with $\sum_{S\ni i}\lambda_S=1$ for all $i$ such that $r > (\sum_S\lambda_S c(S))/c^{\ast}(N)$, then the Temporal Core is empty. Proof-sketch inline, full proof in Suppl. §S4. Empirical coverage audit via `code/scripts/near_complement_coverage_check.py`: 9/10 of the observed NN near-complement cases fire; 1 residual (n=15, A, seed 42) falls short by $\approx 2\times 10^{-3}$. Table 5 extended to 5-way decomposition (37 + 11 + 9 + 1 + 9 = 67 empty). Numbering shift: Observation 15 → 16, Theorem 16 → 17, Remark 17 → 18, Proposition 18 → 19, Corollary 19 → 20 (all via automatic \ref{}). No CSVs touched.)
- v2.2.1 — v2.2.0 verification-report patch (P1: three prose paragraphs in `paper/main.tex` that still spoke of "both" or "two" complement-based mechanisms post-Proposition-15 — §6.4 Analytic sharpness, §6.8 Finding 3(a), §7 Platform-design implication — updated to list all three mechanisms (Theorem 11, Proposition 12, Proposition 15) that Corollary 20 blocks under $k<n-1$. P2: the phrase "near-miss" removed from `docs/v2_1_12_to_v2_2_0_response.md` and `docs/phase2_option1_log.md` and replaced with neutral "failing the strict inequality by approximately $2\times 10^{-3}$" (paper and supplementary were already clean of such language). Proposition 15, its proof, §S4, and all numerical results are unchanged.)
- v2.2.2 — EJOR submission polish (T1: Highlights bullet 4 "both complement-based mechanisms" → "all three complement-based mechanisms" (LaTeX + plain-text versions); §1 Practical-implication parenthetical now lists Prop 15 alongside Thm 11 and Prop 12; abstract and C2/C4 were already current from v2.2.0. T2: §7 "Broader directions" paragraph rewritten as defensive scope-demarcation that frames the single-vehicle setting as a methodological choice isolating temporal coalition-feasibility structure from fleet-assignment confounds, announcing an Online VRG companion manuscript; §1 Structure paragraph gained a one-sentence scope note. One secondary-point sentence in §6.6 trimmed to keep main.pdf at 30 pages. T3: a new `paper/cover_letter.md` drafted for the EJOR submission portal (579 words, addressed to Prof. Słowiński, with author-side placeholders for submission date / e-mail / ORCID). No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, CSVs, or any numerical result.)
- v2.2.3 — external-critique polish (literature additions + minor scope notes; no new results, no numerical changes). Three new bib entries and one sentence each in §2: P1 Lyu, Lalla-Ruiz & Schulte 2025 EJOR (row-generation for collaborative berth allocation; static coalition family, contrasted with our arrival-dynamics restriction); P2 Chen, Wang & Meng 2023 TR-B (cost allocation in autonomous truck platooning); P3 van Zon, Spliet & van den Heuvel 2021 Transp. Sci. (Joint Network Vehicle Routing Game; row-generation for Core allocations over a static coalition family, flagged as the closest algorithmic precedent to our sequential-LP cascade over the time-induced $\mathcal{F}$). P4: one sentence after Theorem 17's proof notes that the BHH uniform-i.i.d. hypothesis extends to general absolutely continuous distributions via the Steele (1997) limiting-functional framework, with the hidden constant then density-dependent. P5: the existing Goyal et al. (2025) citation in §2.2 is expanded with one sentence that makes the orthogonality explicit — their worth $v(\pi)$ is sequence-indexed with full power-set coalitions, while ours is set-valued $c(S)$ on a time-restricted family $\mathcal{F}$. P6: abstract final sentence softened from "preserve Core stability" to "substantially improve Core stability in our experiments". Page-budget offsets: one redundant sentence in §5.3 and one in §6.6 trimmed. The external critique's R3 (Van Zon et al. "The effect of algorithm capabilities on cooperative games", Erasmus working paper EI2021-02) was replaced by the correctly-titled *Transportation Science* 55(1):179–195 paper by the same author team. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any CSV, figure, or `src/` file.
- v2.2.4 — reference-accuracy patch on top of v2.2.3 + first full PDF rebuild. Single bibliographic correction: `vanzon2021joint` first-author given name fixed from "Mart{\'\i}n" to "Mathijs" (verified via INFORMS DOI 10.1287/trsc.2020.1008 and RePEc listing; the v2.2.3 entry was a hallucination of the given name). PDF rebuild performed in this iteration (TeX Live 2026); supplementary.pdf = 8 pages and highlights.pdf = 1 page as expected, but main.pdf rebuilds to 31 pages — 1 page over the EJOR 30-page cap. The v2.2.3 §5.3 / §6.6 trims were therefore NOT overkill and are retained. The 1-page overflow is flagged for author resolution (further trim or local paragraph-packing). No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file.
- v2.2.5 — 1-page overflow fix on top of v2.2.4. `main.pdf` reduced from 31 pages to 30 pages (EJOR cap) via three localized minimal edits: (1) **Tier 1** — removed the non-load-bearing Chen et al. 2023 sentence from §2.1 (one sentence "Related dynamic-vehicle cooperative game applications include cost allocation in autonomous truck platooning") and deleted the `chen2023cost` bib entry; (2) **Tier 2** — two small prose tightenings to address paragraph overfulls (§3.1 "measures this overhead" replacing a redundant trailing clause at line 164; §7(i) "or forecasting-aware policies" replacing "or forecasting-aware dispatch policies" at line 745); (3) **Tier 3** — compressed the v2.2.3 Goyal orthogonality addition in §2.2 from ~58 words to ~33 words while preserving the temporality-axis contrast. Tier 1 alone and Tier 1+2 each still yielded 31 pages; Tier 3 closed the final page. Lyu et al. 2025 and van Zon et al. 2021 citations retained. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file.

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which customers arrive over time and costs must be allocated only
among coalitions realizable under revealed arrival dynamics. This repository
contains all code, seeds, and raw results needed to reproduce the paper's
numerical claims.

## Key results (sanity checkpoints, v2.4.5)

| Paper location | Quantity | Value |
|---|---|---|
| Supplementary §S6 (Solomon C101) | TNu allocation | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 5 | Theorem 9 single-complement fires (NN, 96 applicable) | 37/37 (no false positives) |
| Table 5 | Proposition 10 balanced-complement fires (NN, 80 applicable) | 57/57 (no false positives) |
| Table 5 | Proposition 13 balanced-near-complement fires (NN, 10 near-complement) | 9/10 (no false positives) |
| Table 5 | Proposition 14 partition-pair certificate (NN, 9 intermediate cases) | 9/9 |
| §6.4 | Four-threshold joint coverage of NN empties | 66/67 |
| §6.4 | Five-mechanism decomposition of 67 NN empties | 37 + 11 + 9 + 1 + 9 |
| Corollary 18 (§6.4) | k < n−1 Core empirical nonempty rate | 70/79 (88.6%; 9 intermediate-mechanism exceptions) |
| §6.6 | Sharpness ratio r̄*/r̄**, r̄*/r̄*** | 3.56 (4.351/1.223), 3.97 (4.351/1.096) |
| Supplementary §S2 | Scale invariance (r relative std across α) | 0.00e+00 |
| Supplementary §S3 | Near-complement cases (Supp. Table) | 10 |
| Supplementary §S3 | Intermediate cases (Supp. Table) | 9 |
| Supplementary §S8 | Partition-pair certificates (Proposition 14) | 9/9 |

## Repository structure

```
.
├── paper/             # main_trsc.tex + supplementary_trsc.tex + references.bib
│                      # (main_trsc.pdf + supplementary_trsc.pdf built locally)
│                      # Earlier EJOR-track main.tex / supplementary.tex / highlights.tex
│                      # retained for archival reproducibility (untouched).
├── code/
│   ├── src/           # algorithm implementations (Held-Karp, LKH, TNu LP, policies,
│   │                  #  config.py, generators.py, core_lp_restricted.py)
│   ├── experiments/   # v2 runners + logs (policy_comparison_v2_full.csv,
│   │                  #  scaleup_v2.csv, sensitivity_v2.csv, seed123_core_check.csv)
│   ├── figures/       # figure generation + PDF outputs (make_figures_v3.py)
│   └── requirements.txt
├── docs/              # verification artifacts
│                      # (dev-only: a `figures/` symlink to `code/figures/`
│                      #  exists locally for the paper's graphicspath, but
│                      #  is NOT shipped in the submission ZIP — the ZIP
│                      #  references `code/figures/` directly)
├── scripts/           # gate checks: verify_zip_rebuild.sh, verify_doc_consistency.sh
├── REPRODUCIBILITY.md # full reproduction guide
└── LICENSE
```

## Quick start

```bash
# Install dependencies
pip install -r code/requirements.txt

# Regenerate all figures from v2 experiment data
cd code/figures
python3 make_figures_v3.py

# Reproduce main study (~13 min)
cd ../experiments
python3 run_main.py --output logs/policy_comparison_v2_full.csv
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for full environment details,
random seeds, and mapping between paper tables/figures and scripts.

### EJOR resubmission build

After the TS desk rejection (see REVISION_NOTES v2.5.0), the EJOR
submission package consists of:
- `paper/main_ejor.{tex,pdf}` — manuscript
- `paper/supplementary_ejor.{tex,pdf}` — electronic companion
- `paper/cover_letter_ejor.{md,pdf}` — cover letter
- `paper/references_ejor.bib` — references (Arroyo note stripped vs. shared `references.bib`)

Build sequence: `pdflatex main_ejor → bibtex → pdflatex×2 →
pdflatex supplementary_ejor → bibtex → pdflatex×2 → pdflatex main_ejor`.

Highlights file is deferred for the EJOR submission; the existing
`highlights.{tex,pdf,txt}` content is from the older EJOR baseline and
predates Proposition 14, so it would mislead reviewers if shipped as-is.
A new highlights file should be drafted before final submission.

## Reproducibility tags

- `paper-submission-v1` / `v1.1` / `v1.2`: prior submission states (L = 10 coordinate convention); superseded by v2.1.2 and subsequent iterations.
- `paper-submission-v2.0` / `v2.0.1` / `v2.0.2` / `v2.0.3` / `v2.1.0` (local only): intermediate revisions under Steele N2 convention; superseded by v2.1.2 and subsequent iterations.
- `v2.1.2` / `v2.1.3` / `v2.1.4` / `v2.1.5` / `v2.1.6` / `v2.1.7` / `v2.1.8` / `v2.1.9` / `v2.1.10` / `v2.1.11` (intermediate major-revision iterations): 4-mechanism taxonomy, Proposition 12, Observation 15, corrected feasibility family F; a sequence of documentation-polish and ZIP-rebuildability fixes; the EJOR 30-page compliance split at v2.1.8 (appendices moved to `paper/supplementary.pdf`); the v2.1.9 abstract / keyword / figure-caption desk-check pass; the v2.1.10 Highlights split + package polish; and the v2.1.11 response-to-weaknesses revision (Prop 6/18 downgrades, detection-limit caveat, five new §2 citations, Thm 16 scoping, Remark 17 constant, Suppl. §S4 open-problem). See the version-history block above for per-iteration scope. Restore any locally via `git checkout <tag>`.
- `v2.1.12` (intermediate): reference-accuracy patch against the v2.1.11 verification report (`docs/v2_1_11_verification_report.md` items V2.1 FAIL and V2.4 FAIL). **P1:** The Klijn & Slikker (2005) "Sequencing games with non-linear cost functions" reference added in v2.1.11 was a hallucinated bib entry (Math. Methods of OR 62(1):69–86 does not list such a paper; Klijn and Slikker have no joint 2005 publication). The entry is deleted from `paper/references.bib` and its single citing sentence in §2.2 is removed; no substitute citation is added. **P2:** The Drechsel & Kimms (2010) reference had the correct title/authors/year but the wrong venue; it is now corrected from `Computers & Industrial Engineering, 59(4):547–555` to `International Journal of Production Economics, 128(1):310–321`. The in-text citation `\citet{drechsel2010computing}` in §2.2 is unchanged (bib-key stable; inline text never named a journal). No theoretical, experimental, numerical, figure, or CSV changes. Theorem 11, Proposition 12, Observation 15, Corollary 19 statements / CSVs / `src/` unchanged bit-for-bit. Restore locally via `git checkout v2.1.12`.
- `v2.2.0` (intermediate): new theorem — **Proposition 15 (Balanced-near-complement threshold)** promotes the Supplementary §S4 conjecture (from v2.1.11) to a proven sufficient condition on the mixed collection $B_{n-1}\cup B_{n-2}$. Proof-sketch in main.tex §5.1, full proof in Suppl. §S4. Empirical coverage via the new analysis script `code/scripts/near_complement_coverage_check.py`: fires on 9 of 10 observed NN main-grid near-complement cases (Table 5 now reports a five-mechanism decomposition: 37 single + 11 balanced + 9 balanced-near + 1 near-complement-residual + 9 intermediate = 67 empty). One residual case (n=15, Pattern A, seed 42) fails the strict inequality by $\approx 2\times 10^{-3}$ and remains certified only by the first-stage Core LP; a refined open problem (mixing size-$(n-3)$ coalitions, or relaxing to a covering inequality) is stated in Suppl. §S4. Numbering shift inside §5: Observation 15 → 16, Theorem 16 → 17, Remark 17 → 18, Proposition 18 → 19, Corollary 19 → 20 (all via automatic \ref{}; three literal "Observation~15" in supplementary.tex updated to "Observation~16"). No CSVs touched; no simulator/source code modified; one read-only analysis script added under `code/scripts/`. Bibliography compressed to `\scriptsize` to preserve the 30-page cap. Restore locally via `git checkout v2.2.0`.
- `v2.2.1` (intermediate): verification-report patch against `docs/v2_2_0_verification_report.md` items W3.c FAIL and W7 WARN. **P1 (stale "two-mechanism" prose, W3.c FAIL):** After the v2.2.0 insertion of Proposition 15, three paragraphs in `paper/main.tex` still referred to "both complement-based mechanisms" (Theorem 11 and Proposition 12 only). The three sites — §6.4 "Analytic sharpness of Corollary 20" (line 546), §6.8 Finding 3(a) (line 719), and §7 Platform-design implication (line 741) — are rewritten to list all three mechanisms (Thm 11, Prop 12, Prop 15) that Corollary 20 blocks under $k<n-1$. The logical basis (Corollary 20 requires size-$(n-1)$ feasibility, which all three hypotheses demand) is unchanged and was already captured in Corollary 20's own statement and proof (main.tex lines 439–446). **P2 (non-paper "near-miss" language, W7 WARN):** The phrase "near-miss" appeared once in `docs/v2_1_12_to_v2_2_0_response.md` and once in `docs/phase2_option1_log.md`; both replaced with the neutral "failing the strict inequality by approximately $2\times 10^{-3}$" to match the paper's own phrasing. Paper and supplementary were already clean of the forbidden-list phrasings. Proposition 15, its proof, §S4, Table 5 counts, all numerical results (4.351 / 1.223 / 1.096; sharpness factors 3.56 / 3.97; 37 + 11 + 9 + 1 + 9 = 67 empty Cores), and all CSVs / figures / `src/` files are unchanged bit-for-bit. Restore locally via `git checkout v2.2.1`.
- `v2.2.2` (intermediate): EJOR submission-polish patch — no new results, presentation only. **T1 (Abstract / Highlights / Introduction consistency sweep):** Highlights bullet 4 updated from "blocks both complement-based mechanisms" to "blocks all three complement-based mechanisms" in both `paper/highlights.tex` and `paper/highlights.txt` (still ≤ 85 chars, formula-free). §1 Practical-implication parenthetical updated to list Prop 15 alongside Thm 11 and Prop 12. The abstract, C2, and C4 were already current from v2.2.0 and required no change. **T2 (defensive single-vehicle scope demarcation):** §7 "Broader directions" paragraph rewritten to frame the single-vehicle scope as a deliberate methodological choice that isolates the temporal coalition-feasibility structure of $\F$ from fleet-assignment confounds, announcing an Online VRG companion manuscript in preparation. §1 Structure paragraph gained a one-sentence scope note so readers are informed of the single-vehicle scope upfront. **T3 (cover letter):** `paper/cover_letter.md` drafted for the EJOR submission portal (579 words, addressed to Prof. Słowiński, with author-side placeholders for submission date / e-mail / ORCID). **Page budget:** one redundant "secondary point" sentence in §6.6 Sharpness trimmed to keep main.pdf at exactly 30 pages. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, or any numerical result. Restore locally via `git checkout v2.2.2`.
- `v2.2.3` (intermediate): external-critique polish — literature additions + minor scope notes; no new results, no numerical changes. **P1 (Lyu, Lalla-Ruiz & Schulte 2025, *EJOR* 323(3):888–906):** bib entry `lyu2025collaborative` added; one sentence added to §2.1 framing their collaborative-berth-allocation row-generation approach as a static coalition family, contrasted with our arrival-dynamics restriction. **P2 (Chen, Wang & Meng 2023, *TR-B* 173:119–141):** bib entry `chen2023cost` added; one short sentence added to §2.1 flagging their autonomous-truck-platooning cost-allocation study as a related dynamic-vehicle cooperative game application. **P3 (van Zon, Spliet & van den Heuvel 2021, *Transportation Science* 55(1):179–195):** bib entry `vanzon2021joint` added; one sentence added to §2.2 describing the Joint Network Vehicle Routing Game's row-generation algorithm as the closest static-coalition-family methodological precedent to our sequential-LP cascade over the time-induced $\F$. The external critique's R3 originally cited "The effect of algorithm capabilities on cooperative games" (Erasmus working paper EI2021-02); the verification report replaced that with the correctly-titled JNVRG paper by the same author team. **P4 (Theorem 17 scope note):** one sentence inserted after the proof of Theorem 17, noting that the BHH uniform-i.i.d. hypothesis extends to general absolutely continuous distributions via the Steele (1997) limiting-functional framework, with the hidden constant then density-dependent. **P5 (Goyal orthogonality):** the existing `\citet{goyal2025temporal}` sentence in §2.2 is expanded by one sentence that makes the orthogonality explicit — their worth $v(\pi)$ is a function of the realized sequence $\pi$ while the coalition structure remains the full power set, whereas our Online TSG keeps $c(S)$ set-valued and restricts the coalition family to $\F$. **P6 (abstract mild softening):** the abstract's final sentence changed from "short service windows plus informed dispatch preserve Core stability" to "short service windows plus informed dispatch substantially improve Core stability in our experiments" (matches the observational scope). **Page-budget offsets:** one sentence in §5.3 Discussion ("In the language of queueing theory...") compressed from 85 words to 35 words, and the last sentence of §6.6 Sharpness ("Note that $r^{\ast\ast\ast}$ averages across complements...") removed. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file. Restore locally via `git checkout v2.2.3`.
- `v2.2.4` (intermediate): reference-accuracy patch on top of v2.2.3 + first full PDF rebuild. **P1 (van Zon first-author given-name correction):** `paper/references.bib` entry `vanzon2021joint` has `author = {van Zon, Mart{\'\i}n and Spliet, Remy and van den Heuvel, Wilco}` corrected to `author = {van Zon, Mathijs and Spliet, Remy and van den Heuvel, Wilco}`. The first author's given name is "Mathijs" per INFORMS DOI 10.1287/trsc.2020.1008 and the RePEc listing at `ideas.repec.org/p/ems/eureir/115273.html`; "Mart{\'\i}n" in v2.2.3 was a hallucination that would have rendered as "M. van Zon" in the plainnat citation but as "Martín van Zon" in any listing that expanded given names. No inline paper text referenced the author's given name, so no prose change was needed. **P2 (PDF rebuild):** TeX Live 2026 was available for the first time and all three PDFs were rebuilt from source (pdflatex / bibtex / pdflatex / pdflatex for `main.tex` and `supplementary.tex`; two pdflatex passes for `highlights.tex`). Outcome: `supplementary.pdf` = 8 pages (on-spec), `highlights.pdf` = 1 page (on-spec), `main.pdf` = **31 pages — one over the EJOR 30-page cap**. The v2.2.3 §5.3 / §6.6 trims were therefore insufficient rather than overkill and are retained as-is. The 1-page overflow is a structural artifact of the six v2.2.3 prose additions net of the two trims (estimated ~+50 words net per the v2.2.3 response document, in practice rendered as +1 page under TeX Live 2026's line-breaking). The remediation — a further ~50-word trim somewhere outside the protected regions (Proposition 15, its proof, §S4, Theorems, Table 5) — is **deferred to the author's judgement** and is not performed in v2.2.4 because this iteration is a minimal reference-accuracy patch only. No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file. Restore locally via `git checkout v2.2.4`.
- `v2.2.5` (current, major revision): 1-page overflow fix on top of v2.2.4. `main.pdf` reduced from 31 pages to **30 pages** (EJOR cap); `supplementary.pdf` and `highlights.pdf` unchanged at 8 pages and 1 page respectively. Three localized minimal edits, applied in the order Tier 1 → Tier 2 → Tier 3 and stopping when the 30-page target was achieved. **Tier 1 (§2.1, Chen et al. 2023 removal):** the v2.2.3 P2 sentence "Related dynamic-vehicle cooperative game applications include cost allocation in autonomous truck platooning \citep{chen2023cost}." is removed from `paper/main.tex` §2.1, and the `chen2023cost` entry is removed from `paper/references.bib`. This sentence was a non-load-bearing "related applications" mention; its removal does not affect any theoretical statement or departure argument. Tier 1 alone rebuilt to 31 pages. **Tier 2 (two small overfull-hbox tightenings):** (i) §3.1 line 164 — the trailing redundant clause ", since the online policy must commit to visits without seeing future arrivals" is removed from the sentence defining the competitive ratio, since the anticipation clause is already stated earlier in the same paragraph ("because the online policy cannot anticipate future arrivals"); the sentence now reads "...measures this overhead." (ii) §7(i) line 745 — "Extending to learning-based or forecasting-aware dispatch policies remains open." → "Extending to learning-based or forecasting-aware policies remains open." (one redundant word trimmed; the sentence is in the Dispatch-policy limitation paragraph, so "policies" is unambiguous). Tier 1 + Tier 2 rebuilt to 31 pages. **Tier 3 (§2.2 Goyal orthogonality compression):** the v2.2.3 P5 sentence "The two frameworks are complementary: their worth $v(\pi)$ is a function of the realized arrival sequence $\pi$ while the coalition structure remains the full power set, whereas our Online TSG keeps the characteristic function $c(S)$ set-valued (matching the static TSG exactly) and restricts the coalition family to $\F$ induced by the arrival--service process." is compressed to "Their worth $v(\pi)$ depends on the arrival sequence while coalitions remain unrestricted; our $c(S)$ is set-valued but coalitions are restricted to $\mathcal{F}$, an orthogonal axis of temporality." (58 → 33 words; same contrast preserved). Tier 3 achieved the 30-page target. Lyu et al. 2025 and van Zon et al. 2021 citations are retained (important distinguishing references, not removed). No changes to Proposition 15, its proof, Supplementary §S4, Table 5 counts, any numerical result, CSV, figure, or `src/` file. Restore locally via `git checkout v2.2.5`.

## Citation

If you use this code or build on the results, please cite:

```bibtex
@article{jeong2026online,
  author = {Jeong, Seyun and Tae, Hyunchul},
  title  = {Online Traveling Salesman Games: Core Fragility
            and the Temporal Nucleolus under Dynamic Arrivals},
  year   = {2026},
  note   = {Under review at Transportation Science (INFORMS)}
}
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Contact

- Seyun Jeong, Korea Institute of Industrial Technology (KITECH) — jeongsseyyun@kitech.re.kr
- Hyunchul Tae, Korea Institute of Industrial Technology (KITECH), corresponding author — sage@kitech.re.kr

## v2_5_2 (2026-05-02) — Data availability statement EJOR-appropriate

Replaced the TS-era phrasing "made publicly available upon de-anonymization"
in `main_ejor.tex` with a concrete URL-based statement appropriate to
EJOR's single-blind review:

`All code, data, and reproducibility scripts are publicly available at \url{https://github.com/sage-Tae/online-tsg}.`

(The repository was confirmed already public at the time of v2.5.2, so the
statement uses the present-tense form.)

No other content change. Page count of `main_ejor.pdf` unchanged at 30.
TS-tree files (`main_trsc.{tex,pdf}`, etc.) byte-identical.

## v2_5_1 (2026-05-02) — EJOR 30-page compliance pass

EJOR Guide for Authors caps articles at 30 pages including references and
appendices; v2.5.0's `main_ejor.pdf` was 33 pages, so a four-edit trimming
pass was applied. No theorem statement, proof logic, numerical result, table
data, figure data, CSV, or `code/src/` file modified. The original v2.5.0
theorem/proposition/corollary numbering (Theorem 9, Prop 10, Cor 11, Rem 12,
Prop 13, Prop 14, Obs 15, Thm 16, Rem 17, Cor 18) is preserved bit-for-bit
via an `\addtocounter{theorem}{3}` placed before Theorem 9 to compensate for
the lifted Lemmas 7--8 and the merged Remarks 5--6.

**Edit A — References typography.** `\bibfont`→`\footnotesize`, `\bibsep`
tightened to `1pt plus 0.2ex minus 0.2ex`, references wrapped in
`\begin{spacing}{1.0}` to single-space the bibliography only (main body
remains 1.5-spaced). The original target of `\small` saved less than expected
(still 31 pages); `\footnotesize` was needed to land at 30. Saved ~1 page.

**Edit B — Lemmas 7 and 8 moved to Supplementary §S8.** New section
`\label{app:complement-feasibility-lemmas}` in
`paper/supplementary_ejor.tex`. Lemma proofs unchanged; main body cites them
via `Supplementary Lemma~\ref{lem:lemma51}` / `Supplementary Lemma~\ref{lem:lemma52}`,
with a one-sentence pointer replacing the lifted blocks. Existing
supplementary §S8 (partition-pair) becomes §S9, §S9 (histograms) becomes
§S10; cross-references via `xr` auto-resolved. The two lifted lemmas are
numbered Lemma 4 / Lemma 5 inside the supplementary's local theorem counter.
Saved ~0.5 pages.

**Edit C — Remarks 5/6 collapsed into single paragraph.** `r^{\ast}` /
super-additivity bound restated as one prose paragraph rather than two
`\begin{remark}` blocks. Both `\label{rem:remark1}` and `\label{rem:rstar}`
retained on the merged Remark 5 so existing cross-references continue to
resolve. The "Remarks 5--6" range citation in the proof of Corollary 18 was
shortened to "Remark 5". No content lost. Saved ~0.25 pages.

**Edit D — Limitations rewritten as `enumerate{enumitem}`.** Five
`\emph{(i)} … (v)}` paragraphs collapsed into a tight `enumerate` list with
~50% wording reduction; all five concerns retained verbatim in summary form.
Saved ~0.6 pages.

**Abstract / Practical-implication fallback (per Step 7 verification gate).**
After Edits A--D the build was 31 pages; the Step 7 fallback was applied:
the abstract was tightened by ~30 words ("obscuring a core source of
instability...treats them as if they could" → "distorting fairness when
arrivals are spread in time"), and the `\paragraph{Practical implication.}`
heading in the Introduction was dropped (its content is folded as a
continuation paragraph after the C1--C4 itemize, and tightened by ~40%).
This together with Edit A's `\footnotesize` push landed the build at 30
pages exactly.

**Minor follow-ups from v2.5.0:**
- Supplementary Overview now lists §S8 (auxiliary lemmas) and §S9
  (partition-pair) explicitly (was: jumped from §S7 to §S9, omitting both
  the new section and the partition-pair pointer).
- Cover letter metadata block (`To`, `Journal`, `Date`, `Re`) now renders as
  four separate lines via Markdown trailing `\` line breaks, no longer
  collapsed into a single bold paragraph by pandoc. The pandoc pipe-table
  fallback noted in the plan misrendered (no header separator), so the
  trailing-`\` line-break form was used instead. Cover-letter `Date` updated
  to 2026-05-02 (build date) and the §S8 partition-pair pointer in the
  Reproducibility section updated to §S9 to track Edit B's renumbering.

**Final page counts:** `main_ejor.pdf` = 30 pages (target ≤30, met exactly).
`supplementary_ejor.pdf` = 13 pages (S1--S10, with new §S8 = "Auxiliary
feasibility lemmas"). `cover_letter_ejor.pdf` = 2 pages.

**Build-time figure note.** Figure files were not bundled with the v2.5.0
distribution; placeholder PDFs with the same physical dimensions as the
originals were created in `figures/` so layout (and therefore page count)
matches what a real-figure build would produce. Figures are flagged as
deferred for regeneration in a future pass.

TS tree (`main_trsc.{tex,pdf}`, `supplementary_trsc.{tex,pdf}`,
`cover_letter_trsc.{md,pdf}`) and old-EJOR baseline (`main.tex`,
`supplementary.tex`, `cover_letter.{md,pdf}`) byte-identical to v2.4.6;
v2.5.0 EJOR `references_ejor.bib` byte-identical.

## v2_5_0 (2026-05-01) — EJOR resubmission build

After TS desk rejection (TS-2026-0253, scope grounds), built parallel
EJOR-formatted manuscript tree. New files:
- `paper/main_ejor.tex` (body verbatim from `main_trsc.tex`, EJOR preamble)
- `paper/supplementary_ejor.tex` (body verbatim from `supplementary_trsc.tex`, EJOR preamble)
- `paper/references_ejor.bib` (clone of `references.bib` with Arroyo `note` field stripped)
- `paper/cover_letter_ejor.md`, `paper/cover_letter_ejor.pdf`
- `paper/main_ejor.pdf`, `paper/supplementary_ejor.pdf`

Six small body edits applied in the new tree only (TS tree untouched):
3a — Section 6.2 "four-mechanism" → "five-mechanism".
3b — Theorem 16 Step 1 aligned block expanded to three explicit lines
     (insertion / monotonicity / numeric distance) for visual clarity;
     mathematical content unchanged.
3c — Arroyo Crossref note suppressed via `references_ejor.bib`.
3d — Figure 1 caption clarification on "n=38" legend reconciliation.
3e — Abstract italic-n consistency.
3f — Limitation (ii) and Table 7 footnote: explicit unit qualification on
     the $r-r^{\ast\ast}$ margin vs LKH calibration-error comparison.

No theorem statement, proof logic, numerical result, table data, figure
data, CSV, or `code/src/` file modified. `paper/main_trsc.tex` and
`paper/supplementary_trsc.tex` are bit-identical to v2.4.6. Bit-identical
EJOR-bound 20 files preserved separately.

Highlights file deferred: existing `paper/highlights.{tex,pdf,txt}`
predates Proposition 14 and would mislead reviewers if shipped as-is;
a fresh highlights file is to be drafted before final submission.
Figure regeneration also deferred: `fig2_r_vs_rstar.pdf` (Figure 1)
still bears a "four-mechanism overlay" title-text artifact from the
older plotting script; the body text and caption now resolve this in
words (Fix 3a, Fix 3d), but a re-rendered figure remains a future task.

## v2_4_6 (2026-04-26)
**REPRODUCIBILITY in-place sync + cover letter content update.** Three issues
remained after v2.4.5: (a) `REPRODUCIBILITY.md` still had a "## Compiling
the Paper" / "## EJOR Submission" / "## Submission Verification" block
listing `main.tex` / `main.pdf` / `supplementary.tex` / `highlights.{tex,pdf,txt}`
build commands and 30-page references — the v2.4.5 update only touched the
front matter; (b) `paper/cover_letter_trsc.md` still cited the old paper
title and the pre-Proposition-14 "three complementary sufficient conditions"
+ "57 of 67" framing; (c) `paper/cover_letter_trsc.pdf` was therefore stale.
Five sentence-level edits in `REPRODUCIBILITY.md` (build PDF names + xr
interleaved compile order + "## EJOR Submission" → "## TRSC Submission"
slots + verify_zip_rebuild comment), two sentence-level edits in
`paper/cover_letter_trsc.md` (title alignment with current main title;
contributions reorganized to "three complement-family + unifying
partition-pair certificate (Proposition 14)" with "66 of 67" coverage), and
`pandoc cover_letter_trsc.md → cover_letter_trsc.pdf` rebuild (2 pages,
unchanged page count). No theorem statement, proof, numerical result, table,
figure, CSV, or `code/src/` file modified; `paper/main_trsc.tex` and
`paper/supplementary_trsc.tex` are bit-identical to v2.4.5; main_trsc.pdf
35p / 0 ATTN / 0 `??` and supplementary_trsc.pdf 13p / 0 ATTN / 0 `??`
preserved. EJOR-bound 20 files bit-identical (22 consecutive revisions of
preservation now). See `docs/v2_4_5_to_v2_4_6_response.md` for per-edit
detail.

---

## v2_4_5 (2026-04-26)
**External TRSC re-review pre-submission repair.** Eight categories of edits
responding to the 2026-04-26 external re-review of v2.4.4. No theorem
statement, proof, numerical result (37+11+9+1+9 = 67 empty Cores; 9/10 Prop 13
fires; 0 false positives; 525 policy-instance pairs; r̄** = 1.223;
r̄*** = 1.096; 3.56× / 3.97× sharpness; 9 partition-pair certificates), table
data, figure, CSV, or `code/src/` file modified; this iteration is
wording / framing / numbering / documentation synchronization only.

**STEP 1 (P1) — Supplementary numbering sync**: 18 hardcoded old theorem
numbers in `paper/supplementary_trsc.tex` (Theorem 11→9 ×4, Proposition
12→10 ×1, Proposition 15→13 ×6, Remark 14→12 ×4, Observation 16→15 ×3)
replaced with `\ref{}` pointers to main labels via the existing `xr` package;
all numbering now resolves automatically.

**STEP 2 (P1) — Table 5 caption**: "strictly generalises" replaced by
"contains the Proposition~\ref{prop:bondareva-complement} weighting on the
common applicability domain"; "recovers Proposition 12" (hardcoded number from
before v2_4_3) replaced by "recovers Proposition~\ref{prop:bondareva-complement}".

**STEP 3 (P2) — Abstract**: compressed from 290 to 285 words (safe margin
under TRSC 300-word cap); "Computational experiments on 175 instances..."
sentence tightened; last sentence softened from "The operational implication
is direct: short service-time promises..." to "In our synthetic single-vehicle
experiments, short service-time promises (peak queue $k<n-1$)...".

**STEP 4 (P2) — Definition 2 ex-post framing**: new paragraph "Ex-post,
policy-induced character of $\F$" inserted after Definition 2's
boundary-configurations note, explicitly stating that the Online TSG Core is
an ex-post, policy-induced stability concept rather than a counterfactual
one and pointing forward to §7 Limitation (v).

**STEP 5 (P2) — Proposition 14 framing**: §1 Contribution C2 reorganized from
"four complementary sufficient conditions" to "three complement-family
sufficient conditions plus one unifying partition-pair certificate"
clarifying that Proposition 14 contains Theorem 9 as the singleton-complement
case; new sentence in Proposition 14's "Relationship to earlier thresholds"
paragraph clarifying its certificate-not-predictive-bound character; new
sentence in §6.3 explaining that the 9 partition pairs were extracted from
the first-stage Core LP dual support; §7 first paragraph "general
partition-pair threshold" → "unifying partition-pair certificate".

**STEP 6 (P2) — Table 7 + §7(ii) LKH margin**: "certified a priori by
Theorem 9" replaced (in two sites) by "certified by Theorem 9 (conditional on
LKH-computed $c^{\ast}(S)$ values for $n>20$; minimum $r-r^{\ast\ast}$
margin $0.0159$, with LKH calibration error of $0.000\%$ against Held--Karp
at $n=15$)". Minimum margin 0.0159 measured from
`code/experiments/logs/scaleup_v2.csv` (Pattern A, $n\ge 30$, $r>r^{\ast\ast}$,
9 firing seed-size combinations).

**STEP 7 (P3) — Minor**: "Solver and calibration follows" → "follow"; supp
title aligned with current main title (`Core Fragility and the Temporal
Nucleolus under Dynamic Arrivals`); 7-3 multiply-defined-citation
deduplication SKIPPED per FALLBACK 3 (each of the 4 keys
`guajardo2015nucleolus`, `helsgaun2000effective`, `potters1992tsg`,
`solomon1987benchmarks` appears exactly once in `references.bib`; the warning
is a benign `xr`/`natbib` interaction); 7-4 already absorbed by STEP 5
("threshold that survives" → "threshold surviving"); 7-5
`code/scripts/intermediate_dual_analysis.py` module-level comments updated
("Observation 16" → "Observation 15"; "Proposition 16 candidate" →
"Proposition 14 (general partition-pair certificate)").

**STEP 8 (P1) — Documentation sync**: `README.md` rewritten from v2.2.8 / EJOR
/ `main.pdf` basis to v2.4.5 / TRSC / `main_trsc.pdf` basis: title updated,
venue updated, Key-results table refreshed with current numbering (Theorem 9,
Propositions 10/13/14, Corollary 18) and a new row for Proposition 14
9/9-fires certificate, repository-structure block updated, v2.0–v2.2.x
history collapsed under "Earlier EJOR-track revisions (archived)" heading,
v2.4.x history written as the current TRSC-track block. `REPRODUCIBILITY.md`
front matter rewritten to TRSC submission identity (35 / 13 page counts, two
files only, no separate Highlights), supplementary §S1–§S9 inventory listed,
new "Proposition 14 (general partition-pair certificate) reproduction"
section added with reference output table.

main_trsc.pdf **35 / 35 pages, 0 ATTENTION boxes, 0 `??` cross-ref markers,
0 undefined-reference warnings**; supplementary_trsc.pdf **13 / 15 pages,
0 ATTENTION, 0 `??`, 0 undef**. EJOR-bound 20 files **bit-identical**
(21 consecutive revisions of preservation now: v2_3_3 → … → v2_4_5). All
theorem statements, proofs, empirical fire counts, Wilson 95% CIs, log-log
regression slopes, Phase A/B/v2_4_2/v2_4_3/v2_4_4 fixes, and threshold values
preserved verbatim. multiply-defined-citation warning of 4 keys persists as a
known `xr`/`natbib` interaction (single-entry confirmed in bib database; no
real duplication). See `docs/v2_4_4_to_v2_4_5_response.md` for per-edit
detailed receipts.

---

## v2_4_4 (2026-04-26)
**Narrative consistency cleanup after Proposition 14 addition.** Four
sentence-level rewordings in `paper/main_trsc.tex` to align pre-existing
summary statements with the four-threshold coverage introduced by Proposition
14 in v2_4_3. Each site previously claimed the empirical coverage as "three
thresholds, 57 of 67"; the four sites now consistently state "four thresholds,
66 of 67":

1. **Abstract certify-count** — "the three thresholds jointly certify 57 with
   no false positives" → "the three thresholds certify 57 and a fourth
   partition-pair threshold the remaining 9 (66 of 67 total, no false
   positives)".
2. **Table 5 caption (§6.3)** — opening clause expanded from "three analytic
   thresholds … jointly certify 57 of the 67" to "three complement-based
   analytic thresholds … jointly certify 57 …, and the general partition-pair
   threshold (Proposition~14) certifies the remaining 9 intermediate-coalition
   cases of Observation~15 that operate at $k<n-1$ (66 of 67 jointly)"; "eludes
   all three" → "eludes all four" for the near-complement residual.
3. **§1 Contributions C4** — "9 intermediate-coalition. No false positives" →
   "9 intermediate-coalition cases certified by Proposition~14 (66 of 67
   total). No false positives".
4. **§6.4 prose (after Table 5)** — single long sentence "Theorem~..., Prop~...,
   Prop~... are sufficient conditions jointly covering 57 of 67" → two-sentence
   form leading with "The three complement-based mechanisms cover 57 of 67 NN
   empties; Proposition~14 certifies the 9 intermediate cases of
   Observation~15 (Supplementary~§S9), so the four thresholds jointly cover 66
   of 67. Only the 1 near-complement residual ... is uncovered analytically."

Page-budget management: first compile after the four edits produced 36 pages;
two of the edits (Abstract and §6.4 prose) were tightened to compress the
prose without losing the "66 of 67" claim, restoring main to exactly **35
pages**.

main_trsc.pdf **35 / 35 pages, 0 ATTENTION, 0 `??` refs, 0 undefined-reference
warnings**; supplementary_trsc.pdf **13 / 15 pages, 0 ATTENTION, 0 `??`,
0 undef** (supplementary file is **bit-identical** to v2_4_3 — only main
edited). EJOR-bound 20 files **bit-identical** (20 consecutive revisions of
preservation). No theorem, proposition, proof, table data, or numerical
result modified; the 37/11/9/1/9 fire-count breakdown stands. Phase A
(M1 encoding, M2 caption ref, M3 r***/r⋄ rows, M4 wording, M7 "sequential
arrival regimes", M8 ρ note, abstract caveat), Phase B (Wilson CIs, factorial
rationale, Detection-limit warning, log-log regression), v2_4_2 reorganization
(Example 4, Reduction prop, Inheritance prop, sharpness fig in supp; xr
cross-doc), and v2_4_3 substantive content (Proposition 14, §S9
partition-pair table, Operational trade-offs, Policy-dependence of $\F$,
Limitation (iv) closure) all preserved. Manuscript now consistently claims
"4 thresholds, 66 of 67" throughout abstract, §1 contributions, Table 5,
and §6.4. See `docs/v2_4_3_to_v2_4_4_response.md`. Next round: consolidated
R1 response letter.

---

## v2_4_3 (2026-04-26)
**Reviewer R1 revision — Phases C and D (substantive concerns).** Addresses
all four major reviewer concerns with new analytic content; closes the
analytic gap on the intermediate-coalition mechanism (Concern 1) by
introducing **Proposition 14 (general partition-pair Bondareva–Shapley
threshold)** that certifies all 9 intermediate-coalition empty-Core cases of
Observation 15 (renumbered from 14 due to the insertion).

**Phase D-heavy (Concern 1)**: a new analysis script
`code/scripts/intermediate_dual_analysis.py` re-solves the first-stage Core LP
for each of the 9 intermediate cases under nearest-neighbor dispatch and
extracts the dual prices. Result: in every case the dual is supported on
exactly one feasible partition pair $(S,N\setminus S)$ with
$|S|,|N\setminus S|\ge 2$ and the threshold $r^{(P)}_S=[c(S)+c(N\setminus S)]/c^*(N)$
falls strictly below the realized $r$ (margins $0.008$ to $0.152$). This is a
clean Case-A common-balanced-family pattern. The new Proposition 14, inserted
after Proposition 13 (balanced-near-complement), states the general
partition-pair Bondareva–Shapley threshold and certifies all 9 cases. Theorem 9
(single-complement) is the $|S|=1$ special case; Proposition 14 is the first
threshold that *survives* the structural obstruction of Corollary 18 (formerly
17) at $k<n-1$ via non-singleton partition splits. Per-case partition pairs
and thresholds are tabulated in a new Supplementary §S9
(`app:partition-pair-cases`).

**Phase C2 (Concern 2)**: new "Operational trade-offs" paragraph in §7
acknowledging the operational cost of bounding $k<n-1$ (tighter service-time
commitments / increased fleet capacity / more frequent dispatch) and noting
that $k$ is endogenous to arrival/service rate distributions, not a free
control variable; cites Özener & Ergun (2008) as a direction for explicit
fleet-capacity cost integration.

**Phase C4 (Concern 4)**: new Limitation **(v)** in §7. Articulates that the
thresholds' *values* are policy-independent but the family $\F$ *itself*
depends on realized service times, which are policy-determined; lays out the
policy-induced (adopted) versus counterfactual framings.

**Phase D-light (Concern 1, framing)**: rewritten Limitation (iv).
Acknowledges that Proposition 14 closes the analytic gap for the 9 observed
cases and reframes the open question as a *policy-aware* sufficient condition
predicting *which* arrival-service realizations admit such a partition pair,
ideally derived from queueing-theoretic primitives.

**Header-level updates** in main: §1 C2 contributions ("three" → "four
sufficient conditions"); §1 Practical implication ("intermediate-coalition
mechanism" → "partition-pair mechanism of Proposition 14"); §6.4 prose ("9
intermediate cases certified only by the Core LP" → "9 intermediate cases
now certified by Proposition 14"); §7 Conclusion summary ("three complement-
based thresholds … five-mechanism decomposition" → "four analytic thresholds
… 66 of 67 jointly certified, 1 residual"); §7 Limitations ("Four
limitations" → "Five limitations").

Theorem-counter housekeeping: the new Proposition 14 insertion shifted
Observation 14 → 15, Theorem 15 → 16, Remark 16 → 17, Corollary 17 → 18; all
cross-references via `\ref{}` resolved automatically. Pre-existing hardcoded
numbers in supp captions (residual from before v2_4_2) are left as-is — out
of scope for this round.

main_trsc.pdf **35 / 35 pages, 0 ATTENTION, 0 `??` refs, 0 undefined-reference
warnings**; supplementary_trsc.pdf **13 / 15 pages, 0 ATTENTION, 0 `??`,
0 undef**. EJOR-bound 20 files **bit-identical** (19 consecutive revisions of
preservation). All theorem/proof/empirical-fire-count statements unchanged
except the new Proposition 14; no Table 1–8 numerical content modified;
Phase A fixes (M1 encoding, M2 caption ref, M3 r***/r⋄ rows, M4 wording, M7
"sequential arrival regimes", M8 ρ note, abstract caveat), Phase B fixes
(Wilson CIs, factorial rationale, Detection-limit warning, log-log regression),
and v2_4_2 reorganization (Example 4, Reduction prop, Inheritance prop,
sharpness fig in supp; xr cross-doc) all preserved. New code:
`code/scripts/intermediate_dual_analysis.py`. New result files:
`code/results/intermediate_dual_analysis.json`,
`code/results/partition_pair_threshold.json`. See
`docs/v2_4_2_to_v2_4_3_response.md`. Next round: consolidated R1 response
letter.

---

## v2_4_2 (2026-04-26)
**Demote routine results to supplementary; create page room for Phase C/D.**
Reorganizes six routine-illustration / sanity-check / inheritance blocks from
the main manuscript into the supplementary, replacing each with a 1-paragraph
forward pointer. Net page change: main 35→**33** (−2), supp 9→**12** (+3); 35
and 15 limits preserved with comfortable headroom for Phase C (C2 trade-off +
C4 policy-dependence) and Phase D (C1 mechanism analysis). Cross-doc references
are wired via the `xr` package: `\usepackage{xr}` and
`\externaldocument{supplementary_trsc}` added to main; supp already had the
symmetric declaration. Six items moved:

1. **Example 4 (Solomon C101 first 5 customers)** — main §3.2 → Supp §S6.1.
   Main residue: one paragraph pointer. Reviewer M11 (Supp §S2 review):
   "consider relegating to a one-paragraph mention" — applied directly.
2. **Proposition 6 + proof (Reduction at simultaneous arrivals)** — main §4.3
   → Supp §S6.2. Label renamed `thm:static-equiv` → `prop:static-equiv` to
   align with environment type. Main residue: 1-paragraph descriptor including
   the numerical-coincidence sentence (formerly its own §6.2).
3. **§6.2 Verification of Proposition 6** — folded into §4.3 main residue
   (item 2). Full paragraph moved as "Numerical verification" sub-heading
   under Supp §S6.2.
4. **Proposition 19 + proof (Inheritance of Static Core stability)** — main
   §5.2 → Supp §S7. Label renamed `thm:core-inheritance` →
   `prop:core-inheritance`. Main residue: 1-paragraph descriptor noting the
   proposition's operational weakness (informationally weakest in
   simultaneous-arrival regime, vacuous under typical online overhead).
   Reviewer M10: "theoretically sharp but practically vacuous" — addressed
   directly in main residue and Supp §S7 commentary.
5. **§4.2 "Algorithmic details (two-tier scope)" paragraph** — main §4.2 →
   Supp §S3 (`app:algorithmic-details`, appended). Main residue: 1-sentence
   pointer.
6. **Figure 4 (sharpness histogram, fig5_rstar_vs_rss.pdf)** — main §6.6 →
   Supp §S8 (`app:sharpness`, `fig:rhist`). Main §6.6 prose preserved
   verbatim; only the figure inclusion moved. Main ends with a cross-doc
   forward pointer.

External main-side references that previously cited the moved labels were
updated in three locations (lines 134, 588, 771) to
`Supplementary Proposition~\ref{...}`, `Supplementary Figure~\ref{...}`, and
`(Supplementary~\S\ref{...})` form. Supplementary file gained
`\Fp`/`\CW` macros and theorem-style declarations
(`\newtheorem{theorem}{Theorem}` plus proposition/lemma/corollary/
definition/example/remark) under an independent counter from main; supp
Propositions/Examples are numbered 1, 2, 3, … within supp, with explicit
"Supplementary" prefix in main body text.

main_trsc.pdf **33 / 35 pages, 0 ATTENTION, 0 `??` refs, 0 undefined-reference
warnings**; supplementary_trsc.pdf **12 / 15 pages, 0 ATTENTION, 0 `??`,
0 undef**. EJOR-bound 20 files **bit-identical** (18 consecutive revisions of
preservation). All theorem statements, proofs, lemmas, corollaries, remarks,
observations, equation labels, empirical fire counts, Wilson 95% CIs, log-log
regression slopes, and Finding-3(b) detection-limit text **unchanged**: the
reorganization is purely structural relocation. Phase A fixes (M1 encoding,
M2 caption ref, M3 r*** rows, M4 Definition 3, M7 wording, M8 ρ note,
abstract caveat) and Phase B fixes (Wilson CIs, §6.1 factorial rationale,
Finding 3(b) reposition, log-log regression) all preserved. See
`docs/v2_4_1_to_v2_4_2_response.md`.

---

## v2_4_1 (2026-04-26)
**Reviewer R1 revision — Phase B (statistical reporting).** Addresses TS
Reviewer 1's **Concern 3** (experimental design + statistical reporting)
plus the log-log regression follow-up to Remark 18. Four edits, all in
`paper/main_trsc.tex` plus a one-sentence caption note in
`paper/supplementary_trsc.tex` (Fig S1):

1. **B1 (C3a) — Wilson 95% CIs in Table 7**: each Pattern row's Core-rate
   entry extended from `0.36` → `0.36 [0.20, 0.55]` (and so on for 7 rows
   plus the Overall row); column header → `Core rate [95\% CI]`; caption
   appended with a sentence identifying the bracketed quantities as
   Wilson 95\% intervals and noting the per-pattern (`±20pp`) vs overall
   (`±7pp`) widths. Supp Fig S1 (`fig:core-n`) caption appended with a
   per-cell-CI note (per-cell rates rest on `n=5`, so per-cell CIs are
   wide; concrete example: `4/5=0.80` → `[0.38, 0.96]`).
2. **B2 (C3b) — pattern-selection rationale in §6.1**: added a tight
   paragraph framing the seven patterns as a `(ρ, structure)` factorial
   rather than a `ρ`-only sweep, with `B_medium`/`C` paired at `ρ=2` and
   `D`/`E` paired at `ρ=1` to isolate arrival geometry from arrival rate.
3. **B3 (C3c) — Finding 3(b) repositioning**: 3(b) header now reads
   `(one-sided, weak; see detection-limit warning below)`; the prior
   `Detection-limit caveat` paragraph promoted to
   `Detection-limit warning (n=50 specifically)`, rewritten to state
   outright that 3(b) at `n=50` should be read as a placeholder for
   "intractable to test" (`K=10^4`, per-draw detection probability `~10^{-11}`,
   essentially no evidential weight); only structural claim 3(a) carries
   asymptotic strength. Sampling fraction renamed `K/(2^n-1)` for clarity.
4. **B4 (M-extra, Remark 18 follow-up) — log-log regression**: appended
   one sentence to Finding 1 in §6.8. `r̄**−1` vs `n` regression for
   Pattern A: slope `−0.54` (`R²=0.99`, full eight-point grid
   `n∈{5,7,10,12,15,20,30,50}`) and `−0.62` (`R²=1.00`, scale-up subset
   `n∈{15,20,30,50}`). Empirically close to Theorem 17's `−1/2`, partway
   toward Remark 18's `−1` but still much closer to `−1/2`.

main_trsc.pdf still **35 pages** (Phase B initially overflowed to 36; tightened
the §6.1 rationale paragraph and the Finding 1 regression sentence to fit),
both PDFs **0 ATTENTION**, all 20 EJOR-bound files **bit-identical**
(17th consecutive preservation), all theorem statements/proofs/empirical
fire-counts unchanged, all numerical Pattern rates unchanged (CIs are
pure additions). Phase A's M1 encoding-artifact fix preserved: zero `k¡n`
in PDF text. Phase C (C2 trade-off + C4 policy-dependence of F) and
Phase D (C1 — D-light queueing bound or D-heavy `B_{n-3}` extension; user
decision pending) deferred. See `docs/v2_4_0_to_v2_4_1_response.md`.

---

## v2_4_0 (2026-04-26)
**Reviewer R1 revision — Phase A (critical fixes).** Marks the version-line
transition from `v2_3_x` (pre-submission prep) to `v2_4_x` (post-review
revision). TS Reviewer 1 returned a **Major Revision** recommendation
(positive overall; four major concerns C1–C4 + eleven minors M1–M11). Phase A
processes the typographic, mathematical-notation, and trivial-wording fixes:

1. **M1 (encoding artifact)**: abstract `k<n-1` → `$k<n-1$` (math-mode wrap).
   Eliminates the `k¡n-1` glitch on PDF copy-paste; verified zero `k¡n` in
   post-edit `pdftotext`-equivalent extraction.
2. **M6 (singleton-summation)**: `$\sum_{\{i\}} x_i \le c(\{i\})$` →
   `$x_i \le c(\{i\})$` in §5.1 Remark.
3. **M2 (Fig 1 caption ref)**: `\ref{rem:near-complement}` resolves to Remark
   13 (line 422); 4-pass compile yields zero `??` markers. No source edit
   needed; `paper/supplementary_trsc.tex` bit-identical to v2_3_17.
4. **M3 (Table 1)**: added `r***` (balanced-complement threshold,
   Prop. 12) and `r^(⋄)_min` (Bondareva–Shapley LP optimum, Prop. 14)
   rows after the existing `r**` row.
5. **M4 (§3.2 Definition 3)**: parenthetical "(and used in core constraints
   only for $S\in\Fp$)" rewritten as non-parenthetical clause "with core
   stability constraints imposed only for $S\in\Fp$".
6. **M7 (§5.3 wording)**: "in the steady state" → "for sequential arrival
   regimes" (avoids unwarranted queueing-theoretic connotation).
7. **M8 (§6.1 ρ note)**: appended "(with vehicle speed normalized to $v=1$,
   $\rho = L/\tau$)" to clarify the standard normalization.
8. **Abstract tightening (§1 detailed minor)**: appended caveat
   "(intermediate-coalition emptiness can persist in this regime;
   Observation~\ref{obs:intermediate})" to the $k<n-1$ blocking sentence.

main_trsc.pdf still **35 pages**, both PDFs **0 ATTENTION** boxes,
`paper/supplementary_trsc.tex` and all 11 EJOR originals **bit-identical**
(EJOR-bound files unchanged through 16 revisions: v2_3_3 → v2_4_0). No
theorems, proofs, numerical results, equation labels, or cross-references
modified. Phase B (Wilson CIs / pattern rationale / Finding 3(b)
repositioning) and Phase C/D (trade-off + policy-dependence discussion;
queueing or $B_{n-3}$ extension) deferred to subsequent rounds; full
reviewer response letter to be drafted after Phase D. See
`docs/v2_3_17_to_v2_4_0_response.md`.

---

## v2_3_17 (2026-04-26)
Pre-submission style polish: reduced AI-tell density of compound-hyphenated
modifiers in `paper/main_trsc.tex` from 172 to 147 (-25, -14.5%). Four-tier
edit list, all in `main_trsc.tex` only:

1. **Tier 1 — Chicago §7.86** (-ly adverb + adjective takes no hyphen):
   `moderately-informed` → `moderately informed` (2×),
   `angularly-interleaved` → `angularly interleaved` (1×),
   `dynamically-restricted` → `dynamically restricted` (1×).
2. **Tier 2 — unnecessary / stacked compound modifiers**:
   `cooperative-routing models` → `cooperative routing models` (1×);
   `preserves the no-false-positive guarantee` → `yields no false positives`
   (1×, abstract); `complement-coalition empty-Core mechanisms` →
   `complement-coalition mechanisms for emptying the Core` (3×, paper-defined
   term `complement-coalition` preserved).
3. **Tier 3 — proper-name typography** (residual hyphen → en-dash):
   `Bondareva-Shapley` → `Bondareva--Shapley` (1×),
   `Beardwood-Halton-Hammersley` → `Beardwood--Halton--Hammersley` (1×).
   Other occurrences already en-dashed; `Held--Karp` already correct;
   `Lin-Kernighan` not present (paper uses "LKH").
4. **Tier 4 — math notation** (abstract): `Beardwood--Halton--Hammersley
   square-root rate` → `Beardwood--Halton--Hammersley $\sqrt{n}$ rate`,
   matching §6 usage.

main_trsc.pdf still **35 pages**, both PDFs **0 ATTENTION** boxes,
`paper/supplementary_trsc.tex` and all 11 EJOR originals **bit-identical**
to v2_3_16 (and to v2_3_3 for the EJOR files). All paper terminology
(`single-complement`, `balanced-complement`, `balanced-near-complement`,
`intermediate-coalition`, `complement-coalition`, `Core-fragility`,
`Core-existence`, `arrival-service`, `time-induced`, `nearest-neighbor`,
`cheapest-insertion`, `last-mile`, etc.) preserved unchanged. No theorems,
proofs, numerical results, equation labels, or cross-references touched.
**TS submission package: AI-tell reduced.** See
`docs/v2_3_16_to_v2_3_17_response.md`.

---

## v2_3_16 (2026-04-25)
Single-sentence precision fix at `paper/main_trsc.tex` L228 ("Characteristic
cost versus realized cost" paragraph). The previous sentence claimed
$r^{\ast\ast}$ is "a function of coordinate geometry alone through
$c(\{i\})$, $c(N\setminus\{i\})$, $\cstar(N)$" — technically inaccurate,
since the *minimization index set* $\{i:\,N\setminus\{i\}\in\F\}$ is
determined by realized arrival-service windows, not by coordinates alone.
This is in tension with §6.5 Pattern A discussion where $r^{\ast\ast}$
is "undefined" for some arrival patterns. Revised sentence separates the
two facts: cost values are geometric, applicability and the feasible-
complement index set are temporal.

main_trsc.pdf still **35 pages**, both PDFs **0 ATTENTION** boxes,
`supplementary_trsc.tex` and all 11 EJOR originals **bit-identical** to
v2_3_15. No theorems, proofs, numerical results, equation labels, or
cross-references touched. **TS submission package: internal consistency
restored.** See `docs/v2_3_15_to_v2_3_16_response.md`.

---

## v2_3_15 (2026-04-25)
Novelty reframing (B+): demoted "Temporal Nucleolus" from a primary
contribution to the algorithmic tool used to compute cooperative cost
allocations on the restricted family $\F$. The reviewer-flagged concern
was that the nucleolus-on-$\F$ is structurally a standard Schmeidler
nucleolus computed by the Guajardo–Jörnsten 2015 sequential LP cascade,
not a new solution concept; the genuine novelties are (a) the Online TSG
modeling — $\F$ endogenously induced by arrivals — and (b) the
core-fragility threshold theorems. Four `paper/main_trsc.tex`-only edits:

1. **Title** subtitle reorder: "*Temporal Nucleolus and the Fragility of
   the Core*" → "*Core Fragility and the Temporal Nucleolus*".
2. **Abstract** sentence-4 ("We define the Temporal Nucleolus…") removed
   as a standalone claim; reduced to a parenthetical algorithmic clause
   appended after the threshold-theorem sentence ("Cooperative cost
   allocations on this restricted family are computed via a sequential
   LP cascade (the Temporal Nucleolus)").
3. **Contribution C1** ("We introduce the Temporal Nucleolus…") removed
   as a standalone claim; same algorithmic-tool framing with
   `Section~\ref{sec:nucleolus}` pointer.
4. **§4 header** `\section{The Temporal Nucleolus}` →
   `\section{Cost Allocation: The Temporal Nucleolus}` (label
   `sec:nucleolus` preserved verbatim — all five existing
   `\ref{sec:nucleolus}` callsites continue to resolve).

`paper/supplementary_trsc.tex` **bit-identical** to v2_3_14.
main_trsc.pdf still **35 pages** (and 0 ATTENTION); supplementary_trsc.pdf
still **9 pages** (and 0 ATTENTION). All 11 EJOR originals bit-identical
to v2_3_14 and the entire v2_3_x chain. No theorem statements, proofs,
numerical results, or experiment code modified. **TS submission package:
novelty correctly framed.** See `docs/v2_3_14_to_v2_3_15_response.md`.

---

## v2_3_14 (2026-04-25)
Removed the 3 remaining red "ATTENTION: equation exceeds column width
(240 pt)" boxes from `supplementary_trsc.pdf` — discovered in v2_3_13 as
pre-existing since v2_3_11 (carried forward from earlier versions because
prior verification only counted ATTENTION boxes in main). Three display
equations were broken into multi-line form with `\\` line breaks (math
content unchanged):

1. §S3 first-stage nucleolus LP `align` (objective + constraint pair):
   single row → 2-row split, one constraint per row.
2. §S4 *Balancing LP* preface: $B_{n-1}$ and $B_{n-2}$ definitions
   `\[ B_{n-1} = ..., B_{n-2} = ... \]`: single line → 2-row `aligned`,
   one definition per row.
3. §S4 sharpest-threshold definition `r^{(\diamond)}_{\min} := \min\{ ... \}`:
   long set-builder on one line → 3-row `aligned`, one constraint per row.

**Both PDFs are now ATTENTION-free**: main 0/0 (preserved from v2_3_12),
supp **0/3** (down from 3). main_trsc.pdf still **35 pages**;
supplementary_trsc.pdf still **9 pages**. `main_trsc.tex` bit-identical
to v2_3_13. All 11 EJOR originals bit-identical to v2_3_13 (and earlier
v2_3_x). v2_3_12 and v2_3_13 zips preserved on disk untouched.
**TS submission package: production-warning-clean.** See
`docs/v2_3_13_to_v2_3_14_response.md`.

---

## v2_3_13 (2026-04-25)
Targeted reviewer-pre-check repairs, layered on top of v2_3_12. Four edits:
1. **Supp §S1 prose + figure caption rewritten to match `policy_comparison_v2_full.csv`.**
   Prior text claimed "B_medium, B_light, D, E retain 100% Core existence
   across all $n$"; re-aggregation shows only B_light and D actually do.
   New text reports the correct per-pattern × n rates for all seven patterns.
2. **Abstract closing sentence + §1 *Practical implication* closing sentence**
   reworded from "preserve Core stability" to "structurally block all
   complement-coalition empty-Core mechanisms ... substantially improve
   empirical Core stability", with explicit acknowledgment that intermediate-
   coalition emptiness remains logically possible at high competitive ratios.
3. **§5.1 Proposition 15 discussion** reworded: dropped "strict generalization"
   in favor of "refinement on the subdomain $\F\supseteq B_{n-1}\cup B_{n-2}$",
   with explicit note that Propositions 12 and 15 have different applicability
   domains.
4. **Table 1 entry for $\F$** harmonized with Definition 2: now reads
   "$S\in\F$ iff $|S|=1$ or $\max_{i\in S} a_i < \min_{i\in S} s_i$" instead
   of the now-deprecated "$\CW(S)\neq\emptyset$" form.

main_trsc.pdf still **35 pages** (unchanged); supplementary_trsc.pdf still
**9 pages**. ATTENTION boxes in main: **0** (preserved from v2_3_12). All
EJOR originals (11 files) bit-identical to v2_3_12. No theorem statements,
proofs, numerical results, or experiment code modified. **TS submission
package: data integrity restored, claims appropriately hedged.**
See `docs/v2_3_12_to_v2_3_13_response.md`.

---

## v2_3_12 (2026-04-25)
Removed all 6 red "ATTENTION: equation exceeds column width (240 pt)" boxes
from `main_trsc.pdf`. Each was a display-math equation `\[ ... \]` that
exceeded the 240 pt double-column width that the INFORMS production stage
will eventually use. Six display equations were broken into multi-line
`\begin{aligned}...\end{aligned}` form (math content unchanged; only line
breaks added):

1. L220 Temporal Core definition `Core(N,c,F) := { ... }`
2. L269 numeric allocation example `(x_1,...,x_5) = (16.67,...,16.44)`
3. L286 Temporal Nucleolus definition `TNu(N,c,F) := arglexmin{...}`
4. L364 `δ_i := ...` and `r^{**} := ...` joint definition (Theorem 11)
5. L474 Step-1 inequality chain `0 ≤ δ_{i⁰} ≤ ...` (proof of Theorem 17)
6. L486 Step-3 ratio chain `r^{**} - 1 = ... = O(n^{-1/2})` (proof of Theorem 17)

main_trsc.pdf still **35 pages** (unchanged); supplementary_trsc.tex
**bit-identical** to v2_3_11; supp PDF still 9 pages with identical
content (only build-timestamp metadata differs in PDF bytes). All EJOR
originals (11 files) bit-identical to v2_3_11. **TS submission package
clean of cls warnings.** See `docs/v2_3_11_to_v2_3_12_response.md`.

---

## v2_3_11 (2026-04-25)
Documentation cleanup only: ensures `docs/v2_3_9_to_v2_3_10_response.md` and
the v2_3_10 entry in this file are present in the shipped archive (both were
authored on disk during v2_3_10 but the v2_3_10 zip was assembled before the
docs were written, so both were missing from that archive). No source or PDF
changes — `main_trsc.pdf`, `supplementary_trsc.pdf`, and `cover_letter_trsc.pdf`
remain bit-identical to v2_3_10. **TS submission package final, archive
self-consistent.**

---

## v2_3_10 (2026-04-25)
Cosmetic cleanup of v2_3_9 supplementary Overview. Two edits, both confined
to a single paragraph in `paper/supplementary_trsc.tex` (Overview, L77):
1. "It contains **four** parts" → "It contains **five** parts" (since §S5
   was added in v2_3_9).
2. One-sentence description of §S5 inserted after the §S4 description, before
   the closing sentence about main-manuscript labels.

`main_trsc.tex` is **bit-identical** to v2_3_9. main_trsc.pdf still 35/35,
supp_trsc.pdf still 9/15. EJOR originals (11 files) bit-identical to all
prior v2_3_x. **TS submission package finalized at the limit, cosmetic
loose ends closed.** See `docs/v2_3_9_to_v2_3_10_response.md`.

---

## v2_3_9 (2026-04-25)
Page-limit fix for TS submission. main_trsc.pdf reduced 36 → **35 pages** (at the
35-page TR-SC limit). Three cumulative edits, all on `main_trsc.tex` and
`supplementary_trsc.tex` only:
1. §6.7 second commentary paragraph compressed (122 → 63 words; Stage 2).
2. §6.8 *Solver and calibration* paragraph moved verbatim into Supplementary §S3
   (Stage 2); main retains a one-sentence pointer.
3. §6.7 *Robustness to dispatch policy* moved verbatim into Supplementary as
   new §S5 (Stage 4); main retains a 2-sentence summary subsection (label
   `ssec:policy` preserved so all 5 existing cross-references continue to
   resolve to the summary location).

Supp grew 7 → 9 pages (well within 15-page limit). All EJOR originals (`main.tex`,
`supplementary.tex`, both PDFs, highlights, cover letter, bib, cls, bst) remain
**bit-identical** to v2_3_8. **TS submission package re-finalized at the
page limit.** See `docs/v2_3_8_to_v2_3_9_response.md`.

---

## v2_3_8 (2026-04-25)
TS cover letter compressed from 516 words / 2 pages to 385 words / 1 page.
Same content and reviewers; tighter phrasing. **TS submission package finalized.**
See `docs/v2_3_7_to_v2_3_8_response.md`.

---

## v2_3_7 (2026-04-25)
Task D: Transportation Science cover letter created (`paper/cover_letter_trsc.md`,
`.pdf`). Suggests Toriello, Schiffer, Ulmer as reviewers. EJOR cover letter
preserved as fallback. **TS submission package complete.**
See `docs/v2_3_6_to_v2_3_7_response.md`.

---

## v2_3_6 (2026-04-25)
Task C: Related Work subsections 2.2 (Online Cooperative Games) and 2.3
(Restricted Cooperation Games) swapped for TS reader flow. Atomic block
reorder; no text edits. Compile test: 34 pages (within TS 35-page limit).
See `docs/v2_3_5_to_v2_3_6_response.md`.

---

## v2_3_5 (2026-04-25)
Task B: Abstract rewritten for Transportation Science (Version A, Last-Mile
Operations framing). 263 words. No other content changes.
See `docs/v2_3_4_to_v2_3_5_response.md`.

---

## v2_3_4 (2026-04-25)
Added Transportation Science submission skeleton (Task A).
Parallel track to existing EJOR submission. No content changes.
See `docs/trsc_conversion_report.md`.

---

# Response to Technical Check Results

Manuscript: *Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals*
Authors: Seyun Jeong, Hyunchul Tae
EJOR Manuscript ID: [to be filled by the authors at resubmission]
Branch of the revised source: `revision/v2_3_0` (parent: `840d505 chore: import v2_2_8 baseline`).

---

## 1. Summary

This document covers every change made relative to the version that underwent the technical check. Three categories are disclosed separately so the source of each change is unambiguous.

- **Revision 4 (APA bibliography style)** is the single item that directly responds to the technical check. Section 2 reproduces the technical check comment and our response.
- **Revisions 1, 2, and 5** are minor internal-consistency edits that the authors identified during resubmission preparation. None of them changes the statement of any theorem, proposition, corollary, or lemma; none changes the Temporal Core / Temporal Nucleolus algorithms or the code logic; none changes any experimental table, figure, or numerical value. The per-item invariants are documented in Section 3 and are backed by verification artifacts listed in Section 5.
- **Revision 3 (policy-independence wording)** was examined and confirmed to be already present verbatim in the submitted v2_2_8 manuscript. It is a null change and is documented for completeness in Section 4.

Section 6 provides an explicit scope disclosure covering the totality of the edits.

---

## 2. Response to Technical Check Comment

> **Technical check comment.** "Referencing must be APA with the reference list arranged alphabetically. Please refer to the 'reference style' section of the Guide for Authors."

**Response.** The bibliography style has been replaced from `plainnat` to `apalike-ejor.bst` (`adam-rumpf/apalike-ejor`, v1.2.0), an APA-like BibTeX style specifically aligned with the EJOR *Guide for Authors* reference conventions. This produces:

- an ampersand ("&") connector between author names,
- `volume(issue), page` format with a comma separator between the volume/issue pair and the page range,
- hyperlinked DOI and URL fields (via `hyperref`),
- alphabetical ordering of the reference list.

The rendered output was verified against the EJOR *Guide for Authors* and sample articles in the journal. No reference-list content (authors, titles, years, venues, DOIs) was modified; only the typographic rendering changed. Two arXiv preprint entries (`aziz2025participation`, `goyal2025temporal`) received a `url` field addition so that the arXiv identifier is rendered as a hyperlink; the `howpublished` field and all other fields in those entries are unchanged. A sample of five rendered entries covering the common patterns (three-author article, single-author article, arXiv preprint, same-author-same-year `2016a`/`2016b` disambiguation) is available in `paper/main.bbl`; `bibtex` produced zero warnings on the three-pass build.

Files touched: `paper/main.tex`, `paper/supplementary.tex` (bibstyle line only), `paper/apalike-ejor.bst` (new file, 1 221 lines), `paper/references.bib` (two `url` fields added, no other changes).

---

## 3. Author-Initiated Internal-Consistency Polish

The following three revisions were not requested by the technical check. They were identified during the authors' own pre-resubmission review as minor internal-consistency issues that improve the manuscript's clarity without altering its results.

### R1. Tighten `\Fp` usage in Definition 3 and Proposition 12 proof

- **Scope.** Two text-only edits in `main.tex` that still wrote `\F` in positions where `\Fp` (the proper-feasible-coalition family `\Fp := \F \setminus \{N\}`, already defined in v2_2_8 at line 151) was the set actually intended:
  - Definition 3 parenthetical (line 155): `"used in core constraints only for $S\in\F$"` → `"... only for $S\in\Fp$"`.
  - Proposition 12 (static-core-inheritance) proof (line 438): `"For any $S\in\F\subseteq 2^N\setminus\{\emptyset\}$"` → `"For any $S\in\Fp\subseteq 2^N\setminus\{\emptyset, N\}$"`.
- **Invariants preserved.** Definition 3 (Temporal Core), Definition 5 (Temporal Nucleolus), the first-stage LP (eq.\ (1)), Proposition 12 (balanced-complement threshold), Proposition 15 (balanced-near-complement threshold), Corollary 20 (structural obstruction) — all statements unchanged. The supporting code (`code/src/nucleolus.py`, lines 30–31) already excluded the grand coalition from LP constraints before this revision; no code change.
- **Motivation.** Eliminate a reader-facing inconsistency between the already-introduced `\Fp` convention and two residual mentions of `\F`. No experimental output is affected.

### R2. Closed-interval convention for the common waiting window

- **Scope.** Definition 1 (`def:cw`) redefines `\CW(S)` from the half-open intersection `\bigcap_{i\in S}[a_i, s_i)` to the closed intersection `\bigcap_{i\in S}[a_i, s_i]`. Definition 2 (`def:feasible`) is reformulated to branch explicitly on coalition size: singleton `S` is always feasible; for `|S| >= 2`, the feasibility criterion is the strict inequality `\max_{i\in S} a_i < \min_{i\in S} s_i`, equivalently `\CW(S)` has a non-empty open interior. The separate "singleton convention" clause of v2_2_8 (line 151) is removed because singleton feasibility now follows automatically from the closed-interval `\CW`. Table 1, Example 4, and the §2.3 Related-Work inline recap of `\CW` are updated for consistency.
- **Invariants preserved.**
  - Lemma 9 (feasibility of `N \setminus \{i\}`) and Lemma 10 (fully-sequential arrivals preclude `N \setminus \{i\}`) statements are unchanged. Their proofs continue to rest on the half-open `U_t = \{i : a_i \le t < s_i\}` of Table 1, which was not altered.
  - The feasibility code `code/src/feasibility.py` (lines 56–58 for singletons, lines 60–66 for `|S| >= 2` with strict criterion `max_a < min_s - tol`) already matched the revised Definition 2 prior to this revision; no code change was needed. Four boundary-case unit tests (Section 5) confirm the paper–code equivalence on singletons with `s_i = a_i`, on `|S| = 2` with shared boundary `a_j = s_i`, on `|S| = 2` with proper overlap, and on `|S| = 2` with non-overlap.
  - Example 4 numerical values are unchanged: the feasible family `\F` consists of the 5 singletons (no multi-customer coalition meets the strict criterion), and re-computing the Temporal Nucleolus from the revised `\F` with the paper's published `c({i})` and `C(N)_online = 80.059` reproduces the published allocation `(16.67, 20.51, 11.27, 15.18, 16.44)` to three decimal places, with `core_eps = -52.29 <= 0` confirming the Core-non-empty conclusion.
  - All theorems, propositions, corollaries, lemmas, and experimental results remain unchanged.
- **Motivation.** Remove a latent tension where a singleton with `s_i = a_i` would have `\CW(\{i\}) = [a_i, a_i) = \emptyset` under the half-open definition of v2_2_8, forcing the manuscript to insert a separate "by convention" clause asserting singleton feasibility. Under the closed-interval convention, singleton feasibility is automatic, and the operationally meaningful strict-inequality criterion for `|S| >= 2` is preserved exactly.

### R5. Move Proposition 15 full proof into the main text

- **Scope.** The full proof of Proposition 15 (balanced-near-complement threshold, a central sufficient condition of the paper) was previously given as a six-line "Proof sketch" in the main text with "Full argument in Supplementary Materials §S4." The full proof is now in the main text directly. Supplementary Materials §S4 retains only the coverage-audit diagnostic (Table S6 and the seed-42 residual discussion).
- **Invariants preserved.** The statement of Proposition 15 is unchanged. The proof content is identical to the version previously in §S4; no new mathematical result is introduced. The main-text cross-references to §S4 at lines 353 and 769 remain valid, as they point to the coverage audit that remains in §S4.
- **Motivation.** Improve the main text's self-containedness for a central sufficient condition without expanding its length materially.

---

## 4. Null Change

### R3. Policy-independence wording (Section 6.7)

The authors re-examined Section 6.7's statement of the policy-dependence of the `r**` and `r***` thresholds and confirmed that v2_2_8 already contains the desired two-tier framing verbatim at line 676:

> "The threshold *values* `r**` and `r***` are functions of TSP costs and the arrival sequence alone (not service times), hence policy-independent; the threshold *applicability* (whether `N\{i} \in F`) depends on service times and is therefore weakly policy-dependent."

No edit was made.

---

## 5. Deliverables and Verification Artifacts

**Revised source files.**
- `paper/main.tex` — Revisions 1, 2, 5.
- `paper/supplementary.tex` — Revision 5 (§S4 retained as coverage audit).
- `paper/apalike-ejor.bst` — new file, Revision 4.
- `paper/references.bib` — Revision 4 (two `url` fields added to arXiv preprints).

**Rebuilt outputs.**
- `paper/main.pdf` — 31 pages, rebuilt with `pdflatex + bibtex + pdflatex × 2`, zero errors, zero undefined references, zero `bibtex` warnings.
- `paper/supplementary.pdf` — rebuilt with the same pipeline.

**Verification artifacts.** The claims in Sections 2 and 3 are supported by the following checks, whose outputs are on file with the authors:
1. Four boundary-case unit tests for the revised Definition 2 (R2), comparing paper-stated feasibility against `code/src/feasibility.py` on `S = {i}` with `s_i = a_i`, on `|S| = 2` with shared boundary `a_j = s_i`, on `|S| = 2` with proper overlap, and on `|S| = 2` with non-overlap. All four cases produce identical paper and code verdicts.
2. Example 4 Nucleolus re-computation driving `code/src/nucleolus.py` with the revised `\F` (five singletons) and the published `c({i})` and `C(N)_online`. The output matches the paper's published allocation to three decimal places.
3. Bibliography-rendering sample: five entries extracted from `paper/main.bbl` after the three-pass rebuild, covering three-author articles, single-author articles, arXiv preprints (post-`url` field addition), and same-author-same-year `2016a`/`2016b` disambiguation.

**This document.** `REVISION_NOTES.md` at the repository root.

---

## 6. Scope Disclosure

- No peer-review-relevant content — the abstract, the introduction, the related-work scope, the model or theory statements, the experimental methodology, the numerical results, or the conclusions — has been substantively altered beyond the items disclosed in Sections 2 through 4.
- No new theorem, proposition, corollary, lemma, example, or experimental result is introduced.
- No table or figure is added, removed, or numerically changed. `Tables 5–9` of the main text and all Supplementary Materials tables carry their v2_2_8 values unchanged.
- All bibliographic content (authors, titles, years, venues, DOIs) is unchanged; only the rendering style differs, and two `url` fields were added to existing arXiv entries for hyperlink rendering.
- No change was made to the code base (`code/src/*.py`, `code/scripts/*`, `code/experiments/*`) or to any result CSV (`code/results/*.csv`).

Commit trail on the `revision/v2_3_0` branch (most recent last):
`117fd72` R1, `5f7a0b8` R2, `2459569` R4 (style switch), `09f17f4` R5, `ea165c6` build (rebuild PDFs), `ccd08f8` docs (prior version of this document), `a1efa22` R4 followup (arXiv URL fields).

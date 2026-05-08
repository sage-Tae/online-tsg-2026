# Online Traveling Salesman Games

Code and data for the paper:

> **Online Traveling Salesman Games: Core Fragility and the Temporal Nucleolus under Dynamic Arrivals**
> Seyun Jeong and Hyunchul Tae (Korea Institute of Industrial Technology)
> Submitted to *Transportation Science* (INFORMS), 2026

**Current version: v2.7.0** (External-review compliance, 2026-05-07)

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which customers arrive over time and costs must be allocated only
among coalitions realizable under revealed arrival dynamics. This repository
contains all code, seeds, and raw results needed to reproduce the paper's
numerical claims.

## Key results (sanity checkpoints, v2.8.0)

> **Theorem-numbering note.** Phase 1 of the v2.8.0 polish reorganized §5.1
> so that the general partition-pair statement is labeled as a Theorem and
> the three special cases are labeled as Corollaries (the underlying numerical
> claims are unchanged). The mapping is: original Theorem 9 → Corollary 9
> (single-complement specialization); original Proposition 10 → Corollary 10
> (balanced-complement specialization); original Proposition 13 → Corollary 13
> (balanced-near-complement specialization); original Proposition 14 →
> Theorem 14 (general partition-pair certificate).

| Paper location | Quantity | Value |
|---|---|---|
| Supplementary §S6 (Solomon C101) | TNu allocation | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 5 | Corollary 9 single-complement fires (NN, 96 applicable) | 37/37 (no false positives) |
| Table 5 | Corollary 10 balanced-complement fires (NN, 80 applicable) | 57/57 (no false positives) |
| Table 5 | Corollary 13 balanced-near-complement fires (NN, 10 near-complement) | 9/10 (no false positives) |
| Table 5 | Theorem 14 partition-pair certificate (NN, 9 intermediate cases) | 9/9 |
| §6.4 | Four-threshold joint coverage of NN empties | 66/67 |
| §6.4 | Five-mechanism decomposition of 67 NN empties | 37 + 11 + 9 + 1 + 9 |
| Corollary 19 (§6.4) | k < n−1 Core empirical nonempty rate | 70/79 (88.6%; 9 intermediate-mechanism exceptions) |
| §6.6 | Sharpness ratio r̄*/r̄**, r̄*/r̄*** | 3.56 (4.351/1.223), 3.97 (4.351/1.096) |
| Supplementary §S2 | Scale invariance (r relative std across α) | 0.00e+00 |
| Supplementary §S3 | Near-complement cases (Supp. Table) | 10 |
| Supplementary §S3 | Intermediate cases (Supp. Table) | 9 |
| Supplementary §S8 | Partition-pair certificates (Theorem 14) | 9/9 |
| Supplementary §S4 | $B_{n-3}$ closure attempt (Phase 2 Branch B) | seed 42 still negative ($-3.45\times 10^{-4}$) |

The corresponding cached outputs are committed in this repo for verification:

- `code/experiments/logs/policy_comparison_v2_full.csv` — 525 NN/CI/BR pairs (67 NN empties)
- `code/results/near_complement_coverage_check.csv` — Corollary 13 LP audit (9/10 fires)
- `code/results/near_complement_coverage_check_k3.csv` — Phase 2 $B_{n-3}$ attempt (still 9/10)
- `code/results/intermediate_dual_analysis.json` — Theorem 14 partition-pair certificates (9/9)
- `code/results/summary.csv`, `code/results/theorem5_validation.csv` — per-instance row data

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

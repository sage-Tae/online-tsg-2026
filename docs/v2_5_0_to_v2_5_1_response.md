# v2.5.0 → v2.5.1 Response

## Goal

Bring `paper/main_ejor.pdf` from 33 pages (v2.5.0) to ≤30 pages, the limit
EJOR's Guide for Authors imposes on article + abstract + figures + tables +
references + appendices. Plus two minor follow-ups deferred from v2.5.0:
the supplementary Overview gap and the cover-letter metadata layout.

## Result

| File                          | v2.5.0 | v2.5.1 | Δ    |
|-------------------------------|-------:|-------:|-----:|
| `paper/main_ejor.pdf`         | 33 pp  | **30 pp** | −3 pp |
| `paper/supplementary_ejor.pdf`| 13 pp  | 13 pp  | 0    |
| `paper/cover_letter_ejor.pdf` | 2 pp   | 2 pp   | 0    |

The 30-page cap is met exactly. The supplementary grew in section count
(S1–S9 → S1–S10) but stayed at 13 pages because the lifted Lemmas 4–5
(formerly main Lemmas 7–8) are short and §S8/§S9/§S10 share page 11.

## Per-edit page-count delta

| Edit | Estimated saving | Measured cumulative | Notes |
|------|-----------------:|--------------------:|-------|
| A: References typography  | ~0.8–1.0 pp | landed at 31 pp with `\small` | needed `\footnotesize` to land at 30 |
| B: Lift Lemmas 7/8 to §S8 | ~0.5 pp     | (combined with A, C, D) | clean lift; cor:cor51 proof citation updated |
| C: Merge Remarks 5/6      | ~0.25 pp    | ditto | both labels retained on merged remark |
| D: Limitations enumerate  | ~0.6 pp     | ditto | `enumitem` tight settings (`itemsep=2pt,topsep=2pt`) |
| Step-7 fallback: abstract trim + drop "Practical implication" heading | (fallback) | 30 pp | content folded into Contributions tail |

The four planned edits alone produced a 31-page build (saved ~2 pages
combined, less than the 3.5-page summed estimate). The Step 7 verification
gate's fallback was applied: the abstract was trimmed by ~30 words and the
`\paragraph{Practical implication.}` heading was dropped (its content was
folded into a continuation paragraph after the C1–C4 itemize). With these
plus tightening Edit A's bibliography font from `\small` to `\footnotesize`,
the build landed at 30 pages exactly. No theorem, table, figure, or
numerical result was altered.

## Final supplementary section list

| Section | Title                                                         | Was       |
|---------|---------------------------------------------------------------|-----------|
| §S1     | Per-pattern Core-existence breakdown                          | §S1       |
| §S2     | Scale invariance: empirical verification                      | §S2       |
| §S3     | Restricted Core LP and mechanism classification               | §S3       |
| §S4     | Balanced-near-complement: coverage audit                      | §S4       |
| §S5     | Robustness to dispatch policy                                 | §S5       |
| §S6     | Illustrative example and reduction at simultaneous arrivals   | §S6       |
| §S7     | Inheritance of static Core stability                          | §S7       |
| §S8     | **Auxiliary feasibility lemmas** *(new)*                      | —         |
| §S9     | Partition-pair certification of the 9 intermediate cases      | was §S8   |
| §S10    | Threshold-distribution histograms                             | was §S9   |

§S8's two lemmas are numbered Lemma 4 and Lemma 5 in the supplementary's
local theorem counter (Example 1, Proposition 2, Proposition 3, then
Lemma 4, Lemma 5). The main manuscript references them as
"Supplementary Lemma~\ref{lem:lemma51}" / "Supplementary Lemma~\ref{lem:lemma52}",
which xr resolves to "Supplementary Lemma 4" / "Supplementary Lemma 5".

## Theorem numbering preservation

The four edits incidentally shifted the main theorem counter by −3 (lifting
2 lemmas + merging 2 remarks). Per the task spec ("the main-text numbering
must survive bit-for-bit"), an `\addtocounter{theorem}{3}` was placed
immediately before `\begin{theorem}\label{thm:empty-core}` to restore the
v2.5.0 numbering. Verified post-build:

| Label                              | v2.5.0 | v2.5.1 |
|------------------------------------|--------|--------|
| `thm:empty-core`                   | 9      | **9** |
| `prop:bondareva-complement`        | 10     | **10** |
| `cor:cor51`                        | 11     | **11** |
| `rem:near-complement`              | 12     | **12** |
| `prop:balanced-near-complement`    | 13     | **13** |
| `prop:partition-pair`              | 14     | **14** |
| `obs:intermediate`                 | 15     | **15** |
| `thm:asymptotic`                   | 16     | **16** |
| `rem:asymptotic-tighter`           | 17     | **17** |
| `cor:cor52`                        | 18     | **18** |

(Remark 6 from v2.5.0 was the `r^*`-ratio restatement; merging it into
Remark 5 leaves "Remark 6" unused. No external reference points to
Remark 6, so this is invisible to the cover letter and to the supplementary.)

## Verification gates

All seven Step-7 gates passed.

1. **Page count ≤ 30.** `main_ejor.pdf` = 30 pages (PyMuPDF + macOS
   `mdls -name kMDItemNumberOfPages`).
2. **No broken refs (??).** 0 occurrences in `main_ejor.pdf`,
   0 in `supplementary_ejor.pdf`.
3. **No undefined-reference warnings.** `grep -i undefined` on the two `.log`
   files returns nothing (after excluding the expected `multiply defined`
   warnings from `xr` cross-document citation overlap).
4. **bibtex exit codes 0.** Both `main_ejor.blg` and `supplementary_ejor.blg`
   report `warning$ -- 0` and no errors.
5. **Manual main spot-check.** References render in single-spacing footnotesize;
   Theorem 9 (was 9) intact; Corollary 11 references "Supplementary Lemma 5";
   Limitations renders as `enumerate` `(i)`–`(v)`.
6. **Manual supplementary spot-check.** §S1 through §S10 with no gaps;
   §S8 = Auxiliary feasibility lemmas with Lemmas 4 and 5; §S9 = Partition-
   pair certification; §S10 = Threshold-distribution histograms.
7. **Cover letter.** `To`, `Journal`, `Date`, `Re` render as four separate
   visible lines (Markdown trailing-`\` line-breaks). `§S8` reference in the
   Reproducibility section updated to `§S9` to track Edit B's renumbering.

## Surprises and improvisations

**Missing figure files.** The v2.5.0 distribution does not bundle the figure
PDFs (the original 33-page build referenced `../figures/` which is not in
the zip). Without them, pdflatex falls back to `[draft]` placeholders that
collapse to near-zero height, distorting layout. To get a faithful page
count, five placeholder PDFs (`fig2_r_vs_rstar.pdf`, `fig3_core_vs_k.pdf`,
`fig4_coalition_reduction.pdf`, `fig3_core_vs_n.pdf`, `fig5_rstar_vs_rss.pdf`)
were generated in `figures/` with PyMuPDF, with page sizes matching the
exact `BBox` dimensions of the corresponding Form XObjects in the original
PDFs (extracted via PyMuPDF). The placeholder files contain a thin gray
border and a label, but the layout is identical to a real-figure build.
Figure regeneration is still flagged as deferred.

**Bibliography compression had to go aggressive.** The plan's `\small` font
saved less than expected (~0.4 pages, not 0.8). I used `\footnotesize` to
land at 30 pages, plus `\bibsep` tightened to `1pt plus 0.2ex minus 0.2ex`.
References remain readable but visibly tighter than v2.5.0.

**Step 7 fallback was needed.** After Edits A–D the build was 31 pages.
The plan's fallback (abstract trim + drop "Practical implication" heading)
was applied as written; together with the bibliography font tightening this
landed at 30 pages.

**Pandoc pipe-table for the cover letter metadata didn't work.** The plan's
proposed pipe-table form rendered as literal pipe-separated text because
pandoc requires a header separator row to recognise it as a table. The plan
already noted this fallback ("if pandoc's pipe-table rendering misbehaves,
fall back to literal `\\` line breaks"); applied the trailing-`\`
Markdown form, which renders cleanly with one line per metadata field.

**Theorem-counter restoration.** Not anticipated by the plan but required
by the "main-text numbering must survive bit-for-bit" guardrail. Achieved
with a single `\addtocounter{theorem}{3}` immediately before Theorem 9; this
restored Theorem 9, Prop 10, Cor 11, Rem 12, Prop 13, Prop 14, Obs 15,
Thm 16, Rem 17, Cor 18 to their v2.5.0 numbers. Documented inline with a
TeX comment explaining why.

**Cover-letter `§S8` reference.** Edit B renumbered the partition-pair
section from §S8 to §S9 in the supplementary; the cover letter's
Reproducibility paragraph mentioned `§S8` and was updated to `§S9` for
consistency. Cover-letter `Date` field was updated to the build date
(2026-05-02).

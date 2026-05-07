# Phase 1 Summary — Hierarchy Restructure

Branch: `phase1-hierarchy`

## Goal
Promote the most general result of §5.1 (formerly Proposition 14, "General
partition-pair threshold") to a Theorem, and demote the three special cases
(formerly Theorem 9, Propositions 10 and 13) to Corollaries that are explicitly
labeled as specializations.

## Label mapping

| Role (post-Phase 1)          | New label                          | Old label                            | Auto-rendered number |
|------------------------------|------------------------------------|--------------------------------------|----------------------|
| Theorem (general)            | `thm:partition-pair`               | `prop:partition-pair`                | Theorem 14           |
| Corollary (specialization)   | `cor:single-complement`            | `thm:empty-core`                     | Corollary 9          |
| Corollary (specialization)   | `cor:balanced-complement`          | `prop:bondareva-complement`          | Corollary 10         |
| Corollary (specialization)   | `cor:balanced-near-complement`     | `prop:balanced-near-complement`      | Corollary 13         |

The historical numbering (Theorem 9 / Proposition 10 / Proposition 13 /
Proposition 14) is preserved by the `\addtocounter{theorem}{3}` hack at the
start of §5.1, so the new Corollaries and Theorem inherit the same numbers as
the originals.

## Structural edits (main_ejor.tex)

- §5.1 environments swapped: `theorem`→`corollary` for the three specializations,
  `proposition`→`theorem` for the general partition-pair certificate.
- §5.1 introduction merged into a single `\paragraph{Hierarchy and computability.}`
  block that names Theorem 14 as the general result and lists the three
  specializations with computability character (a priori vs post-hoc).
- Three specialization-pointer sentences inserted at the start of each
  Corollary's discussion paragraph, identifying the corresponding case of
  Theorem 14.
- "Relationship to earlier thresholds" paragraph compressed (option B trim);
  redundant "certificate-vs-predictive-bound" sentence removed (now stated
  once in the merged hierarchy paragraph).
- §6.4 "Load parameter ρ" paragraph compressed to one sentence (option A trim).
- Counter comment at line 289 refreshed to describe the new role-mapping.
- Table caption (`tab:threshold-hierarchy`) and the table label-column
  abbreviations (`Thm.`/`Prop.`) updated to match new roles (`Cor.`/`Thm.`).
- Cross-document supplementary references (`xr` package) automatically pick
  up the renamed labels.

## Abstract / Contribution C2 / Highlights / Cover letter

- Abstract reframed: from "three complementary sufficient conditions" to
  "a general partition-pair sufficient condition with three a priori
  computable specializations ranged by sharpness."
- C2 reframed: now leads with the general theorem and lists the three
  specializations under it.
- `highlights.txt` updated (5 bullets, all ≤85 chars verified).
- `cover_letter_ejor.md` "Core contribution" paragraph rewritten with explicit
  "(formerly Theorem 9 / Proposition 10 / 13 / 14)" parentheticals.

## Bibliography typography

- `\bibsep` reduced from `1pt` to `0pt` (with same plus/minus shrink) to
  recover the bibliography from a 3-page to a 2-page block. Net: −1 page.

## Page-budget compliance

| Document                    | Pages | Cap |
|-----------------------------|-------|-----|
| `main_ejor.pdf`             | 30    | 30  |
| `supplementary_ejor.pdf`    | 13    | 13  |
| `cover_letter_ejor.pdf`     | 3     | —   |

## Verification

- `pdflatex` × 2 + `bibtex` × 1 + `pdflatex` × 2 succeeded for both main and
  supplementary; final cross-references resolved (no `Reference … undefined`
  warnings).
- `grep -E "thm:empty-core|prop:bondareva-complement|prop:balanced-near-complement|prop:partition-pair"`
  on both `main_ejor.tex` and `supplementary_ejor.tex` returns empty.
- `awk '{print length}' highlights.txt` confirms all bullets ≤85 chars.
- `pandoc cover_letter_ejor.md -o cover_letter_ejor.pdf` succeeded.
- `\ref` rendering verified via `.aux`: Corollary 9 / 10 / 13, Theorem 14.

## Files modified

- `paper/main_ejor.tex`
- `paper/supplementary_ejor.tex`
- `paper/cover_letter_ejor.md`
- `paper/highlights.txt`
- (rebuilt) `paper/main_ejor.pdf`, `paper/supplementary_ejor.pdf`,
  `paper/cover_letter_ejor.pdf`

# v2.4.6 → v2.5.0 — EJOR resubmission build

After the *Transportation Science* desk rejection on scope grounds
(TS-2026-0253), a parallel EJOR-formatted manuscript tree was built
from the v2.4.6 TS source. The TS tree (`main_trsc.tex`,
`supplementary_trsc.tex`, `cover_letter_trsc.{md,pdf}`) and the older
EJOR baseline (`main.tex`, `supplementary.tex`, `cover_letter.{md,pdf}`)
were left untouched.

## Files created

| Path | Size | Pages |
|---|---|---|
| `paper/main_ejor.tex`            | 103 KB | — |
| `paper/main_ejor.pdf`            | 581 KB | **33** |
| `paper/supplementary_ejor.tex`   |  37 KB | — |
| `paper/supplementary_ejor.pdf`   | 390 KB | **13** |
| `paper/cover_letter_ejor.md`     |   6 KB | — |
| `paper/cover_letter_ejor.pdf`    |  38 KB | **2** |
| `paper/references_ejor.bib`      |  15 KB | — |

`main_ejor.pdf` is one page longer than the older EJOR baseline
(`main.pdf` = 32 pages), reflecting the post-Prop-14 / scale-up
content added during the TS revisions; `supplementary_ejor.pdf` is at
13 pages, matching `supplementary_trsc.pdf`.

## Body edits applied (EJOR tree only)

Line numbers refer to `paper/main_ejor.tex` and
`paper/references_ejor.bib` after the build.

| Fix | Description | Location |
|---|---|---|
| 3a | "four-mechanism" → "five-mechanism" in Section 6.2 first sentence | `main_ejor.tex:530` |
| 3b | Theorem 16 Step 1 aligned block expanded to three explicit lines (insertion bound / monotonicity / numeric distance); mathematical content unchanged | `main_ejor.tex:417`–`421` |
| 3c | Crossref note line stripped from Arroyo entry | `references_ejor.bib:163`–`168` (no `note` field) |
| 3d | Figure 1 caption appended with the safer "n=38" reconciliation phrasing (avoiding the unverified "70" count) | `main_ejor.tex:559` (caption tail) |
| 3e | Abstract: "as n grows" → "as $n$ grows" | `main_ejor.tex:66` |
| 3f | Limitation (ii) and Table 7 (scaleup) footnote: explicit unit qualification on the $r-r^{**}$ margin vs LKH calibration-error comparison | `main_ejor.tex:679` (Table 7 footnote) and `main_ejor.tex:741` (Limitation (ii)) |

`supplementary_ejor.tex` carries no body-content edits beyond the
preamble swap; the body was transferred verbatim from
`supplementary_trsc.tex`.

## Build sequence and log summary

```
pdflatex main_ejor → bibtex main_ejor → pdflatex × 2
pdflatex supplementary_ejor → bibtex supplementary_ejor → pdflatex × 2
pdflatex main_ejor   (final pass to resolve forward xr refs)
```

Final-pass status:

- `main_ejor.pdf`: 33 pages, **0 undefined references** in
  `main_ejor.log`. 5 `natbib Warning: Citation … multiply defined`
  entries from the xr cross-document overlap (same citation registered
  via both `main_ejor.aux` and `supplementary_ejor.aux`); harmless,
  bibliography is correct.
- `supplementary_ejor.pdf`: 13 pages, **0 undefined references** in
  `supplementary_ejor.log`. Same 5 multiply-defined-citation warnings
  from the xr overlap.
- BibTeX (both): exit 0, no `error message` lines, no "I didn't find a
  database entry" warnings (`warning$ -- 0` in both `.blg` files).
- The Arroyo bibliography entry in `main_ejor.bbl` and
  `supplementary_ejor.bbl` is clean — no Crossref-note text bleeding in.

## Surprises and deferred items

- **Figure 1 image text-overlay artifact (deferred).** The
  `fig2_r_vs_rstar.pdf` image still bears a "four-mechanism overlay"
  title text from the older plotting script. The body and caption now
  resolve this in words (Fix 3a + Fix 3d), so the inconsistency does
  not affect the manuscript's logical content, but a re-rendered figure
  would be cleaner. Per the task's scope guardrails, no re-running of
  plotting scripts was attempted; flagged for a future regeneration
  pass.
- **Highlights file (deferred).** The existing
  `paper/highlights.{tex,pdf,txt}` predates Proposition 14 and the
  partition-pair certificate. The README and REVISION_NOTES now state
  that a fresh highlights file is to be drafted before final EJOR
  submission rather than shipping the stale one.
- **`note`-stripping vs. `\AtBeginDocument`.** The task instructions
  offered both an inline-patch and a copy-and-edit path for Fix 3c. The
  copy path (`references_ejor.bib`) was chosen as cleaner: it leaves
  the shared `references.bib` byte-identical to the TS tree's source,
  which keeps the TRSC build reproducible bit-for-bit and avoids any
  need for fragile per-document patching of bibliography fields.
- **Cover letter pandoc command.** No exact build command was recorded
  for the prior `cover_letter_trsc.pdf`. The standard
  `pandoc … --pdf-engine=xelatex -V geometry:margin=1in -V fontsize=11pt`
  was used; output is 2 pages, matching the TS cover letter exactly.
- **EJOR e-companion S-prefix.** `supplementary_ejor.tex` uses the
  EJOR-style `\renewcommand{\thesection}{S\arabic{section}}` (plus the
  matching figure/table renames) rather than the informs4 `\ECHead`
  mechanism, so all internal cross-references already resolve to the
  expected `S1`, `S2`, … numbering and the main manuscript can refer to
  Supplementary Figures/Tables/Sections as `S1`, `S2`, etc. without
  per-citation gymnastics.
- **No theorem statement, proof logic, numerical result, table data,
  figure data, CSV, or `code/src/` file was modified**, per the task's
  guardrails. `paper/main_trsc.tex` and `paper/supplementary_trsc.tex`
  remain bit-identical to v2.4.6.

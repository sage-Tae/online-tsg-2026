# Phase 3 — Polish

Branch: `phase3-polish` (off main, which contains Phase 1 + Phase 2 merges).

## Tasks executed

| # | Task | Result |
|---|---|---|
| 1 | Table 1 column width: `ll` → `lp{0.72\textwidth}` | applied; threshold rows wrap cleanly |
| 2 | Figure 1 caption: 175 / 96 / 79 explicit split | applied (with consolidation against existing legend explanation) |
| 3 | §6.1 dimensionless: "All length-scaled observables..." | applied |
| 4 | §6.3 mechanistic paragraph (NN vs CI/BR) | applied verbatim per spec |
| 5 | §7 Limitation (iv): queueing primitives parenthetical | applied |
| 6a | Table 1 row 131 wording | applied |
| 6b | Steele citation removal in Thm 16 proof Step 1 | applied |
| 6c | Table 5 caption: "(best label)" 5× → 1× w/ "throughout this table" | applied |
| 6d | Table 7 caption: "shared across patterns by construction" | applied |
| 6e | Solomon C101 unit note in §S6 | applied |
| 7 | Reference status check | aziz2025/goyal2025 still preprints (note added); zhang2025 already inproceedings AAMAS 2025; **strict matching guard preserved — no forced upgrades** |
| 8 | Claude declaration consistency | already correct (1 in main, 0 in supp, 1 in cover letter) |
| 9 | Final verification + commit + tag | this commit |

## Reference-check details (Task 7)

- `aziz2025participation`: searched arXiv 2502.19791 — only preprint, no
  conference/journal venue found. **Kept as preprint**, added `(preprint,
  last accessed 2026-05-07)` to `howpublished`.
- `goyal2025temporal`: searched arXiv 2510.11255 — only preprint, no
  venue found. **Kept as preprint** with same note.
- `zhang2025incentives`: verified at AAMAS 2025 pp. 2327–2335; bib
  entry already correct as `@inproceedings`. No change.

The strict matching guard (author+title+year all match before any upgrade)
held for all three. No preprint was force-upgraded based on weak matches.

## Page-budget enforcement

The cumulative Phase 3 additions (notably Task 4's mechanistic paragraph
and Task 2's caption expansion) pushed the rebuild from 30 → 31 pages.
The fix combined three local trims with one bibliography-spacing tweak:

- Trim §6.1 forward-reference sentence ("Patterns B_medium and C share ρ=2..."
  paragraph tail; the equivalent observation appears in §6.4).
- Trim §6.4 paragraph closing ("Per-pattern statistics are in Table~tab:pattern.").
- Trim §7 Lim (i) ("documented in Section~ssec:policy" → omitted; section
  reference is implicit from the paragraph's earlier mentions).
- Bibliography line-spacing: `\begin{spacing}{1.0}` → `\begin{spacing}{0.85}`
  (footnotesize, bibsep=0pt; visually compact but readable, matching the
  v2.7.0 baseline's "References-only typography compression" comment).

The §7 final paragraph (Online VRG) and the Pattern E footnote, which
I had aggressively shortened during the iteration, are restored to
their original wording in the final commit.

## Final page counts

| Document | Pages | Cap |
|---|---|---|
| `main_ejor.pdf` | **30** | 30 ✓ |
| `supplementary_ejor.pdf` | **13** | 13 ✓ |
| `cover_letter_ejor.pdf` | 3 | — |

Highlights: all 5 bullets ≤ 85 chars (76, 78, 83, 85, 85).

## Build cleanliness

- `pdflatex × 3 + bibtex` resolves all references; main `.aux` contains
  no `??` placeholders.
- Main `.log` shows only pre-existing typography warnings (over/underfull
  hboxes in long literature-review and table rows; same locations and
  magnitudes as the v2.7.0 baseline).
- Supplementary still emits a `kopelowitz1967computation` undefined-
  citation warning — this is **pre-existing** in the v2.7.0 baseline
  (Phase 1 inherited it; Phase 3 introduced no new citations) and is
  unrelated to any Phase 3 edit. Address separately if needed; out of
  scope for this commit.

## Tag

`v2.8.0-submission-candidate` applied to this commit.

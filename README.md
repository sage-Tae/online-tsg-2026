# Online Traveling Salesman Games (EJOR 2026)

Code, data, and reproducibility scripts for the paper:

> **Online Traveling Salesman Games: Core Fragility and the Temporal Nucleolus under Dynamic Arrivals**
> Seyun Jeong and Hyunchul Tae
> *Korea Institute of Industrial Technology (KITECH), Cheonan, Republic of Korea*
> Submitted to *European Journal of Operational Research* (under review, 2026)

**Current version:** v2.5.2 (May 2, 2026)

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which the family of feasibility-admissible coalitions is endogenously
induced by the realized arrival–service process — a temporally-induced
restriction that has no direct counterpart in the graph-restricted or
antimatroid-restricted families of classical restricted-cooperation theory.
On this restricted family we define the *Temporal Nucleolus* as the
lexicographic minimizer of excess and compute it by a sequential linear
program.

The paper provides three complement-family sufficient conditions for empty
Temporal Core:

- **Theorem 9** — single-complement threshold $r^{\ast\ast}$
- **Proposition 10** — balanced-complement threshold $r^{\ast\ast\ast}$ on $B_{n-1}$
- **Proposition 13** — balanced-near-complement threshold on $B_{n-1}\cup B_{n-2}$

plus a unifying partition-pair certificate (**Proposition 14**) that contains
Theorem 9 as the singleton-complement case and additionally fires on
non-singleton partition pairs at $k<n-1$. **Corollary 18** is a structural
obstruction: a bounded peak queue $k<n-1$ simultaneously blocks all three
complement-family mechanisms.

Together the four analytic thresholds certify 66 of the 67 observed empty
Cores in our 175-instance grid (the remaining near-complement case eludes
the closed-form thresholds by $\approx 2\times 10^{-3}$), with **no false
positives across 525 policy-instance pairs** (NN, CI, BR dispatch).

An asymptotic refinement (**Theorem 16**) ties $r^{\ast\ast}\to 1$ to the
classical Beardwood–Halton–Hammersley $\sqrt{n}$ scaling of the Euclidean
TSP. Scale-up to $n=50$ confirms the asymptotic decay.

## Repository contents

```
.
├── paper/
│   ├── main.tex                  # manuscript (30 pp)
│   ├── main.pdf
│   ├── supplementary.tex         # electronic companion (13 pp)
│   ├── supplementary.pdf
│   ├── cover_letter.md           # EJOR cover letter source
│   ├── cover_letter.pdf
│   ├── references.bib
│   └── apalike-ejor.bst
├── figures/                      # rendered figure PDFs used by main.tex
├── docs/                         # per-iteration response documents
├── REVISION_NOTES.md             # version history
├── LICENSE                       # MIT
└── README.md
```

## Building the manuscript locally

```bash
cd paper
pdflatex supplementary.tex && bibtex supplementary && pdflatex supplementary.tex && pdflatex supplementary.tex
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

The supplementary must be built first so that `xr` cross-references resolve.
Three-pass builds on each side close the round-trip.

Final outputs (verified at v2.5.2):
- `main.pdf` — 30 pages (matches the EJOR 30-page cap)
- `supplementary.pdf` — 13 pages
- 0 broken references in either PDF

## Key results (sanity checkpoints, v2.5.2)

| Paper location | Quantity | Value |
| --- | --- | --- |
| Supp. §S6 (Solomon C101) | TNu allocation, n=5 | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 4 (NN) | Theorem 9 single-complement fires | 37 of 37 (no false positives) |
| Table 4 (NN) | Proposition 10 balanced-complement fires | 57 of 57 (no false positives) |
| §6.3 | Five-mechanism decomposition of 67 NN empties | 37 + 11 + 9 + 1 + 9 |
| Corollary 18 (§5.1) | $k < n-1$ Core empirical nonempty rate | 70/79 (88.6%) |
| §6.5 | Sharpness ratio $\bar r^{\ast}/\bar r^{\ast\ast}$, $\bar r^{\ast}/\bar r^{\ast\ast\ast}$ | 3.56, 3.97 |
| Supp. §S2 | Scale invariance ($r$ relative std across $\alpha$) | 0.00e+00 |
| Supp. §S3 | Near-complement cases (Table S2) | 10 |
| Supp. §S3 | Intermediate cases (Table S3) | 9 |
| Supp. §S8 | Auxiliary feasibility lemmas (Lemmas 4, 5) | — |
| Supp. §S9 | Partition-pair certificates for the 9 intermediate cases | all 9 fire |

## Citation

```bibtex
@article{jeong2026online,
  author = {Jeong, Seyun and Tae, Hyunchul},
  title  = {Online Traveling Salesman Games: Core Fragility and the
            Temporal Nucleolus under Dynamic Arrivals},
  year   = {2026},
  note   = {Under review at European Journal of Operational Research}
}
```

## License

MIT License — see [LICENSE](LICENSE).

## Contact

Both authors are at the Korea Institute of Industrial Technology (KITECH),
Cheonan, Republic of Korea.

- Seyun Jeong — `jeongsseyyun@kitech.re.kr`
- Hyunchul Tae (corresponding author) — `sage@kitech.re.kr`

## Notes

- Code (algorithm implementations, experiment runners, figure-generation scripts)
  will be added to this repository in a follow-up commit. The v2.5.2 release
  ships the manuscript, cover letter, and reproducibility documentation; the
  full computational stack from the predecessor repository will be migrated
  with version-tagged provenance.
- A predecessor repository at `sage-Tae/online-tsg` contains earlier
  EJOR-track and TS-track iterations (v2.0–v2.4); that repository is being
  retired in favor of this one.

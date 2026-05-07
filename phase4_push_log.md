# Phase 4 — Push log

## Force-push (with `--force-with-lease`)

```
git push origin phase4-github-publish:main --force-with-lease
```

Output:
```
To https://github.com/sage-Tae/online-tsg-2026.git
 + e1b83ac...b82f1bd phase4-github-publish -> main (forced update)
```

Exit code: `0` (success).

`--force-with-lease` accepted because `e1b83ac` matched what we had
locally fetched immediately before the push (no concurrent change on
the remote).

## Tag push

```
git tag v2.8.0-public
git push origin v2.8.0-public
```

Output:
```
 * [new tag]         v2.8.0-public -> v2.8.0-public
```

## Remote state after push

| Ref | SHA | Notes |
|---|---|---|
| `refs/heads/main` | `b82f1bd0595cc1a30aeafb57352e826ce745a726` | new HEAD: v2.8.0 paper + v2.4.10 code (Phase 4 commit) |
| `refs/tags/v2.5.2` | `5f032d960182b5642f56e577e0c7e8636c84034f` (annotated) → `e1b83aca` (target) | unchanged; preserves the v2.5.x archival snapshot |
| `refs/tags/v2.8.0-public` | `b82f1bd0595cc1a30aeafb57352e826ce745a726` | new tag pinning the published Phase 4 state |

GitHub repo metadata (via `gh api`):
- default_branch: `main`
- pushed_at: `2026-05-07T14:12:24Z`
- size: 1093 KB

## Live URL spot-checks (HTTP 200)

| Path | Status | Purpose |
|---|---|---|
| `code/scripts/near_complement_coverage_check.py` | 200 | balanced-near-complement LP audit (Cor. 13) |
| `code/scripts/near_complement_coverage_check_k3.py` | 200 | Phase 2 $B_{n-3}$ closure attempt |
| `code/results/summary.csv` | 200 | per-instance row data |
| `REPRODUCIBILITY.md` | 200 | reproduction guide (from v2.4.10) |
| `paper/main_ejor.pdf` | 200 | published manuscript (30 pages) |

## Cover-letter URL truthful check

The cover letter (`paper/cover_letter_ejor.md` → `cover_letter_ejor.pdf`)
contains:

> All code, random seeds, and raw CSV results are at
> https://github.com/sage-Tae/online-tsg-2026

After this push, that URL points to a tree containing:
- `code/src/` — algorithm implementations
- `code/scripts/` — analysis scripts (incl. Phase 2 $B_{n-3}$ extension)
- `code/experiments/logs/policy_comparison_v2_full.csv` — 525 NN/CI/BR pairs
- `code/results/` — cached per-instance CSVs and partition-pair JSON
- `REPRODUCIBILITY.md` — full reproduction guide

The cover-letter claim is now **truthful**.

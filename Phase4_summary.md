# Phase 4 — GitHub Publish

Branch: `phase4-github-publish` (off `v2.8.0-submission-candidate`).
Remote: `https://github.com/sage-Tae/online-tsg-2026.git`.
Result: **published**, `main` HEAD = `b82f1bd0`, tag `v2.8.0-public`.

## What was integrated

Onto the `v2.8.0-submission-candidate` paper tree (Phase 1+2+3), this
phase added:

- `code/` — full v2.4.10 code subtree (`src/`, `scripts/`, `experiments/`,
  `results/`, `figures/`, `tests/`, `requirements.txt`).
- `code/scripts/near_complement_coverage_check_k3.py` and
  `code/results/near_complement_coverage_check_k3.csv` — Phase 2's
  $B_{n-3}$ closure attempt artifacts (already inside `code/` because
  the Phase 2 work happened in the v2.4.10 archive).
- `scripts/` — `verify_doc_consistency.sh` and `verify_zip_rebuild.sh`
  from v2.4.10's archive root.
- `REPRODUCIBILITY.md` — full reproduction guide (v2.4.10).
- `LICENSE` — MIT, copied from v2.4.10.
- `.gitignore` — newly authored: ignores LaTeX build artifacts,
  Python caches, macOS metadata, and runtime `*.log` files under
  `code/experiments/logs/`. Cached `*.csv` fixtures (e.g.,
  `policy_comparison_v2_full.csv`) are kept as committed evidence.

`README.md` was updated:
- "Key results (sanity checkpoints, **v2.8.0**)" with renumbered
  references (Cor 9 / Cor 10 / Cor 13 / Thm 14 per the Phase 1
  hierarchy swap; Cor 19 for the structural obstruction).
- A theorem-renumbering note at the top of the table for readers
  comparing against the v2.4.x archived response notes.
- Pointers to the cached output CSVs/JSON for verification.
- New row for the Phase 2 $B_{n-3}$ closure attempt outcome
  (Branch B: still negative, $-3.45\times 10^{-4}$).

## Pre-push safeguards (executed)

1. v2.4.10 archive existence verified at `../TSG_agent/`.
2. `gh auth status` — logged in as `sage-Tae` with `repo` scope.
3. Remote ref snapshot recorded in `phase4_remote_snapshot.md`
   before any local change to `origin`.
4. `git push --dry-run --force-with-lease` confirmed the planned
   ref move (`+ e1b83ac...b82f1bd phase4-github-publish -> main
   (forced update)`).
5. **Stopped and asked the user** for explicit confirmation
   before the actual push. Push proceeded only after the user
   answered "yes".

## Push details (executed after user confirmation)

See `phase4_push_log.md` for the full output. Summary:

- `git push origin phase4-github-publish:main --force-with-lease` —
  succeeded; remote HEAD moved `e1b83ac` → `b82f1bd`.
- `git push origin v2.8.0-public` — new annotated tag pushed.
- Tag `v2.5.2` (pointing to the previous `e1b83ac` snapshot) was
  not touched; the v2.5.x archival state is therefore still
  reachable via that tag.
- `--force-with-lease` (race-condition guard) confirmed nobody had
  pushed concurrently between fetch and push.

## Post-push verification

All five live URLs (HEAD requests via `curl`) returned HTTP 200:

- `code/scripts/near_complement_coverage_check.py`
- `code/scripts/near_complement_coverage_check_k3.py`
- `code/results/summary.csv`
- `REPRODUCIBILITY.md`
- `paper/main_ejor.pdf`

`gh api repos/sage-Tae/online-tsg-2026` reports `default_branch: main`,
`size: 1093 KB`, last `pushed_at: 2026-05-07T14:12:24Z`.

`git ls-remote origin refs/heads/main` returns
`b82f1bd0595cc1a30aeafb57352e826ce745a726` — exact match to local
HEAD.

## Cover-letter truthfulness

Before Phase 4, `paper/cover_letter_ejor.md` claimed:

> All code, random seeds, and raw CSV results are at
> https://github.com/sage-Tae/online-tsg-2026

The remote at that URL was paper-only (no `code/`). After Phase 4,
the URL resolves to a tree containing `code/`, cached CSVs, and
`REPRODUCIBILITY.md`. The claim is now truthful.

## What is *not* in this commit

- No paper edits. All `paper/` files are bit-identical to the
  `v2.8.0-submission-candidate` tag.
- No re-runs. The cached outputs are the v2.4.10 ones that already
  match the v2.8.0 numbers; Phase 2's $B_{n-3}$ artifacts are
  carried over verbatim from the local archive.
- No GitHub Releases entry yet (only the lightweight tag was
  pushed). A Release with notes can be created from
  `v2.8.0-public` whenever needed.

## Tag

Local: `v2.8.0-public` at `b82f1bd`.
Remote: same.

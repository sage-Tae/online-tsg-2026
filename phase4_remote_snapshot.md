# Phase 4 — Remote snapshot before force-push

**Captured:** 2026-05-07 (just before phase4-github-publish push prep)
**Remote:** `https://github.com/sage-Tae/online-tsg-2026.git`

## Refs to be overwritten by force-push to `main`

```
e1b83aca9e16eb049b84fe752ad20d0796b07ca7	HEAD
e1b83aca9e16eb049b84fe752ad20d0796b07ca7	refs/heads/main
5f032d960182b5642f56e577e0c7e8636c84034f	refs/tags/v2.5.2
e1b83aca9e16eb049b84fe752ad20d0796b07ca7	refs/tags/v2.5.2^{}
```

## What this means

- `refs/heads/main` currently points to `e1b83aca` — this is the v2.5.x
  paper-only state I cloned earlier in Phase 2 (`paper/`, `figures/`,
  `docs/`, `README.md`, `REVISION_NOTES.md`, `LICENSE`; **no `code/`**).
  The cover letter's reproducibility URL pointed to this commit and was
  effectively non-truthful.
- The tag `v2.5.2` is detached (it doesn't move) — the force-push will
  not delete it. Past releases under that tag remain accessible.
- The Phase 4 force-push replaces only `refs/heads/main`. After the
  push:
  - `main` → new HEAD (Phase 4 commit on top of `v2.8.0-submission-candidate`)
  - `v2.5.2` tag remains, pointing to the same `e1b83aca` snapshot.
  
So the v2.5.x paper-only state is preserved for archival purposes via
the tag; only the moving `main` ref is updated.

## Recovery (if rollback needed)

```
git push origin --force-with-lease e1b83aca9e16eb049b84fe752ad20d0796b07ca7:refs/heads/main
```

(Anyone with push access to the repo can run this from any clone that
fetched the v2.5.2 tag.)

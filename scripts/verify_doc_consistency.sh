#!/bin/bash
#
# verify_doc_consistency.sh — stale-label sweep for README.md + REPRODUCIBILITY.md.
#
# Usage:
#   bash scripts/verify_doc_consistency.sh
#
# Each category greps the two documents for a specific class of stale text —
# old version labels in non-historical contexts, superseded page counts, old
# seed123 row counts, orphan top-level `figures/` entries in the repo tree,
# retired metric values — and reports either matching lines or `(none)`.
# Every category must report `(none)` for a clean v2.1.7 tree; a non-empty
# result signals a regression that must be reviewed before tagging the next
# iteration.
#
# Historical-context filtering: version-label matches that fall inside a
# "Version history:" / "## Version History" block (up to the next blank
# line or the next top-level heading) are excluded automatically.
#
# The script exits 0 on full pass, 1 if any category has hits. It does NOT
# modify any files.

set -u

CURRENT_VERSION="v2.2.5"
CURRENT_MAIN_PAGES="30"
CURRENT_SUPP_PAGES="8"
SEED123_ROWS="2"

README="README.md"
REPRO="REPRODUCIBILITY.md"

if [ ! -f "$README" ] || [ ! -f "$REPRO" ]; then
    echo "ERROR: run from repo root. README.md or REPRODUCIBILITY.md not found." >&2
    exit 2
fi

FAIL=0

report() {
    local label="$1"
    local hits="$2"
    echo "=== $label ==="
    if [ -z "$hits" ]; then
        echo "  (none)"
    else
        echo "$hits"
        FAIL=1
    fi
}

# Emit `<file>:<lineno>:<line>` for every line that is NOT inside a
# version-history block. A version-history block begins at a line that
# contains "Version history:" or "## Version History" or "## Reproducibility tags"
# and ends at the next blank line followed by a non-list heading/paragraph.
# We use a simple heuristic: skip lines between a version-history marker
# and the next top-level heading (`^## `) or end of file.
strip_history() {
    local file="$1"
    awk '
        BEGIN { skip=0 }
        /^## Version History/ { skip=1; next }
        /^Version history:/   { skip=1; next }
        /^## Reproducibility tags/ { skip=1; next }
        /^## / { if (skip) skip=0 }
        { if (!skip) printf "%s:%d:%s\n", FILENAME, NR, $0 }
    ' "$file"
}

ALL_NONHIST=$(strip_history "$README"; strip_history "$REPRO")

# 1. Stale version labels v2.1.0 – v2.2.4 outside historical blocks.
#    Also exclude per-line historical markers: supersedes / Supersedes /
#    legacy / prior / v2.1.X-and-earlier (phrases that signal the label is
#    being cited as history, not as current). Note: v2.2.5 is the current
#    version, so we match any v2.1.N and v2.2.0–v2.2.4, but not v2.2.5.
VERSION_HITS=$(echo "$ALL_NONHIST" | grep -E ":.*(v2\.1\.[0-9]\b|v2\.1\.1[0-2]\b|v2\.2\.[01234]\b)" 2>/dev/null | \
    grep -vE "supersedes|Supersedes|legacy|Legacy|-and-earlier|and earlier|prior submission|historical" || true)
report "Stale version labels (non-historical)" "$VERSION_HITS"

# 2. Stale page counts — previous main-manuscript page counts (pre-v2.1.8:
#    23 / 29 / 34 / 35) outside historical blocks. Do NOT flag the current
#    values (30 main, 6 supplementary).
PAGE_HITS=$(echo "$ALL_NONHIST" | grep -E ":.*\b(23|29|34|35) pages\b" 2>/dev/null || true)
report "Stale page counts" "$PAGE_HITS"

# 3. Stale seed123 row counts — `5 instances` / `5 rows` / `five instances`
#    etc., with word boundaries to avoid matching `525 rows` or `45 instances`.
#    Also exclude the transition phrasing `5 → 2` / `5 -> 2` / `5 to 2`.
ROW_HITS=$(echo "$ALL_NONHIST" | \
    grep -E ":.*(^| )(5|five) (instances|cases|rows)\b" 2>/dev/null | \
    grep -vE "5 to 2|5 → 2|5 -> 2|\`5 instances\`|\`5 rows\`" || true)
report "Stale seed123 row counts" "$ROW_HITS"

# 4. Orphan top-level figures/ entry in README repo tree — the ZIP does not
#    ship a top-level figures/ directory. Only flag entries at the ROOT of
#    the tree (i.e., ├──/└── with no leading │ subtree indicator).
TREE_HITS=$(grep -nE "^(├──|└──)[[:space:]]*figures/" "$README" 2>/dev/null || true)
report "Orphan top-level figures/ in repo tree" "$TREE_HITS"

# 5. Stale metric values — 1.355 (old r̄** factor retired in v2.1.2) and
#    3.21 (old sharpness value).
METRIC_HITS=$(grep -nE "\b1\.355\b|\b3\.21\b" "$README" "$REPRO" 2>/dev/null || true)
report "Stale metrics (1.355 / 3.21)" "$METRIC_HITS"

echo ""
if [ "$FAIL" = "0" ]; then
    echo "Doc consistency check: PASS (current version = $CURRENT_VERSION, main $CURRENT_MAIN_PAGES pages / supplementary $CURRENT_SUPP_PAGES pages, seed123 = $SEED123_ROWS rows)"
    exit 0
else
    echo "Doc consistency check: FAIL — review hits above."
    exit 1
fi

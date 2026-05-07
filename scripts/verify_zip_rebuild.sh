#!/bin/bash
#
# verify_zip_rebuild.sh — clean-room rebuild validation for a submission ZIP.
#
# Usage:
#   scripts/verify_zip_rebuild.sh <path-to-submission.zip>
#
# The script extracts the ZIP into a temporary directory, runs the standard
# pdflatex → bibtex → pdflatex → pdflatex sequence on BOTH paper/main.tex
# and paper/supplementary.tex (if the latter exists), and reports the page
# counts. Exit code 0 on success; non-zero on missing PDFs, undefined
# refs/cites, or a main.pdf page count exceeding the EJOR 30-page limit.
#
# The intent is to catch path-sensitive bugs that only surface when the
# repository is extracted in isolation from the development tree — e.g.,
# LaTeX \graphicspath entries pointing to symlinks that exist only in the
# working copy — as well as EJOR-compliance regressions on the main PDF.

set -e

ZIP="$1"
if [ -z "$ZIP" ]; then
    echo "Usage: $0 <path-to-submission.zip>" >&2
    exit 2
fi
if [ ! -f "$ZIP" ]; then
    echo "ERROR: ZIP file not found: $ZIP" >&2
    exit 2
fi

ZIP_ABS=$(cd "$(dirname "$ZIP")" && pwd)/$(basename "$ZIP")
EXPECTED_MAIN_PAGES=30

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

cd "$TMPDIR"
unzip -q "$ZIP_ABS"

PAPER_DIR=$(find . -type d -name paper -maxdepth 3 | head -1)
if [ -z "$PAPER_DIR" ]; then
    echo "Clean-room rebuild: FAIL (paper/ directory not found in ZIP)"
    exit 1
fi

cd "$PAPER_DIR"

get_pages() {
    local pdf="$1"
    local log="$2"
    if command -v pdfinfo > /dev/null 2>&1; then
        pdfinfo "$pdf" 2>/dev/null | awk '/^Pages:/ {print $2}'
    else
        awk -v pdf="$pdf" '
            $0 ~ "Output written on " pdf {
                for (i=1;i<=NF;i++) if ($i ~ /^\(/) {gsub(/[()]/, "", $i); print $i; exit}
            }
        ' "$log"
    fi
}

build_one() {
    local stem="$1"
    pdflatex -interaction=nonstopmode "${stem}.tex" > "${stem}_build1.log" 2>&1 || true
    bibtex "$stem" > "${stem}_bibtex.log" 2>&1 || true
    pdflatex -interaction=nonstopmode "${stem}.tex" > "${stem}_build2.log" 2>&1 || true
    pdflatex -interaction=nonstopmode "${stem}.tex" > "${stem}_build3.log" 2>&1 || true
}

check_one() {
    local stem="$1"
    local expected_pages="$2"   # "" means no page-count check
    local log="${stem}_build3.log"
    if [ ! -f "${stem}.pdf" ]; then
        echo "Clean-room rebuild: FAIL (${stem}.pdf not produced)"
        echo "--- tail of final ${stem} build log ---"
        tail -40 "$log"
        return 1
    fi
    local pages
    pages=$(get_pages "${stem}.pdf" "$log")
    local undef_refs undef_cites errors
    undef_refs=$(grep -c "undefined references" "$log" 2>/dev/null || true)
    undef_cites=$(grep -c "Citation .* undefined" "$log" 2>/dev/null || true)
    errors=$(grep -c "^! " "$log" 2>/dev/null || true)

    local page_ok=1
    if [ -n "$expected_pages" ]; then
        # Allow "up to $expected_pages" (i.e., <=)
        if [ "$pages" -gt "$expected_pages" ] 2>/dev/null; then
            page_ok=0
        fi
    fi

    if [ "$errors" = "0" ] && [ "$undef_refs" = "0" ] && [ "$undef_cites" = "0" ] && [ "$page_ok" = "1" ]; then
        if [ -n "$expected_pages" ]; then
            echo "  ${stem}.pdf: PASS ($pages pages, limit $expected_pages)"
        else
            echo "  ${stem}.pdf: PASS ($pages pages)"
        fi
        return 0
    else
        echo "  ${stem}.pdf: FAIL"
        echo "    pages=$pages (limit=${expected_pages:-unchecked}), errors=$errors, undef_refs=$undef_refs, undef_cites=$undef_cites"
        echo "    --- tail of final ${stem} build log ---"
        tail -40 "$log"
        return 1
    fi
}

echo "=== Clean-room rebuild ==="

build_one main
MAIN_OK=0
check_one main "$EXPECTED_MAIN_PAGES" && MAIN_OK=1 || true

SUPP_OK=1
if [ -f supplementary.tex ]; then
    build_one supplementary
    SUPP_OK=0
    check_one supplementary "" && SUPP_OK=1 || true
else
    echo "  supplementary.tex: skipped (not present in ZIP)"
fi

HIGH_OK=1
if [ -f highlights.tex ]; then
    build_one highlights
    HIGH_OK=0
    check_one highlights "" && HIGH_OK=1 || true
else
    echo "  highlights.tex: skipped (not present in ZIP)"
fi

if [ "$MAIN_OK" = "1" ] && [ "$SUPP_OK" = "1" ] && [ "$HIGH_OK" = "1" ]; then
    echo "Clean-room rebuild: PASS"
    exit 0
else
    echo "Clean-room rebuild: FAIL"
    exit 1
fi

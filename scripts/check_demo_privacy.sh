#!/usr/bin/env bash
# Guards the demo build against leaking personal information.
#
# Reads patterns (one per line) from a file OUTSIDE this repo so the filter
# itself doesn't trip its own match. Default path is .privacy-patterns.local
# at the repo root (gitignored). Override with PRIVACY_PATTERNS_FILE=<path>.
#
# Usage:
#   ./scripts/check_demo_privacy.sh [target-dir]
#
# Exits 0 on clean, 1 on hit (with grep output above), 2 on missing patterns
# file or missing grep.
set -euo pipefail

TARGET="${1:-docs/}"
PATTERNS_FILE="${PRIVACY_PATTERNS_FILE:-.privacy-patterns.local}"

if ! command -v grep >/dev/null 2>&1; then
  echo "error: grep not on PATH; cannot run privacy check" >&2
  exit 2
fi

if [[ ! -r "$PATTERNS_FILE" ]]; then
  cat >&2 <<EOF
error: privacy patterns file not readable: $PATTERNS_FILE

Set PRIVACY_PATTERNS_FILE to a path outside the repo (recommended), e.g.
  export PRIVACY_PATTERNS_FILE=~/.config/pm-job-search/privacy-patterns.txt

…or create $PATTERNS_FILE at the repo root (already in .gitignore).
The file format is one pattern per line; blank lines and lines starting
with '#' are ignored.
EOF
  exit 2
fi

if [[ ! -d "$TARGET" ]]; then
  echo "error: target dir not found: $TARGET" >&2
  exit 2
fi

# Strip blanks/comments, join with '|' for grep -E alternation.
PATTERN=$(grep -vE '^\s*(#|$)' "$PATTERNS_FILE" | paste -sd'|' -)
if [[ -z "$PATTERN" ]]; then
  echo "error: no patterns found in $PATTERNS_FILE" >&2
  exit 2
fi

# Excluded subdirs: superpowers/ holds specs and plans that quote the patterns
# verbatim in command examples — including these in the scan would always trip.
# Extend with EXTRA_EXCLUDE_DIRS="foo bar" if you need more.
EXCLUDE_DIRS=(superpowers .git node_modules ${EXTRA_EXCLUDE_DIRS:-})
EXCLUDE_ARGS=()
for d in "${EXCLUDE_DIRS[@]}"; do
  EXCLUDE_ARGS+=(--exclude-dir="$d")
done

# grep -REi: recursive, extended regex, case-insensitive.
# grep -I: skip binary files — the demo bundle ships a .mp4 whose raw bytes
# coincidentally match short patterns like hex IDs. Binary assets carry no
# readable PII anyway; manual review is the right control for those.
# Exits 0 on match (== violation), 1 on no match (== clean), 2 on error.
set +e
HITS=$(grep -REIi --color=never "${EXCLUDE_ARGS[@]}" "$PATTERN" "$TARGET" 2>/dev/null)
status=$?
set -e

case "$status" in
  0)
    echo "$HITS" >&2
    echo "" >&2
    echo "privacy violation: patterns above found in $TARGET" >&2
    exit 1
    ;;
  1)
    echo "privacy grep ok: no matches in $TARGET"
    exit 0
    ;;
  *)
    echo "error: grep exited with status $status" >&2
    exit 2
    ;;
esac

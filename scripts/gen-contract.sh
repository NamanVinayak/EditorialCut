#!/usr/bin/env bash
# Regenerate the per-CLI contract copies from the single source of truth.
#
# AGENTS.md is the canonical working contract. Claude Code reads CLAUDE.md,
# Gemini/Antigravity read GEMINI.md, and GitHub Copilot reads
# .github/copilot-instructions.md -- so each is kept as a byte-identical copy
# of AGENTS.md rather than a hand-maintained sibling. Edit AGENTS.md, run this,
# commit. scripts/check_public_tree.py fails the build if a copy drifts.
#
# Idempotent: re-running with no AGENTS.md change is a no-op.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SRC="AGENTS.md"
COPIES=(
  "CLAUDE.md"
  "GEMINI.md"
  ".github/copilot-instructions.md"
)

if [ ! -f "$SRC" ]; then
  echo "!! $SRC not found -- nothing to generate from" >&2
  exit 1
fi

changed=0
for dest in "${COPIES[@]}"; do
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ] && cmp -s "$SRC" "$dest"; then
    echo "-- $dest already up to date"
  else
    cp "$SRC" "$dest"
    echo "-- wrote $dest from $SRC"
    changed=1
  fi
done

if [ "$changed" -eq 0 ]; then
  echo "== contract copies already in sync with $SRC =="
else
  echo "== regenerated contract copies from $SRC =="
fi

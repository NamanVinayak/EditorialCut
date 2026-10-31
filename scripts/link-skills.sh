#!/usr/bin/env bash
# Fan the single skills/ source out to every coding CLI's skills directory.
#
# There is ONE canonical copy of each skill: skills/<name>/SKILL.md. Different
# CLIs scan different skill roots (.claude/skills, .agents/skills,
# .opencode/skills, .gemini/skills, and the user-global ~/.codex/skills,
# ~/.agents/skills). Rather than duplicate skill bodies, this script (re)creates
# each root as a set of symlinks back to skills/<name>. Idempotent: a link that
# already points where we want is left alone; a stale link of ours is refreshed;
# anything that is NOT one of our symlinks (a real file/dir the user owns) is
# never clobbered -- we warn and skip it.
#
# NOTE ON WINDOWS / core.symlinks=false: the .claude/skills/<name> links are
# committed so Claude Code (including cloud/Cowork, which only see the committed
# tree) works on a fresh clone with no setup. On a checkout where git symlink
# support is off (Windows default), those committed links land as small text
# files instead of links. Re-run this script there (Git Bash / WSL) to rebuild
# them as real links, or point your CLI at skills/ directly.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SKILLS_SRC="skills"

# Every skills/<name> that actually contains a SKILL.md (skips CATALOG.md).
skill_names() {
  for d in "$SKILLS_SRC"/*/; do
    [ -f "${d}SKILL.md" ] || continue
    basename "$d"
  done
}

# (re)create one symlink safely. Never overwrites a real file/dir we did not
# create -- only refreshes a symlink or fills an empty slot.
safe_link() {
  local link="$1" target="$2"
  if [ -L "$link" ]; then
    [ "$(readlink "$link")" = "$target" ] && return 1   # already correct
    rm -f "$link"                                        # our stale link
  elif [ -e "$link" ]; then
    echo "!! skipping $link -- exists and is not a symlink (leaving your file alone)" >&2
    return 1
  fi
  ln -s "$target" "$link"
  return 0
}

# Link one skills root: link_root <root-dir> <symlink-target-prefix>
link_root() {
  local root="$1" prefix="$2"
  mkdir -p "$root"
  local made=0 total=0
  while IFS= read -r name; do
    total=$((total + 1))
    safe_link "$root/$name" "$prefix/$name" && made=$((made + 1)) || true
  done < <(skill_names)
  echo "-- $root: $total skills ($made new/updated)"
}

echo "== linking skills into per-tool skill roots =="

# Repo-local roots (two levels deep -> ../../skills). .claude/skills is committed;
# the rest are git-ignored and created here at setup time.
link_root ".claude/skills"   "../../skills"
link_root ".agents/skills"   "../../skills"
link_root ".opencode/skills" "../../skills"
link_root ".gemini/skills"   "../../skills"

# User-global roots for CLIs that only discover skills under $HOME. Absolute
# symlink targets, since they live outside the repo.
link_root "$HOME/.codex/skills"  "$ROOT/$SKILLS_SRC"
link_root "$HOME/.agents/skills" "$ROOT/$SKILLS_SRC"

echo "== done. one source (skills/), fanned out to every tool =="

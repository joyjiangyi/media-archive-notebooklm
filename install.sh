#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_root="${CODEX_HOME:-$HOME/.codex}/skills"
force=0

if [[ "${1:-}" == "--force" ]]; then
  force=1
elif [[ -n "${1:-}" ]]; then
  echo "Usage: ./install.sh [--force]" >&2
  exit 2
fi

mkdir -p "$target_root"
for source_dir in "$repo_dir"/skills/*; do
  skill_name="$(basename "$source_dir")"
  target_dir="$target_root/$skill_name"
  if [[ -e "$target_dir" && "$force" -ne 1 ]]; then
    echo "Refusing to overwrite $target_dir. Re-run with --force after reviewing it." >&2
    exit 1
  fi
  if [[ -e "$target_dir" ]]; then
    backup_dir="${target_dir}.backup.$(date +%Y%m%d%H%M%S)"
    mv "$target_dir" "$backup_dir"
    echo "Backed up existing skill to $backup_dir"
  fi
  cp -R "$source_dir" "$target_dir"
  echo "Installed $skill_name"
done

echo "Restart Codex to load the skills."

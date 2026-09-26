#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

local_hugo="$root/.tools/hugo/0.166.0/hugo"
if [[ -x "$local_hugo" ]]; then
  hugo="$local_hugo"
elif command -v hugo >/dev/null 2>&1; then
  hugo="$(command -v hugo)"
else
  echo 'Hugo 0.166.0 is required. Install it and retry.' >&2
  exit 1
fi

if [[ "$("$hugo" version)" != *'hugo v0.166.0'* ]]; then
  echo "Hugo 0.166.0 is required; found: $("$hugo" version)" >&2
  exit 1
fi

if [[ ! -f themes/PaperMod/theme.toml ]]; then
  echo 'Initializing the Hugo theme submodule...'
  git submodule update --init --recursive
fi

case "${1:-serve}" in
  serve)
    exec "$hugo" server --buildDrafts --bind 127.0.0.1 --port 1313
    ;;
  *)
    echo "Unknown mode: $1" >&2
    exit 2
    ;;
esac

#!/usr/bin/env bash
# run-windows.sh — from Ubuntu, run this project natively on Windows.
#   ./scripts/run-windows.sh <app arguments>      e.g. ./scripts/run-windows.sh status
# See run-windows.ps1 for when (and why) to use this.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v powershell.exe >/dev/null 2>&1; then
  echo "This only works inside WSL on Windows." >&2
  exit 1
fi
exec powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w "$here/run-windows.ps1")" "$@"

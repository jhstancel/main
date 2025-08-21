#!/usr/bin/env bash
set -euo pipefail
if ! command -v valgrind >/dev/null 2>&1; then
  echo "valgrind not found"; exit 1
fi
make
for bin in build/*_demo; do
  echo ">>> Valgrind $bin"
  valgrind --leak-check=full --error-exitcode=1 "$bin"
done
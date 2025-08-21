#!/usr/bin/env bash
set -euo pipefail
make
for bin in build/*_demo; do
  echo ">>> Running $bin"
  "$bin"
done
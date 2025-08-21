#!/usr/bin/env bash
set -euo pipefail
command -v clang-format >/dev/null 2>&1 || { echo "clang-format not found"; exit 1; }
find src include tests -type f \( -name '*.cpp' -o -name '*.hpp' -o -name '*.h' \) -print0 | xargs -0 clang-format -i
echo "Formatted."
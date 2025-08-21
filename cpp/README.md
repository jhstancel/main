# CPSC 2120 C++ Template

Standardized layout for data structures and algorithms work.

## Layout
- `src/` topic-based implementations
- `include/` shared headers
- `labs/` lab submissions
- `projects/` larger assignments
- `tests/` simple test harness
- `data/` sample inputs/outputs
- `build/` compiled binaries (ignored)
- `scripts/` automation (format, run tests, valgrind)

## Build
```bash
make            # builds all demos into build/
make run DEMO=sorting_demo
make clean
```

## Notes
- C++17 by default. Adjust in `Makefile` if needed.
- Add per-lab or per-project Makefiles as desired.
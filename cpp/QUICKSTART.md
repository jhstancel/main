# CPSC2120 C++ Project — Quickstart Guide

This is your cheat sheet for building, running, testing, and syncing your code.

---

## **1. Build Everything**
```bash
make

    Compiles all demo programs into cpp/build/.

2. Run a Specific Demo

make run DEMO=sorting_demo

Available demos:

    linked_list_demo

    stack_queue_demo

    sorting_demo

    hashing_demo

    trees_demo

    heaps_demo

    graphs_demo

    algorithms_demo

Example:

make run DEMO=linked_list_demo
# Output: 1 2 3

3. Format All Code

make format

Uses scripts/format_code.sh and clang-format to clean up code automatically.
4. Run All Demos

make test

Runs every demo binary sequentially.
5. Check for Memory Leaks

make valgrind

Uses valgrind on every compiled demo program.
6. Clean & Rebuild

make clean
make

    Deletes everything in build/

    Recompiles from scratch

7. Git Workflow
Sync your repo:

git pull origin main

Save changes:

git add -A
git commit -m "meaningful message"
git push origin main

Stop tracking compiled junk (already set up):

# Compiled binaries live in cpp/build/, which is now ignored.

8. Project Structure

cpp/
├── build/          # Compiled binaries (.gitignored)
├── include/        # Header files (.hpp)
├── labs/           # Lab assignments
├── projects/       # Larger projects
├── scripts/        # Formatting & testing tools
├── src/            # Source code, organized by topic
├── tests/          # Demo test drivers
└── Makefile        # Build system

9. Common Commands Cheat Sheet
Action	Command
Build everything	make
Run a demo	make run DEMO=sorting_demo
Format code	make format
Test all demos	make test
Memory check	make valgrind
Clean & rebuild	make clean && make
Commit & push	git add -A && git commit -m "msg" && git push origin main

Tip: Always run make clean before switching branches or pulling changes to prevent stale binaries from breaking builds.


---

## **How to Add It**
```bash
nano QUICKSTART.md
# Paste content, save (Ctrl+O, Enter) and exit (Ctrl+X)

git add QUICKSTART.md
git commit -m "docs: add QUICKSTART.md cheat sheet"
git push origin main

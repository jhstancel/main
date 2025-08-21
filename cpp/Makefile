# =========================
#   CPSC 2120 Makefile
# =========================

CXX       := g++
CXXFLAGS  := -std=c++17 -O2 -Wall -Wextra -Wpedantic -Wshadow -Wconversion -MMD -MP -Iinclude
LDFLAGS   :=
BUILD_DIR := build

DEMOS := \
    linked_list_demo \
    stack_queue_demo \
    sorting_demo \
    hashing_demo \
    trees_demo \
    heaps_demo \
    graphs_demo \
    algorithms_demo

# Default: build all demos
all: $(addprefix $(BUILD_DIR)/,$(DEMOS))

# Create build directory if missing
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Demo targets
$(BUILD_DIR)/linked_list_demo: src/linked_lists/singly_linked_list.cpp tests/demo_linked_list.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/stack_queue_demo: src/stacks_queues/stack_array.cpp src/stacks_queues/queue_array.cpp tests/demo_stack_queue.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/sorting_demo: src/sorting/quick_sort.cpp src/sorting/merge_sort.cpp tests/demo_sorting.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/hashing_demo: src/hashing/hash_table_chaining.cpp tests/demo_hashing.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/trees_demo: src/trees/binary_search_tree.cpp tests/demo_trees.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/heaps_demo: src/heaps/min_heap.cpp tests/demo_heaps.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/graphs_demo: src/graphs/bfs.cpp src/graphs/dfs.cpp tests/demo_graphs.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/algorithms_demo: src/algorithms/dynamic_programming.cpp tests/demo_algorithms.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

# ------------------------
#   Utility Targets
# ------------------------

# Run a single demo: make run DEMO=sorting_demo
run:
	@[ -n "$(DEMO)" ] || (echo "Usage: make run DEMO=<target>"; exit 1)
	@$(BUILD_DIR)/$(DEMO)

# Format code with clang-format
format:
	./scripts/format_code.sh

# Run all demos automatically
test:
	./scripts/run_all_tests.sh

# Run valgrind memory check on all demos
valgrind:
	./scripts/valgrind_check.sh

# Remove build directory & artifacts
clean:
	rm -rf $(BUILD_DIR)

# Auto-include dependency files
-include $(BUILD_DIR)/*.d

.PHONY: all run format test valgrind clean

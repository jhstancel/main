CXX ?= g++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -Wpedantic -Wshadow -Wconversion -Iinclude
LDFLAGS ?=
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

all: $(addprefix $(BUILD_DIR)/,$(DEMOS))

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

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

run: # make run DEMO=sorting_demo
	@[ -n "$(DEMO)" ] || (echo "Specify DEMO=<target> (e.g., sorting_demo)"; exit 1)
	@$(BUILD_DIR)/$(DEMO)

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all run clean

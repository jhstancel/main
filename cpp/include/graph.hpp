#pragma once
#include <cstddef>
#include <queue>
#include <vector>

struct Graph {
    std::size_t n{};
    std::vector<std::vector<int>> adj;
    explicit Graph(int nIn) : n(static_cast<std::size_t>(nIn)), adj(static_cast<std::size_t>(nIn)) {}
    void addEdge(int u, int v) {
        adj[static_cast<std::size_t>(u)].push_back(v);
        adj[static_cast<std::size_t>(v)].push_back(u);
    }
};

std::vector<int> bfs(const Graph& g, int s);
std::vector<int> dfs(const Graph& g, int s);

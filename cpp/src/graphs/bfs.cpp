#include "graph.hpp"
#include <cstddef>
#include <vector>

std::vector<int> bfs(const Graph& g, int s) {
    std::vector<int> dist(g.n, -1);
    std::queue<int> q;
    dist[static_cast<std::size_t>(s)] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g.adj[static_cast<std::size_t>(u)]) {
            if (dist[static_cast<std::size_t>(v)] == -1) {
                dist[static_cast<std::size_t>(v)] = dist[static_cast<std::size_t>(u)] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

#include "graph.hpp"
#include <stack>
#include <vector>

std::vector<int> dfs(const Graph& g, int s) {
    std::vector<int> vis(g.n, 0), order;
    std::stack<int> st; st.push(s);
    while (!st.empty()) {
        int u = st.top(); st.pop();
        if (vis[static_cast<std::size_t>(u)]) continue;
        vis[static_cast<std::size_t>(u)] = 1;
        order.push_back(u);
        for (int v : g.adj[static_cast<std::size_t>(u)]) {
            if (!vis[static_cast<std::size_t>(v)]) st.push(v);
        }
    }
    return order;
}

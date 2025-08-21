#include <iostream>
#include "graph.hpp"
int main(){
    Graph g(4);
    g.addEdge(0,1); g.addEdge(1,2); g.addEdge(2,3);
    auto d = bfs(g, 0);
    for (int x: d) std::cout << x << ' ';
    std::cout << "\n";
    return 0;
}

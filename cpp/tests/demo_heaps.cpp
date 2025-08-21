#include <iostream>
#include "heap.hpp"
int main(){
    BinaryHeap<int> h;
    h.push(3); h.push(1); h.push(2);
    std::cout << h.top() << "\n";
    h.pop();
    std::cout << h.top() << "\n";
    return 0;
}

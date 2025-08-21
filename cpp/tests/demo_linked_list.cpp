#include <iostream>
#include "linked_list.hpp"
int main(){
    SinglyLinkedList<int> L;
    L.pushFront(3); L.pushFront(2); L.pushFront(1);
    int x;
    while (L.popFront(x)) std::cout << x << " ";
    std::cout << "\n";
    return 0;
}

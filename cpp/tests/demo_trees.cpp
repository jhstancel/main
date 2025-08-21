#include <iostream>
#include "bst.hpp"
int main(){
    BST<int> t; t.insert(5); t.insert(2); t.insert(7);
    std::cout << t.contains(2) << t.contains(9) << "\n";
    return 0;
}

#include <iostream>
#include <vector>
#include "sorting.hpp"
int main(){
    std::vector<int> a{5,1,4,2,8,0,2};
    auto b = a;
    quickSort(a);
    mergeSort(b);
    for (int x: a) std::cout << x << ' '; std::cout << "\n";
    for (int x: b) std::cout << x << ' '; std::cout << "\n";
    return 0;
}

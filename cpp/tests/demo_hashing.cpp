#include <iostream>
#include <string>
#include "hash_table.hpp"
int main(){
    HashTableChaining<std::string,int> H(7);
    H.insert("a",1); H.insert("b",2); H.insert("c",3);
    auto v = H.find("b");
    std::cout << (v ? *v : -1) << "\n";
    return 0;
}

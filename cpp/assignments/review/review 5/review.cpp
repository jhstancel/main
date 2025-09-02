#include "review.h"
#include <iostream>
#include <vector>
/*
Your name (username): John Stancel
Date submitted: 9/5/2025
Lab section: #2
Assignment name: review
*/


// this function will return the 
std::vector<int> InitializeArray(int size) {
    std::vector<int> arr;
    arr.resize(size);
    for (int i=size;i--;i>0) {
        arr[i] = 0;
    }
    return arr;
}
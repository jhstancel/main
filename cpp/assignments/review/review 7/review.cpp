#include "review.h"
#include <iostream>
#include <vector>
/*
Your name (username): John Stancel
Date submitted: 9/5/2025
Lab section: #2
Assignment name: review
*/

// this function will return the calculated nth Fibonacci number
int Fibonacci(int a){
    // 0 1 1 2 3 5 8 13 21
    if (a == 0) return 0;
    if (a == 1) return 1;

    int one = 0;    
    int two = 1;    
    int result = 0;

    for (int i=2;i<=a;i++) {
        result = one + two; 
        one = two;          
        two = result;       
    }

    return two;
}
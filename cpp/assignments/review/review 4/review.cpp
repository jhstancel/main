#include "review.h"
#include <iostream>
#include <vector>
/*
Your name (username): John Stancel
Date submitted: 9/5/2025
Lab section: #2
Assignment name: review
*/


// this function will return the string entered into the terminal until 'q'
void ReadWrite(){
    std::string input = "";
    std::string output = "";
    std::cin >> input;
    while (input != "q") {
        output += input + " ";
        std::cin >> input;
    }
    std::cout << output << std::endl;

}
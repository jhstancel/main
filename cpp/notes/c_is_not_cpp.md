# DEFINITION

/*
The main difference between C and C++:
- C    | Procedural Programming
- C++  | Object-Oriented Programming

In C++, almost everything is treated as an object containing both data and functions.

----------------------------------------------------------------------
CLASSES & OBJECTS
----------------------------------------------------------------------

- A class is a data structure with its own variables and functions.
- An object is an **instance of a class** that gets memory allocated when created.
- Classes can define **access specifiers**:
    - Public    | Any function can access.
    - Private   | Only member functions of the class can access.
    - Protected | Accessible by the class and its derived classes.

**Encapsulation** → Containing variables and functions within a class.

**Structs vs Classes**:
- In C++, structs and classes are almost the same.
- Difference:
    - Struct variables | Public by default.
    - Class variables  | Private by default.
- No `typedef` is required for either.

**General Practice**:
- Make **variables private**.
- Make **functions public**.

----------------------------------------------------------------------
CONSTRUCTORS
----------------------------------------------------------------------

- A **constructor** creates an instance of a class.
- Types:
    - **Default Constructor** → No parameters.
    - **Parameterized Constructor** → Accepts parameters.
    - **Copy Constructor** → Creates a new object as a copy of another.

Remember the **scope resolution operator**: `::`

----------------------------------------------------------------------
BEST PRACTICES
----------------------------------------------------------------------

- Use `const` instead of `#define`.
- Avoid writing `int foo(void)` → The `void` is deprecated.
- Prefer the `bool` data type when applicable.

----------------------------------------------------------------------
POINTERS
----------------------------------------------------------------------

- C++ uses **`new`** and **`delete`** for dynamic memory allocation and deallocation.  
- Rarely uses legacy C functions: **`malloc`**, **`calloc`**, **`realloc`**, and **`free`**.
- C++11 introduced **`nullptr`** → replaces the old **`NULL`** keyword.
- `nullptr` provides better type safety and should always be used instead of `NULL`.

Example:
int* ptr = new int(10);   // allocate memory
delete ptr;               // free memory

----------------------------------------------------------------------
RECURSION
----------------------------------------------------------------------

A **recursive function** is a function that calls itself to solve smaller subproblems.  
The function **must have a base case** to avoid infinite recursion.

Example: Factorial using recursion

int factorial(int n) {
    if (n <= 1) return 1;          // base case
    return n * factorial(n - 1);   // recursive case
}

----------------------------------------------------------------------
HEADER FILE
----------------------------------------------------------------------

- Class declarations go in the **header file** (`.h`).
- Class implementations go in the **implementation file** (`.cpp`).
- The **header file** and **implementation file** should have the **same name** as the class.
- The **header file** should be `#include`'d in the **implementation file**.
- Implementation (`.cpp`) files should **NOT** be `#include`'d anywhere.
- Header files should have **include guards**:
    #ifndef MYCLASS_H
    #define MYCLASS_H

    class MyClass {
        // declarations
    };

    #endif
- Alternatively, you may use `#pragma once`.
- Tiny helper classes can be added in other files if appropriate.sh

----------------------------------------------------------------------
MORE FOR CLASSES
----------------------------------------------------------------------

1. Const
*/

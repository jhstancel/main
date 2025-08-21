CXX      := clang++
CXXFLAGS := -std=c++20 -Wall -Wextra -Wpedantic -O2
LDFLAGS  :=

hello: main.cpp
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f hello

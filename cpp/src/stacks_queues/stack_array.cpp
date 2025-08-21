#include <vector>
template <typename T>
class StackArray {
    std::vector<T> a;
public:
    void push(const T& v){ a.push_back(v); }
    void pop(){ a.pop_back(); }
    const T& top() const { return a.back(); }
    bool empty() const { return a.empty(); }
};
template class StackArray<int>;

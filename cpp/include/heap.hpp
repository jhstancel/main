#pragma once
#include <vector>
template <typename T, typename Cmp=std::less<T>>
class BinaryHeap {
public:
    void push(const T& v);
    const T& top() const;
    void pop();
    bool empty() const { return data_.empty(); }
private:
    std::vector<T> data_;
    Cmp cmp_;
    void siftUp(std::size_t i);
    void siftDown(std::size_t i);
};

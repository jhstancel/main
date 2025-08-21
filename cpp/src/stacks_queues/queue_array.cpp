#include <queue>
template <typename T>
class QueueArray {
    std::queue<T> q;
public:
    void push(const T& v){ q.push(v); }
    void pop(){ q.pop(); }
    const T& front() const { return q.front(); }
    bool empty() const { return q.empty(); }
};
template class QueueArray<int>;

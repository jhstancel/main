#pragma once
#include <cstddef>
template <typename T>
struct Node {
    T data;
    Node* next{nullptr};
    explicit Node(const T& v): data(v) {}
};

template <typename T>
class SinglyLinkedList {
public:
    ~SinglyLinkedList();
    void pushFront(const T& v);
    bool popFront(T& out);
    bool empty() const { return head_ == nullptr; }
    std::size_t size() const { return size_; }
private:
    Node<T>* head_{nullptr};
    std::size_t size_{0};
};

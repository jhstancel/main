#include "linked_list.hpp"
template <typename T>
SinglyLinkedList<T>::~SinglyLinkedList() {
    auto* cur = head_;
    while (cur) { auto* n = cur->next; delete cur; cur = n; }
}
template <typename T>
void SinglyLinkedList<T>::pushFront(const T& v) {
    auto* n = new Node<T>(v);
    n->next = head_;
    head_ = n;
    ++size_;
}
template <typename T>
bool SinglyLinkedList<T>::popFront(T& out) {
    if (!head_) return false;
    auto* n = head_;
    head_ = head_->next;
    out = n->data;
    delete n;
    --size_;
    return true;
}
// Explicit instantiations for common types (extend as needed)
template class SinglyLinkedList<int>;
template class SinglyLinkedList<long>;
template class SinglyLinkedList<double>;

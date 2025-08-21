#include "heap.hpp"
#include <stdexcept>
template <typename T, typename Cmp>
void BinaryHeap<T,Cmp>::push(const T& v){
    data_.push_back(v); siftUp(data_.size()-1);
}
template <typename T, typename Cmp>
const T& BinaryHeap<T,Cmp>::top() const{
    if (data_.empty()) throw std::runtime_error("empty heap");
    return data_.front();
}
template <typename T, typename Cmp>
void BinaryHeap<T,Cmp>::pop(){
    std::swap(data_.front(), data_.back());
    data_.pop_back();
    if (!data_.empty()) siftDown(0);
}
template <typename T, typename Cmp>
void BinaryHeap<T,Cmp>::siftUp(std::size_t i){
    while(i>0){
        std::size_t p=(i-1)/2;
        if (!cmp_(data_[i], data_[p])) break;
        std::swap(data_[i], data_[p]); i=p;
    }
}
template <typename T, typename Cmp>
void BinaryHeap<T,Cmp>::siftDown(std::size_t i){
    for(;;){
        std::size_t l=2*i+1, r=2*i+2, m=i;
        if (l<data_.size() && cmp_(data_[l], data_[m])) m=l;
        if (r<data_.size() && cmp_(data_[r], data_[m])) m=r;
        if (m==i) break;
        std::swap(data_[i], data_[m]); i=m;
    }
}
template class BinaryHeap<int,std::less<int>>;

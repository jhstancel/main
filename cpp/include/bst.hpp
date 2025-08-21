#pragma once
template <typename T>
struct BSTNode {
    T key;
    BSTNode* left{nullptr};
    BSTNode* right{nullptr};
    explicit BSTNode(const T& k): key(k) {}
};
template <typename T>
class BST {
public:
    ~BST();
    void insert(const T& k);
    bool contains(const T& k) const;
private:
    BSTNode<T>* root_{nullptr};
};

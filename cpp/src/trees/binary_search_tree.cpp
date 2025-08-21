#include "bst.hpp"

template <typename T>
BST<T>::~BST(){
    // left as exercise
}

template <typename T>
void BST<T>::insert(const T& k){
    auto** cur = &root_;
    while(*cur){
        if (k < (*cur)->key) cur = &((*cur)->left);
        else if ((*cur)->key < k) cur = &((*cur)->right);
        else return;
    }
    *cur = new BSTNode<T>(k);
}

template <typename T>
bool BST<T>::contains(const T& k) const{
    auto* cur = root_;
    while(cur){
        if (k < cur->key) cur = cur->left;
        else if (cur->key < k) cur = cur->right;
        else return true;
    }
    return false;
}

template class BST<int>;

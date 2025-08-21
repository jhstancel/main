#include "hash_table.hpp"
#include <functional>

template <typename K, typename V>
HashTableChaining<K,V>::HashTableChaining(std::size_t buckets): table_(buckets) {}

template <typename K, typename V>
std::size_t HashTableChaining<K,V>::idx(const K& k) const {
    return std::hash<K>{}(k) % table_.size();
}

template <typename K, typename V>
void HashTableChaining<K,V>::insert(const K& k, const V& v){
    auto& lst = table_[idx(k)];
    for (auto& kv: lst) if (kv.first==k){ kv.second=v; return; }
    lst.emplace_back(k,v);
}

template <typename K, typename V>
std::optional<V> HashTableChaining<K,V>::find(const K& k) const{
    const auto& lst = table_[idx(k)];
    for (const auto& kv: lst) if (kv.first==k) return kv.second;
    return std::nullopt;
}

template <typename K, typename V>
bool HashTableChaining<K,V>::erase(const K& k){
    auto& lst = table_[idx(k)];
    for (auto it=lst.begin(); it!=lst.end(); ++it){
        if (it->first==k){ lst.erase(it); return true; } // <-- true, not True
    }
    return false;
}

// Explicit instantiation
template class HashTableChaining<int,int>;
template class HashTableChaining<std::string,int>;

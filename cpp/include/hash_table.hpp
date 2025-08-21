#pragma once
#include <vector>
#include <list>
#include <optional>
template <typename K, typename V>
class HashTableChaining {
public:
    explicit HashTableChaining(std::size_t buckets=101);
    void insert(const K& k, const V& v);
    std::optional<V> find(const K& k) const;
    bool erase(const K& k);
private:
    std::vector<std::list<std::pair<K,V>>> table_;
    std::size_t idx(const K& k) const;
};

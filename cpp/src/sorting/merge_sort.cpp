#include "sorting.hpp"
#include <cstddef>
#include <vector>

template <typename T>
static void mrec(std::vector<T>& a, std::vector<T>& tmp, std::size_t l, std::size_t r) {
    if (l >= r) return;
    std::size_t m = (l + r) / 2;
    mrec(a, tmp, l, m);
    mrec(a, tmp, m + 1, r);

    std::size_t i = l, j = m + 1, k = l;
    while (i <= m || j <= r) {
        if (j > r || (i <= m && a[i] <= a[j])) tmp[k++] = a[i++];
        else                                    tmp[k++] = a[j++];
    }
    for (std::size_t t = l; t <= r; ++t) a[t] = tmp[t];
}

template <typename T>
void mergeSort(std::vector<T>& a) {
    if (a.empty()) return;
    std::vector<T> tmp(a.size());
    mrec(a, tmp, 0, a.size() - 1);
}

template void mergeSort<int>(std::vector<int>&);

#include "sorting.hpp"
#include <algorithm>
#include <cstddef>
#include <vector>

template <typename T>
static std::size_t part(std::vector<T>& a, std::size_t l, std::size_t r) {
    T p = a[r];
    std::size_t i = l;
    for (std::size_t j = l; j < r; ++j) {
        if (a[j] < p) { std::swap(a[i], a[j]); ++i; }
    }
    std::swap(a[i], a[r]);
    return i;
}

template <typename T>
static void qrec(std::vector<T>& a, std::size_t l, std::size_t r) {
    if (l >= r) return;
    std::size_t m = part(a, l, r);
    if (m > 0) qrec(a, l, m - 1);
    qrec(a, m + 1, r);
}

template <typename T>
void quickSort(std::vector<T>& a) {
    if (!a.empty()) qrec(a, 0, a.size() - 1);
}

template void quickSort<int>(std::vector<int>&);

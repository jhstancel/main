#include <cstddef>
#include <vector>

long long fibDP(int n) {
    if (n <= 1) return n;
    std::vector<long long> dp(static_cast<std::size_t>(n) + 1);
    dp[0] = 0; dp[1] = 1;
    for (std::size_t i = 2; i <= static_cast<std::size_t>(n); ++i)
        dp[i] = dp[i - 1] + dp[i - 2];
    return dp[static_cast<std::size_t>(n)];
}

# 121. Best Time to Buy and Sell Stock [Easy]
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
# Accepted 2026-05-21  runtime 58 ms  memory 28.6 MB

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l , r = 0, 1
        maxP = 0

        while r < len(prices):
            if prices[l] < prices[r]:
                profit = prices[r] - prices[l]
                maxP = max(maxP , profit)
            else:
                l = r
            r += 1
        return maxP

# 875. Koko Eating Bananas [Medium]
# https://leetcode.com/problems/koko-eating-bananas/
# Accepted 2026-05-16  runtime 172 ms  memory 20.6 MB

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        res = r

        while l <= r:
            k = (l + r) // 2
            hours = 0
            for p in piles:
                hours += math.ceil(p / k)
            if hours <= h:
                res = min(res, k)
                r = k - 1
            else: 
                l = k + 1
        return res

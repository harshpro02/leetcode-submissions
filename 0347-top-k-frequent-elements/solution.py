# 347. Top K Frequent Elements [Medium]
# https://leetcode.com/problems/top-k-frequent-elements/
# Accepted 2026-09-07  runtime 3 ms  memory 22.8 MB

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        for n in nums:
            count[n] = 1 + count.get(n , 0)
        sorted_nums = sorted(count.keys(), key = lambda x: count[x], reverse = True)
        return sorted_nums[:k]

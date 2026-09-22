# 704. Binary Search [Easy]
# https://leetcode.com/problems/binary-search/
# Accepted 2026-05-12  runtime 0 ms  memory 20.5 MB


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        
        while l <= r :
            m = ( l + r ) // 2
            if nums[m] > target :
                r = m - 1
            elif nums[m] < target :
                l = m + 1
            else :
                return m
        return -1

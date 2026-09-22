# 35. Search Insert Position [Easy]
# https://leetcode.com/problems/search-insert-position/
# Accepted 2026-05-12  runtime 0 ms  memory 19.9 MB

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        
        while l <= r :
            m = (l + r) // 2
            if target == nums[m]:
                return m 
            if target > nums[m]:
                l = m + 1
            else:
                r = m - 1
        return l

# 153. Find Minimum in Rotated Sorted Array [Medium]
# https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
# Accepted 2026-05-16  runtime 0 ms  memory 19.2 MB

class Solution:
    def findMin(self, nums: List[int]) -> int:
        res = nums[0]
        l , r = 0, len(nums)-1

        while l <= r:
            if nums[l] < nums[r]:
                res = min(res , nums[l])
                break
            
            m = (l + r) // 2
            res = min(res,nums[m])
            if nums[m] >= nums[l]:
                l = m + 1
            else:
                r = m - 1
        return res

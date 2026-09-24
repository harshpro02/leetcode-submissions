# 15. 3Sum [Medium]
# https://leetcode.com/problems/3sum/
# Accepted 2026-09-24  runtime 542 ms  memory 22.1 MB

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        for i , n in enumerate(nums):
            if i > 0 and n == nums[i-1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                total = n + nums[l] + nums[r]
                if total > 0:
                    r -= 1
                elif total < 0:
                    l += 1
                else:
                    res.append([n, nums[l],nums[r]])
                    l += 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
        return res

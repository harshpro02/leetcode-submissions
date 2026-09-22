# 238. Product of Array Except Self [Medium]
# https://leetcode.com/problems/product-of-array-except-self/
# Accepted 2026-06-12  runtime 19 ms  memory 25.4 MB

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix 
            prefix *= nums[i]
    

        postfix = 1 
        for i in range(len(nums) -1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        return res

# 1. Two Sum [Easy]
# https://leetcode.com/problems/two-sum/
# Accepted 2026-09-22  runtime 0 ms  memory 20.5 MB

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevmap = {} 
        for i, n in enumerate(nums): 
            diff = target - n 
            if diff in prevmap: 
                return [prevmap[diff],i] 
            prevmap[n] = i

# 128. Longest Consecutive Sequence [Medium]
# https://leetcode.com/problems/longest-consecutive-sequence/
# Accepted 2026-06-12  runtime 36 ms  memory 36.5 MB

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longest = 0

        for n in numSet:                      
            if n - 1 not in numSet:           
                length = 1                    
                while (n + length) in numSet:
                    length += 1
                longest = max(longest, length) 

        return longest

# 167. Two Sum II - Input Array Is Sorted [Medium]
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
# Accepted 2026-09-22  runtime 0 ms  memory 22.5 MB

class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l, r = 0, len(numbers)-1
        while l < r:
            total = numbers[l] + numbers[r]
            if target < total:
                r -= 1
            elif target > total:
                l += 1
            else:
                return [l+1,r+1]

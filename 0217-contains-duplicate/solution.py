# 217. Contains Duplicate [Easy]
# https://leetcode.com/problems/contains-duplicate/
# Accepted 2026-08-28  runtime 14 ms  memory 32.1 MB

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False

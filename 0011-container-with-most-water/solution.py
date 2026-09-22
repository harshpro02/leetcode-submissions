# 11. Container With Most Water [Medium]
# https://leetcode.com/problems/container-with-most-water/
# Accepted 2026-01-25  runtime 52 ms  memory 29.5 MB

class Solution:
    def maxArea(self, height: List[int]) -> int:
        res = 0
        l, r = 0, len(height) - 1

        while l < r:
            area = (r - l) * min(height[l], height[r])
            res = max(res, area)

            if height[l] < height[r]:
                l += 1
            else:
                r-=1
        return res

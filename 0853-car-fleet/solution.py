# 853. Car Fleet [Medium]
# https://leetcode.com/problems/car-fleet/
# Accepted 2026-02-09  runtime 239 ms  memory 40.4 MB

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
         pair = [[p, s] for p, s in zip (position, speed)]
         stack = []

         for p, s in sorted(pair)[::-1]:
            stack.append((target - p) / s)
            if len(stack) >= 2 and stack[-1] <= stack[-2]:
                stack.pop()
         return len(stack)

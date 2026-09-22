# 739. Daily Temperatures [Medium]
# https://leetcode.com/problems/daily-temperatures/
# Accepted 2026-02-05  runtime 136 ms  memory 36 MB

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        stack =[]

        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:
                stackT, stackInd = stack.pop()
                res[stackInd] = (i - stackInd)
            stack.append([t, i])
        return res

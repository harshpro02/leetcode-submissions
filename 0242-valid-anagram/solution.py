# 242. Valid Anagram [Easy]
# https://leetcode.com/problems/valid-anagram/
# Accepted 2026-09-02  runtime 11 ms  memory 19.4 MB

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s)!=len(t):
            return False
        countS, countT = {},{}
        for i in range (len(s)):
            countS[s[i]] = 1 + countS.get(s[i],0)
            countT[t[i]] = 1 + countT.get(t[i],0)
        return countS==countT

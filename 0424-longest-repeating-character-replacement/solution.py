# 424. Longest Repeating Character Replacement [Medium]
# https://leetcode.com/problems/longest-repeating-character-replacement/
# Accepted 2026-05-22  runtime 139 ms  memory 19.6 MB

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        res = 0
        l = 0 

        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r] , 0)
            while (r - l + 1) - max(count.values()) > k:
                count[s[l]] -= 1
                l += 1
            res = max(res , r - l + 1)
        return res

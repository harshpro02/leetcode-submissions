# 3. Longest Substring Without Repeating Characters [Medium]
# https://leetcode.com/problems/longest-substring-without-repeating-characters/
# Accepted 2026-09-22  runtime 207 ms  memory 20.1 MB

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        l = 0
        longest = 0
        for r in range(len(s)):
            while s[r] in seen:
                seen.remove(s[l])
                l += 1
            seen.add(s[r])
            longest = max(longest, r - l + 1)
        return longest

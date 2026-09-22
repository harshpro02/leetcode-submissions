# 49. Group Anagrams [Medium]
# https://leetcode.com/problems/group-anagrams/
# Accepted 2026-06-10  runtime 12 ms  memory 21.9 MB

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for word in strs:
            key = ''.join(sorted(word))
            if key not in groups:
                groups[key] = []
            groups[key].append(word)
        return list(groups.values())

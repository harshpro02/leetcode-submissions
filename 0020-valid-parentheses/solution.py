# 20. Valid Parentheses [Easy]
# https://leetcode.com/problems/valid-parentheses/
# Accepted 2026-02-02  runtime 0 ms  memory 19.4 MB

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        closeToOpen = { ")" : "(", "]" : "[", "}" : "{" }
        

        for c in s:
            if c in closeToOpen:
                if stack and stack[-1] == closeToOpen[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)

        return True if not stack else False

# 150. Evaluate Reverse Polish Notation [Medium]
# https://leetcode.com/problems/evaluate-reverse-polish-notation/
# Accepted 2026-02-05  runtime 4 ms  memory 20.8 MB

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for c in tokens:
            if c == "+":
                stack.append(stack.pop() + stack.pop())
            elif c == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a) 
            elif c == "*":
                stack.append(stack.pop() * stack.pop())
            elif c == "/":
                 a, b = stack.pop(), stack.pop()
                 stack.append(int(b / a))
            else:
                stack.append(int(c))
        return stack[0]

# 155. Min Stack [Medium]
# https://leetcode.com/problems/min-stack/
# Accepted 2026-02-02  runtime 10 ms  memory 22.6 MB

class MinStack:

    def __init__(self):
        self.stack=[]
        self.minStack=[]


    def push(self, val: int) -> None:
        self.stack.append(val)
        val = min(val, self.minStack[-1] if self.minStack else val)
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()

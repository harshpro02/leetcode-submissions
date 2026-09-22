# 36. Valid Sudoku [Medium]
# https://leetcode.com/problems/valid-sudoku/
# Accepted 2026-06-12  runtime 3 ms  memory 19.2 MB

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = {}
        cols = {}
        boxes = {}

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == ".":
                    continue

                box_key = (r//3 , c//3)

                if r not in rows:
                    rows[r] = set()
                if c not in cols:
                    cols[c] = set()
                if box_key not in boxes:
                    boxes[box_key] = set()

                if val in rows[r] or val in cols[c] or val in boxes[box_key]:
                    return False

                rows[r].add(val)
                cols[c].add(val)
                boxes[box_key].add(val)
        return True

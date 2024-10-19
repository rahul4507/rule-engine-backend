class Solution:

    def __init__(self):
        self.priority = {
            '(': 1,
            'AND':2,
            'OR':2,
            '<':2,
            '>':2,
            '>=':2,
            '<=':2,
            '=':2,
        }

    def expTree(self, tokens: list) -> 'Node':
        ops = [] # not Node yet
        stack = [] # already Node

        for token in tokens:
            if token == '(':
                ops.append(token)
            elif isinstance(token,str):
                stack.append(Node(token))
            elif token == ')':
                while ops[-1] != '(':
                    self.combine(ops, stack)
                ops.pop() # pop left '('
            else: # then operator
                # @note: must be >=, for test case "1+2+3+4+5"
                while ops and self.priority.get(ops[-1], 0) >= self.priority[token]:
                    self.combine(ops, stack)

                ops.append(token)

        while len(stack) > 1: # eg input, '1+2'
            self.combine(ops, stack)

        return stack[0]

    def inorder(self, root):
        if root:
            if root.left:
                print("(", end="")
            self.inorder(root.left)
            print(root.val, end=" ")
            self.inorder(root.right)
            if root.right:
                print(")", end="")

    def combine(self, ops: list, stack: list) -> None:
        root = Node(ops.pop())
        # right first, then left, since it's a stack
        root.right = stack.pop()
        root.left = stack.pop()

        stack.append(root)


class Node:

    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None

import re

rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

# Tokenize the string using regex to handle words, operators, and parentheses separately
tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", rule)

# Iterate through the list of tokens and print each one
for token in tokens:
    print(token)

rule1 = Solution()
root = rule1.expTree(tokens)
rule1.inorder(root)

import re
import json
from collections import Counter


class ExpressionTree:
    def __init__(self, rule_string):
        """Initialize with the rule string."""
        self.rule_string = rule_string
        self.priority = {
            '(': 1,
            'AND': 2,
            'OR': 3,
            '<': 3,
            '>': 3,
            '>=': 3,
            '<=': 3,
            '=': 3,
        }
        # Tokenize the rule string using regex to separate operands, operators, and parentheses
        self.tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", self.rule_string)

    def build_tree(self) -> dict:
        """Build the expression tree as a nested dictionary."""
        ops = []  # Stack for operators
        stack = []  # Stack for nodes (operands and sub-trees represented as dicts)

        for token in self.tokens:
            if token == '(':
                ops.append(token)
            elif token == ')':
                # Pop and combine until '(' is found
                while ops and ops[-1] != '(':
                    self.combine(ops, stack)
                ops.pop()  # Remove the '('
            elif token in self.priority:
                # Ensure operator precedence is respected
                while ops and self.priority.get(ops[-1], 0) >= self.priority[token]:
                    self.combine(ops, stack)
                ops.append(token)
            else:
                # Treat any other token as an operand (number, variable, or string)
                stack.append({"val": token, "left": None, "right": None})

        # Combine remaining operators in the ops stack
        while ops:
            self.combine(ops, stack)

        return stack[0] if stack else None

    def print_tree(self, node: dict, level=0, label='.'):
        """Print tree in structured format using nested dict."""
        indent = '   ' * level + label + ': '
        print(indent + node['val'])
        if node.get('left'):
            self.print_tree(node['left'], level + 1, 'L')
        if node.get('right'):
            self.print_tree(node['right'], level + 1, 'R')

    def inorder(self, root: dict) -> str:
        """In-order traversal of the dictionary-based tree to return the expression."""
        result = []

        def traverse(node):
            if node:
                if node['left']:
                    result.append("(")
                traverse(node['left'])
                result.append(f"{node['val']} ")
                traverse(node['right'])
                if node['right']:
                    result.append(") ")

        traverse(root)
        return ''.join(result)

    def combine(self, ops: list, stack: list) -> None:
        """Combine the top two nodes in the stack with the operator."""
        if len(ops) == 0 or len(stack) < 2:
            return  # Safeguard for underflow issues

        operator = ops.pop()
        right = stack.pop()
        left = stack.pop()

        # Create a new dictionary node for the operator
        root = {
            "val": operator,
            "left": left,
            "right": right
        }

        stack.append(root)


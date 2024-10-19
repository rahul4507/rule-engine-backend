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
            'OR': 2,
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

    def get_tree_json(self):
        """Return the tree as a JSON object."""
        tree = self.build_tree()
        return json.dumps(tree, indent=4)

    def combine_rules(rules):
        combined_tree = None
        combined_tokens = []

        # Step 1: Tokenize each rule and build individual ASTs
        for rule in rules:
            tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", rule)
            builder = ExpressionTree(rule)
            ast = builder.expTree(tokens)
            combined_tokens.append(ast)

        # Step 2: Combine the individual ASTs into a single AST
        if combined_tokens:
            # A heuristic could be to always combine using the main logical operator
            # Here, we assume we are combining using 'OR' as an example
            combined_tree = {
                "val": "OR",
                "left": combined_tokens[0],
                "right": combined_tokens[1] if len(combined_tokens) > 1 else None
            }

            # Combine remaining ASTs
            for i in range(2, len(combined_tokens)):
                combined_tree = {
                    "val": "OR",
                    "left": combined_tree,
                    "right": combined_tokens[i]
                }

        return combined_tree

    def combine_rules_based_on_most_frequent_op(self, rules: list) -> dict:
        """Combine a list of rule strings into a single AST based on the most frequent operator."""
        operator_count = Counter()

        # Count operators in all rules
        for rule in rules:
            tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", rule)
            for token in tokens:
                if token in self.priority:
                    operator_count[token] += 1

        # Determine the most frequent operator
        most_common_operator = operator_count.most_common(1)[0][0] if operator_count else None

        # Build combined rule string
        combined_rule = f" {' '.join(['(' + rule + ')' for rule in rules])} "  # Wrap each rule in parentheses
        combined_rule = combined_rule.replace(") (", f") {most_common_operator} (")  # Add the most common operator

        # Tokenize the combined rule
        combined_tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", combined_rule)

        # Create a new expression tree
        return self.expTree(combined_tokens)

import re
from collections import Counter

class ExpressionTree:
    def __init__(self, rule_string=None, ast=None, data=None):
        """Initialize with the rule string."""
        self.rule_string = rule_string
        self.ast=ast
        self.data = data
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
        self.operators = {
            'AND': lambda x, y: x and y,
            'OR': lambda x, y: x or y,
            '>': lambda x, y: float(x) > float(y),
            '<': lambda x, y: float(x) < float(y),
            '>=': lambda x, y: float(x) >= float(y),
            '<=': lambda x, y: float(x) <= float(y),
            '=': lambda x, y: str(x).strip("'") == str(y).strip("'")
        }
        # Tokenize the rule string using regex to separate operands, operators, and parentheses
        if self.rule_string:
            self.tokens = re.findall(r"\w+|[><=()]|'.+?'|AND|OR", self.rule_string)
        else:
            self.tokens=[]

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

        self.ast = stack[0] if stack else None
        return self.ast

    def combine(self, ops: list, stack: list) -> None:
        """Combine the top two nodes in the stack with the operator."""
        if len(ops) == 0 or len(stack) < 2:
            return

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

    def print(self):

        def print_tree(node,level=0, label='.'):
            """Print tree in structured format using nested dict."""
            indent = '   ' * level + label + ': '
            print(indent + node['val'])
            if node.get('left'):
                print_tree(node['left'], level + 1, 'L')
            if node.get('right'):
                print_tree(node['right'], level + 1, 'R')

        print_tree(self.ast,2)

    def inorder(self) -> str:
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

        traverse(self.ast)
        return ''.join(result)

    def evaluate(self):
        """Evaluates the entire expression tree."""
        return self._evaluate_node(self.ast)

    def _evaluate_node(self, node):
        """Recursively evaluates each node in the tree."""
        if not node:
            return None

        # If it's a leaf node
        if node['left'] is None and node['right'] is None:
            # If it's a field name, get the value from data
            if node['val'] in self.data:
                return self.data[node['val']]
            # Otherwise return the value (might be a literal)
            return node['val']

        # Get operator
        operator = node['val']

        # If it's a comparison operator
        if operator in {'>', '<', '>=', '<=', '='}:
            left_val = self._evaluate_node(node['left'])
            right_val = self._evaluate_node(node['right'])
            return self.operators[operator](left_val, right_val)

        # If it's a logical operator (AND/OR)
        left_result = self._evaluate_node(node['left'])
        right_result = self._evaluate_node(node['right'])
        if operator in self.operators:
            return self.operators[operator](left_result, right_result)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def count_operators(self, ast):
        """Recursively count only AND and OR operators in the AST."""
        if not ast or (ast['left'] is None and ast['right'] is None):
            return Counter()

        # Count the current operator only if it's AND or OR
        operator_counter = Counter()
        if ast['val'] in ['AND', 'OR']:
            operator_counter[ast['val']] += 1

        # Recursively count in left and right subtrees
        operator_counter.update(self.count_operators(ast['left']))
        operator_counter.update(self.count_operators(ast['right']))

        return operator_counter

    def combine_two_asts(self, ast1, ast2):
        """Combine two ASTs based on the most frequent operator heuristic."""
        # Count operators in both ASTs
        ast1_operators = self.count_operators(ast1)
        ast2_operators = self.count_operators(ast2)

        # Combine the operator counts
        combined_operators = ast1_operators + ast2_operators

        # Find the most frequent operator
        most_frequent_operator = combined_operators.most_common(1)[0][0]

        # Create the new root node with the most frequent operator
        combined_ast = {
            "val": most_frequent_operator,
            "left": ast1,
            "right": ast2
        }

        return combined_ast

    def combine_multiple_asts(self, asts):
        """Combine multiple ASTs into a single AST using the most frequent operator heuristic."""
        if not asts:
            return None
        if len(asts) == 1:
            return asts[0]

        combined_ast = asts[0]

        # Combine each AST one by one
        for ast in asts[1:]:
            combined_ast = self.combine_two_asts(combined_ast, ast)

        self.ast = combined_ast
        return self.ast

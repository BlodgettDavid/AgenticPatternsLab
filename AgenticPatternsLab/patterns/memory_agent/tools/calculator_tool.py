import ast
import operator

class CalculatorTool:
    """
    A deterministic, safe arithmetic expression evaluator.
    Supports +, -, *, /, **, and parentheses.
    """

    name = "calculate"

    # Allowed operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def run(self, expression: str) -> str:
        expression = expression.strip()
        if not expression:
            return "No expression provided."

        try:
            node = ast.parse(expression, mode="eval").body
            result = self._eval(node)
            return str(result)
        except Exception:
            return f"Invalid expression: '{expression}'"

    def _eval(self, node):
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n

        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.OPERATORS:
                raise ValueError("Unsupported operator")
            return self.OPERATORS[op_type](self._eval(node.left), self._eval(node.right))

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self.OPERATORS:
                raise ValueError("Unsupported unary operator")
            return self.OPERATORS[op_type](self._eval(node.operand))

        raise ValueError("Unsupported expression")
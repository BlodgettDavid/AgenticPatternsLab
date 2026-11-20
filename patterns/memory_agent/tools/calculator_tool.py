import ast
import operator
from typing import Any, Dict
from utils.tool_base import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "A deterministic, safe arithmetic expression evaluator."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate.",
            }
        },
        "required": ["expression"],
    }

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def run(self, expression: str = "", **kwargs: Any) -> str:
        if not expression and "expression" in kwargs:
            expression = kwargs.get("expression", "")
        expression = str(expression).strip()
        
        if not expression:
            raise ValueError("No expression provided.")

        try:
            node = ast.parse(expression, mode="eval").body
            result = self._eval(node)
            return str(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: '{expression}'")

    def _eval(self, node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Constant):
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
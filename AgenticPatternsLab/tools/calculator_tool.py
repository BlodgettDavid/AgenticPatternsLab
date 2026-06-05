def calculator_tool(expr: str) -> str:
    """
    Evaluate simple arithmetic expressions safely.
    Supports +, -, *, /.
    """
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in expr):
        return "Error: invalid characters"

    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Error: invalid expression"
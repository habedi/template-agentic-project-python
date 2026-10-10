"""Custom tools for the assistant agent."""

import ast
import operator
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, cast

# Allowed binary operators for mathematical calculation.
_SAFE_BINARY_OPS: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators for mathematical calculation.
_SAFE_UNARY_OPS: dict[type[ast.unaryop], Callable[[Any], Any]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float | int:
    """Evaluates an abstract syntax tree expression containing arithmetic."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp):
        bin_op_type = type(node.op)
        if bin_op_type not in _SAFE_BINARY_OPS:
            raise ValueError(f"Unsupported binary operator: {bin_op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        res = _SAFE_BINARY_OPS[bin_op_type](left, right)
        return cast(float | int, res)
    elif isinstance(node, ast.UnaryOp):
        unary_op_type = type(node.op)
        if unary_op_type not in _SAFE_UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {unary_op_type.__name__}")
        operand = _safe_eval(node.operand)
        res = _SAFE_UNARY_OPS[unary_op_type](operand)
        return cast(float | int, res)
    else:
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Evaluates an arithmetic expression.

    Args:
        expression: A mathematical expression string, such as '15 * 4 + (100 / 5)'.

    Returns:
        The evaluated result as a string or an error description.
    """
    try:
        parsed = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(parsed.body)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as exc:
        return f"Error evaluating expression '{expression}': {exc}"


def get_current_utc_time() -> str:
    """Returns the current date, time, and day of the week in UTC.

    Returns:
        A formatted string with the current UTC datetime.
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC (%A)")


def text_statistics(text: str) -> dict[str, Any]:
    """Computes statistics for a given body of text.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing word_count, character_count, and line_count.
    """
    words = text.split()
    lines = text.splitlines()
    return {
        "character_count": len(text),
        "word_count": len(words),
        "line_count": len(lines),
    }

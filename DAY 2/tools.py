import ast
import operator
from config import VENUE_PRICES

def get_venue_price(venue_name: str) -> str:
    """Look up the booking price for one event venue."""
    fee = VENUE_PRICES.get(venue_name.strip().upper())
    return str(fee) if fee is not None else f"Unknown venue: {venue_name}"

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"

TOOL_FUNCTIONS = {"get_venue_price": get_venue_price, "calculator": calculator}

TOOLS = [
    {"type": "function", "function": {
        "name": "get_venue_price",
        "description": "Get the price in rupees for a single venue, for example GRAND_HALL.",
        "parameters": {"type": "object", "properties": {"venue_name": {"type": "string"}}, "required": ["venue_name"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}}
]
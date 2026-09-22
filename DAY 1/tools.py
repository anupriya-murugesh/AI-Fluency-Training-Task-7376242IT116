import ast
import operator

from config import MENU_PRICES


def get_item_price(item_name: str) -> str:
    price = MENU_PRICES.get(item_name)

    if price is None:
        return f"Unknown item: {item_name}"

    return str(price)


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    try:
        result = _evaluate(
            ast.parse(expression, mode="eval").body
        )
        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "get_item_price": get_item_price,
    "calculator": calculator,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_item_price",
            "description": "Get the price of a canteen item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string"
                    }
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


if __name__ == "__main__":
    print(
        "get_item_price('Fried Rice') ->",
        get_item_price("Fried Rice")
    )

    print(
        "calculator('100+25') ->",
        calculator("100+25")
    )
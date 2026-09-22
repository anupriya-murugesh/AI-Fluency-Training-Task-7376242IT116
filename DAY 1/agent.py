import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, get_item_price, calculator


SYSTEM_PROMPT = """
You are a canteen assistant.

Rules:
1. Never guess item prices.
2. Always use get_item_price.
3. Use calculator for arithmetic.
4. Available items:
   Veg Sandwich
   Masala Dosa
   Fried Rice
   Lemon Juice
   Coffee
   Samosa
"""


def agent(question, max_steps=10):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            if "<|channel|>" in tool_name:
                tool_name = tool_name.split("<|channel|>")[0]

            args = json.loads(
                tool_call.function.arguments
            )

            if tool_name == "get_item_price":
                result = get_item_price(**args)

            elif tool_name == "calculator":
                result = calculator(**args)

            else:
                result = f"Unknown tool: {tool_name}"

            print(
                f" step {step}: "
                f"{tool_name}({args}) -> {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "Maximum steps reached."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:
        print("Q:", question)

        try:
            print("A:", agent(question))

        except Exception as error:
            print("ERROR:", error)

        print("-" * 70)
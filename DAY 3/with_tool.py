import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DAY 1')))

from config import client, MODEL
from my_tool import read_library_notice


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_library_notice",
            "description": "Read the library fine rules from the notice file.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


question = """
I returned a library book 8 days late.
How much fine should I pay?
"""

messages = [
    {
        "role": "system",
        "content": (
            "If the user asks about library fines, "
            "use the read_library_notice tool before answering."
        )
    },
    {
        "role": "user",
        "content": question
    }
]


response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    temperature=0
)

message = response.choices[0].message

print("=" * 50)
print("WITH TOOL")
print("=" * 50)

print("\nQUESTION:")
print(question)


if message.tool_calls:

    tool_call = message.tool_calls[0]

    print("\nTOOL CALLED:")
    print(tool_call.function.name)

    tool_result = read_library_notice()

    print("\nTOOL RESULT:")
    print(tool_result)

    messages.append(
        {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            ]
        }
    )

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        }
    )

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    print("\nFINAL ANSWER:")
    print(final_response.choices[0].message.content)

else:

    print("\nNO TOOL WAS CALLED")
    print("\nANSWER:")
    print(message.content)
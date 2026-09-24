import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DAY 1')))

from config import client, MODEL

question = """
I returned a library book 8 days late.
How much fine should I pay?
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=0
)

print("=" * 50)
print("WITHOUT TOOL")
print("=" * 50)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(response.choices[0].message.content)
import json
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are an event booking assistant. Never guess a price: always use get_venue_price. "
    "Use calculator for any arithmetic. Available venues: GRAND_HALL, GARDEN_TENT, ROOFTOP. "
    "If no tool is needed, answer directly."
)

def agent(question, max_steps=6, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        message = response.choices[0].message
        
        if not message.tool_calls:
            return message.content.strip()
            
        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function", "function": {"name": call.function.name, "arguments": call.function.arguments}} for call in message.tool_calls]
        })
        
        for call in message.tool_calls:
            name = call.function.name
            arguments = json.loads(call.function.arguments or "{}")
            function = TOOL_FUNCTIONS.get(name)
            result = str(function(**arguments)) if function else f"Unknown tool: {name}"
            if verbose:
                print(f" step {step}: {name}({arguments}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
            
    return "Stopped: maximum steps reached without a final answer."
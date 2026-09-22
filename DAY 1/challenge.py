from workflow import workflow
from agent import agent

question = (
    "I have Rs. 120. "
    "Which items can I buy from the canteen?"
)

print("Q:", question)
print()

print("Workflow :", workflow(question))
print()

print("Agent    :", agent(question))
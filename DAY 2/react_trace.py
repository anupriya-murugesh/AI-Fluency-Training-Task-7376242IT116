from agent import agent

QUESTION = (
    "What is the total cost for the GRAND_HALL and GARDEN_TENT after a 20% discount? By how much is it cheaper than the full price?"
)

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")
answer = agent(QUESTION, max_steps=8)
print("\nFINAL ANSWER:", answer)
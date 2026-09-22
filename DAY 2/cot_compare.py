from config import client, MODEL, banner

QUESTIONS = [
    "An event has 120 guests. Catering costs Rs. 500 per guest, plus a flat Rs. 5,000 service fee. If the total bill is split evenly between 2 hosts, how much does each host pay?",
    "A decorator brings 50 chairs. They find 5 are broken. They rent out half of the remaining chairs to another event, then find 10 more in storage. How many usable chairs do they have now?",
    "Table A is closer to the stage than Table B. Table C is further from the stage than Table B. Table D is closer to the stage than Table A. Which table is closest to the stage, and which is furthest?"
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."
COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step.\n"
    "Number each step and show the calculation in that step.\n"
    "After the steps, write the last line exactly as: Final Answer: <answer>"
)

def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")
from config import MENU_PRICES, QUESTIONS


def workflow(question):
    text = question.lower()

    if "fried rice" in text and "price" in text:
        return f"Price of Fried Rice: Rs. {MENU_PRICES['Fried Rice']}"

    if "coffee" in text and "lemon juice" in text and "total" in text:
        total = MENU_PRICES["Coffee"] + MENU_PRICES["Lemon Juice"]
        return f"Total cost: Rs. {total}"

    if "150" in text and "fried rice" in text and "coffee" in text:
        total = MENU_PRICES["Fried Rice"] + MENU_PRICES["Coffee"]

        if total <= 150:
            return f"Yes. Total cost is Rs. {total}"
        else:
            return f"No. Total cost is Rs. {total}"

    return "Sorry, I do not have a rule for this question."


if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW ===\n")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)
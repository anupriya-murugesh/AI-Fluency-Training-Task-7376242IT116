# Agentic AI Foundations and Open-Source Practice – Day 1

## Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

### Project Overview

This project demonstrates three different approaches to solving the same problem using a **College Canteen Assistant** scenario.

The objective is to answer user questions about menu items, prices, total costs, and budget-based purchases using private canteen data stored locally in the project.

The three approaches implemented are:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent

---

## Scenario

The canteen maintains private menu-price data that is not publicly available.

### Menu Data

| Item | Price (Rs.) |
|------|-------------|
| Fried Rice | 100 |
| Veg Sandwich | 60 |
| Masala Dosa | 50 |
| Lemon Juice | 30 |
| Coffee | 25 |
| Samosa | 20 |

---

## Example Questions

The systems were tested using the following questions:

1. What is the price of Fried Rice?
2. What is the total cost of Coffee and Lemon Juice?
3. I have ₹150. Can I buy Fried Rice and Coffee?
4. Write a two-line welcome message for canteen visitors.

### Challenge Question

> I have Rs. 120. Which items can I buy from the canteen?

---

## System 1 – Plain Chatbot

The chatbot sends the user's question directly to the Large Language Model (LLM).

```text
User Question
      ↓
     LLM
      ↓
   Response
```

Characteristics:

- Uses only an LLM
- Cannot directly access private menu data
- Good for general conversation
- May produce incomplete or assumed answers for private-data questions

---

## System 2 – Rule-Based Workflow

The workflow uses predefined Python rules and conditions.

```text
User Question
      ↓
Python Rules
      ↓
Calculation
      ↓
Response
```

Characteristics:

- No LLM involved
- Uses private menu data directly
- Reliable for known tasks
- Limited to predefined rules

---

## System 3 – AI Agent

The AI Agent combines an LLM with tools and an iterative reasoning loop.

Available tools:

- `get_item_price()` – retrieves menu prices
- `calculator()` – performs arithmetic operations

```text
User Question
      ↓
     LLM
      ↓
Reason
      ↓
Use Tool
      ↓
Observe Result
      ↓
Repeat if Needed
      ↓
Final Answer
```

Characteristics:

- Uses LLM + Tools + Loop
- Can access private menu data through tools
- Handles multi-step tasks
- More flexible than a rule-based workflow

---

## Project Structure

```text
.
├── agent.py
├── chatbot.py
├── workflow.py
├── tools.py
├── challenge.py
├── config.py
├── check_setup.py
├── requirements.txt
├── analysis.md
├── README.md
├── .gitignore
└── Output/
    ├── chatbot.png
    ├── workflow.png
    ├── agent.png
    └── challenge.png
```

---

## Technologies Used

- Python 3
- Groq API
- OpenAI GPT OSS 20B Model
- Python Virtual Environment (venv)

---

## Key Learning

This project demonstrates the core idea of Agentic AI:

```text
LLM + Tools + Loop = AI Agent
```

A plain chatbot relies only on an LLM, a workflow relies on predefined rules, while an AI agent can reason, use tools, observe results, and continue working until the task is completed.

For a detailed comparison and analysis, refer to **analysis.md**.

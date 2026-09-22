
# Analysis of Plain Chatbot, Rule-Based Workflow, and AI Agent for a College Canteen Assistant

## Introduction

For this project, I selected a **College Canteen Assistant** scenario. The canteen contains private menu-price information that is stored locally inside the project. The objective is to answer user questions about item prices, total costs, budget checks, and canteen-related messages.

The private data used in this scenario is shown below:

| Item | Price (Rs.) |
|------|-------------|
| Fried Rice | 100 |
| Veg Sandwich | 60 |
| Masala Dosa | 50 |
| Lemon Juice | 30 |
| Coffee | 25 |
| Samosa | 20 |

The same problem was solved using three different approaches:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent

The goal was to understand how each approach handles private data, calculations, decision-making, and user requests.

---

# 3.1 Explanation of Each Approach

## A. Plain Chatbot

The plain chatbot uses only a Large Language Model (LLM). It does not have direct access to the private canteen menu stored in the project files.

When a user asks a question, the request is sent directly to the LLM. The model generates a response based on its training and reasoning ability. Since it cannot see the private canteen data, it does not know the actual menu prices.

For example, when asked:

> What is the price of Fried Rice?

the chatbot could not provide the correct answer because it did not know the menu data. Instead, it asked the user to provide the canteen details.

Similarly, when asked to calculate the total cost of Coffee and Lemon Juice, it requested the prices before performing the calculation.

Interestingly, for the budget question:

> I have ₹150. Can I buy Fried Rice and Coffee?

the chatbot produced an answer using assumed prices rather than the private data. This demonstrates a major limitation of a plain chatbot. Although it can generate fluent responses, it cannot reliably access private information and may produce answers that do not match the actual data.

The chatbot performed well only for the welcome-message task because that question required general language generation rather than access to private data.

Therefore, a plain chatbot mainly provides responses using an LLM alone and cannot reliably answer questions that depend on private information.

---

## B. Rule-Based Workflow

The rule-based workflow does not use an LLM at all. Instead, it follows predefined Python rules and conditions.

When a user submits a question, the workflow checks whether the question matches one of the patterns that were explicitly programmed. If a matching rule is found, the workflow performs the required calculation and returns the result.

For example:

- The workflow correctly returned the price of Fried Rice.
- It correctly calculated the total cost of Coffee and Lemon Juice.
- It correctly checked whether Fried Rice and Coffee could be purchased within a ₹150 budget.

These tasks worked because corresponding rules were already implemented.

However, the workflow failed when asked:

> Write a two-line welcome message for canteen visitors.

Since no rule existed for generating creative text, the workflow returned:

> Sorry, I do not have a rule for this question.

The challenge question also revealed a limitation. The workflow could not reason about multiple menu combinations because no rule had been created for that scenario.

This approach is highly reliable for known situations but becomes difficult to maintain as the number of possible user requests grows.

The rule-based workflow therefore follows predefined steps and conditions, uses no LLM, and can only solve problems that were anticipated during development.

---

## C. AI Agent

The AI Agent combines an LLM, tools, and an iterative decision-making loop.

Unlike the chatbot, the agent can access private menu information through tools. In this project, two tools were available:

- `get_item_price()` – retrieves the price of a menu item.
- `calculator()` – performs arithmetic calculations.

When a question is received, the LLM first reasons about what information is required. It then decides whether a tool should be called.

If information is needed, the agent:

1. Selects the appropriate tool.
2. Executes the tool.
3. Observes the result.
4. Decides whether additional actions are required.
5. Repeats the process until it can answer the question.

This follows the pattern:

```text
Reason → Act → Observe → Repeat
```

For example, when asked:

> What is the total cost of Coffee and Lemon Juice?

the agent:

1. Retrieved the price of Coffee.
2. Retrieved the price of Lemon Juice.
3. Called the calculator tool.
4. Generated the final answer.

Similarly, for the budget question:

> I have ₹150. Can I buy Fried Rice and Coffee?

the agent retrieved both prices, calculated the total cost, compared it with the available budget, and produced the correct response.

The challenge question demonstrated the biggest advantage of the agent. It automatically explored multiple item combinations and identified affordable options within the specified budget. This required several reasoning and tool-use steps that were not explicitly hard-coded.

The AI Agent therefore combines an LLM + Tools + Loop. It reasons about the task, selects tools, observes results, and continues taking actions until the task is completed.

---

# 3.2 Comparison Table

| Basis for Comparison | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---------------------|---------------|---------------------|----------|
| Flexibility | High for general conversations | Low | High |
| Decision-making | LLM generates response directly | Fixed rules only | Dynamic reasoning with tools |
| Tool usage | No | No | Yes |
| Private-data access | No | Yes | Yes |
| Multi-step task handling | Limited | Only if explicitly coded | Excellent |
| Automation | Low | Medium | High |
| Reliability | Moderate | High for known cases | High when tools are available |

---

# 3.3 Suitability Analysis

For the College Canteen Assistant scenario, the AI Agent is the most suitable approach.

The chatbot provides natural responses but cannot reliably access private menu-price information. As observed during testing, it either requested additional information or used assumptions that did not match the actual data.

The rule-based workflow performed accurately for predefined tasks such as price lookup, cost calculation, and budget checking. However, it could not handle new requests outside its programmed rules. Every new feature would require additional coding.

The AI Agent combines the strengths of both approaches. It can access private data through tools while also using LLM reasoning to understand user requests. The agent successfully handled all test questions and the challenge task. It dynamically selected tools, performed calculations, and generated meaningful responses without requiring a separate rule for every possible situation.

Based on flexibility, multi-step reasoning, tool usage, and private-data access, the AI Agent is the most effective solution for this scenario.

---

# 3.4 Conclusion

This project highlights the differences between a plain chatbot, a rule-based workflow, and an AI agent.

A plain chatbot is most suitable for general conversations, creative writing, explanations, and situations where private data access is not required. It is easy to use but may provide incorrect information when asked about data it cannot access.

A rule-based workflow is most suitable for simple business processes with predictable requirements. It offers consistent and reliable outputs but struggles with unexpected requests and complex reasoning tasks.

An AI agent is most suitable when tasks require both reasoning and access to external information. By combining an LLM, tools, and a decision-making loop, an agent can retrieve private data, perform calculations, and adapt to more complex user requests.

Therefore, while all three approaches have their own strengths, AI agents provide the most powerful and flexible solution when real-world tasks involve private data, tool usage, and multi-step decision-making.

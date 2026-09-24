
# From Prompt to Action: Understanding LLMs, Tools, and Agents

## Scenario

For this task, I selected a **college library fine system** as my scenario. The library rules are stored in a local file named `library_notice.txt`.

The notice contains the following information:

- 1 to 5 days late: Rs. 2 per day
- 6 to 10 days late: Rs. 5 per day
- Above 10 days late: Rs. 10 per day

The goal is to compare how a plain Large Language Model (LLM) responds to questions about library fines versus how an LLM behaves when given access to a tool that can read the library notice file.

---

# 3.1 Explanation of Concepts

## What is a Large Language Model?

A Large Language Model (LLM) is an AI system trained on a large collection of text. It learns patterns, language structure, facts, and relationships between words from its training data.

An LLM can answer many questions correctly when the information is already part of its training knowledge. For example, if a user asks:

> What is machine learning?

the model can provide a correct explanation because machine learning is common knowledge that likely appeared in its training data.

However, an LLM cannot reliably answer questions that depend on information outside its training data. In my scenario, the library fine rules are stored in a local file that the model has never seen before. Therefore, when asked:

> I returned a library book 8 days late. How much fine should I pay?

the model does not know the library's policy and cannot determine the answer from memory alone.

In the actual experiment, the plain LLM responded by asking for additional information about the library rules instead of providing a definite answer.

This demonstrates that an LLM is powerful at language generation and reasoning but has no built-in access to external files or current information.

---

## What is an Agent?

An agent is a system that combines a language model with external tools and the ability to decide when those tools should be used.

A normal chat response is produced entirely from the model's internal knowledge. An agent can examine a question, determine whether additional information is required, use a tool to obtain that information, and then generate a final answer.

In my scenario, the plain LLM could not answer the library fine question because it had no access to the notice file.

The agent version behaved differently. It recognized that the answer depended on information stored in the library notice, called a tool to read the file, and then used the returned information to generate an answer.

Therefore, an agent extends the capabilities of a language model beyond its own memory.

---

## What is a Tool and What is a Tool Call?

A tool is an external function that performs a specific task for the language model.

Examples include:

- Reading files
- Performing calculations
- Accessing databases
- Searching websites
- Calling APIs

A tool call occurs when the model decides that it needs information or functionality from a tool before answering a question.

In this project, the tool is:

```python
read_library_notice()
```

Its purpose is to read the contents of the `library_notice.txt` file.

The tool is described to the model using a schema that includes:

- Tool name
- Tool description
- Parameters

The schema helps the model understand:

- What the tool does
- When it should be used
- What input it requires

Without this description, the model would not know that the tool exists.

---

## Tool Call Flow

The complete tool-call process in my project is shown below.

### Step 1

The user asks:

> I returned a library book 8 days late. How much fine should I pay?

### Step 2

The model examines the question.

### Step 3

The model determines that the answer depends on library rules that are not available in its own knowledge.

### Step 4

The model calls the tool:

```python
read_library_notice()
```

### Step 5

The tool reads the contents of `library_notice.txt`.

### Step 6

The tool returns the notice text to the model.

### Step 7

The model reads the returned information and identifies the relevant fine rule.

### Step 8

The model generates the final answer for the user.

This process allows the model to use external information instead of relying only on its training data.

---

## Why Should a Tool Return Plain Text Even When It Fails?

A tool should return a readable text message even when an error occurs.

For example, if the notice file does not exist, the tool can return:

> Read Error: File not found.

The language model can understand this message and explain the problem to the user.

If the tool instead crashes the program, the conversation stops completely and the user receives no useful guidance.

Returning plain text improves reliability and allows the model to continue interacting with the user even when problems occur.

---

# 3.2 Comparison Table

| Basis for Comparison | Plain LLM Prompt (No Tool) | LLM With One Tool |
|---------------------|----------------------------|-------------------|
| Source of answer | Internal training knowledge | Internal knowledge + tool output |
| Can fetch information outside memory? | No | Yes |
| Reliability on factual or file-based questions | Limited | Higher |
| Transparency | User only sees the answer | User can observe the tool call and final answer |
| Speed / Cost | Faster and cheaper | Slightly slower because tool execution is required |

---

# 3.3 Minimal Implementation

The implementation contains three components.

### Tool

The tool `read_library_notice()` reads the contents of a local text file containing the library fine rules.

### Plain LLM Script

The script `without_tool.py` asks the language model a question directly without giving it access to any tools.

### Tool-Enabled Script

The script `with_tool.py` provides the file-reading tool to the language model and allows the model to call the tool whenever necessary.

This implementation demonstrates the difference between answering from memory and answering using external information.

---

# 3.4 Observation

## Question 1

### User Question

> What is machine learning?

### Plain LLM Result

The model answered correctly using its existing knowledge.

### Tool-Enabled Result

The model also answered correctly and did not call the tool.

### Observation

The tool was not needed because the answer was general knowledge.

---

## Question 2

### User Question

> I returned a library book 8 days late. How much fine should I pay?

### Plain LLM Result

The model responded:

> I need more information about the library and its fine policy.

The model could not provide a definite answer because it did not know the library rules.

### Tool-Enabled Result

The model called the tool:

```python
read_library_notice()
```

The tool returned the library fine rules.

The model then calculated and responded:

> Total fine: Rs. 25

### Observation

The tool allowed the model to access information that was unavailable in its training data. Without the tool, the model could not answer the question.

---

## Question 3

### User Question

> What is the fine rate for books returned more than 10 days late?

### Plain LLM Result

The model could not know the library policy and would require additional information.

### Tool-Enabled Result

The model called the tool and identified the rule:

> Above 10 days: Rs. 10 per day

### Observation

The tool improved factual accuracy by providing direct access to the source document.

---

# 3.5 Suitability and Conclusion

In this scenario, the plain LLM was sufficient for answering general knowledge questions such as explaining machine learning. These questions could be answered directly from information already present in the model's training data.

However, the plain LLM was unable to answer questions that depended on the specific library rules stored in a local file. When asked about the fine for returning a book late, the model required additional information because it had no access to the library notice.

The tool-enabled version successfully read the library notice and used that information to generate a specific answer. This demonstrated how tools allow language models to obtain information that is not part of their internal knowledge.

More generally, a plain LLM prompt is sufficient when the task involves explanation, summarization, brainstorming, writing, or common knowledge. Tools become necessary when the task requires access to files, databases, websites, calculations, or any external information source.

Therefore, tools extend the capabilities of language models and make AI systems more reliable for real-world tasks.
# Library Fine Agent – LLM vs Tool Calling

## Project Overview

This project demonstrates the difference between a plain Large Language Model (LLM) and an LLM that has access to an external tool.

The chosen scenario is a college library fine system. The library rules are stored in a local text file. A user asks questions about library fines. Some questions require access to the file, while others can be answered directly from the model's knowledge.

The project contains:

- A plain LLM script without tool access
- A tool-enabled LLM script
- A simple file-reading tool
- Output screenshots
- A written analysis

## Files

### library_notice.txt
Contains the library fine rules.

### my_tool.py
Implements a tool that reads the library notice file.

### without_tool.py
Sends questions directly to the LLM without any tool access.

### with_tool.py
Provides the file-reading tool to the LLM and allows it to call the tool when needed.

### analysis.md
Contains the conceptual explanation, comparison table, observations, and conclusions.

### Output/
Contains screenshots of program outputs.

## Scenario

Example question:

> I returned a library book 8 days late. How much fine should I pay?

A plain LLM does not know the specific library rules and may guess.

A tool-enabled LLM can read the notice file, identify the correct rule, and provide a reliable answer.

## Learning Outcomes

Through this project, I learned:

- What a Large Language Model is
- What an AI agent is
- What tools and tool calls are
- How tool schemas help a model decide when to use a tool
- How external tools improve reliability for factual questions
- The difference between prompting and tool-assisted reasoning
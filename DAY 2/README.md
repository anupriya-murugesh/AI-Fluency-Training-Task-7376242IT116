# AI Fluency Training – Day 2 Task
**Topic:** Reasoning and Acting (Direct Prompting vs. CoT vs. ReAct)  
**ID:** AI-Fluency-Training-7376242IT116  

---

## 1. Project Overview

This repository contains the code and analytical report for the Day 2 Task of the AI Fluency Training course. It explores how large language models handle logic, mathematics, and private data retrieval using three distinct AI methodologies:
1. **Direct Prompting** (Zero-Shot)
2. **Chain-of-Thought** (CoT)
3. **ReAct Agent** (Reason + Act)

### The Custom Scenario
The scenario developed for this task is an **Event Management System**. The AI must navigate private venue booking prices and solve complex event logistics (e.g., seating arrangements, catering splits, and rental inventory logic). 

**Private Venue Data:**
*   `GRAND_HALL`: Rs. 50,000
*   `ROOFTOP`: Rs. 40,000
*   `GARDEN_TENT`: Rs. 30,000

---

## 2. Project Structure

```text
Day_2_Task/
│
├── config.py             # Private venue data (VENUE_PRICES) and API config
├── tools.py              # Tool schemas (get_venue_price, calculator)
├── agent.py              # The ReAct loop implementation
├── react_trace.py        # Script to execute the ReAct agent
├── cot_compare.py        # Script comparing Direct Prompting vs CoT
├── self_consistency.py   # Script testing CoT temperature voting
├── analysis.md           # The graded evaluation report
├── requirements.txt      # Project dependencies
├── README.md             # This documentation
│
└── screenshots/          # Terminal execution evidence
    ├── react_trace.png
    ├── cot_compare.png
    └── self_consistency.png
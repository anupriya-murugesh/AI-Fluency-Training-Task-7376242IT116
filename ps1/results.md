# Day 8 – In-Class Task: Extended College Helpdesk Agent Results

## Summary Table

| # | Tools called (in order) | Agent's answer (short) | Correct? (Y/N) | If N, why? |
|---|-------------------------|------------------------|----------------|------------|
| 1 | `search_handbook` | CGPA of 6.5 or higher and no standing arrears (`placement_policy.md`) | Y | - |
| 2 | `check_exam_eligibility` | Eligible with condonation: pay Rs. 500 per course with medical/official certificate | Y | - |
| 3 | `search_handbook`, `get_course_fee`, `get_course_fee`, `calculator` | Rs. 32,000 (CS101: 12,000 + AI202: 18,000 + maximum late fee: 2,000) | Y | - |
| 4 | `calculator` | Rs. 30,500 (Uses memory of Q3: 12,000 + 18,000 + 5 days late fee 500) | Y | - |
| 5 | `search_handbook` | "I don't know" (`search_handbook` returned `NO_MATCH`) | Y | - |

**Model used:** `openai/gpt-oss-120b` (via Groq)  
**Embedding model:** `BAAI/bge-small-en-v1.5` (`fastembed`, 384 dimensions)  
**MAX_DISTANCE:** `0.40`  
**Scores - placements question:** `0.1768` (Source: `placement_policy.md`)  
**Scores - France question:** `0.5731` (Best distance: `0.5731`, all matches > 0.40 -> `NO_MATCH`)

---

## Part A – New Document Evidence

### 1. File Created: `data/placement_policy.md`
Contains placement eligibility (CGPA >= 6.5, no standing arrears, registration before 31 July), pre-placement training attendance (90%), and one student one job policy.

### 2. Output of `python 1_ingest.py`:
```text
Loaded 6 documents
Split into 27 chunks (chunk_size=300, overlap=50)
Example chunk -> '## Contact\nQueries about the training can be sent to the Training & Placement Cell office, Room 104, Main Block.' {'source': 'ai_fluency_training.md'}
Stored 27 vectors in ./chroma_db using EMBED_PROVIDER=fastembed
Vector length: 384
```
*Confirmation:* Document count increased to 6, split into 27 chunks.

### 3. Output of `python 2_search.py`:
```text
Q: How much is the late fee for paying fees after the due date?
  0.197  [fee_policy.md]  "## Late fee\nA late fee of Rs. 100 per day is charged after the due date.\nThe maximum late fee is Rs. 2,000 per semester. After 30 days of non-payment the student's ERP login is blocked until the dues are cleared."
  0.299  [fee_policy.md]  '## Tuition fee\nThe annual tuition fee must be paid before 15 July for the odd semester and before 15 December for the even semester.\nFees can be paid through the college ERP portal (UPI, net banking or debit card) or by demand draft at the accounts office.'
  0.333  [exam_regulations.md]  '## Revaluation\nRevaluation can be applied for within 5 working days of the result announcement. The revaluation fee is Rs. 300 per paper.'

Q: What time should hostel students return?
  0.130  [hostel_rules.md]  '## In-time\nAll hostel residents must return to the hostel by 9.00 PM. Students attending approved evening programmes (for example the AI Fluency Training, 5.00 PM to 7.00 PM) must still be inside the hostel by 9.00 PM.\nLate entry requires a written permission slip signed by the warden.'
  0.295  [hostel_rules.md]  '## Leave\nTo go home, a student must submit a leave form to the warden at least one day in advance. Parents are informed by SMS when the leave is approved.'
  0.300  [hostel_rules.md]  '# Hostel Rules (Greenfield College of Engineering - sample document)'

Q: Can I write the exam with 70% attendance?
  0.247  [exam_regulations.md]  '## Attendance requirement\nA student needs a minimum of 75% attendance in each course to write the end-semester examination.\nStudents with attendance between 65% and 74% may apply for condonation by paying a condonation fee of Rs. 500 per course along with a medical or official certificate.'
  0.332  [exam_regulations.md]  'Students below 65% attendance are not permitted to write the examination and must redo the course.'
  0.336  [placement_policy.md]  '## Pre-placement training\nA minimum of 90% attendance in pre-placement training is required to sit for company\ndrives.'

Q: What CGPA do I need to be eligible for placements?
  0.177  [placement_policy.md]  '# Placement Policy (Greenfield College of Engineering - sample document)\n\n## Eligibility\nStudents with a CGPA of 6.5 or above and no standing arrears are eligible for campus\nplacements.\nStudents must register on the placement portal before 31 July of their final year.'
  0.236  [fee_policy.md]  '## Scholarships\nStudents with a CGPA of 9.0 or above in the previous year receive a 25% tuition fee waiver for the next year.'
  0.318  [placement_policy.md]  '## Pre-placement training\nA minimum of 90% attendance in pre-placement training is required to sit for company\ndrives.'

Filtered to library.md:
   library.md -> ## Fines A fine of Rs. 2 per day per book is charged for late return. Lost books must be replaced or paid for at twice the current price.
   library.md -> # Library Rules (Greenfield College of Engineering - sample document)  ## Borrowing UG students can borrow up to 4 books at a time for 14 days. Books can be renewed once if no other student has reserved them.
```
*Confirmation:* For question "What CGPA do I need to be eligible for placements?", the top retrieved chunk is from `placement_policy.md` with distance `0.177`.

---

## Part B – New Tool Evidence (`check_exam_eligibility`)

Direct testing before invoking the agent with test values 82, 70, 50, and 120:
```text
check_exam_eligibility(82) -> ELIGIBLE: With 82.0% attendance, the student may write the end-semester examination.
check_exam_eligibility(70) -> CONDONATION: With 70.0% attendance, the student may write the exam with condonation by paying Rs. 500 per course along with a medical or official certificate.
check_exam_eligibility(50) -> NOT ELIGIBLE: With 50.0% attendance (below 65%), the student is not permitted to write the examination and must redo the course.
check_exam_eligibility(120) -> Error: Attendance percentage 120.0 is invalid. It must be between 0 and 100.
```
*Confirmation:*
- `82` returns `ELIGIBLE`
- `70` returns `CONDONATION` with Rs. 500 fee requirement
- `50` returns `NOT ELIGIBLE`
- `120` returns error message without raising an exception

---

## Part C – Relevance Guard Evidence

### Cosine Distance Measurements:
- **Good question:** *"What CGPA do I need to be eligible for placements?"*
  - Top 3 distances: `0.1768` (`placement_policy.md`), `0.2364` (`fee_policy.md`), `0.3182` (`placement_policy.md`).
- **Bad question:** *"What is the capital of France?"*
  - Top 3 distances: `0.5731` (`hostel_rules.md`), `0.5732` (`hostel_rules.md`), `0.5772` (`library.md`).

### Threshold Selection:
- Selected `MAX_DISTANCE = 0.40`.
- All relevant chunks for placement queries fall below 0.35 (`<= 0.40`).
- All retrieved chunks for out-of-domain queries like France are `>= 0.5731` (`> 0.40`).
- When no chunk passes the threshold, `search_handbook` returns:
  `NO_MATCH: this is not covered in the college handbook`
- SYSTEM prompt instructs the model to state "I don't know" when `NO_MATCH` is returned.

---

## Part D – Test Execution Output (`run_log.txt`)

Here is the full terminal transcript from running `python task_agent.py`:

```text
=== Mermaid Diagram ===
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc


=== Direct Tool Tests (Part B) ===
check_exam_eligibility(82) -> ELIGIBLE: With 82.0% attendance, the student may write the end-semester examination.
check_exam_eligibility(70) -> CONDONATION: With 70.0% attendance, the student may write the exam with condonation by paying Rs. 500 per course along with a medical or official certificate.
check_exam_eligibility(50) -> NOT ELIGIBLE: With 50.0% attendance (below 65%), the student is not permitted to write the examination and must redo the course.
check_exam_eligibility(120) -> Error: Attendance percentage 120.0 is invalid. It must be between 0 and 100.

=== Five Test Questions on thread 'task-run' (Part D) ===

[task-run] USER: What CGPA do I need to be eligible for placements?
   agent  -> call search_handbook({'query': 'CGPA eligibility for placements'})
   tools  -> search_handbook returned '[placement_policy.md] # Placement Policy (Greenfield Co'...
   agent  -> ANSWER: You need a CGPA of **6.5 or higher** (and no standing arrears) to be eligible for campus placements.  
*Source: placement_policy.md*

[task-run] USER: My attendance is 70%. Can I write the exam?
   agent  -> call check_exam_eligibility({'attendance_percent': 70})
   tools  -> check_exam_eligibility returned 'CONDONATION: With 70.0% attendance, the student may wri'...
   agent  -> ANSWER: Yes. With 70 % attendance you can write the exam, but you’ll need to obtain condonation—pay the Rs 500 per-course fee and provide a medical or official certificate.

[task-run] USER: What is the total of the CS101 fee, the AI202 fee and the maximum late fee?
   agent  -> call search_handbook({'query': 'late fee maximum'})
   tools  -> search_handbook returned '[fee_policy.md] ## Late fee\nA late fee of Rs. 100 per d'...
   agent  -> call get_course_fee({'course_code': 'CS101'})
   tools  -> get_course_fee returned 'CS101 fee is Rs. 12000'...
   agent  -> call get_course_fee({'course_code': 'AI202'})
   tools  -> get_course_fee returned 'AI202 fee is Rs. 18000'...
   agent  -> call calculator({'expression': '12000 + 18000 + 2000'})
   tools  -> calculator returned '32000'...
   agent  -> ANSWER: The total is **Rs 32,000** (CS101 = 12,000 + AI202 = 18,000 + maximum late fee = 2,000).

[task-run] USER: And if I pay only 5 days late instead?
   agent  -> call calculator({'expression': '12000 + 18000 + 500'})
   tools  -> calculator returned '30500'...
   agent  -> ANSWER: If you’re only 5 days late, the late fee would be 5 × Rs 100 = Rs 500.  
So the total becomes **Rs 30,500** (12,000 + 18,000 + 500).

[task-run] USER: What is the capital of France?
   agent  -> call search_handbook({'query': 'capital of France'})
   tools  -> search_handbook returned 'NO_MATCH: this is not covered in the college handbook'...
   agent  -> ANSWER: I’m sorry, but I don’t have that information.

=== Stretch Goal: Thread 'task-run-2' asking only Question 4 ===

[task-run-2] USER: And if I pay only 5 days late instead?
   agent  -> call search_handbook({'query': 'late payment 5 days penalty'})
   tools  -> search_handbook returned '[fee_policy.md] ## Late fee\nA late fee of Rs. 100 per d'...
   agent  -> ANSWER: If you pay 5 days after the due date, the late-fee will be 5 × Rs 100 = Rs 500 (subject to the overall Rs 2,000 maximum).  
*Source: fee_policy.md*

=== State Verification ===
Thread task-run has 26 messages saved in memory
Thread task-run-2 has 4 messages saved in memory
```

---

## Stretch Goals Explanation

1. **Why does Thread `task-run-2` produce a different answer for Question 4?**
   - In thread `task-run`, Question 4 ("*And if I pay only 5 days late instead?*") directly followed Question 3. Because the `InMemorySaver` checkpointer preserves conversational state across turns within the same thread ID, the model remembered that the student was asking about the total fee for CS101 (Rs. 12,000) and AI202 (Rs. 18,000), replaced the maximum late fee (Rs. 2,000) with 5 days × Rs. 100 = Rs. 500, and computed the new total: **Rs. 30,500**.
   - In thread `task-run-2`, Question 4 was asked as an isolated, standalone query with zero prior context. Without memory of the specific course codes or fees, the model searched `fee_policy.md` for late fees, calculated only the 5-day fee (**Rs. 500**), and answered that late fees are Rs. 100/day totaling Rs. 500 without adding any course fees.
   - This empirically proves that thread-isolated memory functions as designed in LangGraph.

2. **Mermaid Diagram:**
   ```mermaid
   graph TD;
   	__start__([start]) --> agent;
   	agent -.-> __end__([end]);
   	agent -.-> tools;
   	tools --> agent;
   ```

3. **`library_fine` tool:**
   - Implemented as `@tool def library_fine(days_late: int, books: int = 1) -> str:` calculating `days_late * books * 2`.

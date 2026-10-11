import ast
import operator
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore

COURSE_FEES = {"CS101": 12000, "AI202": 18000, "DS303": 15000}   # same data as Day 1
store = get_vectorstore()

# Part C: MAX_DISTANCE relevance guard threshold
# Measured on fastembed (bge-small-en-v1.5):
# Placements question lowest distance: ~0.1768
# France question lowest distance: ~0.5731
# 0.40 cleanly separates relevant handbook questions from out-of-domain queries.
MAX_DISTANCE = 0.40


@tool
def search_handbook(query: str) -> str:
    """Search the college handbook and return relevant passages."""
    docs_with_scores = store.similarity_search_with_score(query, k=3)
    relevant_docs = [doc for doc, score in docs_with_scores if score <= MAX_DISTANCE]

    if not relevant_docs:
        return "NO_MATCH: this is not covered in the college handbook"

    return "\n\n".join(
        f"[{doc.metadata['source']}] {doc.page_content}"
        for doc in relevant_docs
    )


@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee in rupees for a course code such as CS101, AI202 or DS303."""
    fee = COURSE_FEES.get(course_code.strip().upper())
    return f"{course_code.upper()} fee is Rs. {fee}" if fee else f"Unknown course code {course_code}"


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


@tool
def calculator(expression: str) -> str:
    """Evaluate simple arithmetic such as '18000 + 15000' or '100 * 12'."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("only + - * / on numbers")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except Exception as e:                       # tell the model, don't crash the graph
        return f"Error: {e}"


# Part B: New tool check_exam_eligibility
@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the
    end-semester exam."""
    # TODO 1: if the value is outside 0-100, return an error message (do not raise)
    if attendance_percent < 0 or attendance_percent > 100:
        return f"Error: Attendance percentage {attendance_percent} is invalid. It must be between 0 and 100."

    # TODO 2: 75 or above -> "ELIGIBLE: ..."
    if attendance_percent >= 75:
        return f"ELIGIBLE: With {attendance_percent}% attendance, the student may write the end-semester examination."

    # TODO 3: 65 to below 75 -> "CONDONATION: ... Rs. 500 per course"
    if attendance_percent >= 65:
        return (
            f"CONDONATION: With {attendance_percent}% attendance, the student may write the exam "
            f"with condonation by paying Rs. 500 per course along with a medical or official certificate."
        )

    # TODO 4: below 65 -> "NOT ELIGIBLE: ..."
    return (
        f"NOT ELIGIBLE: With {attendance_percent}% attendance (below 65%), "
        f"the student is not permitted to write the examination and must redo the course."
    )


# Stretch Goal tool: library_fine
@tool
def library_fine(days_late: int, books: int = 1) -> str:
    """Calculate the library fine for late return of books at Rs. 2 per day per book."""
    fine = days_late * books * 2
    return f"Library fine for {books} book(s) returned {days_late} day(s) late is Rs. {fine} (Rs. 2 per day per book)."


tools = [search_handbook, get_course_fee, calculator, check_exam_eligibility]
model = get_model().bind_tools(tools)

SYSTEM = (
    "You are the Greenfield College helpdesk. "
    "Use search_handbook for any handbook rule, college policy, or questions to verify if they are covered in the handbook (such as 'What is the capital of France?'). "
    "If search_handbook returns NO_MATCH, say you don't know. "
    "Use check_exam_eligibility to check exam eligibility when an attendance percentage is given. "
    "Use get_course_fee for course fees and calculator for arithmetic. "
    "Answer briefly and name the source file when available. "
    "If the tools do not provide the answer, say you don't know."
)


def agent(state: MessagesState):
    """The LLM node: read the conversation, either answer or ask for a tool."""
    reply = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))          # runs every tool call in the last message
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # tool calls? -> "tools", else -> END
builder.add_edge("tools", "agent")                  # the LOOP back to the LLM
graph = builder.compile(checkpointer=InMemorySaver())  # checkpointer = memory per thread


def ask(question, thread_id):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 10}
    print(f"\n[{thread_id}] USER: {question}")
    for step in graph.stream({"messages": [("user", question)]}, config, stream_mode="updates"):
        for node, update in step.items():
            for msg in update["messages"]:
                if getattr(msg, "tool_calls", None):
                    for c in msg.tool_calls:
                        print(f"   {node:6} -> call {c['name']}({c['args']})")
                elif node == "tools":
                    print(f"   {node:6} -> {msg.name} returned {msg.content[:55]!r}...")
                else:
                    print(f"   {node:6} -> ANSWER: {msg.content}")


if __name__ == "__main__":
    print("=== Mermaid Diagram ===")
    print(graph.get_graph().draw_mermaid())

    print("\n=== Direct Tool Tests (Part B) ===")
    for val in [82, 70, 50, 120]:
        print(f"check_exam_eligibility({val}) -> {check_exam_eligibility.invoke({'attendance_percent': val})}")

    print("\n=== Five Test Questions on thread 'task-run' (Part D) ===")
    thread_id = "task-run"

    # Question 1
    ask("What CGPA do I need to be eligible for placements?", thread_id)

    # Question 2
    ask("My attendance is 70%. Can I write the exam?", thread_id)

    # Question 3
    ask("What is the total of the CS101 fee, the AI202 fee and the maximum late fee?", thread_id)

    # Question 4
    ask("And if I pay only 5 days late instead?", thread_id)

    # Question 5
    ask("What is the capital of France?", thread_id)

    print("\n=== Stretch Goal: Thread 'task-run-2' asking only Question 4 ===")
    ask("And if I pay only 5 days late instead?", "task-run-2")

    print("\n=== State Verification ===")
    for t in ("task-run", "task-run-2"):
        saved = graph.get_state({"configurable": {"thread_id": t}}).values["messages"]
        print(f"Thread {t} has {len(saved)} messages saved in memory")

from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.router import decide_route
from agent.judge import judge_answer
from agent.reporter import build_report

from mcp_client import call_mcp_tool


MAX_RETRIES = 1


def log(message: str):

    print(message)


# --------------------------------------------------
# ROUTER
# --------------------------------------------------

def router_node(state: AgentState):

    question = state["question"]

    decision = decide_route(question)

    log("\n[ROUTER]")
    log(f"Question : {question}")
    log(f"Route    : {decision.route}")
    log(f"Reason   : {decision.reason}")

    return {
        "route": decision.route,
        "route_reason": decision.reason,
    }


def route_next(state: AgentState):

    return state["route"]


# --------------------------------------------------
# RAG TOOL
# --------------------------------------------------

def rag_tool_node(state: AgentState):

    log("\n[RAG MCP]")
    log("Calling ask_documents...")

    answer = call_mcp_tool(
        "ask_documents",
        state["question"]
    )

    log(f"RAG Response: {answer}")

    return {
        "rag_answer": answer
    }


# --------------------------------------------------
# SQL TOOL
# --------------------------------------------------

def sql_tool_node(state: AgentState):

    log("\n[SQL MCP]")
    log("Calling generate_sql...")

    answer = call_mcp_tool(
        "generate_sql",
        state["question"]
    )

    log(f"SQL Response: {answer}")

    return {
        "sql_answer": answer
    }


# --------------------------------------------------
# BOTH TOOLS
# --------------------------------------------------

def both_tool_node(state: AgentState):

    log("\n[BOTH MCP TOOLS]")

    rag_answer = call_mcp_tool(
        "ask_documents",
        state["question"]
    )

    sql_answer = call_mcp_tool(
        "generate_sql",
        state["question"]
    )

    log(f"RAG Response: {rag_answer}")
    log(f"SQL Response: {sql_answer}")

    return {
        "rag_answer": rag_answer,
        "sql_answer": sql_answer,
    }


# --------------------------------------------------
# REVIEW NODE
# --------------------------------------------------

def review_node(state: AgentState):

    log("\n[REVIEW AGENT]")

    parts = []

    if state.get("rag_answer"):
        parts.append(
            f"RAG RESPONSE:\n{state['rag_answer']}"
        )

    if state.get("sql_answer"):
        parts.append(
            f"SQL RESPONSE:\n{state['sql_answer']}"
        )

    merged_answer = "\n\n".join(parts)

    decision = judge_answer(
        state["question"],
        merged_answer
    )

    attempts = state.get("attempts", 0)

    log(f"Satisfactory : {decision.satisfactory}")
    log(f"Next Action  : {decision.next_action}")
    log(f"Reason       : {decision.reason}")
    log(f"Attempt      : {attempts}")

    return {
        "merged_answer": merged_answer,
        "satisfactory": decision.satisfactory,
        "judge_reason": decision.reason,
        "next_action": decision.next_action,
        "attempts": attempts + 1,
    }


# --------------------------------------------------
# REVIEW DECISION
# --------------------------------------------------

def review_next(state: AgentState):

    if state["satisfactory"]:

        return "report"

    attempts = state.get("attempts", 0)

    if attempts >= MAX_RETRIES:

        return "clarify"

    next_action = state["next_action"]

    return next_action


# --------------------------------------------------
# REPORT
# --------------------------------------------------

def report_node(state: AgentState):

    log("\n[REPORT]")

    report = build_report(
        question=state["question"],
        route=state["route"],
        rag_answer=state.get("rag_answer"),
        sql_answer=state.get("sql_answer"),
        merged_answer=state["merged_answer"],
    )

    return {
        "report": report,
        "final_answer": report,
    }


# --------------------------------------------------
# CLARIFY
# --------------------------------------------------

def clarify_node(state: AgentState):

    message = """
I could not generate a sufficiently reliable answer
from the available information.

Please provide additional details such as:

- Metric
- Date range
- Location
- Project
- Employee
- Or relevant business context
"""

    return {
        "final_answer": message
    }


# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------

def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)

    builder.add_node(
        "rag_tool",
        rag_tool_node
    )

    builder.add_node(
        "sql_tool",
        sql_tool_node
    )

    builder.add_node(
        "both_tool",
        both_tool_node
    )

    builder.add_node(
        "review",
        review_node
    )

    builder.add_node(
        "report",
        report_node
    )

    builder.add_node(
        "clarify",
        clarify_node
    )

    # START
    builder.add_edge(
        START,
        "router"
    )

    # ROUTER → TOOL
    builder.add_conditional_edges(
        "router",
        route_next,
        {
            "rag": "rag_tool",
            "sql": "sql_tool",
            "both": "both_tool",
        }
    )

    # TOOL → REVIEW
    builder.add_edge(
        "rag_tool",
        "review"
    )

    builder.add_edge(
        "sql_tool",
        "review"
    )

    builder.add_edge(
        "both_tool",
        "review"
    )

    # REVIEW → REPORT / RETRY
    builder.add_conditional_edges(
        "review",
        review_next,
        {
            "report": "report",
            "rag": "rag_tool",
            "sql": "sql_tool",
            "both": "both_tool",
            "clarify": "clarify",
        }
    )

    # END
    builder.add_edge(
        "report",
        END
    )

    builder.add_edge(
        "clarify",
        END
    )

    return builder.compile()
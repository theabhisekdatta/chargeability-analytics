from typing import TypedDict, Literal


class AgentState(TypedDict, total=False):
    question: str
    route: Literal["rag", "sql", "both"]
    route_reason: str

    rag_answer: str
    sql_answer: str
    merged_answer: str

    satisfactory: bool
    judge_reason: str

    attempts: int

    report: str
    final_answer: str
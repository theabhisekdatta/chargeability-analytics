from typing import Literal

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from agent.config import GROQ_API_KEY, LLM_MODEL


class RouteDecision(BaseModel):

    route: Literal["rag", "sql", "both"] = Field(
        description=(
            "Choose the MCP tool required for answering the user's question. "
            "Use 'rag' for document/contextual questions, "
            "'sql' for numerical/data questions, "
            "and 'both' when both document knowledge and numerical data are required."
        )
    )

    reason: str = Field(
        description="Explain briefly why this route was selected."
    )


llm = ChatGroq(
    model=LLM_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the routing agent for a Chargeability Analytics system.

Your job is to understand the user's question semantically
and decide which MCP tool or tools should be called.

Available MCP tools:

1. RAG MCP tool
   - Used for information contained in documents.
   - Definitions
   - Explanations
   - Policies
   - Concepts
   - Descriptions
   - Business context
   - Document-based reasoning

2. SQL MCP tool
   - Used for structured data stored in PostgreSQL.
   - Counts
   - Averages
   - Totals
   - Percentages
   - Trends
   - Comparisons
   - Rankings
   - Numerical analysis
   - Time-based analysis

3. BOTH
   - Use both tools when the question requires:
       a) information from documents AND
       b) numerical/database information.

Important:
Do NOT use simple keyword matching.
Understand the actual intent and meaning of the question.

Examples:

Question:
"What is Generating Labor Cost?"
Route:
rag

Question:
"Which location has the highest average chargeability?"
Route:
sql

Question:
"Why is Chennai's chargeability lower than other locations?"
Route:
both

Return only the structured routing decision.
""",
        ),
        ("human", "{question}"),
    ]
)


router_chain = prompt | llm.with_structured_output(RouteDecision)


def decide_route(question: str) -> RouteDecision:

    decision = router_chain.invoke(
        {
            "question": question
        }
    )

    return decision
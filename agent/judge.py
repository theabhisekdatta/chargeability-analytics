from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from agent.config import GROQ_API_KEY, LLM_MODEL


class JudgeDecision(BaseModel):

    satisfactory: bool = Field(
        description="Whether the answer sufficiently answers the user's question."
    )

    next_action: str = Field(
        description=(
            "If satisfactory is false, choose the next action: "
            "rag, sql, or both. "
            "If satisfactory is true, use report."
        )
    )

    reason: str = Field(
        description="Brief explanation of the decision."
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
You are the quality-review agent for a Chargeability Analytics system.

You receive:
1. The user's original question.
2. The response returned by one or more MCP tools.

Your job is to determine whether the answer is sufficient.

If the answer is sufficient:
    satisfactory = true
    next_action = "report"

If the answer is NOT sufficient:
    satisfactory = false

Then decide what should be called next:

- "rag" if additional document/contextual information is needed.
- "sql" if additional numerical/database information is needed.
- "both" if both are required.

Do not simply reject an answer because it is short.
Check whether it actually answers the user's question.

Return only the structured decision.
""",
        ),
        (
            "human",
            """
USER QUESTION:
{question}

TOOL RESPONSE:
{answer}
""",
        ),
    ]
)


judge_chain = prompt | llm.with_structured_output(JudgeDecision)


def judge_answer(
    question: str,
    answer: str
) -> JudgeDecision:

    return judge_chain.invoke(
        {
            "question": question,
            "answer": answer,
        }
    )
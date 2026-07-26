def build_report(question: str, route: str, rag_answer: str | None, sql_answer: str | None, merged_answer: str) -> str:
    rag_section = rag_answer.strip() if rag_answer else "Not used."
    sql_section = sql_answer.strip() if sql_answer else "Not used."

    return f"""
==================================================
              CHARGEBILITY ANALYTICS
==================================================

User Question
-------------
{question}

Selected Route
--------------
{route.upper()}

RAG Output
----------
{rag_section}

SQL Output
----------
{sql_section}

Final Synthesized Answer
------------------------
{merged_answer}

==================================================
""".strip()
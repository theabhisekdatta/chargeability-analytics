import os

from mcp.server.fastmcp import FastMCP

from rag.rag_tool import RAGTool
from nl2sql.sql_tool import SQLTOOL


mcp = FastMCP("Chargeability Analytics")


def get_rag_tool() -> RAGTool:
    if not hasattr(mcp, "_rag_tool") or mcp._rag_tool is None:
        mcp._rag_tool = RAGTool()
    return mcp._rag_tool


def get_sql_tool() -> SQLTOOL:
    if not hasattr(mcp, "_sql_tool") or mcp._sql_tool is None:
        mcp._sql_tool = SQLTOOL()
    return mcp._sql_tool


# Tool 1 for the RAG pipeline: Ask documents from the knowledge base
@mcp.tool()
def ask_documents(question: str) -> str:
    """
    The tool retrieve relevant information from the Chargeability Analytics knowledge base
    and generate an answer using a Retrieval-Augmented Generation (RAG) pipeline.

    Args:
        question (str):
            The user's question related to Chargeability Analytics documents.

    Returns:
        str:
            A concise answer generated from the retrieved documents.
    Notes:
        - Answers are generated only from the documents available in the
          Chargeability Analytics knowledge base.
    """
    try:
        result = get_rag_tool().ask(question)
        return result["answer"] if isinstance(result, dict) else str(result)
    except Exception as exc:
        return f"RAG Error: {exc}"


# Tool 2: Generate SQL queries from natural language questions
@mcp.tool()
def generate_sql(question: str) -> str:
    """
    The tool generates a PostgreSQL SQL query from a natural language question.

    Args:
        question (str):
            The user's natural language question related to the Chargeability
            Analytics database.

    Returns:
        str:
            A PostgreSQL SQL query generated from the user's question.

    Notes:
        - The tool does not execute the generated SQL query; it only generates it.
        - The generated SQL query adheres to PostgreSQL syntax and best practices.
    """
    try:
        sql_tool = get_sql_tool()
        sql_query = sql_tool.generate_sql(question)
        results = sql_tool.execute_sql(sql_query)

        answer = sql_tool.generate_description(
            question=question,
            sql_query=sql_query,
            results=results,
        )
        return answer
    except Exception as exc:
        return f"SQL Error: {exc}"


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
    )
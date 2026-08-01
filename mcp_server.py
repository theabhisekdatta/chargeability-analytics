from mcp.server.fastmcp import FastMCP
from rag.rag_tool import RAGTool
from nl2sql.sql_tool import SQLTOOL


mcp = FastMCP("Chargeability Analytics")

rag = RAGTool()
sql = SQLTOOL()

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
    result = rag.ask(question)
    return result["answer"]

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
    sql_query = sql.generate_sql(question)

    results = sql.execute_sql(sql_query)

    answer = sql.generate_description(
        question=question,
        sql_query=sql_query,
        results=results,
    )

    return answer

# if __name__ == "__main__":
#     rag = RAGTool()
#     response = ask_documents(
#         "What are Determining Expense Report Costs"
#     )
#     print(response)


# if __name__ == "__main__":
#     response = generate_sql("Which location has the lowest average chargeability?")
#     print(response)


if __name__ == "__main__":
    # Start MCP server using stdio transport
    mcp.run(
        transport= "streamable-http"
    )
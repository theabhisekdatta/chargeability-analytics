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
    Retrieve relevant information from the Chargeability Analytics knowledge base
    and generate an answer using a Retrieval-Augmented Generation (RAG) pipeline.

    The tool performs semantic search against the indexed documents stored in
    the vector database, retrieves the most relevant document chunks, and uses
    an LLM to generate a context-aware response.

    Args:
        question (str):
            The user's question related to Chargeability Analytics documents.
            Example:
            "What is the Generating Labor Cost?"

    Returns:
        str:
            A concise answer generated from the retrieved documents.
            If the required information is not available in the knowledge base,
            the tool will indicate that sufficient information was not found.

    Notes:
        - Answers are generated only from the documents available in the
          Chargeability Analytics knowledge base.
        - The tool does not use external knowledge sources.
    """
    result = rag.ask(question)
    return result["answer"]

# Tool 2: Generate SQL queries from natural language questions
@mcp.tool()
def generate_sql(question: str) -> str:
    """
    Generate a PostgreSQL SQL query from a natural language question.

    The tool uses an LLM to convert the user's question into a valid SQL query
    based on the schema of the Chargeability Analytics database.

    Args:
        question (str):
            The user's natural language question related to the Chargeability
            Analytics database.
            Example:
            "Which location has the highest average chargeability?"

    Returns:
        str:
            A PostgreSQL SQL query generated from the user's question.
            The query is guaranteed to be a SELECT statement and will only use
            tables and columns that exist in the database schema.

    Notes:
        - The tool does not execute the generated SQL query; it only generates it.
        - The generated SQL query adheres to PostgreSQL syntax and best practices.
    """
    sql_query = sql.generate_sql(question)
    results = sql.execute_sql(sql_query)
    return results

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
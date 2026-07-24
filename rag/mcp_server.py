from mcp.server.fastmcp import FastMCP
from rag_tool import RAGTool


mcp = FastMCP("Chargeability Analytics")

rag = RAGTool()


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

# if __name__ == "__main__":
#     rag = RAGTool()
#     response = rag.ask(
#         "What are "
#         "What are Determining Expense Report Costs"
#     )
#     print(response["answer"])


if __name__ == "__main__":
    # Start MCP server using stdio transport
    mcp.run(
        transport= "streamable-http"
    )
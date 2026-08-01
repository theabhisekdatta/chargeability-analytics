import pytest


@pytest.mark.integration
def test_rag_mcp(mcp):
    """
    Integration Test

    Pytest
        ↓
    MCP Client
        ↓
    MCP Server
        ↓
    RAG Tool
        ↓
    Qdrant
    """

    question = "What is the Chargeability?"

    answer = mcp(
        "ask_documents",
        question,
    )

    assert isinstance(answer, str)

    assert len(answer) > 20

    assert "error" not in answer.lower()

    # Optional domain validation
    assert "chargeability" in answer.lower()
    assert "transaction" in answer.lower()
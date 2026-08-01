import pytest


@pytest.mark.integration
def test_sql_mcp(mcp):
    """
    Integration Test

    Pytest
        ↓
    MCP Client
        ↓
    MCP Server
        ↓
    SQL Tool
        ↓
    PostgreSQL
    """

    question = "Which location has the highest average chargeability?"

    answer = mcp(
        "generate_sql",
        question,
    )

    assert isinstance(answer, str)

    assert len(answer) > 20

    assert "error" not in answer.lower()

    # Domain validation
    assert "Hyderabad" in answer

    assert "chargeability" in answer.lower()
import pytest


@pytest.mark.integration
def test_complete_sql_flow(graph):
    """
    End-to-End SQL Flow

    Router
        ↓
    SQL MCP
        ↓
    Review
        ↓
    Report
    """

    result = graph.invoke(
        {
            "question": "Which location has the highest average chargeability?",
            "attempts": 0,
        },
        config={"recursion_limit": 20},
    )

    assert result["route"] == "sql"

    assert result["final_answer"] != ""

    assert "Hyderabad" in result["final_answer"]


@pytest.mark.integration
def test_complete_rag_flow(graph):
    """
    End-to-End RAG Flow
    """

    result = graph.invoke(
        {
            "question": "What is the Chargeability?",
            "attempts": 0,
        },
        config={"recursion_limit": 20},
    )

    assert result["route"] == "rag"

    assert result["final_answer"] != ""

    assert "chargeability" in result["final_answer"].lower()
    assert "RAG" in result["final_answer"]


@pytest.mark.integration
def test_complete_both_flow(graph):
    """
    End-to-End BOTH Flow
    """

    result = graph.invoke(
        {
            "question": "Why is Hyderabad's chargeability lower than other locations?",
            "attempts": 0,
        },
        config={"recursion_limit": 20},
    )

    assert result["route"] == "both"

    assert result["final_answer"] != ""

    assert len(result["final_answer"]) > 50
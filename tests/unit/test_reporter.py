import pytest

from agent.reporter import build_report


@pytest.mark.unit
def test_report_contains_all_sections():

    report = build_report(
        question="Which location has the highest average chargeability?",
        route="sql",
        rag_answer=None,
        sql_answer="Hyderabad has the highest average chargeability at 60.40%.",
        merged_answer="Hyderabad has the highest average chargeability at approximately 60.40%."
    )

    assert "CHARGEBILITY ANALYTICS" in report
    assert "User Question" in report
    assert "Selected Route" in report
    assert "SQL Output" in report
    assert "Final Synthesized Answer" in report


@pytest.mark.unit
def test_report_route_is_uppercase():

    report = build_report(
        question="Test question",
        route="sql",
        rag_answer=None,
        sql_answer="SQL Answer",
        merged_answer="Final Answer"
    )

    assert "SQL" in report


@pytest.mark.unit
def test_report_handles_unused_rag():

    report = build_report(
        question="Test question",
        route="sql",
        rag_answer=None,
        sql_answer="SQL Answer",
        merged_answer="Final Answer"
    )

    assert "Not used." in report


@pytest.mark.unit
def test_report_handles_unused_sql():

    report = build_report(
        question="What is Generating Labor Cost?",
        route="rag",
        rag_answer="This is the RAG answer.",
        sql_answer=None,
        merged_answer="This is the final answer."
    )

    assert "Not used." in report


@pytest.mark.unit
def test_report_contains_final_answer():

    final_answer = (
        "Hyderabad has the highest average chargeability "
        "at approximately 60.40%."
    )

    report = build_report(
        question="Which location has the highest average chargeability?",
        route="sql",
        rag_answer=None,
        sql_answer=final_answer,
        merged_answer=final_answer
    )

    assert final_answer in report
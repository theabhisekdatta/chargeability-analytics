from agent.reporter import build_report


def test_report_contains_question():

    report = build_report(
        question="Which location has the highest average chargeability?",
        route="sql",
        rag_answer=None,
        sql_answer=(
            "Hyderabad has the highest average chargeability "
            "at approximately 60.40%."
        ),
        merged_answer=(
            "Hyderabad has the highest average chargeability "
            "at approximately 60.40%."
        ),
    )

    assert "highest average chargeability" in report.lower()


def test_report_contains_sql_answer():

    sql_answer = (
        "Hyderabad has the highest average chargeability "
        "at approximately 60.40%."
    )

    report = build_report(
        question="Which location has the highest average chargeability?",
        route="sql",
        rag_answer=None,
        sql_answer=sql_answer,
        merged_answer=sql_answer,
    )

    assert "Hyderabad" in report
    assert "60.40%" in report
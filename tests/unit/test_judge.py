import pytest
from unittest.mock import Mock, patch

from agent.judge import JudgeDecision, judge_answer


@pytest.mark.unit
def test_judge_accepts_good_answer():

    expected = JudgeDecision(
        satisfactory=True,
        next_action="report",
        reason="The answer completely satisfies the user's question."
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.judge.judge_chain", mock_chain):

        result = judge_answer(
            question="Which location has the highest average chargeability?",
            answer="Hyderabad has the highest average chargeability at approximately 60.40%."
        )

    assert result.satisfactory is True
    assert result.next_action == "report"


@pytest.mark.unit
def test_judge_requests_sql_retry():

    expected = JudgeDecision(
        satisfactory=False,
        next_action="sql",
        reason="The answer lacks sufficient numerical analysis."
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.judge.judge_chain", mock_chain):

        result = judge_answer(
            question="Which location has the highest average chargeability?",
            answer="I couldn't determine the location."
        )

    assert result.satisfactory is False
    assert result.next_action == "sql"


@pytest.mark.unit
def test_judge_requests_rag_retry():

    expected = JudgeDecision(
        satisfactory=False,
        next_action="rag",
        reason="More document-based information is required."
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.judge.judge_chain", mock_chain):

        result = judge_answer(
            question="What is Generating Labor Cost?",
            answer="No relevant information was found."
        )

    assert result.satisfactory is False
    assert result.next_action == "rag"


@pytest.mark.unit
def test_judge_requests_both():

    expected = JudgeDecision(
        satisfactory=False,
        next_action="both",
        reason="Both numerical data and document context are required."
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.judge.judge_chain", mock_chain):

        result = judge_answer(
            question="Why is Hyderabad's chargeability lower than other locations?",
            answer="The available information is incomplete."
        )

    assert result.satisfactory is False
    assert result.next_action == "both"
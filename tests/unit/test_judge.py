from unittest.mock import Mock, patch

from agent.judge import JudgeDecision, judge_answer


def test_judge_accepts_good_answer():

    expected = JudgeDecision(
        satisfactory=True,
        next_action="report",
        reason="Good answer"
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.judge.judge_chain", mock_chain):

        result = judge_answer(
            "Which location has highest chargeability?",
            "Hyderabad has the highest chargeability."
        )

    assert result.satisfactory
    assert result.next_action == "report"
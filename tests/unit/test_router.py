from unittest.mock import Mock, patch

from agent.router import RouteDecision, decide_route


def test_router_selects_rag():

    expected = RouteDecision(
        route="rag",
        reason="Document question"
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.router.router_chain", mock_chain):

        result = decide_route(
            "What is Generating Labor Cost?"
        )

    assert result.route == "rag"


def test_router_selects_sql():

    expected = RouteDecision(
        route="sql",
        reason="Numerical analysis"
    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.router.router_chain", mock_chain):

        result = decide_route(
            "Which location has the highest average chargeability?"
        )

    assert result.route == "sql"


def test_router_selects_both():

    expected = RouteDecision(
        route="both",
        reason="Need both"

    )

    mock_chain = Mock()
    mock_chain.invoke.return_value = expected

    with patch("agent.router.router_chain", mock_chain):

        result = decide_route(
            "Why is Chennai chargeability lower?"
        )

    assert result.route == "both"
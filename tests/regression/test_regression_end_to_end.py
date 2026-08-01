import pytest

from agent.graph_builder import build_graph
from tests.regression.regression_data import REGRESSION_CASES


graph = build_graph()


@pytest.mark.regression
@pytest.mark.parametrize("case", REGRESSION_CASES)
def test_end_to_end_regression(case):

    result = graph.invoke(
        {
            "question": case["question"],
            "attempts": 0,
        },
        config={"recursion_limit": 20},
    )

    assert result["route"] == case["expected_route"]

    assert result["final_answer"] != ""

    assert len(result["final_answer"]) > 20
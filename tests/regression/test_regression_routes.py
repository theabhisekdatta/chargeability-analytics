import pytest

from agent.router import decide_route
from tests.regression.regression_data import REGRESSION_CASES


@pytest.mark.regression
@pytest.mark.parametrize("case", REGRESSION_CASES)
def test_router_regression(case):

    decision = decide_route(case["question"])

    assert decision.route == case["expected_route"]